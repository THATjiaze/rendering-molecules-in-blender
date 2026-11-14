#!/usr/bin/env python3
"""Build the site: content/*.md + theme/ -> docs/ (plain HTML, no server needed).

    pip install -r requirements.txt
    python3 build.py

Each part is one Markdown file with a fixed shape, which this script relies on:

    # Part title
    intro paragraphs
    ## Chapter 3. Fields            (or any "## Heading" for an unnumbered section)
    ### Objectives                  a bullet list, drawn as the chapter's output sockets
    ### Any heading                 ordinary prose
    ### Exercise 3.1: do the thing  steps, then a paragraph starting "What you should see:"
    ### Check yourself              a numbered list of "Question? *Answer in italics.*"
"""
import html
import json
import re
import shutil
import tomllib
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt

ROOT = Path(__file__).parent
CONTENT, THEME, OUT = ROOT / "content", ROOT / "theme", ROOT / "docs"
MD = MarkdownIt("commonmark", {"html": True}).enable("table")


def slugify(text):
    text = re.sub(r"<[^>]+>|[`*_]", "", text).lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "section"


def plain(markup):
    """HTML -> text, for the search index and meta descriptions."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


def split_at(text, level):
    """Split Markdown at headings of one level -> (text before the first, [(heading, body), ...])."""
    bits = re.split(rf"^{'#' * level} (.+)$", text, flags=re.M)
    return bits[0], list(zip(bits[1::2], bits[2::2]))


class Ids:
    """Hands out ids that are unique within one page."""

    def __init__(self):
        self.seen = set()

    def make(self, wanted):
        candidate, n = wanted, 1
        while candidate in self.seen:
            n += 1
            candidate = f"{wanted}-{n}"
        self.seen.add(candidate)
        return candidate


class Site:
    def __init__(self):
        self.cfg = tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))
        self.parts = [dict(p) for p in self.cfg["part"]]
        self.by_file = {p["file"]: p for p in self.parts}
        self.search = []
        for part in self.parts:
            self.parse(part)
        for part in self.parts:  # second pass: every id now exists, so cross-references can be resolved
            self.render(part)

    # ---------------------------------------------------------------- parsing

    def parse(self, part):
        text = (CONTENT / f"{part['file']}.md").read_text(encoding="utf-8")
        title = re.match(r"# (.+)\n", text)
        part["title"] = title.group(1)
        lead, chapters = split_at(text[title.end():], 2)
        ids = Ids()
        part.update(lead_md=lead, chapters=[], chapter_ids={}, exercise_ids={})
        for heading, body in chapters:
            numbered = re.match(r"Chapter (\d+)\. (.+)", heading)
            num, name = (int(numbered.group(1)), numbered.group(2)) if numbered else (None, heading)
            chapter = {"num": num, "title": name, "id": ids.make(f"chapter-{num}" if num else slugify(name)), "sections": []}
            if num:
                part["chapter_ids"][num] = chapter["id"]
            chapter["lead_md"], sections = split_at(body, 3)
            for sec_title, sec_body in sections:
                section = {"title": sec_title, "md": sec_body, "kind": "prose"}
                if sec_title == "Objectives":
                    section["kind"] = "objectives"
                elif sec_title.startswith("Exercise "):
                    label, _, name = sec_title.partition(": ")
                    section.update(kind="exercise", label=label, name=name[:1].upper() + name[1:], id=ids.make(slugify(label)))
                    number = re.match(r"Exercise ([\w.]+)", label).group(1)
                    part["exercise_ids"].setdefault(number, section["id"])
                elif sec_title.startswith("Check yourself"):
                    section.update(kind="check", id=ids.make(f"{chapter['id']}-check"))
                section.setdefault("id", ids.make(slugify(sec_title)) if section["kind"] == "prose" else None)
                chapter["sections"].append(section)
            part["chapters"].append(chapter)
        part["n_chapters"] = len(part["chapters"])
        part["n_exercises"] = sum(s["kind"] == "exercise" for c in part["chapters"] for s in c["sections"])

    # -------------------------------------------------------------- rendering

    def markdown(self, text, part):
        """Markdown -> HTML, with figures inlined, tables made scrollable and links pointed at pages."""

        def figure(match):
            svg = (CONTENT / match.group(2)).read_text(encoding="utf-8")
            svg = re.sub(r'\sfont-family="[^"]*"', "", svg, count=1)  # inherit the page's font when inline
            return f'<figure class="figure">{svg.strip()}<figcaption>{html.escape(match.group(1))}</figcaption></figure>'

        text = re.sub(r"^!\[(.+?)\]\((figures/[\w-]+\.svg)\)$", figure, text, flags=re.M)
        out = MD.render(text)
        out = out.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

        def link(match):
            target = self.by_file.get(match.group(1))
            return f'href="{target["slug"]}.html{match.group(2) or ""}"' if target else match.group(0)

        out = re.sub(r'href="([\w-]+)\.md(#[\w-]+)?"', link, out)
        out = re.sub(r'<a href="(https?://[^"]+)"', r'<a href="\1" rel="noopener"', out)
        return self.link_references(out, part)

    def link_references(self, markup, part):
        """Turn "Chapter 6", "Chapters 2 to 4" and "Exercise 3.1" into links.

        A chapter number belongs to this part unless the sentence says otherwise in one of two ways:
        "Chapter 7 of the <link to another part>" or "<link to another part>, Chapter 7".
        """
        slugs = {p["slug"]: p for p in self.parts}
        bits = re.split(r"(<[^>]+>)", markup)
        skip = 0  # depth inside <a>, <code> or a figure, where nothing is linked
        literal = 0  # depth inside <code> or a figure, where text is left exactly as written
        last_link = None  # the part most recently linked to, while we are still right after that link
        for i, bit in enumerate(bits):
            if bit.startswith("<"):
                tag = re.match(r"</?(\w+)", bit)
                name = tag.group(1) if tag else ""
                if name in ("a", "code", "svg"):
                    skip += -1 if bit.startswith("</") else 1
                if name in ("code", "svg"):
                    literal += -1 if bit.startswith("</") else 1
                if name == "a" and not bit.startswith("</"):
                    href = re.search(r'href="([\w-]+)\.html', bit)
                    last_link = slugs.get(href.group(1)) if href else None
                elif name not in ("a", "em", "strong"):
                    last_link = None
                continue
            if not literal:  # arrows mean "connect these sockets"; draw them in the interface typeface, where they are larger
                bit = bits[i] = re.sub(r"[→←]", lambda m: f'<span class="arrow">{m.group(0)}</span>', bit)
            if skip or not bit.strip():
                continue
            ahead = re.search(r'<a href="([\w-]+)\.html', bits[i + 1] if i + 1 < len(bits) else "")
            ahead = slugs.get(ahead.group(1)) if ahead else None

            def chapters(match, bit=bit, last_link=last_link, ahead=ahead):
                target = part
                rest = bit[match.end():]
                if not rest.startswith(" here"):
                    if ahead and rest.strip() in ("of the", "of"):
                        target = ahead
                    elif last_link and re.fullmatch(r"[,(]?\s*", bit[: match.start()]):
                        target = last_link
                page = "" if target is part else f"{target['slug']}.html"

                def one(number):
                    anchor = target["chapter_ids"].get(int(number.group(0)))
                    return f'<a class="ref" href="{page}#{anchor}">{number.group(0)}</a>' if anchor else number.group(0)

                return match.group(1) + re.sub(r"\d+", one, match.group(2))

            new = re.sub(r"\b(Chapters? )(\d+(?:(?:, | and |, and | to | or )\d+)*)", chapters, bit)

            def exercise(match):
                anchor = part["exercise_ids"].get(match.group(1))
                return f'<a class="ref" href="#{anchor}">{match.group(0)}</a>' if anchor else match.group(0)

            bits[i] = re.sub(r"\bExercise ([A-Z]?\d+(?:\.\d+)?)\b", exercise, new)
            if bit.strip(" ,("):
                last_link = None
        return "".join(bits)

    def render(self, part):
        url = f"{part['slug']}.html"
        part["lead"] = self.markdown(part["lead_md"], part)
        self.index(part, None, part["title"], url, part["lead"])
        for chapter in part["chapters"]:
            chapter["lead"] = self.markdown(chapter["lead_md"], part)
            chapter["objectives"] = []
            entry = self.index(part, chapter, chapter["title"], f"{url}#{chapter['id']}", chapter["lead"])
            for section in chapter["sections"]:
                body = self.markdown(section["md"], part)
                if section["kind"] == "objectives":
                    # The list becomes the chapter node's sockets; whatever follows it opens the chapter.
                    end = body.find("</ul>") + len("</ul>") if "<ul>" in body else 0
                    items = re.findall(r"<li>(.*?)</li>", body[:end], flags=re.S)
                    chapter["objectives"] = [re.sub(r"^\s*<p>(.*)</p>\s*$", r"\1", item, flags=re.S) for item in items]
                    chapter["lead"] += body[end:]
                    entry["x"] = plain(chapter["lead"] + " " + body[:end])
                    continue
                if section["kind"] == "exercise":
                    body = re.sub(r"<p>(What you should \w+): (\w?)",
                                  lambda m: f'<p class="result"><span class="result-label">{m.group(1)}</span> {m.group(2).upper()}', body)
                    section["key"] = f"{part['slug']}/{section['id']}"
                elif section["kind"] == "check":  # the questions are the first list; anything after it is ordinary text
                    end = body.find("</ol>") + len("</ol>")
                    body, section["after"] = body[:end], body[end:]
                    body = re.sub(r"<li>(.*?)</li>", self.question, body, flags=re.S)
                section["html"] = body
                self.index(part, chapter, section["title"], f"{url}#{section['id']}", body)

    @staticmethod
    def question(match):
        """'Question? <em>Answer.</em>' -> the question, with the answer folded away."""
        inner = re.sub(r"^\s*<p>(.*)</p>\s*$", r"\1", match.group(1), flags=re.S).strip()
        split = re.match(r"^(.*\S)\s+<em>(.+)</em>$", inner, flags=re.S)
        if not split:
            return match.group(0)
        return f'<li><p class="q">{split.group(1)}</p><details><summary>Answer</summary><p>{split.group(2)}</p></details></li>'

    def index(self, part, chapter, title, url, markup):
        where = part["short"] + (f", Chapter {chapter['num']}" if chapter and chapter["num"] else "")
        entry = {"t": plain(title), "w": where, "u": url, "x": plain(markup)}
        self.search.append(entry)
        return entry

    # ------------------------------------------------------------- front page

    def graph(self):
        """Lay out the front page's node graph: parts as nodes, wires from site.toml."""
        col_x, node_w, end_w = [16, 252, 510, 768, 1066], 204, 136
        top, pitch, head, row = 14, 112, 28, 24
        nodes = {}
        for p in self.parts:
            col, r = p["graph"]
            x, y = col_x[col], top + r * pitch
            nodes[p["slug"]] = {"part": p, "x": x, "y": y, "w": node_w, "h": head + 2 * row + 8,
                                "out": (x + node_w, y + head + row / 2 + 2), "in": (x, y + head + row * 1.5 + 2)}
        rows = max(p["graph"][1] for p in self.parts)
        mid = top + rows * pitch / 2
        sockets = list(dict.fromkeys(w["socket"] for w in self.cfg["wire"] if w["to"] == "out"))
        in_node = {"x": col_x[0], "y": mid - 10, "w": end_w, "h": head + row + 8}
        in_node["out"] = (in_node["x"] + end_w, in_node["y"] + head + row / 2 + 2)
        out_node = {"x": col_x[4], "y": mid - 34, "w": end_w, "h": head + len(sockets) * row + 8, "sockets": []}
        for i, name in enumerate(sockets):
            out_node["sockets"].append({"name": name, "y": out_node["y"] + head + row * (i + 0.5) + 2})
        wires = []
        for w in self.cfg["wire"]:
            x1, y1 = in_node["out"] if w["from"] == "in" else nodes[w["from"]]["out"]
            if w["to"] == "out":
                x2, y2 = out_node["x"], next(s["y"] for s in out_node["sockets"] if s["name"] == w["socket"])
            else:
                x2, y2 = nodes[w["to"]]["in"]
            bend = max(36, (x2 - x1) * 0.5)
            socket = "float" if w["from"] == "in" else nodes[w["from"]]["part"]["socket"]
            wires.append({"d": f"M{x1:.0f} {y1:.0f}C{x1 + bend:.0f} {y1:.0f} {x2 - bend:.0f} {y2:.0f} {x2:.0f} {y2:.0f}", "socket": socket})
        height = top * 2 + rows * pitch + head + 2 * row + 8
        return {"nodes": list(nodes.values()), "in": in_node, "out": out_node, "wires": wires,
                "width": col_x[4] + end_w + 16, "height": height, "head": head, "row": row}

    # ---------------------------------------------------------------- writing

    def write(self):
        if OUT.exists():
            shutil.rmtree(OUT)
        (OUT / "assets").mkdir(parents=True)
        for item in ("style.css", "site.js", "favicon.svg"):
            shutil.copy(THEME / item, OUT / "assets" / item)
        shutil.copytree(THEME / "fonts", OUT / "assets" / "fonts")
        (OUT / ".nojekyll").write_text("")
        index = json.dumps(self.search, ensure_ascii=False, separators=(",", ":"))
        (OUT / "assets" / "search-index.js").write_text(f"window.SEARCH_INDEX = {index};\n", encoding="utf-8")

        env = Environment(loader=FileSystemLoader(THEME), trim_blocks=True, lstrip_blocks=True)
        totals = {"parts": len(self.parts), "chapters": sum(p["n_chapters"] for p in self.parts),
                  "exercises": sum(p["n_exercises"] for p in self.parts)}
        shared = {"site": self.cfg, "parts": self.parts, "totals": totals}
        pages = {"index.html": env.get_template("home.html").render(**shared, graph=self.graph(), current=None)}
        for i, part in enumerate(self.parts):
            neighbors = {"prev": self.parts[i - 1] if i else None, "next": self.parts[i + 1] if i + 1 < len(self.parts) else None}
            pages[f"{part['slug']}.html"] = env.get_template("part.html").render(**shared, part=part, current=part, **neighbors)
        about = (CONTENT / "about.md").read_text(encoding="utf-8").replace("{{ repo }}", self.cfg.get("repo") or "")
        title = re.match(r"# (.+)\n", about)
        pages["about.html"] = env.get_template("plain.html").render(
            **shared, current=None, title=title.group(1), body=MD.render(about[title.end():]))
        for name, page in pages.items():
            (OUT / name).write_text(page, encoding="utf-8")
        print(f"Built {len(pages)} pages into {OUT.relative_to(ROOT)}/: {totals['chapters']} chapters, "
              f"{totals['exercises']} exercises, {len(self.search)} search entries.")


if __name__ == "__main__":
    Site().write()
