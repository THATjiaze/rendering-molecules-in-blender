#!/usr/bin/env python3
"""Check a build before publishing it. Run from anywhere, after build.py:

    python3 tools/check.py

1. Every paragraph, list item, table cell and heading in content/*.md is present in the built page,
   so nothing was dropped on the way from Markdown to HTML.
2. Every link between pages points at a page and an anchor that exist, and no page repeats an id.

Exits with status 1 if anything is wrong.
"""
import html
import re
import sys
import tomllib
from pathlib import Path

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
MD = MarkdownIt("commonmark", {"html": True}).enable("table")


def text_of(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


def squash(text):
    return re.sub(r"\W+", "", text).lower()


def check_text():
    problems = 0
    for part in tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))["part"]:
        source = (ROOT / "content" / f"{part['file']}.md").read_text(encoding="utf-8")
        page = (DOCS / f"{part['slug']}.html").read_text(encoding="utf-8")
        main = page[page.index("<main"):page.index("</main>")]
        main = re.sub(r"<svg.*?</svg>|<summary>Answer</summary>", " ", main, flags=re.S)
        built = squash(text_of(main))
        rendered = MD.render(re.sub(r"^!\[(.+?)\]\(.+?\)$", r"\1", source, flags=re.M))
        blocks = re.findall(r"<(p|li|td|th|h1|h2|h3)>(.*?)</\1>", rendered, flags=re.S)
        missing = []
        for tag, inner in blocks:
            if tag == "li" and "<p>" in inner:
                continue  # its paragraphs are checked on their own
            text = text_of(inner)
            if tag == "h2":
                text = re.sub(r"^Chapter \d+\. ", "", text)
            if tag == "h3":
                text = text.partition(": ")[2] or text
            if squash(text) and squash(text) not in built:
                missing.append(text[:100])
        print(f"{part['slug']}: {len(blocks)} blocks, {len(missing)} missing")
        for text in missing[:10]:
            print(f"    missing: {text}")
        problems += len(missing)
    return problems


def check_links():
    pages = {p.name: p.read_text(encoding="utf-8") for p in DOCS.glob("*.html")}
    ids, problems, count = {}, 0, 0
    for name, page in pages.items():
        found = re.findall(r'\sid="([^"]+)"', page)
        ids[name] = set(found)
        for repeated in sorted({i for i in found if found.count(i) > 1}):
            print(f"    {name}: id used twice: {repeated}")
            problems += 1
    for name, page in pages.items():
        for href in re.findall(r'href="([^"]+)"', page):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            count += 1
            target, _, anchor = href.partition("#")
            target = target or name
            if target.endswith(".html"):
                if target not in pages or (anchor and anchor not in ids[target]):
                    print(f"    {name}: broken link {href}")
                    problems += 1
            elif not (DOCS / target).exists():
                print(f"    {name}: missing file {href}")
                problems += 1
    print(f"links: {count} checked, {problems} problems")
    return problems


if __name__ == "__main__":
    sys.exit(1 if check_text() + check_links() else 0)
