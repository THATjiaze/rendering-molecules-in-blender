# Geometry Nodes, from zero

Materials decide how a surface looks; Geometry Nodes decides what the surface is. Every Molecular Nodes object is a Geometry Nodes tree, so learning it is learning how your maps and models are built, and it is what the sticky slime in the [Recipes part](01-material-recipes.md) is made of. This part goes from what a node tree is, through attributes and fields, to volumes and SDFs, and ends with the slime project built chain by chain.

**Notation.** Shift + A › Geometry › Read is a menu path. Node › Socket names one output of a node, so Separate XYZ › Z is the Z output of a Separate XYZ node. An arrow, →, is a link you draw from one socket to the next.

## Chapter 1. What Geometry Nodes is

### Objectives

- Explain what a Geometry Nodes modifier does and why it never damages the original data.
- Find your way around the Geometry Nodes workspace and the Group Input and Group Output nodes.
- Open any Molecular Nodes object and see it as a tree you can read.

### A pipeline on a modifier

Geometry Nodes is a modifier. Like a Subdivision Surface or a Solidify modifier, it sits in the Modifier Properties tab, takes the object's geometry in, and hands transformed geometry out to the viewport and the renderer. The difference is that what it does is not fixed: it is a tree of nodes you build. The original mesh is never touched; the tree runs again every time something it depends on changes, which is why you can drag a threshold slider and watch a density surface reshape itself.

Read a tree from left to right. Group Input on the left is where the object's own data enters. Each node takes what arrives, does one operation, and passes the result on. Group Output on the right is what Blender shows. Anything not connected to Group Output does not exist as far as the viewport is concerned, which is a useful way to park work in progress.

The same tree can be applied to different objects, and the values you expose on Group Input appear as sliders in the modifier panel, so a tree is also a tool: build it once, reuse it on every map.

### The workspace

The Geometry Nodes workspace tab at the top of Blender gives the standard layout: the 3D viewport top right, the node editor across the bottom, and the Spreadsheet top left. The Spreadsheet shows the actual numbers of a geometry, one row per vertex or point and one column per attribute, and it is the single most useful debugging tool, because it shows what the data is rather than what you think it is. The menu at its top left chooses which geometry it shows: **Evaluated** is the modifier's final result, **Original** is the object's data before any modifier (what Group Input receives), and **Viewer Node** is whatever is connected to a Viewer node. Selecting a node in the editor does not change what it shows; to inspect a point in the tree, connect that point to a Viewer.

In the node editor: Shift + A adds nodes, and typing immediately after Shift + A searches them by name. Drag from a socket to connect; drag a link into empty space to disconnect. Ctrl + right-drag across links cuts them. Tab enters a node group. Home frames the whole tree. N opens the sidebar, where the Group tab lists the tree's exposed inputs and outputs. Ctrl + Shift + click on a node connects it to a Viewer so the viewport and Spreadsheet show that node's result.

Sockets are typed and colored: green for geometry, gray for a number, yellow for a color, blue for a vector, pink for a boolean, orange for an object or collection, and a diamond shape means a field (Chapter 3). A link between mismatched types converts where it can and refuses where it cannot.

### Why every Molecular Nodes object is one

Molecular Nodes does not model a cartoon. It imports the atoms as points, with the data from the file stored on them as attributes, and adds a Geometry Nodes modifier whose tree reads those attributes and builds the cartoon, the sticks or the surface. A density map imports as a volume with the map values in a grid, and its tree turns the grid into a surface at a threshold. Click any Molecular Nodes object with the Geometry Nodes workspace open and you will see the tree: Group Input, a color node, a style node, Group Output. Everything in the Molecular Nodes menu is a node group designed to fit into that pattern, and everything in this part applies to it.

### Which tree you are looking at

The node editor shows one tree: the one in the active modifier of the active object. Its breadcrumb at the top left reads object › modifier › node group, and the Modifier tab (the wrench) shows the same group in each Geometry Nodes modifier's field. That field is the only link between an object and a tree: pick a different group there, or click New, and the object runs that one instead. A group with a user count of 0 beside its name belongs to no object and is gone after the file is saved and reopened, so point the modifier back at a Molecular Nodes tree before saving if you replaced it by accident.

To give a new object its own tree, select it, Add Modifier › Geometry Nodes, and click New in the empty field; rename the group at once (double-click its name) so that Geometry Nodes.001 and .002 do not pile up. Tab's meaning depends on where the mouse is: over the viewport it toggles Edit Mode, where X opens a menu for deleting vertices of the active object rather than the object itself; over the node editor it enters and leaves a node group. If the viewport header reads Edit Mode and you did not ask for it, press Tab again.

### Exercise 1.1: a tree from nothing

1. Add a Cube. In Modifier Properties, Add Modifier › Geometry Nodes, and click New. Open the Geometry Nodes workspace.
2. Between Group Input and Group Output, add Shift + A › Mesh › Operations › Subdivide Mesh (Level 2), then Shift + A › Geometry › Operations › Transform Geometry (Scale 2).
3. Disconnect the Transform node's output from Group Output, then reconnect it.

What you should see: the cube gains edges, then doubles in size, and disappears entirely while the output is disconnected. Apply nothing; the cube in Edit Mode is still eight vertices.

### Exercise 1.2: open a Molecular Nodes tree

1. Select your map and your model in turn with the Geometry Nodes workspace open.
2. Set the Spreadsheet's menu (top left) to Original and read the row count and the column names. Then Ctrl + Shift + click the style node, which connects it to a Viewer and switches the menu to Viewer Node, and read them again.

What you should see: the model's Group Input is a few thousand points with columns like `chain_id` and `b_factor`; after the style node it is a mesh with far more vertices and a `Color` column. The map's Group Input is a volume with a grid; after the style node it is a mesh. Each node changed the kind of data as well as its shape.

### Check yourself

1. What happens to geometry that is not connected to Group Output? *It is not shown; it exists only in the tree.*
2. Where do you see the actual numbers a node produces? *The Spreadsheet, after connecting the node to a Viewer with Ctrl + Shift + click; selecting the node is not enough.*
3. Which Spreadsheet setting shows the data Group Input receives? *Original.*
4. What does a Molecular Nodes model object contain before its tree runs? *Points, one per atom, with the file's data stored as attributes.*

## Chapter 2. Geometry and attributes

### Objectives

- Name the five geometry types and the domains each one has.
- Read and write attributes with Named Attribute and Store Named Attribute.
- List the attributes Molecular Nodes puts on a model and know which domain each lives on.
- Check the world scale of your file.

### The geometry types

A green socket can carry any of five kinds of geometry, and one geometry can contain several at once (a mesh plus some instances, say). Nodes act on the kinds they understand and pass the others through.

- **Mesh**: vertices, edges and faces, with face corners as a fourth level. Everything renderable as a surface is a mesh by the time it reaches Group Output.
- **Curves**: control points joined into splines, with a radius per point. They render only after Curve to Mesh or with a profile; Molecular Nodes builds cartoons by making curves through the backbone and sweeping a profile along them.
- **Point cloud**: points with a radius and no connections. A Molecular Nodes model is a mesh with only vertices, which behaves like points; Mesh to Points converts it to a true point cloud for instancing.
- **Instances**: references to a piece of geometry placed many times, each with a transform. Cheap to display and render; Realize Instances turns them into real geometry when a later node needs to edit them.
- **Volume**: a grid of values in space, either as a Blender volume object or as named grids inside geometry. A density map is this. Grids have no vertices; they are converted to a mesh at a threshold (Chapter 6).

### Domains

An attribute lives on one domain of its geometry: Point (vertices or points), Edge, Face, Face Corner, Spline (for curves), Instance, or Layer (for Grease Pencil). `position` is on Point. A face's shade-smooth flag is on Face. Molecular Nodes stores its atom data on Point, one row per atom. When a node needs an attribute on a different domain, Blender interpolates: reading a Point attribute on Face averages the face's corners. Store Named Attribute lets you pick the domain explicitly, and the Spreadsheet has a tab per domain so you can see where a column lives.

### Reading and writing attributes

- **Named Attribute** (Shift + A › Geometry › Read › Named Attribute) reads an attribute by name, as a field of the chosen type: Float for `b_factor`, Integer for `chain_id`, Color for `Color`, Vector for `position`. An attribute that does not exist reads as zero, and the node shows a warning, which is the first thing to check when a chain does nothing.
- **Store Named Attribute** (Shift + A › Geometry › Write) writes a value into an attribute on a domain, creating it if needed. Geometry passes through. This is how a computed value, such as a distance, becomes something the material can read with its Attribute node.
- **Capture Attribute** stores a value under an anonymous name for use later in the same tree, which Chapter 3 explains.
- Attributes are also visible in the Data tab of the Properties editor under Attributes, where they can be added, removed and renamed by hand.

### What Molecular Nodes gives you

On a model, on the Point domain ([Attributes](https://bradyajohnston.github.io/MolecularNodes/attributes.html)):

| Attribute | Type | Meaning |
| --- | --- | --- |
| `position` | Vector | Atom coordinates, scaled by the world scale |
| `Color` | Color | The current per-atom color, written by the Color nodes |
| `chain_id` | Int | Chain, as an integer index; the names are in the Molecular Nodes panel |
| `res_id` | Int | Residue number |
| `res_name` | Int | Residue type as an integer code |
| `atomic_number` | Int | Element |
| `b_factor` | Float | B-factor, or pLDDT for AlphaFold models |
| `vdw_radii` | Float | Van der Waals radius in world units |
| `sec_struct` | Int | Secondary structure class |
| `is_backbone`, `is_side_chain`, `is_alpha_carbon` | Bool | Backbone classification |
| `entity_id`, `model_id`, `occupancy`, `charge` and others | Various | From the file, where present |

Strings cannot be attributes, so chain and residue names are stored as integers, and the Molecular Nodes select nodes translate between the two.

On a map, the data is a grid named after the file, not a Point attribute. After the Density Style Surface it is a mesh with a `Color` attribute and nothing else, which is why coloring a map needs data sampled from the model (Chapter 5).

### World scale

Molecular Nodes scales coordinates on import. In Blender 5 the scale is 0.1, so 1 nm equals 1 m and a 15 nm complex is 15 m across; in earlier versions it was 0.01, so 1 Å equaled 1 cm and the same complex was 1.5 m. Every distance in this guide, from Subsurface Scale to the wet collar's reach, depends on it. Check once per file: select the model, press N › Item and read Dimensions, then compare with the real size.

### Exercise 2.1: read the Spreadsheet

1. Select the model and set the Spreadsheet's menu to Original, which shows the atoms exactly as Group Input receives them.
2. Show only one residue with a row filter. The Spreadsheet cannot sort, but it can filter: with the mouse over the Spreadsheet press N to open its sidebar, add a row filter with the + button, set its column to `res_id`, Equal To, 19, and make sure the funnel icon (Use Filter) in the Spreadsheet's header is on.
3. Ctrl + Shift + click the style node to view its output, then switch the domain list on the left from Vertex to Face.

What you should see: a handful of rows for residue 19, one per atom, each with its element and chain. After the style node, the Vertex tab still has the atom columns, because Style Cartoon copies them onto the cartoon's vertices, but the Face tab has different, face-level columns. Where a column appears tells you which domain it lives on.

### Exercise 2.2: write an attribute and read it in a material

1. Add a Store Named Attribute node (Domain Point, Float, Name `height`) and drop it onto the link between the style node and Join Geometry so it splices in. Its Geometry output must continue on to Group Output; a Store node on a side branch writes to a copy that is thrown away.
2. Add a Position node and a Separate XYZ node, and draw Position → Separate XYZ's Vector input. Separate XYZ › Z is now each vertex's height in meters.
3. Rescale it to 0 to 1 so the material needs no numbers. Add an Attribute Statistic node (Float, Point): style node's Geometry → its Geometry, Separate XYZ › Z → its Attribute. Add a Map Range: Separate XYZ › Z → Value, Attribute Statistic › Min → From Min, Attribute Statistic › Max → From Max, To Min 0, To Max 1. Then Map Range › Result → Store Named Attribute's Value. The Spreadsheet's Vertex tab now shows a `height` column running from 0 to 1.
4. Make a material for the test. A Molecular Nodes object has no material in its slots, because the style node assigns it, so the Material tab only offers New: click New, double-click the name and rename it `height_test`, then on the style node click its Material field (it shows Default) and pick `height_test`. Open the Shader Editor: click the Editor Type menu in the top-left corner of the node editor and choose Shader Editor, **or click the Shading workspace tab at the top of the window.** With the model selected, the Shader Editor's header shows `height_test`. Press Shift + A, type Attribute to add one, and set its Name to `height`. Add a Color Ramp the same way, then draw Attribute › Fac → Color Ramp's Fac, and Color Ramp › Color → Principled BSDF's Base Color.
5. Turn the Viewer off (the icon in its header) and view in Material Preview or Rendered. Solid mode never shows a shader.

What you should see: the model colored by height. The whole route from a geometry node to a pixel is Store Named Attribute on one side and Attribute on the other.

### Check yourself

1. Which domain do Molecular Nodes atom attributes live on? *Point.*
2. Why are chain names stored as integers? *Geometry Nodes cannot store strings as attributes.*
3. A Named Attribute node reads all zeros. What is the likeliest cause? *The name is misspelled or the attribute is on a different geometry than the one connected.*
4. How do you confirm the world scale of a file? *N › Item › Dimensions on the model, compared with its real size.*

## Chapter 3. Fields

### Objectives

- Explain what a field is and recognize one by its diamond socket.
- Use Position, Index, Normal and Named Attribute as fields inside Math and Compare nodes.
- Drive a Selection input with a comparison.
- Explain why Capture Attribute exists and when you need it.
- Bring data from one geometry onto another with Sample Index, Sample Nearest and Geometry Proximity.

Fields are the idea that makes Geometry Nodes different from a flowchart, and the one that confuses everyone at first. Once it is clear, every node in Chapter 4 reads the same way.

### A field is a function, not a number

A gray socket carrying a number can carry two different things. A circle socket carries one value: a single roughness, a single scale. A diamond socket carries a field: a rule that produces a value for each element of whatever geometry it is eventually evaluated on. The Position node outputs a field; it does not output one position, it outputs "the position of this element," and the node that consumes it, say Set Position, evaluates it once per vertex.

So a Math node fed by Position → Separate XYZ › Z does not compute one number; it computes "Z of this point" for every point of the geometry the result is applied to. Which geometry? The one connected to the node that finally consumes the field. The field itself is geometry-free until then, which is why the Spreadsheet shows nothing for it and why the same chain can be reused on a different mesh.

A diamond socket with a dot in it means the field is currently just a single value; a plain diamond means it depends on per-element data. Hover over any socket for a tooltip saying which.

### The built-in fields

- **Position**: the location of the element, in the object's local space.
- **Index**: the element's number, 0 upward, in the order the geometry stores it. Molecular Nodes stores atoms in file order, so Index on the atoms is the atom's serial position.
- **Normal**: the direction a face or point faces.
- **Named Attribute**: any stored attribute, by name, including everything in the table in Chapter 2.
- **ID**, **Radius**, **Spline Parameter** and the rest are the same idea for their domains.

Any Math, Vector Math, Compare, Map Range, Color Ramp or Mix node accepts fields and stays a field, so you can write expressions: "points whose `b_factor` is above 60," "the distance of this point from the origin," "a color from `res_id`."

### Why Position has no input

The Spreadsheet is the right picture of a field. Each row is one element, and Position is one of its columns. A node with no geometry input and a diamond output is a question each element answers about itself: Position asks "where am I?", so it needs no wire telling it which geometry to read.

A chain such as Position → Separate XYZ › Z → Map Range is a formula written once, height = (Z − Min) / (Max − Min), that nobody has run yet. Separate XYZ and Map Range only extend the formula. It runs the moment it reaches a node with a Geometry input beside the field input: Store Named Attribute, Attribute Statistic, Set Position, or a Selection socket on Delete Geometry. That node supplies the rows and computes the formula for each one. This is why Store Named Attribute must sit after Style Cartoon in Exercise 2.2: the geometry flowing into it decides whose positions are read.

Dashed links carry a formula; solid links carry one number. In the height chain, Z → Map Range and Map Range → Store are dashed. Min and Max arrive on solid links, because Attribute Statistic collapses the whole column into single numbers. Map Range mixes the two: a value that changes per row and two constants.

The same Position can answer differently for two consumers. Feed Attribute Statistic the atoms (Group Input › Atoms) and feed the cartoon mesh to Store Named Attribute: Min and Max come from atom positions, while the written values come from cartoon vertices.

| Node | What it asks each element |
| --- | --- |
| Position | Where am I? |
| Normal | Which way does the surface face here? |
| Index | Which row am I? |
| Named Attribute | What is in my column called X? (`chain_id`, `res_id`, `b_factor`) |
| Spline Parameter | How far along my curve am I, 0 to 1? |
| Random Value | A random number, different for each element |
| Sample Grid | What value does a grid hold at my position? (Chapter 7, project 2) |

Scene Time and Object Info also have no geometry input, but they give one answer for everything, so they are single values, not fields. Some nodes read Position without a wire: Set Position, Geometry Proximity, Sample Nearest and Sample Grid use each element's own position when their position socket is left empty. That is how chain 1 of the slime measures distance from every cartoon vertex with no Position node in sight.

The Shader Editor works the same way. Texture Coordinate and Geometry have no inputs either; they answer per shading point instead of per vertex.

### Selections

Most nodes have a Selection input, a boolean field that defaults to true everywhere. Connect a Compare node (Shift + A › Utilities › Math › Compare) and the node acts only where the comparison is true: Named Attribute `chain_id` → Compare (Equal, B = 0) → Selection on a Delete Geometry node deletes chain 0 only. Molecular Nodes' Select nodes are prebuilt comparisons of exactly this kind, which is why they plug into the Selection socket of every style node.

### Capture Attribute: freezing a field

A field is evaluated on the geometry at the point where it is consumed. If the geometry changes between where you set up the field and where you use it, the field evaluates on the new geometry, which is usually not what you meant. The standard example: after Instance on Points and Realize Instances, Index and Random Value count the vertices of every sphere instead of the atoms, so a random color per atom turns into a speckle per vertex. Capture Attribute (Shift + A › Attribute) evaluates the field on the geometry passing through it right now and carries the result forward as an anonymous attribute, so later nodes read the frozen values: Instance on Points copies it onto each instance, and Realize Instances onto every vertex of that instance. The rule of thumb: when a value should be computed on the geometry before a node that changes the geometry, capture it before that node. Fields wired into a node's own inputs need no capture: Instance on Points evaluates its Selection, Rotation and Scale on the points it receives.

### Data from another geometry

Fields read from the geometry they are evaluated on. To read from a different geometry, three nodes bridge the gap:

- **Sample Index** (Shift + A › Geometry › Sample): read the value of an attribute at a given index on another geometry. Molecular Nodes uses it internally to copy atom data onto the cartoon it builds.
- **Sample Nearest**: for each element here, find the nearest element of another geometry and return its index; chain it into Sample Index to read that element's attribute. Older Molecular Nodes versions packaged this pair as a Sample Nearest Attribute node; with or without it, the pair is how a map borrows the model's colors.
- **Geometry Proximity**: for each position here, the closest point on another geometry and the distance to it. It is a distance field to any object, which is the basis of the wet collar in the slime project.

In every case the other geometry arrives through an Object Info node (Shift + A › Input › Scene › Object Info), with Relative ticked so the two objects' transforms are reconciled.

### Exercise 3.1: see a field evaluate

1. On the subdivided cube from Chapter 1, add Set Position between the Subdivide and the Transform nodes.
2. Position → Separate XYZ › Z → Math (Multiply, 0.5) → Combine XYZ (into Z only) → Set Position › Offset.
3. Ctrl + Shift + click the Math node, and look at the Spreadsheet.

What you should see: the top of the cube lifts and the bottom sinks, by an amount that depends on each vertex's own height; and the Spreadsheet's Viewer column lists one number per vertex, which is the field evaluated.

### Exercise 3.2: a selection on the model

1. On the model, before the style node, add Delete Geometry. Named Attribute (Float, `b_factor`) → Compare (Greater Than, B 80) → Selection.

What you should see: the most mobile atoms vanish from the cartoon, and the threshold is a single number you can drag. Swap Delete Geometry for Separate Geometry and both halves are available to style differently.

### Exercise 3.3: capture before you instance

1. Mesh to Points on the model's atoms (Group Input › Atoms, or Set Color's output so the chain colors come along) → Instance on Points with an Icosphere: Mesh to Points' output → its Points socket, and an Ico Sphere (Shift + A › Mesh › Primitives, Radius 0.08, Subdivisions 2) → its Instance socket, so one sphere lands on every atom. Position → Separate XYZ › Z → Map Range (To Min 0.5, To Max 2) → the Scale socket on the instancer, Instance on Points, so each sphere is sized by its atom's height. From Min and From Max come from an Attribute Statistic (Float, Point) with Mesh to Points' output in its Geometry and the same Z in its Attribute; with nothing in Geometry both read 0, and every sphere gets To Min.
2. Add Realize Instances after Instance on Points, then Store Named Attribute (Float, Point, Name rand) with a Random Value (Float) as its Value. Spheres made in the tree have no material of their own, so give them one: click New in the Material tab and rename it, then add Set Material (Shift + A › Material) after Store with that material picked. In the Shader Editor (Editor Type menu at the node editor's top-left, as in Exercise 2.2), read rand in a material: Attribute › Fac → Color Ramp → Base Color. Then insert a Capture Attribute (Point) between Mesh to Points and Instance on Points, drag Random Value › Value into its empty bottom socket to add a capture item, and connect that item's output, on the node's right side, to Store's Value instead.

What you should see: after step 1 every sphere is sized by its atom's height, with no capture, because Instance on Points evaluates its Scale field on the points it receives. In step 2 the uncaptured version speckles every sphere, because after Realize Instances the random number is drawn once per sphere vertex; the captured version paints each sphere one solid color, because the number was drawn once per atom and carried onto every vertex of its sphere.

The same trap catches a selection placed after instancing. Separate Geometry, Delete Geometry and Set Position on the Point domain reach inside each instance and evaluate on the instanced mesh itself. Named Attribute `b_factor` → Compare → Separate Geometry after Instance on Points therefore reads 0 on the sphere's own vertices: Greater Than removes every sphere and Less Than keeps them all, whatever the threshold. Set the domain to Instance, where Instance on Points has copied `b_factor` onto each instance, or wire the comparison into Instance on Points' Selection socket so the unwanted atoms never get a sphere.

### Exercise 3.4: four more formulas on the height chain

Each variant reuses the tree from Exercise 2.2. Change only what is named, keep Attribute Statistic and Map Range, and watch the `height` column and the material update.

1. Side to side: connect Sepfarate XYZ › X instead of Z to both Map Range's Value and Attribute Statistic's Attribute.
2. B-factor, like `spectrum b` in PyMOL: replace Position → Separate XYZ with Named Attribute (Float, Name `b_factor`), feeding both nodes. Check first that `b_factor` appears among the Spreadsheet's columns on the Viewer output.
3. Which way the surface faces: replace Position with Normal and keep Separate XYZ › Z. Upward-facing parts read 1 and downward-facing parts −1 before Map Range rescales them.
4. Core versus surface: distance from the center only works for a sphere, so measure to the surface instead. Add Style Surface on Group Input › Atoms as a branch that goes nowhere else, then Geometry Proximity with Target Element set to Faces and that surface as Target; leave Sample Position empty. Its Distance is each vertex's depth below the nearest surface, including the lining of a channel or cavity. Feed Distance into Attribute Statistic and Map Range in place of Z. An SDF grid holds true distances only within its band (3 voxels for Points to SDF Grid), so Proximity is the exact route.

What you should see: a gradient across the model in each case: left to right, by refinement B-factor, by facing, and from the surface inward. In variant 4 the exposed loops are dark and the buried core bright whichever way the model is turned, because a depth does not depend on the view, and the lining of any channel through the model is dark as well.

### Check yourself

1. What is the difference between a circle socket and a diamond socket? *A circle carries one value; a diamond carries a field, a rule evaluated per element.*
2. On which geometry is a field evaluated? *The geometry connected to the node that consumes it.*
3. What does Capture Attribute protect you from? *A field evaluating on later, changed geometry instead of the geometry you meant.*
4. Which node gives a distance from every point of one object to the surface of another? *Geometry Proximity.*

## Chapter 4. The core vocabulary

### Objectives

- Recognize the twenty nodes that do most of the work in any tree.
- Say, for each, what goes in, what comes out, and what you would use it for on a molecule.

Geometry Nodes has several hundred nodes. These twenty cover nearly every tree you will read or build. Each is listed by the menu path under Shift + A, with search by name as the faster route.

| Node | Menu | Takes | Gives | Use it for |
| --- | --- | --- | --- | --- |
| Set Position | Geometry › Write | Geometry, Position or Offset field | Moved geometry | Deforming, pushing along normals, jitter |
| Transform Geometry | Geometry › Operations | Geometry, Translation, Rotation, Scale | Moved geometry | Placing a part, scaling a whole map |
| Join Geometry | Geometry | Several geometries | One geometry | Combining two styles, adding a collar to a map |
| Separate Geometry | Geometry › Operations | Geometry, Selection | Selected and Inverted | Two styles for two parts of one model |
| Delete Geometry | Geometry › Operations | Geometry, Selection | The rest | Hiding solvent, trimming a map |
| Set Material | Geometry › Material | Geometry, Selection, Material | Geometry with material | Assigning your slime material after a join |
| Mesh to Points | Mesh › Operations | Mesh | Point cloud | Preparing atoms for instancing |
| Instance on Points | Instances | Points, Instance geometry, Scale, Rotation | Instances | Spheres on atoms, arrows on residues |
| Realize Instances | Instances | Instances | Real mesh | Before any node that edits instance geometry |
| Curve Line, Curve Circle, Bézier Segment | Curve › Primitives | Points or parameters | A curve | Strands, profiles for sweeps |
| Set Curve Radius | Curve › Write | Curve, Radius field | Curve | Tapering strands |
| Curve to Mesh | Curve › Operations | Curve, Profile curve | Mesh | Turning a strand or a backbone into a tube |
| Spline Parameter | Curve › Read | Curve (field) | Factor 0 to 1 along the spline | Driving taper or color along a strand |
| Points to Volume, Volume to Mesh | Point, Volume | Points and radius; volume and threshold | Volume; mesh | Blobby envelopes around atoms |
| Mesh to SDF Grid, Grid to Mesh | Volume | Mesh, voxel size; grid | SDF grid; mesh | The meniscus chain (Chapter 6) |
| SDF Grid Boolean, SDF Grid Fillet | Volume › Operations | Two grids; a grid and Iterations | Combined grid | Smooth unions |
| Geometry Proximity | Geometry › Sample | Target geometry, Source Position | Position and Distance fields | Wetness by distance to the map |
| Sample Nearest, Sample Index | Geometry › Sample | Another geometry, an attribute | Index; the value at an index | Borrowing the model's color for the map |
| Named Attribute, Store Named Attribute | Geometry › Read, Write | Name; name, value, domain | Field; geometry with attribute | Reading `chain_id`; writing `wet` |
| Object Info | Input › Scene | An object | Its geometry, location, rotation | Bringing the map into the model's tree |

Three habits make the table usable. First, Geometry passes through almost every node, so chains are built by inserting a node onto an existing link (drop it on the link and it splices in). Second, the gray inputs are fields, so any of them can be driven by a computation rather than a number. Third, a node that does not do what you expect is usually receiving the wrong geometry type: a Set Curve Radius on a mesh, a Realize Instances on nothing instanced.

### Exercise 4.1: spheres on atoms, by hand

1. Start clean: hide your other molecules (the eye icons in the Outliner) and import the structure again with Molecular Nodes, from its tab in the viewport sidebar (N), the way you imported it the first time; any style will do, since you will delete it. The new object comes with its own node tree: check that the breadcrumb at the top of the node editor names the new object. In that tree, delete the style node, which leaves Set Color's Atoms output free.
2. Set Color › Atoms → Mesh to Points' Mesh, then Mesh to Points → Instance on Points with Shift + A › Mesh › Primitives › Ico Sphere (Radius 1, Subdivisions 2) as the Instance. With a radius of 1, the Scale you give each copy is its radius in scene units.
3. Named Attribute (Float, `vdw_radii`) → Scale on the instancer, so every sphere takes its element's van der Waals radius; Molecular Nodes stores it in scene units, 0.17 for carbon. For ball-and-stick proportions, put Math (Multiply, 0.3) in between. Then Realize Instances → Set Material → Group Output.

What you should see: a space-filling model built from four nodes, with atom radii by element. This is what Molecular Nodes' Style Spheres does inside, plus color.

### Exercise 4.1, part 2: one look per element

Molecular Nodes stores each atom's element as `atomic_number`: 1 hydrogen, 6 carbon, 7 nitrogen, 8 oxygen, 16 sulfur. Instance on Points and Realize Instances carry it onto every vertex of that atom's sphere, so Set Material nodes after Realize Instances can choose a material by element.

1. Check which elements your model has. With the Viewer on Realize Instances' output, add a Spreadsheet row filter on `atomic_number`, Equal To 1. Cryo-EM models refined in Phenix usually carry no hydrogens, so expect no rows; to have them, add hydrogens in ChimeraX (`addh`), save the model, and import that file.
2. Make one material per element. In the Material tab press + to add a slot, click New and rename it; repeat for `atom_C` (light gray, Roughness 0.6), `atom_O` (red), `atom_N` (blue), `atom_S` (yellow) and `atom_H` (white). The slots make each material reachable from the Shader Editor's Slot menu. Give them different Roughness or Coat values too, and the elements differ in finish as well as color.
3. After Realize Instances, chain five Set Material nodes. The first sets `atom_C` with nothing in Selection, so every sphere starts as carbon. Each of the others sets one element, with Selection = Compare (Integer, Equal, B = that element's number) whose A comes from one shared Named Attribute (Integer, `atomic_number`).
4. Optional: to hide hydrogens, as most figures do, put Delete Geometry before Mesh to Points with Selection = Compare (Integer, Equal, A = `atomic_number`, B = 1).

What you should see: the space-filling model in the standard CPK colors, carbon gray, oxygen red, nitrogen blue, sulfur yellow, with hydrogens white and visibly smaller, since their van der Waals radius is 1.2 Å against carbon's 1.7 Å. A later Set Material overrides an earlier one only where its selection is true, which is why carbon goes first as the catch-all.

One material instead of five: in a single material, Attribute (`atomic_number`) › Factor → Map Range (From Min 0, From Max 20, To Min 0, To Max 1) → Color Ramp set to Constant, with a stop just below each element's value: white at 0.03, gray at 0.28, blue at 0.33, red at 0.38, yellow at 0.78. With Constant interpolation each atom takes the stop at or below its value, and placing the stops slightly below keeps rounding from dropping an atom into the previous color. This colors by element but gives every element the same finish, which is what separate materials add.

### Exercise 4.2: a tube from scratch

1. Curve Line (Start 0,0,0, End 0,0,1) → Resample Curve (Count 32) → Set Curve Radius with Spline Parameter › Factor → Float Curve (a dip in the middle) → Curve to Mesh with a Curve Circle (Radius 0.02) as Profile → Set Material.

What you should see: a tube that is thin in the middle, which is the strand from the slime project. Replace the Curve Line with a Bézier Segment and it sags.

### Check yourself

1. Which node must come before editing the mesh of instanced spheres? *Realize Instances.*
2. Which node brings another object's geometry into a tree? *Object Info.*
3. What is the quickest way to insert a node into an existing chain? *Drop it onto the link.*
4. Which pair of nodes writes a computed value for the material to read? *Store Named Attribute in the tree, Attribute in the material.*

## Chapter 5. Reading and editing a Molecular Nodes tree

### Objectives

- Read the default model tree and the default density tree node by node.
- Give different chains different styles and materials in one object.
- Color a density surface from the model it encloses.
- Expose a value to the modifier panel so it can be changed without opening the tree.

Molecular Nodes' node groups are ordinary Geometry Nodes groups with a consistent design, so once you know the pattern, every tree it makes is readable ([Fetch from the PDB](https://bradyajohnston.github.io/MolecularNodes/tutorials/importing.html)).

### The model tree

Group Input carries the atoms as points with their attributes. The first node is a Color node, for example Color Common or Color Chain, which writes the `Color` attribute by element or by chain; it changes data, not geometry. The last node is a Style node, Style Cartoon, Style Ribbon, Style Surface, Style Sticks, Style Ball and Stick or Style Spheres, which builds new geometry from the atoms and copies `Color` onto it. Group Output shows the style's result. Every style node has a Selection socket, so a Select node (Select Chain, Select Res ID and the rest, under Shift + A › Molecular Nodes › Select) plugged into it limits the style to part of the model, and a Material socket, which is how the [Recipes part](01-material-recipes.md) assigns your materials.

To add nodes from the Molecular Nodes library use Shift + A › Molecular Nodes, which has submenus for Style, Select, Color, Animate, Topology, Density and Utilities. Each is a node group; Tab opens it to see how it is built, and this part's chapters are enough to read what you find inside.

### The density tree

Group Input carries the volume. A Density Style Surface, Wire or ISO Surface node turns it into a mesh at the Threshold and gives it a color and material. Group Output shows the mesh. There are no atom attributes anywhere in this tree, which is why the map's material has only the style's Color to work with unless you sample from the model.

### Two styles in one object

The style must be the last thing applied to a piece of geometry, because its output is a mesh and no longer atom-like. To show cartoon for one chain and sticks for another, run two style nodes in parallel from the same Color node, each with its own Select node on Selection, and merge them with Join Geometry before Group Output. Each branch can carry its own material. The same pattern gives ribbons for the backbone and ball-and-stick for a ligand: Select Res Name picks the ligand into one branch, and its inverse (the Select node's Inverted output, or a Boolean Math Not) picks the rest into the other.

### Coloring a map from the model

The map mesh has no chain data, so it borrows the model's: for every vertex of the surface, find the nearest atom and copy its `Color`. Current Molecular Nodes versions no longer list a Sample Nearest Attribute node under Density, so build the same thing from Blender's own nodes in the map's tree. Object Info (Relative on) brings in the model. Sample Nearest (Point) takes the model's geometry and returns, for each surface vertex, the index of the nearest atom. Sample Index (Color, Point) takes the model's geometry, Named Attribute (Color, `Color`) as its Value and Sample Nearest › Index as its Index, and returns that atom's color. Store Named Attribute (Color, Point, Name `Color`) writes it onto the surface, between the Density Style node and Join Geometry. The model object should ideally be outputting atoms, not a cartoon, so that every bit of density takes the color of the atom inside it, side chains and glycans included; the CryoEM Maps tutorial duplicates the model and removes the style on the copy ([CryoEM Maps](https://bradyajohnston.github.io/MolecularNodes/tutorials/cryoem.html), which still shows the older node). On that copy, also mute the Color Element node (M), so every atom carries its chain color: Color Element paints nitrogens blue and oxygens red, and a surface sampled from them comes out speckled. Sampling the cartoon object directly also works and needs no copy, because the cartoon's vertices carry the chain colors of their alpha carbons; but the cartoon holds only the backbone, so density over side chains, glycans and ligands takes the color of the nearest backbone, which at a chain interface can be the neighboring chain's. The material then reads `Color` with an Attribute node, as in the [Recipes part](01-material-recipes.md).

### Exposing inputs

Any value in a tree can become a slider on the modifier panel: drag a link from the node's input socket to the empty socket at the bottom of Group Input, and name it in the N panel's Group tab. A density threshold, a wetness reach or a strand radius exposed this way can be adjusted from the Modifier Properties without opening the node editor, and keyframed there for animation. Group Input sockets also accept an Object, which is how a tree can be pointed at a different map without editing it.

### Exercise 5.1: two styles, two materials

1. On the model, add a second style node, Style Ball and Stick, fed from the same Color node, with Select Chain set to one chain on its Selection; set the cartoon's Select Chain to the inverse.
2. Join Geometry both into Group Output. Give the cartoon branch the satin plastic material and the ball-and-stick branch glossy candy.

What you should see: one chain as colored sticks with glossy balls, the rest as a satin cartoon, in one object.

### Exercise 5.2: expose the threshold

1. On the map, drag the Density Style Surface's Threshold input to Group Input and name it `Contour`.
2. In Modifier Properties, change `Contour` and watch the surface.

What you should see: the contour level as a slider on the modifier, which is how you would keyframe a contour sweep for a talk.

### Check yourself

1. Why must a style node be last in its branch? *Its output is a mesh, not atoms; later Molecular Nodes nodes expect atoms.*
2. How do two styles end up in one object? *Parallel branches from one Color node, joined by Join Geometry.*
3. Why does the map need Sample Nearest and Sample Index to show chain colors? *Its mesh carries no atom data; the pair copies `Color` from the nearest atom of the model.*
4. How do you make a tree value adjustable from the modifier panel? *Connect it to a new Group Input socket and name it.*

## Chapter 6. Volumes, grids and SDFs

### Objectives

- Explain what a grid is, and the difference between a density grid and an SDF grid.
- Convert between meshes and grids in both directions and choose a voxel size.
- Build smooth unions, offsets and fillets with the SDF nodes.

A density map is a grid, so this chapter is the one that explains what your maps are and what the SDF chain in the slime project does.

### What a grid is

A grid is a value at every point of a regular 3D lattice of voxels. A cryo-EM map is a grid of density values; the Density Style node draws the surface where the value crosses the threshold. A signed distance field, SDF, is a grid of a different quantity: at every voxel, the distance to the nearest surface, negative inside and positive outside. Its surface is where the value crosses zero. SDFs are what make shape operations easy: union is the minimum of two distances, intersection the maximum, offset adds a constant, and smoothing filters the values. Meshes make these operations hard; grids make them one node each.

In Blender 5, grids travel inside geometry alongside meshes and curves, with a name each. Get Named Grid and Store Named Grid read and write them; Grid Info reports voxel size and bounds; the Spreadsheet's Volume Grids tab lists them. A Molecular Nodes map carries one grid named after the file.

### Converting

- **Grid to Mesh** (Shift + A › Volume › Operations): a surface at a threshold, with Adaptivity to reduce triangles on flat regions. For a density grid the threshold is the contour level; for an SDF it is 0. This is what the Density Style Surface does inside.
- **Mesh to SDF Grid**: a closed mesh becomes an SDF grid. Voxel Size sets resolution; Band Width, in voxels, is how far from the surface distances are stored. A mesh with holes gives a grid with leaks.
- **Mesh to Density Grid**: a mesh becomes a filled density grid, for use with scatter and fog rather than shape operations.
- **Points to SDF Grid**: points with radii become a blobby SDF, which is the metaball effect as a grid; useful for a cloud of atoms as one surface.
- **Points to Volume** and **Volume to Mesh**: the older, simpler pair, which still works and is what Molecular Nodes' Style Surface uses for the molecular surface.
- **Field to Grid**: any field evaluated on a lattice becomes a grid, which is how a formula or a distance becomes a volume.

### Shape operations on SDFs

- **SDF Grid Boolean**: Union, Intersection or Difference of two grids. Both need the same voxel size.
- **SDF Grid Fillet**: rounds the concave creases of a grid a little further with each of its Iterations, which is what turns a union into a smooth blend and gives the slime a meniscus. The rounding is measured in voxels, so a coarser Voxel Size gives a larger fillet for the same Iterations.
- **SDF Grid Offset**: grows or shrinks the surface by a distance, the grid version of a Solidify or a shell.
- **SDF Grid Mean** and **Median**, **Laplacian**: smoothing filters, each a different flavor of blur on the distances, for taking the voxel steps out of a surface or the noise out of a map-derived one.
- **Grid Dilate & Erode**, **Prune Grid**, **Clip Grid**: housekeeping, for trimming a grid to a box or removing stray voxels.

### Choosing a voxel size

Voxel size is the resolution of everything after it. Too large and the surface shows steps and loses detail; too small and the grid is slow and heavy, since halving the voxel size multiplies the voxel count by eight. A rule for a meniscus: voxel size about a tenth of the tube width, so a 0.1 m tube uses 0.01 m voxels. For an envelope around a whole map, a fiftieth of the map's width is plenty. Match the voxel size on every grid that meets in a Boolean.

### The map's own threshold

The contour level on a density map is a threshold on density; the SDF nodes need a distance. To treat a map as a shape, first make a mesh from it at the contour level (the style node does this), then Mesh to SDF Grid. Going the other way, Grid to Mesh on the raw density grid at a chosen threshold reproduces the style node without Molecular Nodes, which is useful when you want the map in a tree with no add-on dependency.

### Exercise 6.1: smooth union

1. A Cube and a UV Sphere overlapping, both in one tree via Object Info. Mesh to SDF Grid on each (Voxel Size 0.02), SDF Grid Boolean (Union), Grid to Mesh.
2. Insert SDF Grid Fillet before Grid to Mesh with Iterations 0, 3 and 10.

What you should see: a cube and sphere fused with a sharp crease, then a soft crease, then a melted join. That melt is the meniscus of the slime project.

### Exercise 6.2: atoms as one blob

1. On the model, Mesh to Points → Points to SDF Grid (Radius 0.08, Voxel Size 0.02) → Grid to Mesh → Set Material.

What you should see: a space-filling envelope built from one grid, smoother than instanced spheres. Raise Radius and the envelope swells into a molecular surface.

### Check yourself

1. What value does an SDF store at each voxel? *The signed distance to the nearest surface: negative inside, positive outside.*
2. What threshold draws the surface of an SDF grid? *Zero.*
3. Why must two grids share a voxel size before a Boolean? *The operation compares them voxel by voxel.*
4. What does SDF Grid Fillet do? *Rounds concave creases, further with each iteration, turning a union into a smooth blend.*

## Chapter 7. Worked projects: the sticky slime and local resolution

### Objectives

- Build the four effects of the sticky slime as node chains and explain every node in them.
- Combine data from two objects in one tree.
- Leave the result adjustable from the modifier panel.
- Paint cryoSPARC's local resolution onto a map surface and onto the model built into it with Sample Grid.

This chapter builds two projects with everything from Chapters 2 to 6. The first is the sticky slime: the [Recipes part](01-material-recipes.md) gives its settings, this chapter the reasoning, chain by chain. Build it on your map and model with the slime material from the [Recipes part](01-material-recipes.md) already assigned. The second, after the slime exercises, paints cryoSPARC's local resolution onto the map surface and onto the model.

### Chain 1: the wet collar (model tree)

The goal is a per-vertex number on the cartoon, 1 where it touches the slime and 0 a short way out, that the material reads.

1. **Object Info**, Object: the map, Relative on. This brings the map's evaluated geometry, which is the surface the style node made, into the model's tree, in the model's coordinate space.
2. **Geometry Proximity**, Target Element: Faces. Target: the Object Info geometry. Its Distance output is a field: for every element it is evaluated on, the distance to the nearest point of the map surface.
3. **Map Range**, From 0 to 0.2, To 1 to 0, Clamp on. Turns distance into wetness: 1 at contact, 0 at 0.2 m and beyond. The From Max is the reach; expose it to Group Input as `Wet reach`.
4. **Store Named Attribute**, inserted on the link after the style node, Domain Point, Float, Name `wet`, Value from the Map Range. Because the geometry passing through is the cartoon, the proximity field is evaluated on the cartoon's vertices, which is what you want.

The material then reads `wet` with an Attribute node into Coat Weight, a darkening Mix and Roughness, as the [Recipes part](01-material-recipes.md) lists. If `wet` reads as zero in the material, the Store node is before the style node rather than after it, so the attribute was written on atoms the style discarded.

### Chain 2: the meniscus (map tree)

The goal is a surface that is the slime and the tubes fused, with the crease between them rounded.

1. **Density Style Surface** as before, its output mesh going on to the next node.
2. **Mesh to SDF Grid**, Voxel Size 0.02, Band Width 3. The slime surface as distances.
3. **Object Info**, Object: the model, Relative on, into a second **Mesh to SDF Grid** with the same Voxel Size. The model must be outputting closed mesh geometry: cartoon, ribbon or sticks are closed tubes; Style Spheres as points is not a mesh.
4. **SDF Grid Boolean**, Union. The minimum of the two distances, which is both shapes as one.
5. **SDF Grid Fillet**, Iterations 3. Rounds the concave crease where the tubes enter the slime into a curve that climbs the tube. Expose Iterations as `Meniscus`.
6. **Grid to Mesh**, Threshold 0, Adaptivity 0.2 to keep the mesh light. **Set Material** with the slime material, then Group Output.

The union mesh wraps the tubes in a thin slime skin everywhere, not only at the exits. Two ways to handle it: keep the original model object visible so its own material shows through the skin, which works because the skin is thin and the slime is translucent; or limit the union to the exits by inserting **Delete Geometry** on the model's mesh before its Mesh to SDF Grid, deleting where Geometry Proximity to the slime surface is greater than the meniscus reach, so only the parts of the tubes near the surface are fused in.

### Chain 3: strands (a new object)

Strands are curves with a tapered radius, swept into tubes.

1. On a new Empty mesh object with a Geometry Nodes modifier: **Bézier Segment**, Start and End exposed as `From` and `To`, with Start Handle and End Handle pulled downward for sag.
2. **Resample Curve**, Count 32, so the taper has enough points.
3. **Spline Parameter** › Factor → **Float Curve** shaped as a dip to 0.3 at the center → **Set Curve Radius**.
4. **Curve to Mesh**, Profile Curve: a **Curve Circle** (Resolution 8, Radius 0.01). **Set Material**: slime.

To place strands, set `From` to a point on a tube just outside the surface and `To` to a point on the slime. For several strands, instead of duplicating objects, feed the whole chain a set of points: Points (Count 4) with randomized positions near an exit, Instance on Points with the strand as the instance, and Realize Instances; each strand then needs its own sag, which a Random Value into the handle offsets gives.

### Chain 4: drips

Drips are easiest as a metaball object, outside Geometry Nodes, because metaballs merge by themselves. In Geometry Nodes the equivalent is Points to SDF Grid on two points, one large radius and one small below it, Grid to Mesh: the two blobs merge into a drop shape because an SDF of points is the metaball function. Animate the lower point downward and the drop stretches and separates, which is what Points to SDF Grid gives for free.

### Putting it together

Four objects: the model with chain 1, the map with chain 2, a strand object with chain 3, and drips. One slime material on everything except the model, which has the chain-colored material reading `wet`. Three exposed values, `Wet reach`, `Meniscus` and `Contour`, on the modifier panels. A backlight. That is the entire effect, and every node in it is one you can now explain.

### Exercise 7.1: the whole chain, with the Viewer

1. Build chain 1 and, after each node, Ctrl + Shift + click it and read the Spreadsheet's Viewer column.

What you should see: at the Proximity node, distances in meters; at the Map Range, values between 0 and 1 with the vertices near the map at 1; at the Store node, a `wet` column in the attribute list. If a column is missing, the previous node is where the chain broke.

### Exercise 7.2: the meniscus with a limited union

1. Build chain 2 with the Delete Geometry limit described above, exposing the reach.

What you should see: the slime surface rises up each tube for a short distance and the tubes beyond it keep their own material, with no thin skin over the whole model. Change the reach and the collar of fused slime grows and shrinks.

### Project 2: local resolution from cryoSPARC

The goal is the figure ChimeraX makes with `color sample`: the map surface colored by local resolution, and the same colors on the model built into that map. cryoSPARC's Local Resolution Estimation job writes `*_map_locres.mrc`, a map on the same grid as the half maps in which each voxel holds a resolution in Å instead of a density. (Local Filtering writes a filtered density, which is not the file to sample.) In Geometry Nodes the Sample Grid node reads that map at any position, and because the result is stored as an attribute, one chain serves both the surface and the cartoon.

### Step 1: three imports in one frame

1. Import the density (`*_map_sharp.mrc`, or the unsharpened map) through the Molecular Nodes Density panel with Center Density off and Invert Data off. This object's tree makes the isosurface.
2. Import the local resolution map (`*_map_locres.mrc`) the same way, with the same two settings. Its tree will try to contour resolution values as if they were density, which means nothing, so hide the object with its eye icon in the Outliner. It only needs to exist so its grid can be read.
3. Import the model with Centre off. A model refined into this map in Phenix already sits in the map's coordinate frame, so with nothing recentered the three objects overlap in the viewport. If the model sits outside the density, one import was centered: import it again rather than moving objects by hand.
4. Find the grid's name: select the locres object and choose Volume Grids in the Spreadsheet's domain list. A map imported with Molecular Nodes has one grid, named `density`.

### Step 2: resolution onto the map surface

In the density object's tree, after the style node that makes the mesh (Style Density Surface):

1. Object Info (Relative) with Object set to the locres object → Get Named Grid (Float, Name `density`); search the Add menu for "named grid". It takes the volume at its Geometry input and outputs the grid.
2. Sample Grid (Float, Interpolation Trilinear): Get Named Grid › Grid → Grid. Leave Position empty; it defaults to Position, so each element reads the resolution where it sits. Value is a field: "the resolution in Å at this vertex."
3. Map Range: Sample Grid › Value → Value, From Min 3.0, From Max 6.0, To Min 0, To Max 1, Clamp on. Type the range the color bar will span, in Å, taken from the job's reported range. Do not use Attribute Statistic here: a fixed range keeps panels comparable and matches a printed color bar.
4. Store Named Attribute (Float, Point, Name `locres`): the style node's mesh → Geometry, Map Range › Result → Value, in line before Group Output.

Check with the Viewer on Store's output, Vertex tab: a `locres` column from 0 to 1 that varies across the surface. The same number everywhere means Sample Grid is returning a constant: the grid name is wrong, the two maps do not overlap, or Object Info points at the wrong object. World scale needs no correction, because the grid's values are resolutions, not coordinates, and both maps were scaled alike.

### Step 3: the material

Duplicate `height_test` from Exercise 2.2 and rename it `locres`. In the Shader Editor change the Attribute node's Name to `locres`. On the Color Ramp make the left stop blue (0, the best resolution), add a white stop at 0.5, and make the right stop red (1, the worst). Assign it through the density style node's Material field. The convention in most papers is blue for high resolution and red for low; keep the same ramp and the same two numbers in every panel of a figure.

### Step 4: the same values on the model

In the model's tree, after Style Cartoon, repeat step 2 word for word: Object Info to the locres object → Get Named Grid → Sample Grid → Map Range with the same 3.0 and 6.0 → Store Named Attribute `locres` on the cartoon mesh. Each cartoon vertex reads the resolution at its own position, so a flexible domain comes out red on both the map and the model. Assign the same `locres` material through Style Cartoon's Material field.

This works for the reason in Chapter 3: Sample Grid has no geometry input of its own, and the geometry that reaches Store Named Attribute decides where the samples are taken. Swap the surface mesh for the cartoon and the sampling chain does not change.

### Variants

- Per residue instead of per vertex: after Sample Grid, Accumulate Field (Float) with the value as Value and Named Attribute `ures_id` as Group ID gives each residue's Total; `ures_id` is unique across chains, where `res_id` repeats. A second Accumulate Field with Value 1 and the same Group ID gives the count. A Math node set to Divide gives the mean, and every vertex of a residue carries it.
- Model in weak density: sample the density grid instead of the locres grid (Object Info to the density object). Parts of the model sitting in weak density go dark, which is `measure mapvalues` in ChimeraX.
- Color bar: put the Color Ramp in a node group (Ctrl + G) and use it in a second material on a plane, with Texture Coordinate › Generated → Separate XYZ › X as the ramp's Fac. Render the plane beside the figure, labeled with the two numbers from Map Range, or draw the bar in Illustrator with those numbers.
- Outside the mask: where the job's mask ends, the locres map holds a fill value rather than an estimate, and those vertices land at one end of the ramp. If a fringe of the surface shows a solid end color, read its value with the Viewer, then cut it with Delete Geometry using a Compare on the same Sample Grid value as the selection.

### Exercise 7.3: the map by local resolution

1. Build steps 1 to 3 on your sharpened map and its locres map, with the Viewer on Store Named Attribute's output. Set Interpolation to Nearest first, then to Trilinear.

What you should see: with Nearest, patches of flat color the size of a voxel; with Trilinear, smooth blends between them. The best-resolved core sits at the blue end and the periphery and any flexible domain at the red end, in the same places ChimeraX colors them.

### Exercise 7.4: the model by local resolution

1. Build step 4 on the model. Duplicate the `locres` material for the map, set its Alpha to 0.3 (Render Method Blended in EEVEE), and render the surface over the cartoon with both colored by `locres`.

What you should see: the cartoon's colors match the surface around it, because both read the same voxels. Where they disagree, the model has drifted out of the map's frame; check the Center settings of the imports.

### Check yourself

1. Why must Store Named Attribute come after the style node in chain 1? *So the attribute is written on the cartoon's vertices rather than on atoms the style discards.*
2. What does Relative on Object Info do? *Puts the other object's geometry into this object's coordinate space, so distances and unions line up.*
3. Why does the union wrap the whole model in slime, and what limits it? *The Boolean fuses all of the model's mesh; deleting the parts far from the surface before the SDF step limits it to the exits.*
4. Which single node produces a metaball-like merge of points? *Points to SDF Grid.*
5. Why does the local resolution chain use typed numbers in Map Range instead of Attribute Statistic? *So every panel and the color bar share one scale; the statistic would change the scale with each map.*
6. Why can one Sample Grid chain color both the surface and the cartoon? *Sample Grid is a field: the geometry reaching Store Named Attribute decides where it is evaluated.*

## Chapter 8. Working habits and debugging

### Objectives

- Find where a tree breaks in under a minute.
- Keep trees readable and reusable with frames and node groups.
- Keep heavy trees responsive, and bake what need not recompute.

### Debugging in order

1. **Look at the socket colors and warnings.** A red link is a type mismatch; a node with a warning triangle has a tooltip saying what is wrong, most often a missing attribute name or the wrong geometry type.
2. **View each node.** Ctrl + Shift + click walks the Viewer along the chain. The viewport shows that node's geometry and the Spreadsheet shows its data. The first node whose output is not what you expect is the bug; everything before it is fine.
3. **Read the Spreadsheet, not the viewport.** Row counts tell you whether a selection deleted everything or nothing; the domain tabs tell you whether an attribute landed on points or faces; the Viewer column shows a field's actual numbers.
4. **Check which geometry a field is evaluated on.** If the values look right in the Spreadsheet but wrong in the result, the field is being consumed after a node that changed the geometry; capture it earlier (Chapter 3).
5. **Check the modifier order.** Geometry Nodes runs in the modifier stack's order; a Subdivision Surface above it changes what Group Input receives.
6. **Mute, do not delete.** M mutes a node so the geometry passes through unchanged, which isolates its effect without rebuilding anything.

### Keeping trees readable

- **Frames** (Shift + A › Layout › Frame, or select nodes and Ctrl + J) box a chain with a label. One frame per effect, named for what it does, means a tree you can read in a year.
- **Node groups** (select nodes, Ctrl + G) collapse a chain into one node with its own inputs and outputs. The wet-collar chain as a group called `Wetness` with one Reach input is reusable on any object, and editing the group updates every copy. Tab enters a group, Tab exits.
- **Reroutes** (Shift + right-drag across a link) tidy long links.
- **Name every exposed input** in the N panel's Group tab, with a tooltip and a sensible min and max, so the modifier panel reads like a tool.
- **Mark assets.** Right-click a node group in the Blender File view and Mark as Asset, and it appears in the Asset Browser for drag-and-drop into any file, which is how Molecular Nodes itself ships its nodes.

### Performance

- The timing overlay (the node editor's Overlays popover, Timings) shows how long each node takes. The expensive ones are almost always voxel conversions at small voxel sizes, Realize Instances on many instances, and Mesh Boolean.
- Keep instances as instances until the last possible node; a million spheres as instances are cheap, realized they are a million meshes.
- Lower voxel size only where it shows. Build at a coarse size and halve it for the final render.
- Use Delete Geometry early to drop what the rest of the tree does not need, such as solvent atoms or the far side of a map.
- **Bake** (Shift + A › Geometry › Operations › Bake) stores a node's result on disk so it is not recomputed; put one after the SDF chain once the meniscus is settled, and the rest of the tree stays interactive.

### Zones, briefly

Two node pairs form loops. A **Simulation Zone** carries geometry from one frame to the next, so what leaves the zone at frame 10 enters it at frame 11; it is how particles, growth and drips that accumulate are built, and it needs the timeline to play. A **Repeat Zone** runs its contents a fixed number of times in one evaluation, for iterative smoothing or building a chain of segments. Neither is needed for anything in this guide, but they are what you will meet next in other people's trees.

### Exercise 8.1: break and find

1. In the wet-collar chain, misspell the attribute name in the material's Attribute node, then in the Store node, then switch Object Info's object to the wrong one.
2. For each, find the break using only the ordered list above.

What you should see: the first two show as a warning on the Named Attribute or a missing Spreadsheet column; the third shows as a Proximity distance that is wrong everywhere. Each takes one Viewer click to locate.

### Exercise 8.2: make it a tool

1. Select the four nodes of the wet-collar chain, Ctrl + G, name the group `Wetness`, expose Reach and the target object as group inputs, and Mark as Asset.
2. Apply it to a second model from the Asset Browser.

What you should see: one node on the second model's tree that does the whole job, with a Reach slider and an object picker. That is the difference between a chain and a tool.

### Check yourself

1. What is the fastest way to find which node breaks a chain? *Walk the Viewer along it with Ctrl + Shift + click and read the Spreadsheet.*
2. What does muting a node do? *Passes geometry through unchanged, so you can isolate the node's effect.*
3. When should instances be realized? *As late as possible; realized instances are heavy.*
4. What does a Bake node save you? *Recomputing an expensive result every time something upstream changes.*

## Chapter 9. The chooser, a glossary and sources

### I want this; use that

| I want | Use |
| --- | --- |
| A value from the file on every atom | Named Attribute with the name from the Chapter 2 table |
| A computed value the material can read | Store Named Attribute, then Attribute in the material |
| Only some atoms | A Select node, or Compare on an attribute, into a Selection socket |
| Two representations in one object | Two style branches joined with Join Geometry |
| A sphere or arrow on every atom | Mesh to Points, Instance on Points, Realize Instances only if needed |
| The map colored by the model | Sample Nearest → Sample Index on the model's atoms via Object Info, stored as Color |
| Distance from each point to another object | Geometry Proximity on Object Info's geometry |
| Depth below the surface, any shape | Geometry Proximity, Faces, with a Style Surface branch as Target |
| A smooth blob around points | Points to SDF Grid, Grid to Mesh |
| Two shapes fused with a rounded join | Mesh to SDF Grid on each, SDF Grid Boolean, SDF Grid Fillet, Grid to Mesh |
| A tapered tube between two points | Bézier Segment, Resample, Set Curve Radius, Curve to Mesh |
| A slider on the modifier panel | Connect the input to Group Input and name it |
| A reusable tool | Ctrl + G into a node group, Mark as Asset |
| The value a field actually has | Ctrl + Shift + click the node and read the Spreadsheet |
| An expensive result frozen | A Bake node after it |
| Something that changes over frames | A Simulation Zone |
| The map or model colored by local resolution | Sample Grid on the locres grid via Object Info and Get Named Grid, then Store Named Attribute |

### Glossary

- **Attribute**: a named value stored on each element of a domain.
- **Bake**: storing a node's result on disk so it is not recomputed.
- **Capture Attribute**: freezing a field's values on the current geometry for use later in the tree.
- **Domain**: the level an attribute lives on: Point, Edge, Face, Face Corner, Spline, Instance.
- **Field**: a rule evaluated once per element of the geometry that consumes it; shown as a diamond socket.
- **Grid**: values on a regular lattice of voxels; a density map is one.
- **Group Input, Group Output**: where geometry enters and leaves a tree.
- **Instance**: a reference to geometry placed many times, cheap until realized.
- **Node group**: a tree collapsed into one node with its own sockets.
- **Realize**: convert instances into real editable geometry.
- **Sample Grid**: a field that reads a grid's value at each element's own position; the node behind local resolution coloring.
- **SDF**: signed distance field; a grid of distances to a surface, negative inside.
- **Selection**: a boolean field that limits where a node acts.
- **Spreadsheet**: the editor that shows a geometry's elements and attributes as a table.
- **Viewer**: the node that sends a geometry and a field to the viewport and Spreadsheet for inspection.
- **Voxel size**: the resolution of a grid, in scene units.
- **World scale**: the factor Molecular Nodes applies to coordinates on import.

### Sources

- [Geometry Nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html) (Blender Manual), including [Fields](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/fields.html) and [Attributes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/attributes_reference.html)
- [Molecular Nodes attributes](https://bradyajohnston.github.io/MolecularNodes/attributes.html), [Fetch from the PDB](https://bradyajohnston.github.io/MolecularNodes/tutorials/importing.html) and [CryoEM Maps](https://bradyajohnston.github.io/MolecularNodes/tutorials/cryoem.html) (Molecular Nodes documentation)
