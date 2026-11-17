# About this guide

## How it was made

This guide was written by Claude, an AI model made by Anthropic, over a series of working sessions with Jiaze Liu, a structural biologist who was learning Blender at the time. He asked the questions, did the exercises in Blender 5.2 LTS on a Mac, and sent back a screenshot whenever a step did not behave as written. Each time, the text was corrected.

## How far to trust it

Not every chapter has been through that loop. Most of *Geometry Nodes, from zero* and scattered exercises in the other parts were done in Blender and fixed where they failed. The rest has not been checked click by click, so expect some wrong menu paths, renamed nodes and settings that have moved, more so in a version of Blender or Molecular Nodes other than the one above.

*Art direction* was checked another way. The numbers it marks as tested come from scripted renders in Blender 5.2 with Molecular Nodes, and its names were read from Blender's own interface definitions, but its click paths were not clicked through, so a menu path there may be off where a number is not.

The explanations of how things work are more reliable than the exact names of nodes and menus. When a step fails, the [Blender manual](https://docs.blender.org/manual/en/latest/) and the [Molecular Nodes documentation](https://bradyajohnston.github.io/MolecularNodes/) are the authorities, and most parts end with the pages they lean on.

## Reporting a mistake

If you find one, please say so. Select the passage on any page and a "Report this passage" button appears; it opens a GitHub issue with the passage quoted and its place in the guide filled in. The text lives in the repository as Markdown, one file per part, so a correction is usually a one-line change.

## Typefaces

The text is set in Literata, the interface in Inter, which is also Blender's own interface typeface, and code in JetBrains Mono. All three are used under the SIL Open Font License.
