# Notes for Claude

This repository is a published guide, "Rendering Molecules in Blender": Markdown in `content/`, turned into a
static site in `docs/` by `build.py`. GitHub Pages serves `docs/` from the `main` branch. README.md describes
the layout and the shape every content file must keep. Read it before the first edit.

Unless the maintainer says otherwise, this repository is the master copy of the text. It began as a Claude Doc
with one tab per part; that doc is not kept in step with the site.

## Changing the text

Most requests look like this, often arriving through the site's "Fix with Claude" button:

    In content/05-geometry-nodes.md (Geometry Nodes, from zero / Chapter 3: Fields / Exercise 3.1: See a field evaluate), this passage:

    "The top of the cube lifts and the bottom sinks..."

    Change: <what the maintainer wants>

1. Find the passage with `grep -n` on a distinctive few words. The quote is taken from the rendered page, so
   Markdown marks (`**`, backticks, links) are missing from it and a long quote may not match as one string.
2. Edit the Markdown. Change what was asked and nothing around it.
3. Rebuild and check, every time (Python 3.11 or later; an older `python3` fails on `import tomllib`):

       pip install -r requirements.txt     (once per session)
       python3 build.py
       python3 tools/check.py

4. Commit the Markdown together with the regenerated `docs/`. The change is live once it is on `main`.

If a request is a screenshot or a description of something going wrong in Blender, work out which step of
which exercise it contradicts, fix that step, and say in your reply what you changed and why.

## Getting Blender right

The guide's worth is that its steps work. Blender 5.2 LTS and the current Molecular Nodes add-on are the
reference versions.

- Do not write a node name, socket name, menu path, shortcut or default value from memory as if it were
  checked. Look it up in the Blender manual or the Molecular Nodes documentation when you can, and when you
  cannot, say in your reply that the detail is unverified.
- When the maintainer reports what Blender actually showed, that outranks the manual and your memory.
- `content/about.md` tells readers which parts have been tested in Blender. Keep that statement true when
  the maintainer reports testing more.

## Conventions in the text

- The ten files are "parts". The word "tab" is kept for Blender's own interface tabs (Material tab,
  Modifier tab), never for a part of this guide.
- Link to another part as `[Lighting part](03-lighting.md)`. `build.py` turns these into page links.
- "Chapter 6" and "Exercise 3.1" become links by themselves and point within the same part. To point at a
  chapter of another part, write "Chapter 7 of the [Geometry Nodes part](05-geometry-nodes.md)" or
  "[Geometry Nodes part](05-geometry-nodes.md), Chapter 7"; those two forms are the ones the build recognizes.
- `Shift + A › Mesh › Plane` is a menu path, `Separate XYZ › Z` is one socket of a node, and `→` is a link
  drawn between sockets. Attribute names and typed values go in backticks.
- An exercise is numbered steps followed by one paragraph starting "What you should see:". A self-check is a
  numbered list of "Question? *Answer in italics.*"; the site folds the answers away.
- Voice: second person, plain and exact, no em dashes, no filler. Say what to click and what will happen.
- Figures are hand-written SVG in `content/figures/`, colored only through the CSS variables `--fig-line`,
  `--fig-grid`, `--fig-accent`, `--fig-ink`, `--fig-muted` and `--fig-tint`, plus `--fig-cat-2` to `--fig-cat-7`
  for a figure that needs more hues (each with a fallback), so they follow the light and dark themes. Figures
  from a Claude Doc come across with `tools/widget_to_svg.js`. Renders are WebP files in the same folder, kept at full resolution
  because each one links to itself at full size.

## Adding a chapter or a part

A new chapter is a new `## Chapter N. Title` in the right file, in the shape README.md describes (numbering may
start at 0; a part that numbers its chapters is credited with only those, not its About or appendices). A new part
is a new file in `content/` plus a `[[part]]` entry in `site.toml` (with a socket color not yet used and a
place on the front page's graph). After either, look at the front page and the new page in a browser at a
wide and a narrow width before committing.

## The site itself

`theme/style.css` opens with the one design idea (the Blender node) and where it is allowed to appear. Keep
new interface elements quiet and in the existing vocabulary, and check both themes and a 400 px wide window.
The pages must keep working with JavaScript off and when opened from disk.
