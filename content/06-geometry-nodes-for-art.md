# Geometry Nodes for art

The same nodes that draw a cryo-EM map draw the paper spirals in the manual's Geometry Nodes introduction. This part turns the [Geometry Nodes part](05-geometry-nodes.md) around: the data comes from formulas instead of files, the goal is a feeling instead of a fact, and surprises are kept rather than debugged. Work through it in a new, empty scene.

**Notation.** As in the [Geometry Nodes part](05-geometry-nodes.md): Shift + A › menu is a path, Node › Socket names an output, and → is a link you draw. Every exercise starts from Add › Mesh › Plane with a new Geometry Nodes modifier and Group Input disconnected, unless it says otherwise.

## Chapter 1. What changes when the goal is a picture

### Objectives

- Say what procedural art is and why a node tree suits it.
- Name the five parts every piece is built from.
- Adopt the working habit: expose, scrub, keep.

### The same tool, turned around

In the [Geometry Nodes part](05-geometry-nodes.md) a tree starts with atoms from a file and ends in a faithful picture of them. Here the tree starts with nothing and ends in a shape that never existed, and the nodes are the same. A Molecular Nodes tree is a generator, a distribution and a style; a piece of art is the same three with the file replaced by a formula.

Three things change. The data comes from primitives and math, so there is nothing to be faithful to. Randomness is a material, not a bug: a seed slider is often the best control in the tree. And judging the result means looking, not checking a column in the Spreadsheet.

### The five parts of any piece

| Part | What it does | Typical nodes |
| --- | --- | --- |
| Generator | Makes something from nothing | Grid, Cube, Curve Circle, Spiral, Points |
| Distribution | Decides where things go | Distribute Points on Faces, Points with a formula, Curve to Points |
| Repetition | Copies one thing many times | Instance on Points, Duplicate Elements |
| Variation | Makes the copies differ | Index, Random Value, Noise Texture, Map Range |
| Surface | Gives it color and light | Set Material, Store Named Attribute read by a material |

Most pieces are these five in that order, and most troubleshooting is asking which part is missing. A grid of identical cubes lacks variation; a noise landscape with nothing on it lacks repetition.

### The working habit

Expose every number you touch twice to the modifier panel and name it. Scrub it with the mouse while watching the viewport, and when something good happens by accident, duplicate the object (Shift + D) before you change anything else. A piece is usually chosen from a dozen accidents, not designed in advance.

Keep Material Preview on, with a plain studio HDRI from the viewport shading popover, so color reads from the start. Save often: a scrubbed slider is easy to lose.

### Exercise 1.1: read the manual's spiral

1. Open the Blender manual's Geometry Nodes introduction and look at the paper-spiral image without reading. Name its five parts in a sentence each: what generates, what distributes, what repeats, what varies, and what the surface does.

What you should see: a spiral curve swept into a ribbon (generator), a scatter of points (distribution), one ribbon copied onto each (repetition), rotation, size and color differing per copy (variation), and a matte pastel material under soft light (surface). Chapter 8 builds exactly this.

### Check yourself

1. What replaces the file in an art tree? *A generator: a primitive, a formula, or a scatter of points.*
2. Which of the five parts is missing from a field of identical spheres? *Variation.*
3. What is the first thing to do when an accident looks good? *Duplicate the object before changing anything else.*
4. Why does the Spreadsheet matter less here? *The result is judged by looking; there is no reference to check against.*

## Chapter 2. Something from nothing

### Objectives

- Start a tree on an object that contributes no geometry.
- Use mesh primitives, curve primitives and the Points node as generators.
- Build the Spiral node into a coil and expose its controls.

### An object that gives nothing

Every tree needs an object to live on, but the object's own mesh need not be used. Add › Mesh › Plane, add a Geometry Nodes modifier, and in the tree disconnect Group Input from Group Output. Whatever you plug into Group Output replaces the plane. The object is now a container for the tree, and its origin is where the tree's (0, 0, 0) sits.

### Mesh primitives

Shift + A › Mesh › Primitives holds Grid, Cube, UV Sphere, Ico Sphere, Cylinder, Cone and Mesh Circle. Each takes dimensions and vertex counts, and most output a UV Map field you can store for texturing. Grid is the workhorse: a flat sheet to scatter on, displace, or instance over. Ico Sphere at Subdivisions 1 is the cheap low-poly ball of a thousand pieces.

### Curve primitives

Shift + A › Curve › Primitives holds Curve Circle, Curve Line, Arc, Star, Quadrilateral, Bézier Segment, Quadratic Bézier and Spiral. A curve draws nothing until something gives it a surface (Chapter 5), so a curve primitive is a path, not a shape. Curve Circle and Quadrilateral double as profiles: the cross-section swept along another curve.

The Spiral node is the one behind the manual's picture. Resolution is points per turn, Rotations the number of turns, Start Radius and End Radius the size at each end, and Height the rise over the whole length. Height 0 gives a flat coil, Height 2 a spring. Reverse flips the winding.

### Points from a count

The Points node makes N points at one position; with a field in Position it makes N points wherever the formula says, which is how Chapter 4 draws a sunflower. Mesh to Points turns any mesh's vertices into points, and Distribute Points on Faces scatters them over faces (Chapter 3).

### Exercise 2.1: a coil

1. Add Spiral (Resolution 32, Rotations 3, Start Radius 0.1, End Radius 1, Height 0) → Curve to Mesh's Curve, and Curve Circle (Radius 0.05) → Curve to Mesh's Profile Curve. Curve to Mesh → Group Output.
2. Set Height to 1, then Rotations to 8, then Resolution to 6.
3. Connect Rotations and End Radius to Group Input, name them, and scrub them from the modifier panel.

What you should see: a flat coiled tube, then a spring, then a tight spring, then a chunky hexagonal one when Resolution drops. The modifier panel shows two sliders that reshape it live.

### Exercise 2.2: a sheet and a ball

1. Add Grid (Size 4 × 4, Vertices 40 × 40) and view it with Shade Smooth off.
2. Replace it with Ico Sphere at Subdivisions 1, then 3.
3. Join both with Join Geometry and move the sphere up 1 m with Transform Geometry.

What you should see: a flat lattice, a twenty-sided ball, a smoother ball, and finally the ball floating over the sheet, all from one object with no mesh of its own.

### Check yourself

1. Why disconnect Group Input? *So the plane's own mesh plays no part; the tree builds everything.*
2. What does a curve primitive look like in a render? *Nothing, until Curve to Mesh or another node gives it a surface.*
3. What does Spiral's Height do? *Lifts the end of the coil above the start; 0 keeps it flat.*
4. Where is the tree's origin? *At the object's origin, the orange dot.*

## Chapter 3. Repetition

### Objectives

- Scatter points by density or by a formula.
- Copy a shape onto points with Instance on Points, and vary which shape with Pick Instance.
- Decide when instances must be realized.

### Points to put things on

Distribute Points on Faces (Shift + A › Point) scatters points across any mesh. Random mode takes Density and Seed. Poisson Disk mode adds Distance Min, so no two points sit closer than that, which is what a tidy scatter needs. Its Rotation output aligns each point with the face normal, so things stand up on a slope.

Mesh to Points puts one point on every vertex, and Curve to Points spaces them along a curve. Points with a formula in Position puts them wherever the math says.

### Instance on Points

Instance on Points (Shift + A › Instances) takes Points, Instance (the thing to copy), Rotation and Scale, and makes one lightweight copy per point. The copies share one mesh, so a million instances cost little until Realize Instances turns them into real geometry. Rotation and Scale are fields evaluated per point, which is where Chapter 4's variation plugs in.

Pick Instance, with a collection from Collection Info (Separate Children on) as the Instance, chooses one child per point by Instance Index. Index → Math Modulo 3 cycles through three shapes; Random Value (Integer, 0 to 2) picks at random.

### Realize or not

Leave instances as instances for speed and for the Object Info › Random trick in Chapter 6. Realize when a later node needs real vertices: Set Position on the copies' points, Mesh Boolean, Merge by Distance, or any mesh-level smoothing. Realize Instances is where memory jumps, so put it last and only when needed.

### Exercise 3.1: a field of coils

1. Grid (Size 6 × 6, Vertices 2 × 2) → Distribute Points on Faces (Poisson Disk, Distance Min 0.6, Density Max 10, Seed 0) → Instance on Points' Points.
2. The coil from Exercise 2.1 (Curve to Mesh's output) → Instance on Points' Instance.
3. Scrub Seed, then Distance Min.

What you should see: a few dozen coils in a tidy scatter, re-rolled on each Seed change, sparser as Distance Min grows. All identical for now; Chapter 4 fixes that.

### Exercise 3.2: three shapes by lot

1. Make a collection called Shapes with a small Cube, Cone and Ico Sphere in it, each at the origin, and hide the collection in the Outliner.
2. Collection Info (Separate Children on, Reset Children on) → Instance on Points' Instance, Pick Instance on, Random Value (Integer, Min 0, Max 2) → Instance Index.
3. Replace Random Value with Index → Math Modulo 3.

What you should see: the scatter from 3.1 with a random mix of three shapes, then a strict repeating order of cube, cone, sphere.

### Check yourself

1. What does Poisson Disk give that Random does not? *A minimum spacing between points.*
2. Why are a million instances cheap? *They share one mesh; only a transform is stored per copy.*
3. When must you realize? *When a later node needs the copies' own vertices, such as Set Position or a Boolean.*
4. What does Pick Instance need to work? *A geometry with several children, from Collection Info with Separate Children on, and an Instance Index.*

## Chapter 4. Variation

### Objectives

- Drive scale, rotation, position and color from Index, Random Value and Noise Texture.
- Write a formula into Points' Position and draw a sunflower.
- Keep variation adjustable with a seed and a strength.

### Three sources of difference

Index is orderly: it counts 0, 1, 2 along the points, so Index → Map Range gives a gradient and Index → Math Modulo gives a repeat. Random Value is disorderly: a different number per element, re-rolled by Seed. Noise Texture is smooth: nearby points get similar values, so clumps and waves appear rather than static. Most pieces mix one orderly and one smooth source.

### Where variation plugs in

Scale on Instance on Points: Random Value (Float, 0.6 to 1.4), or Noise Texture › Fac → Map Range. Rotation: Random Value (Vector, Min 0 and Max 6.283 on Z only) → Instance on Points' Rotation, which spins each copy about its axis. Position: Set Position with Offset = Noise Texture › Color minus 0.5, scaled, which jitters or warps. Color: Store Named Attribute (Color, Point) on the points before instancing, read in the material (Chapter 6).

Noise Texture's Scale is features per meter; Detail adds finer ripples and Roughness sets their strength. Set the node to 4D and feed W from Scene Time › Seconds for noise that drifts (Chapter 7).

### A formula in Position

Points (Count 400) with a field in Position places each point by a formula of its Index. The sunflower, or phyllotaxis, pattern is angle = Index × 2.39996 radians (the golden angle) and radius = 0.08 × √Index. Combine XYZ (radius × cos angle, radius × sin angle, 0) → Position.

### Exercise 4.1: make the coils differ

1. On the field from Exercise 3.1, Random Value (Float, 0.5 to 1.5, Seed 1) → Instance on Points' Scale.
2. Random Value (Vector, Min (0, 0, 0), Max (0, 0, 6.283)) → Rotation.
3. Noise Texture (Scale 0.4) › Fac → Map Range (0 to 1 → 0.3 to 1.6) → Scale, replacing step 1.

What you should see: coils of random size, then also randomly turned, then sizes that swell and shrink in smooth patches across the field instead of at random.

### Exercise 4.2: a sunflower

1. Points (Count 400) → Instance on Points with Ico Sphere (Radius 0.05) as Instance.
2. Index → Math Multiply 2.39996 → Math Cosine and Math Sine. Index → Math Square Root → Math Multiply 0.08. Multiply the radius by each, Combine XYZ → Points' Position.
3. Index → Map Range (0 to 400 → 0.3 to 1.2) → Scale. Expose Count and the 0.08.

What you should see: the seed head of a sunflower, spheres growing toward the rim, with the familiar crossing spirals. Change 2.39996 to 2.4 and the spirals become straight arms: the pattern depends on the golden angle to the fourth decimal.

### Check yourself

1. Which source gives clumps rather than static? *Noise Texture; nearby points get similar values.*
2. How do you spin instances at random about Z only? *Random Value, Vector, with Min and Max zero on X and Y and 0 to 6.283 on Z, into Rotation.*
3. Where does the sunflower's formula live? *In Points' Position, as a field of Index.*
4. What makes a repeat rather than a gradient from Index? *Math Modulo.*

## Chapter 5. Curves as a pen

### Objectives

- Give a curve a body with Curve to Mesh and profiles.
- Shape it along its length with Spline Parameter, Set Curve Radius and Set Curve Tilt.
- Cut and grow it with Trim Curve.

### Profiles

Curve to Mesh sweeps a profile curve along a path. Curve Circle gives a tube, Curve Line gives a ribbon, Quadrilateral gives a strip with thickness, and Star gives a ridged cord. The profile's own size sets the body's size, so a thin ribbon is a Curve Line 0.3 long and a thick one a Quadrilateral 0.02 wide and 0.3 tall. Fill Caps closes the ends of a closed profile.

Which way the profile stands depends on the path's normals. Add Set Curve Normal set to Z Up before Curve to Mesh and the orientation stops depending on the curve's twist. If a strip then lies flat where it should stand, swap the profile's Width and Height.

### Along the length

Spline Parameter › Factor runs 0 to 1 along each spline, and nodes that take a field use it to vary with length. Set Curve Radius with Factor → Float Curve scales the profile for a taper, as in the slime strands. Set Curve Tilt with Factor → Math Multiply 6.283 twists the profile one full turn over the length, which turns a ribbon into a helix. Resample Curve first, with Count 64 or more, so the twist has points to show on.

### Cutting and bending

Trim Curve keeps the part between Start and End, as factors 0 to 1; driving End with time grows a line (Chapter 7). Fillet Curve rounds the corners of a polyline, which is how a Star becomes a flower. Set Spline Type to Bézier or NURBS smooths a jagged primitive. Curve to Points places things along the path; Curve Length and Sample Curve read it.

### Exercise 5.1: the paper ribbon

1. Spiral (Resolution 48, Rotations 2.5, Start Radius 0.05, End Radius 0.8, Height 0) → Resample Curve (Count 200) → Set Curve Normal (Z Up) → Curve to Mesh's Curve.
2. Quadrilateral (Rectangle, Width 0.02, Height 0.35) → Curve to Mesh's Profile Curve. Set Shade Smooth → Group Output.
3. Insert Set Curve Tilt before Curve to Mesh: Spline Parameter › Factor → Math Multiply 0.5 → Tilt.

What you should see: a strip of paper rolled into a flat spiral, standing on its edge, the thickness visible on the outer end; after step 3 the strip leans as it unrolls, like a loosened roll of quilling paper.

### Exercise 5.2: a twisted cord

1. Curve Line (Start (0, 0, 0), End (3, 0, 0)) → Resample Curve (Count 128) → Set Curve Tilt (Spline Parameter › Factor → Math Multiply 12.566 → Tilt) → Curve to Mesh with Star (Points 5, Inner Radius 0.05, Outer Radius 0.1) as the profile.
2. Replace Set Curve Tilt with Set Curve Radius (Factor → Float Curve, 1 at both ends and 0.3 in the middle).

What you should see: a five-ridged cord twisting twice along its length, then an untwisted cord pinched in the middle.

### Check yourself

1. What decides the thickness of a swept body? *The profile curve's own size.*
2. Which field runs 0 to 1 along a spline? *Spline Parameter › Factor.*
3. Why resample before tilting? *A twist shows only where the curve has points.*
4. What node grows a line over time? *Trim Curve with End driven by Scene Time.*

## Chapter 6. Color and light for a piece

### Objectives

- Give each copy its own color, three ways.
- Build a palette rather than picking colors one by one.
- Light a piece for mood instead of for measurement.

### Color per copy

The quickest way needs no attribute: in the material, Object Info › Random → Color Ramp → Base Color. In Cycles each instance draws a different random number, so a field of coils gets a scatter of ramp colors from one node. It only works on instances left unrealized, and it cannot be steered.

The controlled way stores the color in the tree. Before Instance on Points, Store Named Attribute (Color, Point, Name `tint`) on the points, fed by whatever you like: Index → Map Range → Color Ramp for a gradient across the field, Random Value → Color Ramp for a scatter, Noise → Color Ramp for patches. Instance on Points carries point attributes onto the copies, and Realize Instances carries them onto the realized mesh. In the material, Attribute (Name `tint`) › Color → Base Color.

The third way is per element inside one mesh: Store Named Attribute on the points of a displaced grid, read the same way, which paints a landscape by height or slope.

### A palette

Set a Color Ramp to Constant interpolation and give it four or five stops: that is a palette. Any 0 to 1 input then picks one of the colors, never a mix, which is what makes a piece look designed rather than rendered. Pastel palettes (low saturation, high value) on a dark background are the look of most procedural work; one accent color on a tenth of the copies, chosen by Random Value, is usually enough.

### The surface of paper and plastic

The [Recipes part](01-material-recipes.md)'s rows still apply. Matte paper is Roughness 0.6, Specular IOR Level 0.3 and a touch of Sheen; soft plastic is Roughness 0.4 with Subsurface 0.05 so edges glow; clay is Roughness 0.8. Keep Metallic at 0 unless the piece is about metal. Set Shade Smooth on the instance before instancing, once, rather than on the realized mesh.

### Light for mood

The [Lighting part](03-lighting.md)'s scientific rig is deliberately neutral. For a piece, start from its high-key setup and break two rules on purpose: let the key be warm (4500 K) and the fill cool (7500 K), and let the shadows go dark. A large Area key 30 degrees above the camera and a World from a studio HDRI at Strength 0.5 carry most pieces. Add Depth of Field on the camera (F-Stop 2, focus on the nearest coil) for the miniature look of the manual's image.

### Exercise 6.1: three ways to color the field

1. On the field from Exercise 4.1, give the coil's material Object Info › Random → Color Ramp (two pastel stops) → Base Color, and render in Cycles.
2. Replace it: Store Named Attribute (Color, Point, `tint`) on the points before Instance on Points, with Noise Texture › Fac → Color Ramp (Constant, four stops) as the value; Realize Instances after instancing; Attribute `tint` → Base Color.
3. Change the Color Ramp to Linear interpolation.

What you should see: a random scatter of two tints; then four flat colors in patches that follow the noise, with realized geometry in the Spreadsheet; then smooth blends between the four.

### Exercise 6.2: mood

1. Light the field with one Area key (Size 3 m, 45 degrees from above, 4500 K), a World HDRI at 0.5, and a dark gray ground plane.
2. Add Depth of Field, F-Stop 2, with the nearest coil as the focus object.

What you should see: warm-lit coils with soft shadows, the far ones melting into blur: the same scene as the manual's picture, on your own objects.

### Check yourself

1. Why does Object Info › Random stop working after Realize Instances? *Realized copies are one mesh in one object, so there is one random number.*
2. How does a stored point color reach an instance's material? *Instance on Points carries point attributes onto the copies, Realize Instances carries them onto the mesh, and Attribute reads them.*
3. What does Constant interpolation on a Color Ramp give? *A palette: one of the stops, never a blend.*
4. Which rule of the scientific rig is broken for mood? *Neutral color; a warm key and cool fill are allowed.*

## Chapter 7. Motion

### Objectives

- Drive any value with Scene Time.
- Grow, spin and breathe a piece.
- Build a first Simulation Zone that accumulates.

### Time as an input

Scene Time (Shift + A › Input › Scene) outputs Seconds and Frame, single values that change every frame. Any socket fed from it animates with no keyframes: Spiral's Rotations from Seconds, a Transform Geometry rotation from Seconds × 0.5, Noise Texture's W from Seconds so patches drift. Keyframing an exposed modifier input (hover it, press I) works too, and gives easing in the Graph Editor.

### Three motions

Grow: Trim Curve with End = Scene Time › Seconds → Map Range (0 to 4 → 0 to 1), so a line draws itself over four seconds. Spin: Rotate Instances with Scene Time › Seconds → Rotation on Z, which turns every copy in place. Breathe: Instance on Points' Scale from Math Sine of (Seconds + Index × 0.3), remapped to 0.7 to 1.3, so a wave of size runs across the field.

### A Simulation Zone, briefly

A Simulation Zone (Shift + A › Simulation) feeds its output back as the next frame's input, so the tree can accumulate. Inside the zone, Set Position with a small Offset from Noise moves points a little each frame, and because the input is last frame's output, the points wander instead of jittering. Play the timeline to see it; return to frame 1 to reset. It is the door to particles, growth and cloth, and Chapter 8 of the [Geometry Nodes part](05-geometry-nodes.md) says more.

### Exercise 7.1: draw the spiral

1. Spiral (Rotations 4) → Trim Curve (End = Scene Time › Seconds → Map Range (0 to 5 → 0 to 1)) → Curve to Mesh with Curve Circle (Radius 0.03).
2. Set the scene's End frame to 150 and press Space over the viewport.

What you should see: the coil drawing itself from the center outward over five seconds, finished at frame 120.

### Exercise 7.2: wander

1. Points (Count 200) with Random Value (Vector, −2 to 2) → Position → a Simulation Zone; inside, Set Position with Offset = Noise Texture (4D, W from Scene Time › Seconds) › Color minus 0.5, scaled by 0.05 → the zone's output.
2. After the zone, Instance on Points with a small Ico Sphere. Play.

What you should see: two hundred specks drifting in slow currents, each path smooth, never snapping back; stop and return to frame 1 and they jump home.

### Check yourself

1. What does Scene Time output? *Seconds and Frame, as single values.*
2. Which node makes a curve draw itself? *Trim Curve with End driven by time.*
3. Why does the Simulation Zone wander rather than jitter? *Its input each frame is the previous frame's output, so the offsets add up.*
4. How is a scrubbed value animated with easing instead? *Keyframe the exposed modifier input with I.*

## Chapter 8. Three worked pieces

Each piece lists its full chain once, with the chapter that explains each step, then what you should see. Build them in order; each reuses the one before.

### Piece 1: the paper spirals from the manual

1. Ribbon (Chapter 5): Spiral (Resolution 48, Rotations 2.5, Start Radius 0.05, End Radius 0.8, Height 0) → Resample Curve (200) → Set Curve Normal (Z Up) → Set Curve Tilt (Spline Parameter › Factor → Multiply 0.4) → Curve to Mesh with Quadrilateral (0.02 × 0.35) → Set Shade Smooth.
2. Scatter (Chapter 3): Grid (8 × 8, 2 × 2 vertices) → Distribute Points on Faces (Poisson Disk, Distance Min 1.0, Density Max 4) → Instance on Points with the ribbon.
3. Variation (Chapter 4): Random Value (Float, 0.5 to 1.3) → Scale; Random Value (Vector, 0 to 6.283 on Z) → Rotation.
4. Color (Chapter 6): Random Value (Float) → Color Ramp (Constant, five pastel stops) → Store Named Attribute (Color, Point, `tint`) on the points before instancing; Realize Instances; material Attribute `tint` → Base Color, Roughness 0.6.
5. Camera from above at 60 degrees, one warm Area key, HDRI at 0.5, Depth of Field at F-Stop 2.8.

What you should see: a tabletop of rolled paper strips in five colors, each a different size and turn, leaning as they unroll, the far ones softening into blur. Scrub Distance Min down to 0.6 for the overlapping crowd of the manual's picture.

### Piece 2: a phyllotaxis flower

1. Points (Count 300) with Position from the sunflower formula of Chapter 4, radius 0.08 × √Index.
2. Petal: Curve Line (Start (0, 0, 0), End (0.6, 0, 0)) → Resample Curve (16) → Set Curve Radius (Spline Parameter › Factor → Float Curve: 0 at the start, 1 at 0.6, 0 at the end) → Curve to Mesh with Curve Circle (Radius 0.08, Resolution 8) → Set Shade Smooth.
3. Instance on Points with the petal. Rotation: Align Rotation to Vector (Axis X) with Vector = Position, so every petal points away from the center; then Rotate Rotation (Local) by an Euler whose Y is Index → Map Range (0 to 300 → −0.8 to 0), so inner petals tilt up.
4. Scale: Index → Map Range (0 to 300 → 0.2 to 1).
5. Color: Index → Map Range (0 to 300 → 0 to 1) → Color Ramp (Linear, yellow at 0 to red at 1), stored as `tint` before instancing, realized, read by the material.

What you should see: a flower seen from above, small upright petals at the center opening into large flat ones at the rim, color running from the center out, every petal sitting on one of the crossing spirals.

### Piece 3: a low-poly island

1. Ground: Grid (10 × 10, 60 × 60 vertices) → Set Position with Offset = Combine XYZ (0, 0, Z), where Z = Noise Texture (Scale 0.3, Detail 2) › Fac → Map Range (0 to 1 → −0.5 to 1.5). A second Noise Texture at Scale 2, × 0.1, added to Z gives small bumps. Shade Flat.
2. Water: Grid (10 × 10, 2 × 2) raised to Z 0.2 with Transform Geometry, a blue glossy material, joined with Join Geometry.
3. Trees: Distribute Points on Faces on the ground (Poisson Disk, Distance Min 0.25, Density Max 30), with Selection = Position → Separate XYZ › Z → Compare Greater Than 0.4, so nothing grows below the waterline, and Density Factor = Noise Texture (Scale 1) › Fac so trees cluster. Instance on Points with a tree (Cone, Radius 0.12, Depth 0.4, on a Cylinder, Radius 0.02, Depth 0.15, joined and Shade Flat); Rotation from the Distribute node's Rotation output; Scale from Random Value (0.6 to 1.2).
4. Color: Store Named Attribute `height` (the displaced Z) on the ground's points; its material reads it into a Color Ramp (Constant: sand, grass, dark green, gray, white).
5. Light: Sun at 35 degrees, 5500 K, Strength 3; World sky at 0.3; camera at 45 degrees.

What you should see: a faceted island with sand at the shore, green slopes, gray peaks and white tops, forested in clumps above the water, lit by one sun with crisp shadows: the low-poly look in one tree.

### Check yourself

1. In piece 1, why store the color before Instance on Points? *So each point's color rides onto its copy; after instancing, the points no longer exist.*
2. In piece 2, what makes petals point outward? *Align Rotation to Vector with each point's Position as the vector.*
3. In piece 3, why does the Distribute node's Rotation output matter? *It stands each tree on the slope's normal instead of straight up.*
4. Which pieces need Realize Instances, and why? *Pieces 1 and 2, for the stored color; piece 3 does not, because its trees share one plain material.*

## Chapter 9. Chooser, glossary and sources

### I want this, use that

| I want | Use |
| --- | --- |
| A shape from nothing | Mesh Primitives or Curve Primitives, with Group Input disconnected |
| Things scattered evenly | Distribute Points on Faces, Poisson Disk |
| Points placed by a formula | Points with a field of Index in Position |
| One thing copied everywhere | Instance on Points |
| Several things mixed | Collection Info, Pick Instance, Instance Index |
| Copies that differ at random | Random Value into Scale, Rotation or a stored color |
| Copies that differ in patches | Noise Texture into the same sockets |
| A gradient across the piece | Index or Position → Map Range |
| A path with a body | Curve to Mesh with a profile |
| A ribbon that twists | Set Curve Tilt from Spline Parameter |
| A line that draws itself | Trim Curve, End from Scene Time |
| A flat palette | Color Ramp, Constant interpolation |
| Color per copy, quick | Object Info › Random in the material, Cycles |
| Color per copy, controlled | Store Named Attribute before instancing, Realize, Attribute in the material |
| Motion with no keyframes | Scene Time into any socket |
| Motion that accumulates | Simulation Zone |
| The blocky low-poly look | Low vertex counts and Shade Flat |

### Glossary

- **Generator**: a node that makes geometry from numbers alone: a primitive, Points, or a formula.
- **Golden angle**: 2.39996 radians, 137.5 degrees; the turn between successive seeds in phyllotaxis.
- **Instance**: a lightweight copy that shares one mesh; cheap until realized.
- **Palette**: a Color Ramp set to Constant, so inputs pick colors instead of blending them.
- **Pick Instance**: choosing one of several children per point by Instance Index.
- **Poisson Disk**: a scatter with a minimum spacing between points.
- **Profile**: the cross-section curve that Curve to Mesh sweeps along a path.
- **Realize**: turn instances into real geometry, carrying their attributes onto it.
- **Scene Time**: the node that outputs the current Seconds and Frame.
- **Seed**: the integer that re-rolls a random node; the same seed gives the same result.
- **Simulation Zone**: a region whose output becomes the next frame's input.
- **Tilt**: rotation of a curve's profile about the curve's own direction.
- **Trim**: keeping the part of a curve between two factors.

### Sources

- [Blender 5.2 manual: Geometry Nodes](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/index.html). The introduction page carries the paper-spiral image.
- [Blender 5.2 manual: Fields](https://docs.blender.org/manual/en/latest/modeling/geometry_nodes/fields.html).
- In Blender, F1 over any node opens its manual page.
