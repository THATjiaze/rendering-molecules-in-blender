# Rendering Molecules in Blender

A workbook for structural biologists who can already make a figure in ChimeraX and want what Blender adds:
materials, light and geometry you control yourself. Nine parts, 87 chapters and 172 exercises, written for
Blender 5.2 LTS and the [Molecular Nodes](https://bradyajohnston.github.io/MolecularNodes/) add-on.

Read it at **https://thatjiaze.github.io/rendering-molecules-in-blender/**.

| Part | What it covers |
| --- | --- |
| [Material recipes for molecular renders](content/01-material-recipes.md) | Settings tables for named looks, all on one Principled BSDF |
| [Designing a look from scratch](content/02-designing-a-look.md) | Five questions that turn a texture you can picture into settings |
| [Lighting](content/03-lighting.md) | Direction, softness and contrast, the named setups, and inventing your own |
| [Shaders: the whole menu](content/04-shaders.md) | Every shader node, what feeds one, render engines, stylized looks |
| [Geometry Nodes, from zero](content/05-geometry-nodes.md) | Trees, attributes, fields, volumes and SDFs, with two worked projects |
| [Geometry Nodes for art](content/06-geometry-nodes-for-art.md) | The same nodes fed by formulas instead of files |
| [Molecular Nodes as a second ChimeraX](content/07-molecular-nodes.md) | Selections as boolean fields, and what each Molecular Nodes node is built from |
| [Handling objects and modeling](content/08-objects-and-modeling.md) | Selecting, placing, Edit Mode, modifiers, curves and the camera |
| [Art direction: the whole picture](content/09-art-direction.md) | Seven decisions made together for one sentence, four complete looks, and inventing your own |

## How it was made, and how far to trust it

Claude, an AI model made by Anthropic, wrote the text in working sessions with Jiaze Liu, who did the exercises
in Blender and reported what broke. Not every chapter has been checked that way. Expect some wrong menu paths
and renamed nodes, and please open an issue or a pull request when you find one. [content/about.md](content/about.md)
says more.

On the site, selecting any passage offers "Report this passage", which opens an issue here with the passage
quoted and its place in the guide filled in.

## Editing the text

The text is plain Markdown, one file per part, in `content/`. Each file keeps one shape, which the build relies on:

```
# Part title
intro paragraphs
## Chapter 3. Fields              (or any "## Heading" for an unnumbered section)
### Objectives                    a bullet list; drawn as the chapter's output sockets
### Any heading                   ordinary prose
### Exercise 3.1: do the thing    steps, then a paragraph starting "What you should see:"
### Check yourself                a numbered list of "Question? *Answer in italics.*"
```

Links between parts are ordinary relative links to the Markdown file, such as `[Lighting part](03-lighting.md)`,
so they also work when reading the files on GitHub. "Chapter 6" and "Exercise 3.1" become links on their own.
Figures are SVG files in `content/figures/`, placed with `![caption](figures/name.svg)` on a line of its own.
Renders go in the same folder as WebP files, at full resolution, and are placed the same way; the build copies
them into `docs/figures/` and links each to its full size.

## Building the site

```
pip install -r requirements.txt
python3 build.py
```

Both scripts need Python 3.11 or later (they read `site.toml` with `tomllib`); the `python3` that ships with
macOS is older and stops with "No module named 'tomllib'".

Then run `python3 tools/check.py`. The build writes the whole site into `docs/`, which is what GitHub Pages serves (Settings, Pages, "Deploy from a
branch", branch `main`, folder `/docs`). The pages are plain HTML with one stylesheet and one small script;
opening `docs/index.html` from disk works too. Commit `docs/` together with the change that produced it.

| Path | What it is |
| --- | --- |
| `site.toml` | Title, the list of parts, each part's color, and the front page's node graph |
| `content/` | The text and figures |
| `theme/` | Page templates, `style.css`, `site.js` and the fonts |
| `build.py` | Turns the three above into `docs/` |
| `tools/check.py` | Checks a build: no text lost, no broken links. Run it before committing |
| `tools/` (the rest) | Converters used to bring the text and figures in from the original document |
| `CLAUDE.md` | Standing notes for Claude Code sessions that work on this repository |

## Credits

Set in Literata, Inter and JetBrains Mono, each under the SIL Open Font License (see `theme/fonts/`).
The part colors are Blender's socket colors. Blender is a trademark of the Blender Foundation; this guide
is not affiliated with Blender or with Molecular Nodes.
