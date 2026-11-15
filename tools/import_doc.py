"""Turn Markdown exported from the original Claude Doc (one file per tab) into the site's content files.

    python3 tools/import_doc.py <folder of exported .md files> content [-v]

It drops the date and author line, turns the figure placeholders into image lines, and rewords
references between tabs ("the Recipes tab") into links between parts. It overwrites content/NN-*.md,
so anything edited there since the last import is lost: use it only to bring in a tab that has not
been published yet, or when the doc is deliberately being treated as the master copy.
"""
import re, sys, os
RAW, OUT = sys.argv[1], sys.argv[2]
VERBOSE = "-v" in sys.argv
PARTS = [
 ("01-material-recipes", "Material Recipes for Molecular Renders.md", "Material recipes for molecular renders"),
 ("02-designing-a-look", "Designing a look from scratch.md", "Designing a look from scratch"),
 ("03-lighting", "Lighting.md", "Lighting, from zero to designing your own setups"),
 ("04-shaders", "Shaders, the whole menu.md", "Shaders: the whole menu, from zero"),
 ("05-geometry-nodes", "Geometry Nodes, from zero.md", "Geometry Nodes, from zero"),
 ("06-geometry-nodes-for-art", "Geometry Nodes for art.md", "Geometry Nodes for art"),
 ("07-molecular-nodes", "Molecular Nodes as a second ChimeraX.md", "Molecular Nodes as a second ChimeraX"),
 ("08-objects-and-modeling", "Handling objects and modeling.md", "Handling objects and modeling"),
]
FILE = {"Recipes": "01-material-recipes", "Designing": "02-designing-a-look", "design": "02-designing-a-look", "Lighting": "03-lighting",
        "Shaders": "04-shaders", "Geometry Nodes": "05-geometry-nodes", "Geometry Nodes for art": "06-geometry-nodes-for-art",
        "Molecular Nodes": "07-molecular-nodes"}
LABEL = {"Designing": "Designing a look", "design": "Designing a look"}
FIGS = {"Recipe looks placed by roughness and see-through": "recipe-map", "The five questions and the controls each one sets": "five-questions",
        "Three-point setup, seen from above": "three-point-lighting", "Blender's shader nodes grouped by behavior": "shader-families"}
NAMES = "Geometry Nodes for art|Geometry Nodes|Molecular Nodes|Recipes|Lighting|Shaders|Designing|design"

def reword(text, me):
    log = []
    def sub(pat, fn, s):
        def wrap(m):
            new = fn(m)
            if new != m.group(0): log.append((m.group(0), new, s[max(0, m.start()-45):m.end()+35].replace("\n", " ")))
            return new
        return re.sub(pat, wrap, s)
    def link(name):
        f = FILE[name]; lab = LABEL.get(name, name)
        return f"{lab} part" if f == me else f"[{lab} part]({f}.md)"
    t = text
    t = sub(rf"\b([Tt]he|[Ii]n the|of the|from the) ({NAMES}) tab\b", lambda m: f"{m.group(1)} {link(m.group(2))}", t)
    t = sub(rf"\b({NAMES}) and ({NAMES}) tabs\b", lambda m: f"{link(m.group(1)).replace(' part', '')} and {link(m.group(2)).replace(' part', '')} parts", t)
    t = sub(rf"\(({NAMES}) tab([,)])", lambda m: f"({link(m.group(1))}{m.group(2)}", t)
    t = sub(r"the full course is in Lighting\.", lambda m: "the full course is in [Lighting](03-lighting.md).", t)
    t = sub(r"the setup from the first tab", lambda m: "the setup from the [Recipes part](01-material-recipes.md)", t)
    t = sub(r"Check yourself: the whole tab", lambda m: "Check yourself: the whole part", t)
    t = sub(r"\b(this|the whole|does the) doc\b", lambda m: m.group(1) + " guide", t)
    t = sub(r"Part 1, Chapters 1 to 6, covers", lambda m: "The first half, Chapters 1 to 6, covers", t)
    t = sub(r"Part 2, Chapters 7 to 9, is", lambda m: "The second half, Chapters 7 to 9, is", t)
    t = sub(r"Part 2 starts here\.", lambda m: "The second half starts here.", t)
    t = sub(r"How to use this document", lambda m: "How to use this guide", t)
    t = sub(r"\b([Tt])his tab\b", lambda m: f"{m.group(1)}his part", t)
    t = sub(r"\b(other|every) tabs?\b", lambda m: m.group(1) + (" parts" if m.group(1) == "other" else " part"), t)
    for stem, raw, title in PARTS:   # plain mentions of a part by its full name (were mention chips in the doc)
        if stem == me or raw == "Lighting.md": continue
        t = sub(rf"(?<![\[#\w]){re.escape(raw[:-3])}(?!\]|\w)", lambda m, stem=stem, title=title: f"[{title}]({stem}.md)", t)
    return t, log

os.makedirs(OUT, exist_ok=True)
for stem, raw, title in PARTS:
    md = open(os.path.join(RAW, raw), encoding="utf-8").read()
    lines = md.split("\n")
    assert lines[0].startswith("# "), lines[0]
    assert re.match(r"^\w{3} \d{1,2}, \d{4} · @", lines[2]), lines[2]      # date · author chips
    body = "\n".join(lines[3:]).lstrip("\n")
    def fig(m):
        cap = m.group(1); return f"![{cap}](figures/{FIGS[cap]}.svg)"
    body, n = re.subn(r"&#91;embedded content: (.+?)\\\]", fig, body)
    body, log = reword(body, stem)
    if stem == "04-shaders":   # in the doc this figure sits after Chapter 2's self-check; put it where the six behaviors are explained
        fig_block = re.search(r"\n!\[Blender's shader nodes grouped by behavior\]\([^)]+\)\n\n[^\n]+\n", body)
        anchor = "\n### Exercise 2.1"
        assert fig_block and anchor in body
        body = body.replace(fig_block.group(0), "")
        body = body.replace(anchor, fig_block.group(0) + anchor, 1)
    open(os.path.join(OUT, stem + ".md"), "w", encoding="utf-8").write(f"# {title}\n\n{body.rstrip()}\n")
    print(f"{stem}: figures {n}, rewordings {len(log)}")
    if VERBOSE:
        for old, new, ctx in log: print(f"    …{ctx}…  =>  {new}")
    left = [l for l in body.split("\n") if re.search(r"\btabs?\b", l)]
    ui = r"(Material|Modifier|Object Data|Object|Data|Vertex|Face|Group|Item|World|Render|Output|Object Constraints|Volume Grids|workspace|Properties|domain|PDB|Edge|Tool|View|Node|Options|Physics|Particles|Scene|Local) tabs?\b"
    odd = [re.sub(ui, "", l) for l in left]
    for l in odd:
        for m in re.finditer(r".{0,60}\btabs?\b.{0,30}", l):
            print("    LEFT:", m.group(0))
