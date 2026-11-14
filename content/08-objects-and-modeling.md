# Handling objects and modeling

This part starts where you are: you can add a plane and move, turn and scale it. The first half, Chapters 1 to 6, covers what you will use every day on figures: selecting, placing things exactly, relating objects to each other, editing a mesh, modifiers, and curves, text and the camera. The second half, Chapters 7 to 9, is modeling for its own sake, a cartoon house and the road to an anime character, and ends with what carries back to science.

**Notation.** Keys are pressed with the mouse over the 3D viewport. On a Mac, Alt is the Option key, and Ctrl is Control, not Command; only undo, save, copy and paste use Command. A menu path follows in parentheses the first time a key appears, and F3 searches every command by name. Without a number pad, the View menu and the grave accent key, left of 1, reach the same views. Shift + A › menu is a path, as in the other parts.

## Chapter 1. Objects: select, hide, name, organize

### Objectives

- Tell the active object from the selected ones, and know why the difference matters.
- Select, hide and isolate objects quickly.
- Keep a scene findable with names and collections.

### Selected and active

Clicking an object selects it and makes it active. Shift + click adds more: all of them are selected, drawn with an orange outline, and the last one clicked is active, drawn in a lighter yellow-orange. The Properties editor always shows the active object. Commands that involve several objects treat the active one specially: it becomes the parent, the object the others are joined into, or the source that settings are copied from. So the click order matters, and that object goes last.

### Selecting

| To select | Do this |
| --- | --- |
| One object; one more or one fewer | Click; Shift + click |
| Everything; nothing | A; Alt + A |
| A region | Drag a box in empty space with the Select Box tool, or press B and drag |
| The opposite of what is selected | Ctrl + I |
| Every light, camera or mesh | Select › Select All by Type |
| Something buried behind other things | Click its name in the Outliner, or Alt + click in the viewport for a list of what lies under the mouse |

### Hiding and isolating

H hides the selection and Alt + H shows everything again. Numpad / (View › Local View › Toggle Local View) shows only the selection until you press it again, the quickest way to work on one object in a crowded scene. In the Outliner, the eye icon hides an object in the viewport only; the camera icon decides whether it renders. An object can be hidden from you and still render, which is the usual cause of a mystery shape in a render.

### Names and collections

F2 renames the active object; so does a double-click on its name in the Outliner. Name things for what they are (`key light`, `sweep`, `EGFR atoms`): node pickers, the Outliner's filter and you six weeks from now all go by name. A collection is a folder. M moves the selection into a collection or a new one, the checkbox beside a collection switches all of it off, and dragging in the Outliner rearranges. For figures, four collections cover most scenes: subject, lights, backdrop, and helpers that never render.

### Finding any command

F3 opens a search over every command: type `shade smooth` or `origin`, then press Enter. Hover over any button and press F1 to open its page in the manual.

### Exercise 1.1: tidy your scene

1. In the scene with your model, rename the lights, cameras and planes with F2. Select the lights and press M › New Collection, named `lights`; do the same for the planes, as `backdrop`.
2. Click the model, press numpad /, orbit around it, and press numpad / again.
3. Select the two planes: click one, then Shift + click the other. Press H, render a still (Render › Render Image), then press Alt + H.

What you should see: the Outliner reads like a list of parts. In local view the model stands alone on gray. In step 3 the planes vanish from the viewport and still appear in the render, because H does not touch the camera icon.

### Check yourself

1. Which object does the Properties editor show? *The active one, the last clicked.*
2. You select a light, then Shift + click an Empty, and parent. Which is the parent? *The Empty: the active object, clicked last.*
3. An object you hid with H appears in the render. Why? *H hides in the viewport only; the camera icon in the Outliner controls rendering.*

## Chapter 2. Placing things exactly

### Objectives

- Lock a move to an axis and type its amount.
- Choose what a rotation or scale happens around, with the pivot and the 3D cursor.
- Snap one thing onto another.
- Say what an origin is and when to apply a transform.

### G, R and S in full

G moves, R rotates and S scales. Move the mouse, then click or press Enter to keep the change, or right-click to cancel it. During any of them, X, Y or Z locks to that axis, and Shift + X, Y or Z locks to the other two. Pressing the axis key twice uses the object's own axis in place of the world's, so G Z Z moves a tilted lamp along its own beam. Typing a number sets the amount: G X 2 Enter, R Z 45 Enter, S 0.5 Enter. Holding Ctrl snaps to round steps, and Shift slows the mouse for fine control. The N panel's Item tab holds the same values as fields you can type into, plus Dimensions, the object's real size in meters.

### The pivot: what things turn around

R and S act around the pivot point, chosen in the Pivot menu in the middle of the viewport header (the period key opens it under the mouse). Median Point, the default, is the middle of the selection. Individual Origins turns or scales each object about itself. 3D Cursor uses the cursor, which is how you orbit one thing around another: with the cursor on the subject and the pivot set to 3D Cursor, R Z swings a light around the subject and keeps it aimed there.

### The 3D cursor and snapping

The 3D cursor, the red and white ring, is a point you place. New objects appear on it, and it can be the pivot. Shift + right-click puts it under the mouse, and Shift + S opens the Snap menu: Cursor to World Origin, Cursor to Selected, Selection to Cursor. Cursor to Selected on one object, then Selection to Cursor on another, puts the second exactly on the first.

For snapping during a move, hold Ctrl, or switch on the magnet in the header. The menu beside the magnet picks the target: Increment for grid steps, or Vertex, Edge and Face to land on other geometry. Face, with Align Rotation to Target ticked, sets an object down on a surface the right way up, such as a prop on a floor or a marker on a membrane.

### Origins, and why Apply exists

Every object has an origin, the small orange dot. Location is where the origin sits, and the object turns and scales about it. Object › Set Origin moves the origin without moving the mesh: Origin to Geometry centers it, and Origin to 3D Cursor puts it wherever you need a hinge.

Location, Rotation and Scale are a layer on top of the stored mesh. S in Object Mode changes Scale, not the mesh. Tools that measure in the object's own units, such as Bevel, Solidify and most modifiers, then come out stretched, and the status bar warns of non-uniform scale. Ctrl + A › Scale (Object › Apply › Scale) writes the current size into the mesh and resets Scale to 1; nothing visibly moves. Scaling in Edit Mode changes the mesh itself and never needs applying. Do not apply transforms or move origins on Molecular Nodes objects: their mesh is the atoms, and an untouched transform is what keeps a model and its map aligned.

### Exercise 2.1: orbit a light around a subject

1. On the lab bench (a sphere on a plane with one area light), click the sphere and press Shift + S › Cursor to Selected.
2. Click the light, set the Pivot menu to 3D Cursor, and press R Z 45 Enter, then R Z -90 Enter.
3. Set the pivot back to Median Point.

What you should see: the light swings 45 degrees around the sphere, then 90 degrees back the other way, always pointing at the sphere, with the highlight sliding across the sphere as it goes.

### Exercise 2.2: see what Apply fixes

1. Add a cube and press S X 4 Enter in Object Mode. Add a Bevel modifier (Modifier tab › Add Modifier › Generate › Bevel) with Amount 0.2 m and Segments 4.
2. Look at a corner from above, then press Ctrl + A › Scale.

What you should see: before, each rounded edge is four times longer along X than along Y, a stretched curve. After, the corners are even quarter circles and Scale reads 1, 1, 1.

### Check yourself

1. What does G Z Z do that G Z does not? *It moves along the object's own Z axis, not the world's.*
2. How do you swing a light around the subject? *Cursor on the subject, pivot set to 3D Cursor, then R Z.*
3. Why does a bevel look stretched on a scaled object? *It measures in the object's own units; apply the scale first.*
4. What does Set Origin › Origin to 3D Cursor change? *Where the object's origin is, not where its mesh is.*

## Chapter 3. Copies and relationships

### Objectives

- Choose between a copy and a linked copy.
- Join meshes into one object and split them apart.
- Make objects move together by parenting, with an Empty as the handle.
- Keep a light or camera aimed with Track To.

### Two kinds of copy

Shift + D duplicates: a new object with its own mesh. Alt + D makes a linked duplicate: a new object that shares the first one's mesh, so reshaping either in Edit Mode reshapes both, while each keeps its own place, size and modifiers. A number beside a mesh's or material's name is its user count, how many things share it; clicking the number gives this object a copy of its own. For thousands of copies, use instances ([Geometry Nodes part](05-geometry-nodes.md)).

### Join and separate

Ctrl + J joins the selected objects into the active one: one object, one origin, one modifier stack. In Edit Mode, P › Selection splits the selected faces off as a new object, and P › By Loose Parts splits every disconnected piece. Join what should be edited as one mesh. For things that should only travel together, parent them.

### Parenting and Empties

Select the children, then the parent last, and press Ctrl + P › Object. The children now follow the parent's moves, turns and scaling, and can still be moved on their own. Alt + P clears the link. In the Outliner, children nest under their parent.

An Empty (Shift + A › Empty › Plain Axes) has no geometry and never renders, which makes it the standard handle. Parent three lights to an Empty at the subject, and R Z on the Empty turns the whole rig. Parent the camera to another, keyframe the Empty's rotation, and you have a turntable.

### Aiming with Track To

Select the light or camera, Shift + click its target, and choose Object › Track › Track To Constraint (Ctrl + T). It now points at the target wherever either goes. An Empty as the target gives you an aim point you can drag. Alt + T clears it.

### Exercise 3.1: a rig on a handle

1. On the lab bench, put an Empty at the sphere: click the sphere, press Shift + S › Cursor to Selected, then Shift + A › Empty › Plain Axes.
2. Select every light, Shift + click the Empty last, and press Ctrl + P › Object.
3. Select the Empty alone and press R Z 90 Enter, then G X 3 Enter.

What you should see: the lights swing a quarter turn around the sphere together, then the whole rig slides 3 m along X, away from the sphere.

### Exercise 3.2: copy or linked copy

1. Select the sphere and press Shift + D, then X 3 Enter. Select the original again and press Alt + D, then X -3 Enter.
2. Select the original, press Tab, then A and S 0.5 Enter, and press Tab again.

What you should see: the original and the Alt + D copy both shrink to half size, because they share one mesh. The Shift + D copy stays as it was.

### Check yourself

1. Which copy changes when you edit the original's mesh? *The Alt + D linked duplicate.*
2. Join or parent a door to a house you will keep editing? *Parent: they move together and stay separate objects.*
3. What makes an Empty a good handle? *It has no geometry, never renders, and anything can be parented to it.*
4. What does Track To do? *Keeps the object pointed at a target as either one moves.*

## Chapter 4. Edit Mode: the mesh inside the object

### Objectives

- Enter Edit Mode on purpose and say what it changes.
- Select vertices, edges, faces and loops.
- Use the eight core tools.
- Fix shading with smooth, flat and normals.

### Two modes

Object Mode moves whole objects. Tab enters Edit Mode on the selected object, where you reshape the mesh it is made of: vertices (points), edges (lines between two vertices) and faces (surfaces bounded by three or more edges). What you do there changes the stored mesh. The viewport header names the mode; if G suddenly drags a single corner, you are in Edit Mode. One rule for your own work: a Molecular Nodes object's mesh is its atoms and bonds, so stay out of Edit Mode on molecules.

### Selecting parts

The three buttons at the left of the header choose vertex, edge or face selection (1, 2 and 3 on the number row, unless Emulate Numpad is on). Click, Shift + click, A and Alt + A work as on objects. Alt + click on an edge selects its whole edge loop, the line of edges running around the shape. L, with the mouse over a piece, selects everything connected to it. Ctrl + numpad plus and minus grow and shrink the selection (Select › Select More/Less). In solid view a box selection catches only what you can see; Alt + Z turns on X-ray so it reaches through.

### The eight tools

| Tool | Key | What it does | A typical use |
| --- | --- | --- | --- |
| Extrude | E | Pulls the selection out and builds new faces behind it | A wall from an edge, a chimney from a face |
| Inset | I | Shrinks a face inward, leaving a border | A window frame, a panel |
| Bevel | Ctrl + B | Replaces an edge with a slanted or rounded strip | Softened corners, the sweep's fold |
| Loop cut | Ctrl + R | Adds a ring of edges around the shape | More detail where it is needed |
| Knife | K | Draws new edges click by click; Enter confirms | A cut that follows no loop |
| Merge | M | Fuses the selected vertices into one | Closing a roof to a ridge |
| Fill | F | Makes an edge or a face between the selected parts | Closing a hole |
| Delete, dissolve | X | Delete leaves a hole; Dissolve removes and heals the surface | Removing a loop you no longer want |

After any tool, a panel at the bottom left of the viewport holds its numbers: width, segments, number of cuts. Set them there if you have no scroll wheel. G, R and S act on the selection as they do on objects, and G pressed twice slides a vertex or an edge along the surface.

### Soft selection

O switches on Proportional Editing: moving one vertex drags its neighbors along, less with distance. During the move, scroll (or press Page Up and Page Down) to change the radius, drawn as a circle. A flat grid becomes a hill this way, and a membrane gets its curve.

### Smooth, flat and normals

A mesh is flat faces. Shade Smooth (right-click in Object Mode) blends the lighting across them so they read as one curved surface. Shade Flat shows the faces. Shade Auto Smooth, in the same menu, smooths gentle angles and keeps sharp ones crisp. Each face also has a front, given by its normal. If part of a mesh renders dark or a bevel turns inside out, the normals disagree: in Edit Mode press A, then Shift + N (Mesh › Normals › Recalculate Outside). Face Orientation, in the Overlays menu, paints fronts blue and backs red.

### Exercise 4.1: a tray from a cube

1. Add a cube and press Tab. Choose face selection, click the top face, and press I 0.2 Enter, then E -1.5 Enter.
2. Press Ctrl + R and move the mouse over a side until the yellow ring runs horizontally around the cube. Click, then right-click to leave the ring centered. Press S 1.15 Enter.
3. Choose edge selection, Alt + click the outer top rim, and press Ctrl + B, then click. Set Width to 0.05 m and Segments to 3 in the panel at the bottom left. Press Tab.

What you should see: a hollow tray with walls 0.2 m thick and a floor near the bottom, a belt bulging slightly around its middle, and a rounded top rim that catches a highlight.

### Exercise 4.2: a hill by soft selection

1. Add Shift + A › Mesh › Grid, and in the panel at the bottom left set X and Y Subdivisions to 30 and Size to 10 m. Press Tab, choose vertex selection, and click one vertex near the middle.
2. Press O, then G Z. Scroll until the circle covers about a third of the grid, type 2 and press Enter. Press Tab and right-click › Shade Smooth.

What you should see: a smooth hill 2 m high whose width follows the circle. With O off, the same move pulls up a single spike.

### Check yourself

1. What are the three kinds of parts in a mesh? *Vertices, edges and faces.*
2. How do you select a whole edge loop? *Alt + click one of its edges.*
3. Delete or dissolve, to remove a loop without leaving a hole? *Dissolve.*
4. Part of a mesh renders dark after editing. What do you try first? *A, then Shift + N, to recalculate the normals.*

## Chapter 5. Modifiers: edits you can change later

### Objectives

- Add, order and apply modifiers.
- Know the eight used most.
- Shape a smooth form from a simple cage with Subdivision Surface.

### What a modifier is

A modifier is an operation stored on the object and recomputed live. The mesh you edit stays simple, and what you see and render is the modifiers' result. Geometry Nodes is a modifier whose operation you write yourself, and Molecular Nodes is one of those. Add modifiers in the Modifier tab (the wrench) › Add Modifier. They run from top to bottom, so order matters: Mirror above Subdivision Surface gives one smooth whole, and the reverse leaves a crease down the middle. The icons on a modifier's header switch it on in Edit Mode, the viewport and renders. The arrow menu on the header › Apply writes the result into the mesh for good, which you rarely need.

| Modifier | What it does | Use it for |
| --- | --- | --- |
| Subdivision Surface | Splits every face and rounds the shape; Ctrl + 1, 2 or 3 adds it at that level | Smooth forms from a few faces |
| Mirror | Builds the other half across an axis | Anything symmetric: model one half |
| Solidify | Gives a surface a thickness | A sheet into a slab: a wall, a membrane |
| Bevel | Rounds the edges sharper than an angle | Corners that catch light; the sweep |
| Array | Repeats the object in a row | Steps, fences, a lattice |
| Boolean | Cuts another object's shape out of this one, or adds it | Windows, cutaways |
| Simple Deform | Bends, twists, tapers or stretches the whole mesh | A curled strip, a twisted column |
| Decimate | Reduces the number of faces | A heavy surface that slows the viewport |

### Subdivision and where the edges are

Subdivision Surface rounds everything, including corners you wanted crisp. Edges that sit close together stay sharper, so you steer the rounding with loop cuts: a Ctrl + R loop slid toward a corner tightens it. A simple cage, a Mirror and a Subdivision Surface is how most organic models are built, characters included.

### Exercise 5.1: from cube to drum

1. Add a cube and press Ctrl + 2. Right-click › Shade Smooth.
2. Press Tab, then Ctrl + R with the ring running horizontally. Click, slide the ring up near the top face, and click again. Add a second loop near the bottom the same way.

What you should see: the cube turns into a ball. With the two loops, its top and bottom flatten while its sides stay round, a drum shape, and sliding a loop (G pressed twice) changes how tight the rim is.

### Exercise 5.2: a live cutaway

1. Add a UV sphere. Add a cube and press G X 1 Enter, then G Z 1 Enter, so it covers one upper quarter of the sphere.
2. Select the sphere and add Modifier tab › Add Modifier › Generate › Boolean, set to Difference, with the cube picked in its Object field.
3. Select the cube. In the Object tab › Viewport Display, set Display As to Wire, and switch off its camera icon in the Outliner so it never renders. Move the cube with G.

What you should see: a bite out of the sphere in the cube's shape, with flat cut faces, that follows the cube as it moves.

### Check yourself

1. Why does modifier order matter? *Each works on the result of the one above it.*
2. What does Ctrl + 2 do in Object Mode? *Adds a Subdivision Surface modifier at level 2.*
3. How do you keep an edge crisp under Subdivision Surface? *Put a loop cut close to it.*
4. Where does a Boolean's cutter come from? *Another object, picked in the modifier's Object field.*

## Chapter 6. Curves, text and the camera

### Objectives

- Draw a tube with a curve.
- Add text that faces the camera.
- Frame a shot three ways and choose a lens.

### Curves

Shift + A › Curve › Bézier adds a line defined by a few control points. In Edit Mode, G moves a point, E extrudes a new one from an end, and each point's two handles set how the line bends through it. A curve has no thickness until you give it one: in the Object Data tab (the green curve icon) › Geometry › Bevel, Depth makes it a tube and Fill Caps closes its ends. The ribbon light of the [Lighting part](03-lighting.md) is such a tube. The curve stays editable, so a linker, a disordered tail or the shaft of a bent arrow can be redrawn at any time; for an arrowhead, add a Cone at the end. Object › Convert › Mesh turns a finished curve into an ordinary mesh.

### Text

Shift + A › Text adds a text object. Tab lets you type into it, with Backspace to delete, and Tab again leaves. Its Object Data tab (the letter a) sets Font, Size and Alignment, and Geometry › Extrude gives the letters depth. Labels for a figure usually belong in Illustrator, over the render, where they stay sharp and editable. Put text in the scene when it must sit in 3D: hidden behind the model at some angles, or moving in an animation. To keep it facing the viewer, add a Copy Rotation constraint (Object Constraints tab › Add Object Constraint › Copy Rotation) with the camera as its Target.

### The camera

Numpad 0 looks through the active camera (View › Cameras › Active Camera). There are three ways to aim it:

1. Navigate the viewport to a view you like, then choose View › Align View › Align Active Camera to View (Ctrl + Alt + numpad 0). The camera jumps to where your eye was.
2. In camera view, tick N › View › View Lock › Camera to View, then orbit and zoom as usual; the camera follows. Untick it when you are done.
3. In camera view, treat the camera as an object: G moves the frame, G Z Z moves the camera forward and back, and R rolls it.

In the camera's Object Data tab, Focal Length sets the lens: 50 mm is neutral, 85 to 135 mm flattens perspective and suits molecules, and below 35 mm exaggerates depth. Type › Orthographic removes perspective altogether, with Orthographic Scale as the zoom; use it when panels must be comparable. Output tab › Format sets the frame's Resolution. With several cameras, select one and press Ctrl + numpad 0 (View › Cameras › Set Active Object as Camera).

### Exercise 6.1: three lenses

1. Frame your model with the first method. Set Focal Length to 24 mm, 50 mm and 135 mm in turn, using G Z Z each time to bring the model back to the same size in the frame.
2. Set Type to Orthographic and adjust Orthographic Scale until the model fills the frame.

What you should see: at 24 mm the near parts of the model loom and the far parts shrink. At 135 mm the model looks flatter and more compact. In orthographic, parallel helices stay parallel and nothing changes size with depth.

### Exercise 6.2: a tube you can redraw

1. Add Shift + A › Curve › Bézier and set Geometry › Bevel › Depth to 0.1 m. Press Tab, select an end point, then press E, move and click. Repeat twice more.
2. Move one point with G, then turn its handles with R. Press Tab and right-click › Shade Smooth.

What you should see: a smooth tube through five points that re-flows as a point or a handle moves.

### Check yourself

1. What gives a curve thickness? *Bevel Depth, in its Object Data tab.*
2. When does text belong in the scene and not in Illustrator? *When it must be hidden by the model at some angles, or move in an animation.*
3. Which command moves the camera to your current view? *Align Active Camera to View, Ctrl + Alt + numpad 0.*
4. Which lens for figure panels that must be comparable? *Orthographic.*

## Chapter 7. Project: a cartoon house

The second half starts here. The house uses nearly every tool of Chapters 2 to 5 once and takes an evening. Save your work, then start a new file (File › New › General), which gives you a cube, a light and a camera.

### The body and the roof

1. Select the cube and press Tab. Press A, then G Z 1 Enter, so the cube stands on the floor with the object's origin at its base. Press S Y 1.5 Enter: the body is now 2 m wide, 3 m long and 2 m high.
2. Choose face selection, click the top face, and press E 1.2 Enter, then S X 0 Enter. The new top collapses to a line, the ridge. Press A, then M › By Distance to fuse the doubled vertices.
3. Click one sloping roof face and Shift + click the other. Press Shift + D, then right-click to leave the copy in place, then P › Selection. Press Tab.
4. In the Outliner, click the new object and rename it `roof` (F2). Add a Solidify modifier with Thickness 0.12 m and Offset 1. Press Tab, A, S 1.15 Enter, Tab: the roof now overhangs the walls.

### Window, door and chimney

5. Select the body and press Tab. Press Ctrl + R over a long side wall with the yellow ring running top to bottom; click, right-click, and set Number of Cuts to 2 in the panel at the bottom left. Do the same with the ring running horizontally. The wall is now nine faces.
6. Choose face selection, click the middle face, and press I 0.06 Enter, then E -0.08 Enter. Press Tab.
7. Add a cube. In N › Item, set Dimensions to 0.7, 0.08, 1.3 and Location to 0, -1.5, 0.65: a door on the front wall. Add another with Dimensions 0.35, 0.35, 1.2 and Location 0.5, 0.6, 3.0: a chimney. Select both and press Ctrl + A › Scale.

### Finishing

8. Select the body and add a Bevel modifier with Amount 0.03 m and Segments 2. Then select the door, the chimney and the roof, Shift + click the body last, and in the Bevel modifier's arrow menu choose Copy to Selected.
9. Give each object a material with a plain Base Color (Material tab › New): cream walls, a red roof, a brown door, a gray chimney. For the window, select the body, press Tab, select the recessed face, add a second slot with + in the Material tab, make a blue material in it, and press Assign.
10. Select the roof, door and chimney, Shift + click the body last, and press Ctrl + P › Object. Move the body and the house goes with it.

What you should see: a gabled house with an overhanging roof, a recessed blue window, a door and a chimney, every edge slightly rounded so that it catches a highlight. For the flat storybook look, give it the toon material and outline of the [Shaders part](04-shaders.md), Chapter 11, and light it with one sun.

### Check yourself

1. Why move the cube up in Edit Mode and not in Object Mode? *So the origin stays at the base, and Location Z 0 puts the house on the floor.*
2. What turned the flat top into a ridge? *Scaling the top face to zero along X, then merging the doubled vertices.*
3. Why apply scale on the door and chimney before copying the Bevel to them? *Setting Dimensions changed their Scale, which would stretch the bevel.*
4. How does one mesh carry two colors? *Two material slots, with the second assigned to chosen faces in Edit Mode.*

## Chapter 8. An anime character: the road map

A character is the hardest common hobby project because it stacks several separate skills, each one a chapter's worth of practice. Nothing in it is beyond the tools of this part. It is the same extrude, loop cut and modifier, used a few thousand times with judgment about where the edges go. The stages, in the order people learn them:

| Stage | What you learn | Blender tools |
| --- | --- | --- |
| 1. Reference and blocking | Working from front and side drawings; roughing out proportions with simple shapes | Shift + A › Image › Reference, primitives, Mirror |
| 2. Poly modeling | Shaping a low-poly cage for the head, then the body | Mirror and Subdivision Surface, extrude, loop cut, proportional editing |
| 3. Topology | Edge loops that circle the eyes, the mouth and the joints, so the mesh bends well | Knife, loop cut, edge slide, merge |
| 4. Sculpting, an alternative start | Shaping as if in clay, then rebuilding a clean mesh over the sculpt | Sculpt Mode, then retopology with face snapping |
| 5. Hair and clothes | Hair as tapered strands or flat cards; clothes as shells lifted off the body | Curves with a taper, Solidify |
| 6. UV unwrapping | Flattening the surface so a 2D image can wrap around it | Mark Seam, Unwrap, the UV Editing workspace |
| 7. Texturing | Painting the eyes, the face and the shading tints | The Texture Paint workspace, the Image Texture node |
| 8. Toon shading and outline | The anime look: two flat tones and a drawn line | Shader to RGB with a Color Ramp in EEVEE; an outline from Solidify with flipped normals, or Line Art |
| 9. Rigging | A skeleton that moves the mesh | Armature, the Rigify add-on, Ctrl + P › With Automatic Weights |
| 10. Weights and expressions | How strongly each bone pulls each vertex; face shapes for speech and emotion | Weight Paint mode, Shape Keys |
| 11. Posing and animation | Keyframes on bones | Pose Mode, I to insert a keyframe, the Graph Editor |

### A sensible order of projects

1. The house of Chapter 7: hard surfaces, no symmetry and no smoothing.
2. A small prop built with Mirror and Subdivision Surface, such as a mushroom, a mug or a sword: stages 1 and 2 in an hour or two.
3. A simple stylized head with a toon material: stages 1 to 3 and stage 8, where most of the anime look is decided.
4. A full character, one stage at a time, following one complete course made for it instead of many short videos. Blender Studio's [Stylized Character Workflow](https://studio.blender.org/training/stylized-character-workflow/) covers the whole path, sculpting first; it was recorded in Blender 2.8 and most of it needs a subscription, with a free YouTube version listed on the same page.

Expect the house in an evening and a first full character over weeks of regular practice. Stages 6, 7, 9 and 10 are where most beginners stall. They are also the stages that matter least for scientific work, so there is no need to reach them before the rest pays off.

### Check yourself

1. Which two modifiers does character modeling lean on? *Mirror and Subdivision Surface.*
2. What is topology, in one line? *Where the edge loops run, chosen so the mesh bends and shades well.*
3. Which stage gives the anime look? *Toon shading and outline, stage 8.*

## Chapter 9. What carries over to science

Most of it does. Once the molecule is in it, a molecular figure is a scene like any other: it needs staging, props, clean geometry and a camera, and those are general skills. What hobby modeling will not teach is the part unique to this work, data stored on geometry, which is the subject of the [Geometry Nodes](05-geometry-nodes.md) and [Molecular Nodes](07-molecular-nodes.md) parts.

| Skill | Where it shows up in molecular rendering |
| --- | --- |
| Exact transforms, the pivot, the 3D cursor, Empties | Light rigs that orbit the subject, turntables, camera rigs for matching panels |
| Origins and Apply | Bevels and modifiers that behave on backdrops and props |
| Edit Mode: extrude, loop cut, bevel | Sweeps, a membrane slab, a schematic receptor or cell surface, arrows |
| Subdivision and proportional editing | A curved membrane patch, a vesicle, a cell outline |
| Boolean, Solidify, Array | A cutaway through a surface or a map, a bilayer of real thickness, a repeated lattice |
| Curves | Linkers and disordered tails drawn by hand, arrows, glowing ribbons, camera paths |
| Per-face materials, toon shading, outlines | The flat illustrated style of journal schematics |
| Lenses and composition | Every figure |
| Keyframes and shape keys | Morphs between conformations, assembly animations |
| Rigging with bones | Rarely: hinge motions are usually done with morphs or Geometry Nodes |
| UV unwrapping and texture painting | Seldom: molecular surfaces take their color from attributes and procedural textures |
| Sculpting | Sometimes: organelles and cell-scale context |

### Exercise 9.1: a membrane under the receptor

1. Add a plane and press Tab. Press A, then S 25 Enter, then right-click › Subdivide, and set Number of Cuts to 30 in the panel at the bottom left.
2. Choose vertex selection and click a vertex near the middle. Press O, then G Z. Scroll until the circle covers about half the plane, type -3 and press Enter. Press Tab.
3. Add a Solidify modifier with Thickness 4 m, then a Subdivision Surface modifier at level 2, and right-click › Shade Smooth. A bilayer is about 4 nm thick, and 1 nm is 1 m at the Molecular Nodes scale.
4. Move the slab under your model with G Z, and give it the soft wax material from the [Recipes part](01-material-recipes.md).

What you should see: a slab with rounded edges and a broad shallow dip, as thick against the receptor as a real bilayer would be, reading as one soft translucent body under the ectodomain.

### Check yourself

1. Which hobby skills matter least for molecular figures? *UV unwrapping, texture painting and rigging.*
2. Why make the slab 4 m thick? *A bilayer is about 4 nm, and Molecular Nodes imports 1 nm as 1 m.*
3. What does this work need that hobby modeling does not teach? *Attributes and Geometry Nodes: data stored on geometry.*

## Chapter 10. Chooser, glossary and sources

### I want this, use that

| I want to | Use |
| --- | --- |
| Move along one axis by an exact amount | G, the axis key, a number, Enter |
| Orbit one thing around another | 3D cursor on the center, pivot set to 3D Cursor, R |
| Put one object exactly on another | Shift + S: Cursor to Selected, then Selection to Cursor |
| Set an object down on a surface | Snapping to Face with Align Rotation to Target |
| Work on one object alone | Numpad / |
| Stop a bevel or modifier from stretching | Ctrl + A › Scale |
| Change where an object pivots | Object › Set Origin |
| Move several things as one | Parent them to an Empty |
| Keep a light or camera aimed | Track To |
| A copy that stays in sync | Alt + D |
| Round a whole shape | Subdivision Surface, Ctrl + 2 |
| Round only the edges | The Bevel modifier |
| Give a sheet thickness | Solidify |
| Cut a window or a cutaway | Boolean set to Difference |
| A tube along a path | A curve with Bevel Depth |
| The camera where my eye is | Ctrl + Alt + numpad 0 |
| A command I have forgotten | F3 |

### Glossary

- **Active object**: the last one clicked; the one the Properties editor shows and that multi-object commands center on.
- **Apply**: write a transform or a modifier's result into the mesh and reset it.
- **Collection**: a folder of objects in the Outliner.
- **Edge loop**: a line of edges running around a shape; Alt + click selects one.
- **Empty**: an object with no geometry, used as a handle or a target.
- **Modifier**: a stored, live operation on an object's mesh.
- **Normal**: the direction a face's front points.
- **Origin**: the point an object's Location refers to, and that it turns about.
- **Parent**: an object whose transform its children follow.
- **Pivot**: the point a rotation or scale happens around.
- **Proportional Editing**: moving a selection so that its neighbors follow, less with distance.
- **Topology**: how a mesh's edges and faces are laid out.

### Sources

- [Bevel Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html), Blender manual.
- [Stylized Character Workflow](https://studio.blender.org/training/stylized-character-workflow/), Blender Studio.
- In Blender, F1 over any button opens its page in the manual.
