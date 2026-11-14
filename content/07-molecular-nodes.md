# Molecular Nodes as a second ChimeraX

In ChimeraX a selection is a line you type: `select /A:300-350 & ~backbone`. In Molecular Nodes the same selection is a boolean field, True or False for every atom, and each node under Molecular Nodes › Select writes one piece of that line. This part goes through them: what each is for, how to use it, and for every one the plain Geometry Nodes it is built from, so you can read any of them by pressing Tab on it and build your own when none fits. It assumes Chapters 1 to 3 of the [Geometry Nodes part](05-geometry-nodes.md): attributes, the Spreadsheet, fields and selections.

**Notation.** As in the other parts: Shift + A › menu is a path, Node › Socket names an output, → is a link you draw. "Under the hood" names the plain nodes that do the same job as a Molecular Nodes node. Select any Molecular Nodes node and press Tab to see its real contents, Tab again to come back out, and don't edit inside: the groups are shared by every tree that uses them.

## Chapter 1. What a selection is here

### Objectives

- See a selection as a True/False column in the Spreadsheet.
- Know the four places a selection plugs in.
- Read the integer codes that stand in for chain, residue and atom names.
- Recognize the anatomy shared by every Select node.

### A column of True and False

Every node in the Select menu outputs a boolean field: a rule that, evaluated on the atoms, gives each atom True or False. Ctrl + Shift + click a Select node and the Spreadsheet shows that column, while the viewport paints True atoms white and False ones black. ChimeraX's green outline and this column are the same thing.

A selection carries no atoms of its own. Like every field ([Geometry Nodes part](05-geometry-nodes.md), Chapter 3), it is evaluated on whatever geometry reaches the node that consumes it. The same Select Res ID node picks residue 50 on the atoms, or on a cartoon mesh that carries `res_id`.

### Where a selection goes

| Socket | What happens to unselected atoms | ChimeraX |
| --- | --- | --- |
| A style node's Selection | Discarded; the style is built from the rest | `hide`, `show`, `cartoon`, `surface` |
| Set Color › Selection | Keep their color | `color` |
| Separate Atoms › Selection | Go to the Inverted output | two selections |
| Delete Geometry › Selection (plain node) | Removed | `delete` |

Any other boolean socket takes a selection too. Style Cartoon's Helix Shape or a Switch node can be driven by one, so one chain gets cylinder helices and another ribbons.

### Names are integers

Geometry Nodes cannot store text on atoms, so Molecular Nodes stores every name as an integer. `chain_id`: chains sorted alphabetically and numbered from 0. `entity_id`: the same for entities. `res_name`: a fixed table, with ALA 0, ARG 1, ASN 2, ASP 3, CYS 4, GLU 5, GLN 6, GLY 7, HIS 8, ILE 9, LEU 10, LYS 11, MET 12, PHE 13, PRO 14, SER 15, THR 16, TRP 17, TYR 18, VAL 19, DNA bases 30 to 33, RNA 40 to 43 and unknown −1. `atom_name`: another table, N 1, CA 2, C 3, O 4, CB 5, CG 6 and on through the side chains, OXT 38, nucleic names from 50. `sec_struct`: 0 not protein, 1 helix, 2 sheet, 3 loop. `res_id` and `atomic_number` are what they say.

Several booleans are precomputed on import and sit on every atom: `is_alpha_carbon`, `is_backbone`, `is_side_chain`, `is_solvent`, `is_peptide`, `is_nucleic`, `is_lipid`, `is_hetero` and `is_carb`. Read any code off the Spreadsheet. The Select nodes with checkboxes hide the codes behind names, and the generated chain node shows your real chain letters. The full tables are in the Molecular Nodes reference linked in Chapter 7.

### The anatomy of a Select node

Nearly every node in the Select menu has the same shape: inputs **And** (default True) and **Or** (default False) at the top, outputs **Selection** and **Inverted** at the bottom, and its own criterion between them. And means "only where this other selection is also true"; Or means "or where this other selection is true". That is how Select nodes chain into one another without a Boolean Math node between them.

Under the hood: Named Attribute (the attribute in question) → Compare, or nothing for a stored boolean → Boolean Math (And) with the And input → Boolean Math (Or) with the Or input → Selection; Boolean Math (Not) on that → Inverted. Press Tab on Is Alpha Carbon and that is what you find: one Named Attribute reading `is_alpha_carbon` and three Boolean Math nodes.

### Exercise 1.1: look inside

1. In your model's tree, add Shift + A › Molecular Nodes › Select › Is Alpha Carbon. Select it, press Tab, read the nodes, press Tab again.
2. Ctrl + Shift + click the node, open the Spreadsheet's Vertex tab, and filter the Viewer column to True.

What you should see: a Named Attribute and three Boolean Math nodes inside; in the Spreadsheet, one True per residue, a few percent of the atoms, and in the viewport one white dot per residue on a black model.

### Exercise 1.2: the same selection, raw

1. Named Attribute (Integer, `res_id`) → Compare (Integer, Equal, B 50) → Style Spheres › Selection, on a branch from Set Color › Atoms, joined to the cartoon with Join Geometry. Set the style's Sphere menu to Mesh, since Point Cloud renders only in Cycles.
2. Replace the two plain nodes with Select Res ID (Res ID 50).

What you should see: the same handful of spheres both times, one residue's atoms in each chain, sitting on the cartoon. The Molecular Nodes node saved a node and added And, Or and Inverted for free.

### Check yourself

1. What does a Select node output? *A boolean field: True or False per atom, evaluated where it is used.*
2. What happens to unselected atoms at a style node's Selection socket? *They are discarded before the style is built.*
3. Why does `res_name` read 11 for a lysine? *Names are stored as integers from a fixed table, and LYS is 11.*
4. What do the And and Or sockets do? *Combine this node's selection with another one, without a separate Boolean Math node.*

## Chapter 2. Selecting by name: chain, residue, atom

### Objectives

- Pick chains, entities, residue ranges, residue types and atom names.
- Use the precomputed booleans for backbone, side chain, solvent, hydrogens and glycans.
- Translate the common ChimeraX specifiers.

### Chains and entities

Molecular Nodes generates a **Select Chain\_** node for each imported structure, named after it, with one checkbox per chain labeled with the real chain letter; find it by typing "Select Chain" into Shift + A's search. **Select Entity\_** does the same by entity, which groups identical copies: in a dimer with two receptor chains, one entity ticks both. Under the hood: Index Switch (Boolean) with `chain_id` as the index and the checkboxes as its items, which is why the boxes come in `chain_id` order. If the generated node is missing, the raw path is Named Attribute (Integer, `chain_id`) → Compare (Equal), with the code read from the Spreadsheet. ChimeraX: `/A`.

### Residues by number

**Select Res ID** takes one number. **Select Res ID Range** takes Min and Max, inclusive. **Select Res ID String** takes text like `1-20, 45, 100-120`, the way you'd write `:1-20,45,100-120`. Remember that `res_id` restarts in each chain, so residue 50 selects residue 50 of every chain; put a chain selection into the And socket to pin it down. Under the hood: Compare (Equal) for one residue; two Compares (Greater Equal and Less Equal) into Boolean Math (And) for a range; String nodes that split the text at commas and dashes for the string version.

### Residues by type

**Select Res Name** has a checkbox per amino acid, with DNA and RNA bases in their own panels. Under the hood: Index Switch (Boolean) indexed by `res_name`, like the chain node but with a fixed table. For a residue not in the list (a modified residue, a ligand), use the raw Compare on `res_name` or `is_hetero` below. ChimeraX: `:LYS,ARG`.

### Atoms by name and element

**Menu Atom Name** gives a dropdown of atom names (N, CA, C, O, CB and the rest) and outputs the Selection together with the integer code, so it doubles as a lookup for Chapter 1's table. **Is Alpha Carbon** is the shortcut for CA. **Is Backbone** and **Is Side Chain** read the precomputed booleans; Is Side Chain's Include CA counts the alpha carbon as side chain, which keeps side-chain sticks attached to the backbone. **Select Atomic Number** takes one element's number, **Select Element** has a checkbox per element, and **Is Hydrogen** is atomic number 1. Under the hood: Menu Switch (Integer) feeding a Compare; Named Attribute (Boolean) for the Is nodes; Index Switch by `atomic_number` for Select Element. ChimeraX: `@CA`, `backbone`, `sidechain`, `C`, `H`.

### Molecule types and the booleans with no node

**Is Peptide**, **Is Nucleic**, **Is Lipid** and **Is Solvent** read their booleans. **Select Nucleic Type** outputs is\_purine and is\_pyrimidine. **Select Attribute** reads any boolean attribute by name, and is the only way to reach two useful ones: `is_hetero`, everything the file marked HETATM (ligands, ions, waters, glycans), and `is_carb`, the glycans. Under the hood: Named Attribute (Boolean) with the Name you typed. ChimeraX: `protein`, `nucleic`, `solvent`, `ligand`, `~protein`.

### Exercise 2.1: one chain, one domain

1. Select Chain\_, with only the receptor chain ticked → Style Cartoon › Selection.
2. Select Res ID Range (Min 310, Max 481: domain III of EGFR) with the first node's Selection in its And socket → a second Style Cartoon with a different material, joined to the first.

What you should see: only the receptor, then domain III highlighted within it. Untick the chain in the first node and the highlight follows the residue numbers into EGF and the Fab, which is what the And socket prevents.

### Exercise 2.2: glycans as sticks

1. Select Attribute (Name `is_carb`) → Style Sticks › Selection, on a branch from Set Color › Atoms. Join Geometry with the cartoon.
2. Change the Name to `is_hetero`.

What you should see: the N-linked glycans as sticks on the receptor surface; then also any waters and ions, since `is_hetero` is everything that was HETATM.

### Check yourself

1. Why does Select Res ID 50 light up more than one residue? *`res_id` restarts in every chain; add a chain selection in And.*
2. Where do the chain letters in Select Chain\_ come from? *The import: the node is generated per structure and indexed by `chain_id`.*
3. How do you select glycans? *Select Attribute with `is_carb`.*
4. What does Include CA on Is Side Chain do? *Counts the alpha carbon as part of the side chain, so sticks stay attached.*

## Chapter 3. Selecting by structure and property

### Objectives

- Select by secondary structure, computing it when the file has none.
- Select by any number with the plain Compare node.
- Grow a selection to whole residues or along bonds.

### Secondary structure

**Is Helix**, **Is Sheet** and **Is Loop** read `sec_struct` (1, 2 and 3). Under the hood: Named Attribute (Integer, `sec_struct`) → Compare (Equal). A PDB or mmCIF from the databank carries secondary structure in its header, but a freshly built cryo-EM model often doesn't; then every atom reads 0 or 3 and the cartoon is all loop. **Topology DSSP** (Shift + A › Molecular Nodes › Topology) computes `sec_struct` from the backbone geometry and writes it back. Place it right after Group Input and the cartoon, the color nodes and the Is nodes all see it. ChimeraX: `helix`, `strand`, `coil`, `dssp`.

### Any number

There is no Select B-factor node because none is needed. Named Attribute (Float, `b_factor`) → Compare (Float, Greater Than, B 100) is the whole thing, and the same two nodes select by `occupancy`, `charge`, `mass`, or anything you stored yourself (`height` or `locres` from the [Geometry Nodes part](05-geometry-nodes.md)). For a range, two Compares into Boolean Math (And); for a tolerance, Compare's Equal mode with its Epsilon. ChimeraX: `::bfactor>100`.

### Whole residues

A proximity or B-factor cut usually catches part of a residue. **Select Res Whole** (Expand on) makes a residue all True if any of its atoms is. Under the hood: Boolean Any grouped by `ures_id`, which is Accumulate Field counting the Trues per group and testing for more than zero; `ures_id` rather than `res_id`, because `ures_id` is unique across chains. ChimeraX: `select up`, or ending a selection with `:`.

### Along bonds

**Select Bonded** grows a selection by Depth bonds along the edges. Its Bonded output gives the new atoms without the originals, for coloring neighbors differently. Under the hood, one step is: Edge Vertices reads both ends of every bond, Sample Index tests the selection at each end, Boolean Math (Or) marks the bond touched, and Evaluate on Domain brings "any touched bond" back to the atoms; a Repeat Zone runs that Depth times. **Expand Boolean** (Molecular Nodes › Utilities) is the index-wise cousin: it grows a run of Trues by n points either side along the atom order, which follows the sequence.

### Exercise 3.1: color by secondary structure

1. Color Secondary Structure (Molecular Nodes › Color) → Set Color › Color, in place of the chain colors. If everything comes out the Loop color, insert Topology DSSP after Group Input.
2. Is Sheet → Style Spheres (Sphere Mesh, Scale 0.3) › Selection, joined with the cartoon.

What you should see: helices, sheets and loops in three colors, then small spheres on the sheet residues only; domain III of EGFR is mostly sheet and the Fab nearly all of it.

### Exercise 3.2: poorly ordered residues

1. Named Attribute (Float, `b_factor`) → Compare (Greater Than, the top quarter of your model's range; read Min and Max off an Attribute Statistic) → Select Res Whole (Expand on) → Style Sticks › Selection, joined with the cartoon.
2. Mute Select Res Whole (M).

What you should see: whole residues as sticks where the map is weakest, usually at the periphery and in loops; muted, the sticks fray into partial residues.

### Check yourself

1. Why can Is Helix, Is Sheet and Is Loop all give False everywhere? *`sec_struct` is missing or 0; run Topology DSSP.*
2. Which node selects by B-factor? *The plain Compare on Named Attribute `b_factor`.*
3. What is Select Res Whole made of? *Boolean Any over `ures_id`: a residue is True if any of its atoms was.*
4. What is in Select Bonded's Bonded output? *The grown part only, without the starting atoms.*

## Chapter 4. Selecting by space

### Objectives

- Select inside a sphere or a box you can grab and move.
- Select atoms near other atoms, within one object or across two.
- Turn a spatial selection into a clipping box or an interface.

### A sphere or a box you can move

**Select Sphere** selects atoms within an Empty's radius. Adding the node creates an Empty called `Empty_Sphere`; its Scale is the radius in scene units (0.1 per Å), so grab (G) and scale (S) the Empty in the viewport and the selection follows. Under the hood: Object Info (Location, Scale) → Vector Math (Distance) from Position → Compare (Less Than) against the scale.

**Select Cube** does the same with a box that can also rotate. Under the hood: Object Info › Transform → Invert Matrix → Transform Point puts each atom in the box's own frame, and three Compares test that |x|, |y| and |z| are all at most 1. Its Inverted output is a clipping tool: into a style's Selection, everything inside the box disappears, like ChimeraX `clip` but with six faces you can turn.

### Atoms near other atoms

**Select Proximity** is `zone`. Target Atoms is the geometry to measure from; Distance (A) is the cutoff in Å, so no world-scale arithmetic; Subset narrows the target to a selection of it; Expand grows the result to whole residues. Under the hood: Separate Geometry keeps the Subset of the target, Geometry Proximity measures each atom's distance to what is left, Compare (Less Equal) tests the cutoff converted to scene units, and Boolean Any by `ures_id` does Expand. This node has no And or Or sockets; combine its Selection through another node's And socket or a Boolean Math.

Two patterns. Within one object: Target Atoms ← Group Input › Atoms and Subset ← a Select Chain\_ ticking the Fab chains gives everything within the cutoff of the Fab, including the Fab itself at distance zero; feed the result into a Select Chain\_ (receptor ticked) › And to keep the receptor side. Across objects: Target Atoms ← Object Info (Relative) of the other model, which is how a ligand from one file selects its pocket in another. ChimeraX: `select /A & /H,L @<5`, `select zone`.

### Exercise 4.1: the epitope

1. Select Proximity: Target Atoms ← Group Input › Atoms, Subset ← Select Chain\_ with the Fab heavy and light chains ticked, Distance 4.5, Expand on.
2. Its Selection → a second Select Chain\_ (receptor ticked) › And. That node's Selection → Style Sticks on a branch, joined with the cartoon, and → Set Color › Selection with one bright color, placed before the styles.

What you should see: the receptor residues in contact with Fab108 as whole-residue sticks, recolored, on the cartoon. Lower Distance to 3.5 and only the tightest contacts remain; turn Expand off and the sticks break into partial residues.

### Exercise 4.2: a box as a clipping plane

1. Select Cube → Inverted → Style Cartoon › Selection. Move (G) and scale (S) `Empty_Cube` until it covers half the model.
2. Rotate the Empty (R) by 30 degrees.

What you should see: the cartoon cut away wherever the box sits, with a clean edge that follows the box's rotation.

### Check yourself

1. What sets Select Sphere's radius? *The Empty's Scale, in scene units.*
2. Why does a within-object Select Proximity include the target itself? *Target atoms are at distance zero from themselves; an And with the other side excludes them.*
3. Which node is ChimeraX `zone`? *Select Proximity.*
4. How does Select Cube handle a rotated box? *It transforms each atom into the box's frame with the inverted matrix before comparing.*

## Chapter 5. Combining and applying selections

### Objectives

- Combine selections with Boolean Math and the And/Or sockets.
- Apply them to styles, colors and separations, and join the results.
- Expose a selection as a checkbox on the modifier panel.

### Boolean algebra

**Boolean Math** (Shift + A › Utilities › Math) is the full algebra: And, Or, Not, Not And, Nor, Xor, and Subtract, which is A and not B. In ChimeraX terms, `&`, `|`, `~` and `& ~`. The And and Or sockets on Select nodes cover the common two-term cases without it. Read a chain of Select nodes from the top: each node's output is (its own criterion And its And socket) Or its Or socket. For anything with parentheses, draw Boolean Math nodes so the tree looks like the expression; it is easier to check by eye than a chain of sockets.

### Applying

Three habits. One: a style's Selection discards, so "these as sticks and everything as cartoon" is two style nodes on two branches from the same atoms, joined with Join Geometry. Two: Set Color's Selection does not discard, so coloring happens before styling, on the atoms, and every style downstream inherits the `Color`. Three: **Separate Atoms** splits the atoms into Atoms and Inverted geometries and also outputs Index, each atom's index before the split, for when a later node must refer back to the whole structure. **Separate Polymers** is the same split run on `is_peptide`, then `is_nucleic`, with the rest as Other. Under the hood: Separate Geometry, with a Capture Attribute of Index just before it.

### Checkboxes on the modifier

Drag any Select node's And input to Group Input's empty socket and it becomes a checkbox on the modifier panel; drag a Distance or a Res ID and it becomes a slider. A Switch node (Boolean) choosing between two selections, driven by such a checkbox, flips a whole figure between two states without opening the tree.

### Exercise 5.1: a selection with parentheses

1. Build "chain A and (LYS or ARG) and not backbone": Select Chain\_ (one chain ticked) › Selection → Select Res Name (LYS and ARG ticked) › And. Its Selection → Boolean Math (Subtract) › A; Is Backbone › Selection → B.
2. The result → Style Sticks › Selection, on a branch joined with the cartoon.

What you should see: the basic side chains of one chain as sticks, their backbone atoms excluded; tick GLU and ASP too and the salt-bridge partners join them.

### Exercise 5.2: the figure

1. Color: Set Color with Random Color for everything, then a second Set Color with Select Chain\_ (receptor ticked) in Selection and a flat gray, so only the receptor goes gray.
2. Styles: Style Cartoon for all; Style Surface with Select Chain\_ (Fab chains) in Selection and a material at Alpha 0.3; Style Sticks for Exercise 4.1's epitope; Style Sticks for `is_carb`. Four branches, one Join Geometry.
3. Expose the epitope's Distance and the surface's chain checkboxes to the modifier panel.

What you should see: a gray receptor with colored EGF, a translucent antibody surface, contact residues and glycans as sticks, and two controls on the modifier panel that tune it without the node editor.

### Check yourself

1. How do you write A and not B? *Boolean Math set to Subtract, or an And socket fed B's Inverted.*
2. Why color before styling? *Set Color keeps unselected atoms; every style downstream inherits `Color`.*
3. What is Separate Atoms' Index output for? *Referring back to an atom's index in the whole structure after the split.*
4. How does a selection become a checkbox? *Connect its And input to Group Input.*

## Chapter 6. The rest of the ChimeraX toolbox

### Objectives

- Color by chain, entity, rainbow, secondary structure and any attribute.
- Compute what the file lacks: secondary structure, bonds.
- Know the six style nodes and the sockets that matter.
- Measure, center, explode and morph with the utility nodes.

### Coloring

All color nodes output a Color field for **Set Color**, which under the hood is Store Named Attribute writing `Color` on the Point domain with a Selection. **Color Chain\_** and **Color Entity\_** are generated per structure with one swatch per chain or entity (Index Switch of colors by `chain_id`). **Random Color**, the node in your default tree, seeds Random Value with an ID and builds an HSL color. **Color Rainbow** runs a hue along each chain or the whole structure (the Factor menu), from each atom's relative position in its group: ChimeraX `rainbow`. **Color Secondary Structure** is three swatches by `sec_struct`. **Color Attribute Map** is `color byattribute`: Name, Min, Max and two or three colors; under the hood it is Named Attribute → Map Range → Mix Color, the chain you built by hand for `height`, in one node. **Color pLDDT** is that node preset for AlphaFold models. **Color Res Name**, **Color Common** and **Color Element** map `res_name` or `atomic_number` to swatches, and **Color Goodsell** darkens the non-carbon atoms for the Goodsell look.

### Reading attributes

Molecular Nodes › Attributes holds a reader per attribute: Chain ID, Residue ID, Residue Name, Atom Name, B Factor, URes ID, Secondary Structure, Entity ID, VDW Radii. Each is a Named Attribute with the name typed and the type set, plus an Index input for reading another atom's value. Use them for the same reason as the Select nodes: no typos, no wrong data type.

### Computing what the file lacks

**Topology DSSP** computes `sec_struct` (`dssp`). **Find Bonds** adds edges by distance for files without bonds, and **Break Bonds** removes them by a cutoff or a selection (`bond`, `~bond`). **Set URes ID** recomputes `ures_id` after you delete atoms. **Backbone Positions** gives every residue's N, CA, C and O positions as fields, for drawing your own geometry along the backbone.

### The six styles

| Style | ChimeraX | Sockets that matter |
| --- | --- | --- |
| Style Spheres | `show atoms`, `style sphere` | Sphere: Point Cloud is free but renders only in Cycles; Instances or Mesh for EEVEE. Scale multiplies `vdw_radii` |
| Style Ball and Stick | `style ball` | Bond Find for files without bonds; Bond Split for double bonds; Bond Scale in Å |
| Style Sticks | `style stick` | Scale is the stick radius in Å |
| Style Ribbon | `cartoon style tube` | Peptide Radius; Backbone Smoothing |
| Style Cartoon | `cartoon` | Peptide Shape; Helix Shape, for cylinder helices; Sheet Arrows; Loop Radius; Color Blur |
| Style Surface | `surface` | Quality; Scale and Offset grow the surface; Separate By and Group ID make one surface per chain, like `surface /A`; Color Source picks the alpha carbon or the nearest atom |

Every style's Selection discards, and every style's Material socket is where the [Recipes part](01-material-recipes.md)'s materials go.

### Measuring, centering, exploding, morphing

**Centre on Selection** moves the atoms so a selection's centroid sits at the origin (`cofr`, `view`); a Group ID centers each chain separately. **Split to Centred Instances** turns each Group ID (a chain, with `chain_id`) into an instance at its own centroid, so a Scale on the instances explodes the complex apart (`tile`). **Field Remap** and **Normalize Field** rescale a field between a min and a max, grouped if you like: the Attribute Statistic and Map Range chain of the [Geometry Nodes part](05-geometry-nodes.md) in one node. **Group Info** and **Group Parameter** give each atom its residue's size, first and last index, and relative position, with `ures_id` as Group ID. **Offset Float** and its siblings read a value at Index plus an offset: the next residue's value, for differences along the chain. **Sample Mix Vector** mixes positions between two geometries by a Factor, which is a morph between two conformations (`morph`) once the two models have matching atoms. For a distance, Geometry Proximity from one selection to another with a Viewer on its Distance output is `distance`, read off the Spreadsheet.

### Exercise 6.1: color by B-factor in one node

1. Color Attribute Map (Name `b_factor`, Min and Max from your model, A blue, B red, Intermediate on and white) → Set Color › Color.

What you should see: the B-factor coloring of the [Geometry Nodes part](05-geometry-nodes.md), with two numbers on one node instead of three nodes, and the same blue-to-red convention as `spectrum b`.

### Exercise 6.2: one surface per chain

1. Style Surface with Separate By set to chains, or Group ID ← Chain ID (Attributes), Quality 6, and a material at Alpha 0.4.

What you should see: a surface that stops at each chain boundary instead of one skin over the complex, so the Fab and the receptor read as separate bodies pressed together.

### Check yourself

1. Which node is `color byattribute bfactor`? *Color Attribute Map.*
2. Which sphere mode shows in EEVEE? *Instances or Mesh; Point Cloud is Cycles only.*
3. How do you get one surface per chain? *Style Surface with Separate By, or Group ID from `chain_id`.*
4. What does Field Remap replace? *Attribute Statistic plus Map Range.*

## Chapter 7. From ChimeraX to nodes

### The translation table

| ChimeraX | Molecular Nodes |
| --- | --- |
| `select /A` | Select Chain\_ with A ticked |
| `select :100-200` | Select Res ID Range |
| `select :100,105,110-120` | Select Res ID String |
| `select :LYS,ARG` | Select Res Name |
| `select @CA` | Is Alpha Carbon, or Menu Atom Name |
| `select backbone`, `sidechain` | Is Backbone, Is Side Chain |
| `select protein`, `nucleic`, `solvent` | Is Peptide, Is Nucleic, Is Solvent |
| `select ligand` | Select Attribute `is_hetero`, with Is Solvent's Inverted in And |
| glycans | Select Attribute `is_carb` |
| `select H` | Is Hydrogen |
| `select helix`, `strand`, `coil` | Is Helix, Is Sheet, Is Loop |
| `select ::bfactor>80` | Named Attribute `b_factor` → Compare |
| `select /A & /H,L @<5` | Select Proximity (Target Group Input, Subset chains H and L) → Select Chain\_ A › And |
| `select up` | Select Res Whole, Select Bonded |
| `~select`, `select ~sel` | Inverted output, or Boolean Math Not |
| `A & B`, `A \| B`, `A & ~B` | And socket, Or socket, Boolean Math Subtract |
| `hide X`, `show X` | Inverted, or the selection, into a style's Selection |
| `color /A red` | Set Color with Select Chain\_ in Selection |
| `rainbow` | Color Rainbow |
| `color byattribute bfactor` | Color Attribute Map |
| `color bychain`, `color byhetero` | Color Chain\_; Color Element after a chain color |
| `dssp` | Topology DSSP |
| `surface /A` | Style Surface with Separate By, or Group ID from `chain_id` |
| `transparency 60` | the material's Alpha |
| `clip` | Select Cube › Inverted into a style's Selection |
| `cofr sel`, `view sel` | Centre on Selection |
| `tile` | Split to Centred Instances, then Scale the instances |
| `morph` | Sample Mix Vector between two models |
| `distance` | Geometry Proximity › Distance, read in the Spreadsheet |
| `bond`, `~bond` | Find Bonds, Break Bonds |

### Glossary

- **Selection**: a boolean field on atoms, True or False each, evaluated where it is consumed.
- **And, Or sockets**: inputs on most Select nodes that combine another selection with this node's, without Boolean Math.
- **Inverted**: the output that is the Not of Selection.
- **Code**: the integer standing in for a name; `chain_id` from 0 alphabetically, `res_name` and `atom_name` from fixed tables.
- **Generated node**: a node built per imported structure and named after it: Select Chain\_, Select Entity\_, Color Chain\_, Color Entity\_.
- **`ures_id`**: residue number unique across the whole structure; `res_id` restarts in each chain.
- **`is_hetero`, `is_carb`**: precomputed booleans for HETATM records and for carbohydrates, reached with Select Attribute.
- **Expand**: grow an atom-level selection to whole residues, in Select Res Whole and Select Proximity.
- **Target Atoms, Subset**: in Select Proximity, the geometry measured from and the part of it that counts.
- **Under the hood**: the plain Geometry Nodes doing the same job as a Molecular Nodes group; Tab on the node shows the real ones.

### Sources

- [Select nodes](https://bradyajohnston.github.io/MolecularNodes/nodes/select.html), the Molecular Nodes reference for every node in Chapters 1 to 5.
- [Selections tutorial](https://bradyajohnston.github.io/MolecularNodes/tutorials/selections.html), the PyMOL comparison and Boolean Math examples.
- [Attributes](https://bradyajohnston.github.io/MolecularNodes/attributes.html) and [data tables](https://bradyajohnston.github.io/MolecularNodes/data_table.html), every attribute and the integer codes for residue and atom names.
- [Color nodes](https://bradyajohnston.github.io/MolecularNodes/nodes/color.html), [Style nodes](https://bradyajohnston.github.io/MolecularNodes/nodes/style.html), [Topology nodes](https://bradyajohnston.github.io/MolecularNodes/nodes/topology.html), [Geometry nodes](https://bradyajohnston.github.io/MolecularNodes/nodes/geometry.html) and [Utilities / Fields](https://bradyajohnston.github.io/MolecularNodes/nodes/utilities_fields.html), for Chapter 6.
- [Generated node groups](https://bradyajohnston.github.io/MolecularNodes/nodes/generated_nodes.html), the per-structure Select Chain\_ and Color Chain\_ nodes.
- In Blender, Tab on any Molecular Nodes node opens the group itself; the Molecular Nodes documentation describes the sockets, and the group shows the construction.
