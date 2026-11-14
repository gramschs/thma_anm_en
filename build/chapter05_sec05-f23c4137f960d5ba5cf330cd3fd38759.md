---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 5.5 Exercises

These exercises are meant for self-study at home and review the material of
Chapters 5.1 to 5.4. Allow about 90 minutes for them. Before
starting the exercises, run the following two cells. They contain the
plotting function, the functions from Chapters 5.1, 5.3 and 5.4, and the arm
and the part of the SCARA robot.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 5 min)
* ✩✩ Application: write your own code and interpret results (approx. 10 min)
* ✩✩✩ Mini-project: combine several concepts from this chapter (approx. 30 min)

```{code-cell} python
:tags: [hide-input]
# Given plotting function: just run it, you do not need to understand it.
def plot_robot(arms, parts=None, targets=None, path=None, surroundings=None,
               labels=None, title='', limit=0.8):
    """Plots a robot arm in top view.

    arms: points of an arm as an array, row = [x, y], from the first joint to
          the gripper, or a list of such arrays for several positions
    parts: corner points of the part in the gripper as an array, or a list
           with one array per position (optional)
    targets: target points as an array, row = [x, y], marked as crosses (optional)
    path: gripper positions as an array, row = [x, y], drawn as a dashed
          line with dots (optional)
    surroundings: corner points of areas such as a conveyor belt or a box as
                  an array or a list of arrays, filled in gray (optional)
    labels: legend entries, one per position (optional)
    title: plot title
    limit: visible range from -limit to +limit in m
    """
    blue, red, orange, gray = '#005A94', '#E60000', '#E87846', '#484949'
    colors = [blue, red, orange, gray]
    if isinstance(arms, np.ndarray):
        arms = [arms]
    if isinstance(parts, np.ndarray):
        parts = [parts]
    if isinstance(surroundings, np.ndarray):
        surroundings = [surroundings]
    fig, ax = plt.subplots(figsize=(6, 6))

    # surroundings: areas such as a conveyor belt or a box
    if surroundings is not None:
        for area in surroundings:
            ax.fill(area[:, 0], area[:, 1], facecolor='#DDDEDE',
                    edgecolor=gray, linewidth=1, zorder=0)

    # base at the origin
    ax.add_patch(plt.Circle((0, 0), 0.06, facecolor='#CCDEE9', edgecolor=blue,
                            linewidth=1.5, zorder=1))

    # gripper path as a dashed line with dots
    if path is not None:
        ax.plot(path[:, 0], path[:, 1], color=gray, linestyle='--', linewidth=1,
                marker='o', markersize=3, label='Gripper path', zorder=1)

    # arms: joints as circles, gripper as a square, part filled in yellow
    for k in range(len(arms)):
        color = colors[k % len(colors)]
        points = arms[k]
        label = None if labels is None else labels[k]
        ax.plot(points[:, 0], points[:, 1], color=color, linewidth=6,
                solid_capstyle='round', label=label, zorder=2)
        ax.scatter(points[:-1, 0], points[:-1, 1], s=50, color='white',
                   edgecolor=color, linewidth=2, zorder=3)
        ax.scatter(points[-1, 0], points[-1, 1], s=60, marker='s', color=color,
                   zorder=3)
        if parts is not None:
            corners = parts[k]
            ax.fill(corners[:, 0], corners[:, 1], facecolor='#FFEC7F',
                    edgecolor=color, linewidth=1.5, zorder=4)

    # target points as crosses
    if targets is not None:
        targets = np.atleast_2d(targets)
        ax.scatter(targets[:, 0], targets[:, 1], marker='x', s=80, color=gray,
                   linewidth=2, zorder=5, label='Target')

    if labels is not None or targets is not None or path is not None:
        ax.legend(loc='lower left')
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_xlabel('x in m')
    ax.set_ylabel('y in m')
    ax.set_title(title)
    plt.show()
```

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# function from Chapter 5.1
def rotation_matrix(angle):
    """Rotation matrix for a rotation about the origin, angle in radians."""
    return np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle),  np.cos(angle)],
    ])

# functions from Chapter 5.3
def transformation_matrix(angle, tx, ty):
    """Homogeneous matrix: rotate by angle (radians), then shift by (tx, ty)."""
    return np.array([
        [np.cos(angle), -np.sin(angle), tx],
        [np.sin(angle),  np.cos(angle), ty],
        [0.0,            0.0,           1.0],
    ])

def transform(T, points):
    """Applies the homogeneous matrix T to all points, row = [x, y]."""
    points_hom = np.ones((len(points), 3))
    points_hom[:, 0:2] = points
    result = (T @ points_hom.T).T
    return result[:, 0:2]

def rotation_about_point(angle, center):
    """Homogeneous matrix: rotation about the point center, angle in radians."""
    T_to_origin = transformation_matrix(0, -center[0], -center[1])
    T_rot = transformation_matrix(angle, 0, 0)
    T_back = transformation_matrix(0, center[0], center[1])
    return T_back @ T_rot @ T_to_origin

# points of the arm in the home position in m, row = [x, y]
arm = np.array([
    [0.0, 0.0],   # joint 1
    [0.4, 0.0],   # joint 2
    [0.7, 0.0],   # gripper
])

# corners of the part in the gripper in m, home position
part = np.array([
    [0.66, -0.02],
    [0.74, -0.02],
    [0.74,  0.02],
    [0.66,  0.02],
])

# function from Chapter 5.4
def robot_position(alpha, beta):
    """Arm points and part corners for the joint angles in radians."""
    T_alpha = transformation_matrix(alpha, 0, 0)
    T_arm2 = T_alpha @ rotation_about_point(beta, arm[1])
    # arm 1 only with T_alpha, arm 2 and the part with both rotations
    arm1_new = transform(T_alpha, arm[0:2])
    arm2_new = transform(T_arm2, arm[1:3])
    arm_new = np.array([arm1_new[0], arm1_new[1], arm2_new[1]])
    part_new = transform(T_arm2, part)
    return arm_new, part_new
```

````{admonition} Exercise 5.1 (✩)
:class: tip
At $\alpha = 0$ and $\beta = 90°$, the gripper of the SCARA robot is at the
point $(0.4, 0.3)$, as in Chapter 5.3. Now joint 1 rotates by $90°$, and
joint 2 stays bent. Given the following code:

```python
import numpy as np

gripper = np.array([0.4, 0.3])
R = rotation_matrix(np.deg2rad(90))

print(np.round(R, 4))
print(np.round(R @ gripper, 4))
print(np.round(R.T @ gripper, 4))
print(np.round(np.cos(90), 4))
```

Write down your guess in a Markdown cell before you run the code.

1. What are the entries of the matrix `R`?
2. What is the result of `R @ gripper`? Compute the product by hand. How far
   is the gripper from the origin before and after the rotation?
3. Which rotation does `R.T` correspond to, and where does it move the
   gripper?
4. Why does the last line not print 0?
5. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

gripper = np.array([0.4, 0.3])
R = rotation_matrix(np.deg2rad(90))

print(np.round(R, 4))
print(np.round(R @ gripper, 4))
print(np.round(R.T @ gripper, 4))
print(np.round(np.cos(90), 4))
```
Output:

```text
[[ 0. -1.]
 [ 1.  0.]]
[-0.3  0.4]
[ 0.3 -0.4]
-0.4481
```

The columns of `R` are the rotated unit vectors: $\vec{e}_x$ becomes
$(0, 1)^\top$, and $\vec{e}_y$ becomes $(-1, 0)^\top$. By hand, we get

$$\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}
\begin{pmatrix} 0.4 \\ 0.3 \end{pmatrix}
= \begin{pmatrix} 0 \cdot 0.4 + (-1) \cdot 0.3 \\ 1 \cdot 0.4 + 0 \cdot 0.3 \end{pmatrix}
= \begin{pmatrix} -0.3 \\ 0.4 \end{pmatrix}.$$

Before and after the rotation, the gripper is
$\sqrt{0.4^2 + 0.3^2} = 0.5\,\text{m}$ from the origin, because a rotation
does not change lengths. `R.T` is the rotation by $-90°$. It moves the
gripper to $(0.3, -0.4)$, i.e. into the position $\alpha = -90°$,
$\beta = 90°$. The last line uses 90 radians instead of $90°$. Without
`np.deg2rad`, there is no error message, just a wrong result.
````

````{admonition} Exercise 5.2 (✩)
:class: tip
The swivel arm from Chapter 5.2 first swivels the lid by $50°$
counterclockwise and then $20°$ back. Given the following code:

```python
import numpy as np

# corners of the lid in the home position in m
lid = np.array([
    [0.55, -0.03],
    [0.65, -0.03],
    [0.65,  0.03],
    [0.55,  0.03],
])
R_1 = rotation_matrix(np.deg2rad(50))
R_2 = rotation_matrix(np.deg2rad(-20))
lid_new = (R_2 @ R_1 @ lid.T).T

print(lid.T.shape)
print(np.allclose(R_2 @ R_1, rotation_matrix(np.deg2rad(30))))
print(np.allclose(R_2 @ R_1, R_1 @ R_2))

# long edge of the lid from corner 0 to corner 1
edge = lid_new[1] - lid_new[0]
print(np.round(edge, 4))
```

Write down your guess in a Markdown cell before you run the code.

1. What is the shape of `lid.T`, and what is the shape of `lid_new`?
2. What do the two lines with `np.allclose` print? Explain your answer.
3. In the home position, the long edge is $0.1\,\text{m}$ long and points in
   the $x$-direction. Which values do you expect for `edge` after the swivel
   motion? Hint: $\cos 30° \approx 0.866$.
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

lid = np.array([
    [0.55, -0.03],
    [0.65, -0.03],
    [0.65,  0.03],
    [0.55,  0.03],
])
R_1 = rotation_matrix(np.deg2rad(50))
R_2 = rotation_matrix(np.deg2rad(-20))
lid_new = (R_2 @ R_1 @ lid.T).T

print(lid.T.shape)
print(np.allclose(R_2 @ R_1, rotation_matrix(np.deg2rad(30))))
print(np.allclose(R_2 @ R_1, R_1 @ R_2))

edge = lid_new[1] - lid_new[0]
print(np.round(edge, 4))
```
Output:

```text
(2, 4)
True
True
[0.0866 0.05  ]
```

`lid` has four corners and the shape `(4, 2)`, so `lid.T` has the shape
`(2, 4)`. After the second `.T`, `lid_new` again has the shape `(4, 2)`. Both
rotations are about the same joint, so the angles add up to
$50° - 20° = 30°$. In a sum, the order does not matter, which is why the two
matrix products are equal here as well. This holds only for rotations about
the same point. The edge is the difference of two corners, so its position
does not matter. It only rotates: $(0.1, 0)$ becomes
$0.1 \cdot (\cos 30°, \sin 30°) = (0.0866, 0.05)$, and the length stays
$0.1\,\text{m}$.
````

````{admonition} Exercise 5.3 (✩)
:class: tip
Given the following code with a homogeneous transformation matrix and three
points on the straight arm of the SCARA robot:

```python
import numpy as np

T = transformation_matrix(np.deg2rad(180), 0.7, 0.0)

# points on the arm in homogeneous coordinates
joint1 = np.array([0.0, 0.0, 1.0])
gripper = np.array([0.7, 0.0, 1.0])
midpoint = np.array([0.35, 0.0, 1.0])
# direction of the arm in the home position
direction = np.array([1.0, 0.0, 0.0])

print(np.round(T @ joint1, 4))
print(np.round(T @ gripper, 4))
print(np.round(T @ midpoint, 4))
print(np.round(T @ direction, 4))
```

Write down your guess in a Markdown cell before you run the code.

1. What is the result of `T @ joint1`? Which part of `T` shows up in it?
2. Where does `T` move the gripper? Remember that `T` rotates first and then
   shifts.
3. What is the result of `T @ midpoint`? What motion does `T` describe
   overall?
4. `direction` has a 0 as its third coordinate. What is the result of
   `T @ direction`, and why is the direction not shifted?
5. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

T = transformation_matrix(np.deg2rad(180), 0.7, 0.0)

joint1 = np.array([0.0, 0.0, 1.0])
gripper = np.array([0.7, 0.0, 1.0])
midpoint = np.array([0.35, 0.0, 1.0])
direction = np.array([1.0, 0.0, 0.0])

print(np.round(T @ joint1, 4))
print(np.round(T @ gripper, 4))
print(np.round(T @ midpoint, 4))
print(np.round(T @ direction, 4))
```
Output:

```text
[0.7 0.  1. ]
[0. 0. 1.]
[0.35 0.   1.  ]
[-1.  0.  0.]
```

The rotation leaves the origin in place, so for joint 1 only the translation
remains. `T @ joint1` therefore returns the right column of `T`, the
translation vector $(0.7, 0)$. `T` first rotates the gripper to $(-0.7, 0)$
and then shifts it to $(0, 0)$. Joint 1 and the gripper therefore swap
places; only the midpoint of the arm stays at $(0.35, 0)$. Overall, `T` turns
the arm end for end: it is a rotation by $180°$ about the midpoint of the arm,
and
`rotation_about_point(np.deg2rad(180), [0.35, 0])` gives the same matrix. For
`direction`, the right column of `T` is multiplied by the 0. The direction is
only rotated and then points in the $-x$-direction; it is not shifted. A
direction has no location, so this is exactly right.
````

````{admonition} Exercise 5.4 (✩)
:class: tip
A workpiece lies at $(0.1, 0)$ on the table of a machine tool. The table can
rotate about the origin and move in the $x$-direction. Given the following
code:

```python
import numpy as np

T_rot = transformation_matrix(np.deg2rad(90), 0, 0)   # rotation by 90 degrees
T_shift = transformation_matrix(0, 0.2, 0)            # shift by 0.2 m in x
workpiece = np.array([[0.1, 0.0]])

print(np.round(transform(T_shift @ T_rot, workpiece), 4))
print(np.round(transform(T_rot @ T_shift, workpiece), 4))
print(np.round(T_shift @ T_rot, 4))
print(np.round(T_rot @ T_shift, 4))
```

Write down your guess in a Markdown cell before you run the code.

1. Which motion acts first in `T_shift @ T_rot`? Where does the workpiece
   end up?
2. Where does the workpiece end up with `T_rot @ T_shift`?
3. One of the two products equals
   `transformation_matrix(np.deg2rad(90), 0.2, 0)`. Which one, and why?
   Which translation is in the right column of the other product?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

T_rot = transformation_matrix(np.deg2rad(90), 0, 0)
T_shift = transformation_matrix(0, 0.2, 0)
workpiece = np.array([[0.1, 0.0]])

print(np.round(transform(T_shift @ T_rot, workpiece), 4))
print(np.round(transform(T_rot @ T_shift, workpiece), 4))
print(np.round(T_shift @ T_rot, 4))
print(np.round(T_rot @ T_shift, 4))
```
Output:

```text
[[0.2 0.1]]
[[0.  0.3]]
[[ 0.  -1.   0.2]
 [ 1.   0.   0. ]
 [ 0.   0.   1. ]]
[[ 0.  -1.   0. ]
 [ 1.   0.   0.2]
 [ 0.   0.   1. ]]
```

In a matrix product, the right matrix acts first. With `T_shift @ T_rot`, the
table first rotates the workpiece to $(0, 0.1)$ and then shifts it to
$(0.2, 0.1)$. With `T_rot @ T_shift`, the workpiece is first shifted to
$(0.3, 0)$ and then rotated about the origin to $(0, 0.3)$. By its
definition, `transformation_matrix` rotates first and shifts afterward. That
is why `T_shift @ T_rot` equals
`transformation_matrix(np.deg2rad(90), 0.2, 0)`. The other product contains
the translation $(0, 0.2)$, because the rotation has also rotated the
translation vector. As soon as translations are involved, the matrix product
is therefore no longer commutative. The workpiece is an array of shape
`(1, 2)` because `transform` expects the points row by row.
````

```{admonition} Exercise 5.5 (✩✩)
:class: tip
A CNC drilling machine needs to drill six holes on the **bolt circle** of a
flange, i.e. on a circle around the center of the flange. On the machine
table, the center of the flange is at $M = (120, 80)$ in mm, and the bolt
circle has a radius of $50\,\text{mm}$. The first hole is to the right of the
center at $(170, 80)$; the others follow counterclockwise at intervals of
$60°$.

1. Use `rotation_about_point` and `transform` to compute the positions of
   all six holes and store them in an array `holes` of shape `(6, 2)`. You
   get hole $k$ by rotating the first hole by $k \cdot 60°$ about $M$.
2. Use the Pythagorean theorem to check that all holes are $50\,\text{mm}$
   from $M$. How far apart are two neighboring holes? Explain the result
   geometrically.
3. By mistake, the flange was clamped in a position rotated by $15°$ about
   its center. Compute the actual positions with a single transformation and
   plot the nominal and actual positions with `ax.scatter` in one diagram.
   To make the bolt circle look round, add `ax.set_aspect('equal')`. How far,
   in millimeters, is each hole from its nominal position?

Structure your code with IPO comments (input, processing, output).
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# Input
center = np.array([120.0, 80.0])        # center of the flange in mm
first_hole = np.array([[170.0, 80.0]])  # as a row for transform

# Processing: hole k by rotating by k * 60 degrees about the center
holes = np.zeros((6, 2))
for k in range(6):
    T = rotation_about_point(np.deg2rad(60 * k), center)
    holes[k] = transform(T, first_hole)[0]

# distances of all holes to the center
difference = holes - center
dist_center = np.sqrt(difference[:, 0]**2 + difference[:, 1]**2)

# distance between the neighboring holes 0 and 1
difference = holes[1] - holes[0]
dist_neighbor = np.sqrt(difference[0]**2 + difference[1]**2)

# flange rotated by 15 degrees: one rotation about the center for all holes
T_misaligned = rotation_about_point(np.deg2rad(15), center)
holes_actual = transform(T_misaligned, holes)
difference = holes_actual - holes
offset = np.sqrt(difference[:, 0]**2 + difference[:, 1]**2)

# Output
print('Holes in mm:')
print(np.round(holes, 2))
print('Distance to the center in mm:', np.round(dist_center, 2))
print(f'Distance between neighboring holes: {dist_neighbor:.2f} mm')
print('Offset due to the misalignment in mm:', np.round(offset, 2))

fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(holes[:, 0], holes[:, 1], label='Nominal')
ax.scatter(holes_actual[:, 0], holes_actual[:, 1], marker='x',
           label='Actual, rotated by 15°')
ax.scatter(center[0], center[1], marker='+', s=80, color='black',
           label='Flange center')
ax.set_aspect('equal')
ax.set_xlim(50, 190)
ax.set_ylim(10, 170)
ax.set_xlabel('x in mm')
ax.set_ylabel('y in mm')
ax.set_title('Bolt circle of the flange')
ax.legend(loc='upper left')
ax.grid(True)
plt.show()
```
Output:

```text
Holes in mm:
[[170.   80. ]
 [145.  123.3]
 [ 95.  123.3]
 [ 70.   80. ]
 [ 95.   36.7]
 [145.   36.7]]
Distance to the center in mm: [50. 50. 50. 50. 50. 50.]
Distance between neighboring holes: 50.00 mm
Offset due to the misalignment in mm: [13.05 13.05 13.05 13.05 13.05 13.05]
```

The functions work with any unit of length, here mm. All holes are
$50\,\text{mm}$ from the center, because a rotation about $M$ does not change
distances to $M$. Two neighboring holes and the center form a triangle with
two sides of $50\,\text{mm}$ and an angle of $60°$ between them. This
triangle is equilateral, so neighboring holes are also $50\,\text{mm}$ apart.
Due to the misalignment, each hole moves a short distance along the circle
and ends up $13.05\,\text{mm}$ from its nominal position. This is the
straight-line distance, i.e. the chord. The arc itself is slightly longer, at
$50\,\text{mm} \cdot 0.2618 = 13.09\,\text{mm}$, as with the gripper path in
Chapter 5.2. The offset is the same for all holes because they are all the
same distance from $M$. The flange would therefore be scrap. That is why CNC
controllers measure the position of the workpiece before drilling and rotate
the hole pattern accordingly, using exactly this transformation.
````

```{admonition} Exercise 5.6 (✩✩)
:class: tip
In Chapter 5.4 we saw that arm 2 is always rotated by $\alpha + \beta$
relative to the $x$-axis. From this, the gripper position can also be
computed without matrices.

1. Without code, derive formulas for the coordinates $x$ and $y$ of the
   gripper. Joint 2 lies on a circle of radius $l_1 = 0.4\,\text{m}$ around
   the origin, like the gripper in Chapter 5.1. Arm 2 has the length
   $l_2 = 0.3\,\text{m}$ and points from joint 2 in the direction of the
   angle $\alpha + \beta$.
2. Write a function `gripper_formula(alpha, beta)` with a docstring that
   returns the gripper position for angles in radians as an array.
3. For the angle pairs $(30°, 60°)$, $(9°, 99°)$, $(120°, 45°)$ and
   $(180°, 150°)$, use `np.allclose` to compare your function with the
   gripper from `robot_position`.
4. The formula is much shorter than the chain of transformation matrices.
   Why do robot controllers still work with matrices?

Structure your code with IPO comments (input, processing, output).
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# Input
def gripper_formula(alpha, beta):
    """Gripper position of the SCARA robot in m, angles in radians.

    Joint 2 lies at l1 * (cos alpha, sin alpha), arm 2 points in the
    direction alpha + beta.
    """
    l1 = 0.4
    l2 = 0.3
    x = l1 * np.cos(alpha) + l2 * np.cos(alpha + beta)
    y = l1 * np.sin(alpha) + l2 * np.sin(alpha + beta)
    return np.array([x, y])

angle_pairs = np.array([[30, 60], [9, 99], [120, 45], [180, 150]])

# Processing and output
for k in range(len(angle_pairs)):
    alpha = np.deg2rad(angle_pairs[k, 0])
    beta = np.deg2rad(angle_pairs[k, 1])
    gripper = gripper_formula(alpha, beta)
    arm_new, part_new = robot_position(alpha, beta)
    print(f'({angle_pairs[k, 0]:3d}°, {angle_pairs[k, 1]:3d}°): '
          f'gripper at {np.round(gripper, 4)} m, '
          f'same as robot_position: {np.allclose(gripper, arm_new[2])}')
```
Output:

```text
( 30°,  60°): gripper at [0.3464 0.5   ] m, same as robot_position: True
(  9°,  99°): gripper at [0.3024 0.3479] m, same as robot_position: True
(120°,  45°): gripper at [-0.4898  0.4241] m, same as robot_position: True
(180°, 150°): gripper at [-0.1402 -0.15  ] m, same as robot_position: True
```

Joint 2 lies at $l_1 (\cos\alpha, \sin\alpha)$. From there, the gripper is
another $l_2$ away in the direction $\alpha + \beta$:

$$x = l_1 \cos\alpha + l_2 \cos(\alpha + \beta), \qquad
y = l_1 \sin\alpha + l_2 \sin(\alpha + \beta).$$

For all four angle pairs, the formula agrees with `robot_position`. For the
gripper alone, it is indeed shorter. The controller, however, also needs the
corners of the part, and many robots have more than two joints that rotate in
3D space. Each additional quantity would need its own, ever longer formula.
With matrices, each joint gets its own matrix, and the chain of matrix
products looks the same for every robot. That is why robot controllers
describe their arms with homogeneous transformation matrices.
````

```{admonition} Exercise 5.7 (✩✩)
:class: tip
Which points can the gripper of the SCARA robot reach at all? The set of
these points is called the **workspace** of the robot. As in Chapter 5.4,
joint 1 rotates between $0°$ and $180°$, and joint 2 between $0°$ and $150°$.

1. Use `robot_position` to compute the gripper position for all angles
   $\alpha$ from $0°$ to $180°$ and $\beta$ from $0°$ to $150°$ in steps of
   $5°$. Store the positions in an array `points` with
   $37 \cdot 31 = 1147$ rows and two columns. Create it beforehand with
   `np.zeros` and use a row index that you increase by one in the inner
   loop.
2. Plot the points with `ax.scatter(..., s=2)`. Add `ax.set_aspect('equal')`
   so that circles look round.
3. Compute the smallest and the largest distance of the points from the
   origin.
4. Answer without code: why does the workspace have a hole in the middle? Can
   the robot put down a part at $(0.10, 0.15)$?

Structure your code with IPO comments (input, processing, output).
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# Input
alphas_deg = np.linspace(0, 180, 37)
betas_deg = np.linspace(0, 150, 31)

# Processing: gripper position for every combination of angles
points = np.zeros((len(alphas_deg) * len(betas_deg), 2))
row = 0
for alpha_deg in alphas_deg:
    for beta_deg in betas_deg:
        arm_new, part_new = robot_position(np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
        points[row] = arm_new[2]
        row += 1

distances = np.sqrt(points[:, 0]**2 + points[:, 1]**2)

# Output
print('Shape of points:', points.shape)
print(f'Smallest distance from the origin: {np.min(distances):.3f} m')
print(f'Largest distance from the origin:  {np.max(distances):.3f} m')

fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(points[:, 0], points[:, 1], s=2)
ax.set_aspect('equal')
ax.set_xlabel('x in m')
ax.set_ylabel('y in m')
ax.set_title('Workspace of the SCARA robot')
ax.grid(True)
plt.show()
```
Output:

```text
Shape of points: (1147, 2)
Smallest distance from the origin: 0.205 m
Largest distance from the origin:  0.700 m
```

The workspace is a ring-shaped region with the outer radius
$l_1 + l_2 = 0.7\,\text{m}$, which the straight arm reaches. The distance of
the gripper from the origin depends only on the bend angle $\beta$, because
$\alpha$ rotates the whole arm about the origin. The more joint 2 bends, the
closer the gripper gets to the base. Because $\beta$ is at most $150°$,
arm 2 cannot fold all the way back onto arm 1, and a hole with a radius of
$0.205\,\text{m}$ remains in the middle. The point $(0.10, 0.15)$ is
$\sqrt{0.10^2 + 0.15^2} \approx 0.180\,\text{m}$ from the origin, i.e. inside
this hole. The robot cannot put down a part there. The workspace is not an
exact half ring, though. When arm 2 bends, it also turns the gripper
counterclockwise. That is why, on the right, the workspace reaches down to the
$x$-axis only at its outer edge, and on the left, it extends below the
$x$-axis.
````

```{admonition} Exercise 5.8 (✩✩)
:class: tip
In Chapter 5.4, the grid search with steps of $1°$ computed a total of
$27\,331$ positions and still missed the placement site
$P_1 = (0.30, 0.35)$ by $3.2\,\text{mm}$. A finer grid over the whole range
of angles would be too expensive. We therefore search in two stages: first
coarsely over the whole range, then finely in the neighborhood of the coarse
result.

1. Write a function `search(target, alphas_deg, betas_deg)` that tries all
   combinations of the angles from the two arrays. It should return the best
   angles in degrees and the remaining distance.
2. Stage 1: For $P_1$, search the whole range with steps of $5°$, $\alpha$
   from $0°$ to $180°$ and $\beta$ from $0°$ to $150°$.
3. Stage 2: Search with steps of $0.1°$ in a window of $\pm 5°$ around the
   angles from stage 1. How many positions do both stages compute together,
   and how large is the remaining distance? Compare with the search from
   Chapter 5.4.
4. Repeat both stages for $P_2 = (0.40, 0.40)$, once with a window of
   $\pm 5°$ and once with $\pm 1°$. Why does the small window fail?

Structure your code with IPO comments (input, processing, output).
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# Input
def search(target, alphas_deg, betas_deg):
    """Tries all combinations of the angles in degrees.

    Returns: best alpha, best beta in degrees and the remaining distance in m
    """
    best_distance = 10.0
    for alpha_deg in alphas_deg:
        for beta_deg in betas_deg:
            arm_new, part_new = robot_position(np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
            difference = arm_new[2] - target
            distance = np.sqrt(difference[0]**2 + difference[1]**2)
            if distance < best_distance:
                best_distance = distance
                best_alpha = alpha_deg
                best_beta = beta_deg
    return best_alpha, best_beta, best_distance

p1 = np.array([0.30, 0.35])
p2 = np.array([0.40, 0.40])

# Processing and output, stage 1: coarse grid over the whole range
alpha_coarse, beta_coarse, dist_coarse = search(p1, np.linspace(0, 180, 37),
                                                np.linspace(0, 150, 31))
print(f'P1 coarse: α = {alpha_coarse:.1f}°, β = {beta_coarse:.1f}°, '
      f'remaining {dist_coarse * 1000:.2f} mm')

# stage 2: fine grid with 0.1 degrees in a window of +-5 degrees
alpha_fine, beta_fine, dist_fine = search(
    p1, np.linspace(alpha_coarse - 5, alpha_coarse + 5, 101),
    np.linspace(beta_coarse - 5, beta_coarse + 5, 101))
print(f'P1 fine: α = {alpha_fine:.1f}°, β = {beta_fine:.1f}°, '
      f'remaining {dist_fine * 1000:.2f} mm')
print('Total positions:', 37 * 31 + 101 * 101)

# task 4: P2 with a large and a small window
alpha_coarse, beta_coarse, dist_coarse = search(p2, np.linspace(0, 180, 37),
                                                np.linspace(0, 150, 31))
print(f'P2 coarse: α = {alpha_coarse:.1f}°, β = {beta_coarse:.1f}°, '
      f'remaining {dist_coarse * 1000:.2f} mm')
for window in [5, 1]:
    num = int(20 * window + 1)   # steps of 0.1 degrees
    alpha_fine, beta_fine, dist_fine = search(
        p2, np.linspace(alpha_coarse - window, alpha_coarse + window, num),
        np.linspace(beta_coarse - window, beta_coarse + window, num))
    print(f'P2 fine, window ±{window}°: α = {alpha_fine:.1f}°, '
          f'β = {beta_fine:.1f}°, remaining {dist_fine * 1000:.2f} mm')
```
Output:

```text
P1 coarse: α = 10.0°, β = 100.0°, remaining 8.79 mm
P1 fine: α = 9.4°, β = 99.0°, remaining 0.07 mm
Total positions: 11348
P2 coarse: α = 15.0°, β = 70.0°, remaining 12.74 mm
P2 fine, window ±5°: α = 14.5°, β = 73.1°, remaining 0.21 mm
P2 fine, window ±1°: α = 15.3°, β = 71.0°, remaining 7.15 mm
```

The coarse grid misses $P_1$ by almost $9\,\text{mm}$ but shows where to
look more closely. Together, both stages compute $11\,348$ positions,
less than half as many as the $1°$ search from Chapter 5.4. At the same time,
the remaining distance drops from $3.2\,\text{mm}$ to $0.07\,\text{mm}$. A
fine grid over the whole range would need about 2.7 million positions for the
same accuracy. For $P_2$, the best angle $\beta \approx 73.1°$ is just over
$3°$ away from the coarse result $70°$. The window of $\pm 1°$ only extends
to $71°$, and the fine search ends at the edge of the window with a remaining
distance of just over $7\,\text{mm}$. That is even worse than the $1°$ search
from Chapter 5.4. The window must therefore be at least as large as one step
of the coarse grid. A result right at the edge of the window is a sign that
the window is too small.
````

````{admonition} Exercise 5.9 (✩✩✩) Mini-project: A rotary axis at the gripper
:class: tip
In Chapter 5.4, the parts lay at an angle on the circuit board, because the
part is rigidly attached to arm 2 and is always rotated by $\alpha + \beta$.
We therefore equip the SCARA robot with a third rotary axis directly at the
gripper. It rotates the part by the angle $\gamma$ about its own center, i.e.
about the gripper. In the home position $\alpha = \beta = \gamma = 0$, the
gripper is at $(0.7, 0)$. For each site, the placement plan specifies the
angle that the long edge of the part should make with the $x$-axis:

| Site | Position in m | Angles from Chapter 5.4 | Target angle of the part |
| --- | --- | --- | --- |
| $P_1$ | $(0.30, 0.35)$ | $\alpha = 9°$, $\beta = 99°$ | $0°$ |
| $P_2$ | $(0.40, 0.40)$ | $\alpha = 14°$, $\beta = 74°$ | $90°$ |
| $P_3$ | $(0.45, 0.30)$ | $\alpha = 1°$, $\beta = 79°$ | $45°$ |

The feeder, the circuit board and the placement sites from Chapter 5.4:

```python
feeder = np.array([[0.62, -0.06], [0.78, -0.06], [0.78, 0.06], [0.62, 0.06]])
board = np.array([[0.25, 0.25], [0.50, 0.25], [0.50, 0.45], [0.25, 0.45]])
placement_sites = np.array([[0.30, 0.35], [0.40, 0.40], [0.45, 0.30]])
```

**Part 1:** Write a function
`robot_position_with_gripper_axis(alpha, beta, gamma)` that, like
`robot_position`, returns the points of the arm and the corners of the part.
Transform the part with
$\mathbf{T}_\alpha \cdot \mathbf{T}_\beta \cdot \mathbf{T}_\gamma$, where
$\mathbf{T}_\gamma$ rotates about the position of the gripper in the home
position. Check for $\alpha = 30°$ and $\beta = 60°$: with $\gamma = 0$, the
function returns the same as `robot_position`. With $\gamma = 90°$, the
center of the part stays at the gripper. The center is the midpoint of the
diagonal, i.e. `(corners[0] + corners[2]) / 2`.

**Part 2:** For each site, compute the angle $\gamma$ that rotates the part
from the angle $\alpha + \beta$ to the target angle. Use `np.allclose` to
check that the long edge `corners[1] - corners[0]` then equals
$0.08 \cdot (\cos\varphi_\text{target}, \sin\varphi_\text{target})$.

**Part 3:** The gripper axis can only rotate between $-90°$ and $+90°$ so
that the cables to the gripper do not get wound up. Use an `if` statement to
check for which site $\gamma$ lies outside this range. The part is a
rectangle and looks exactly the same after a half turn. Correct $\gamma$ for
this site by $180°$. Then plot all three positions with their parts, the
feeder and the circuit board.

**Closing question:** Why must $\mathbf{T}_\gamma$ be on the far right of the
chain? What would happen to the part if we used
$\mathbf{T}_\gamma \cdot \mathbf{T}_\alpha \cdot \mathbf{T}_\beta$? And why is
the correction from Part 3 not allowed for polarized parts such as diodes?

Structure your code with IPO comments (input, processing, output).
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# Input
feeder = np.array([[0.62, -0.06], [0.78, -0.06], [0.78, 0.06], [0.62, 0.06]])
board = np.array([[0.25, 0.25], [0.50, 0.25], [0.50, 0.45], [0.25, 0.45]])
placement_sites = np.array([[0.30, 0.35], [0.40, 0.40], [0.45, 0.30]])

# angles from Chapter 5.4 and target angle of the part in degrees, row = site
placement_plan = np.array([
    [9, 99, 0],
    [14, 74, 90],
    [1, 79, 45],
])

def robot_position_with_gripper_axis(alpha, beta, gamma):
    """Arm points and part corners with a rotating gripper, angles in radians."""
    T_alpha = transformation_matrix(alpha, 0, 0)
    T_beta = rotation_about_point(beta, arm[1])
    # the gripper axis rotates about the gripper's location in the home position
    T_gamma = rotation_about_point(gamma, arm[2])
    arm1_new = transform(T_alpha, arm[0:2])
    arm2_new = transform(T_alpha @ T_beta, arm[1:3])
    arm_new = np.array([arm1_new[0], arm1_new[1], arm2_new[1]])
    # T_gamma is on the right because it rotates about the gripper's home position
    part_new = transform(T_alpha @ T_beta @ T_gamma, part)
    return arm_new, part_new

# Processing part 1: test the function
alpha = np.deg2rad(30)
beta = np.deg2rad(60)
arm_without, part_without = robot_position(alpha, beta)
arm_0, part_0 = robot_position_with_gripper_axis(alpha, beta, 0)
arm_90, part_90 = robot_position_with_gripper_axis(alpha, beta, np.deg2rad(90))
center_90 = (part_90[0] + part_90[2]) / 2

print('Part 1')
print('gamma = 0 same as robot_position:', np.allclose(arm_0, arm_without)
      and np.allclose(part_0, part_without))
print('gamma = 90°, center at the gripper:', np.allclose(center_90, arm_90[2]))

# Processing parts 2 and 3: gamma for each site, check the range of the axis
print('Parts 2 and 3')
arms = []
parts = []
for k in range(len(placement_plan)):
    alpha_deg = placement_plan[k, 0]
    beta_deg = placement_plan[k, 1]
    target_deg = placement_plan[k, 2]
    gamma_deg = target_deg - (alpha_deg + beta_deg)
    print(f'P{k + 1}: γ = {gamma_deg}°')
    if gamma_deg < -90 or gamma_deg > 90:
        # a rectangle looks the same after a half turn
        gamma_deg = gamma_deg + 180
        print(f'    outside ±90°, corrected to γ = {gamma_deg}°')

    arm_new, part_new = robot_position_with_gripper_axis(
        np.deg2rad(alpha_deg), np.deg2rad(beta_deg), np.deg2rad(gamma_deg))
    arms.append(arm_new)
    parts.append(part_new)

    # compare the long edge with the target direction
    edge = part_new[1] - part_new[0]
    edge_target = 0.08 * np.array([np.cos(np.deg2rad(target_deg)),
                                   np.sin(np.deg2rad(target_deg))])
    print(f'    Edge in target direction: {np.allclose(edge, edge_target)}, '
          f'in opposite direction: {np.allclose(edge, -edge_target)}')

# Output part 3
plot_robot(arms, parts=parts, targets=placement_sites,
           surroundings=[feeder, board], labels=['P1', 'P2', 'P3'],
           title='Placing parts with a rotating gripper')
```
Output:

```text
Part 1
gamma = 0 same as robot_position: True
gamma = 90°, center at the gripper: True
Parts 2 and 3
P1: γ = -108°
    outside ±90°, corrected to γ = 72°
    Edge in target direction: False, in opposite direction: True
P2: γ = 2°
    Edge in target direction: True, in opposite direction: False
P3: γ = -35°
    Edge in target direction: True, in opposite direction: False
```

With $\gamma = 0$, the robot behaves as before, and for every $\gamma$ the
center of the part stays at the gripper. The gripper axis therefore changes
only the orientation, not the position. The part is now rotated by
$\alpha + \beta + \gamma$. For the target angle, we therefore need
$\gamma = \varphi_\text{target} - (\alpha + \beta)$. For $P_1$, this gives
$-108°$, and the axis cannot rotate that far. With $\gamma = 72°$, the part is
rotated a further $180°$. The edge then points in the opposite direction, but
the rectangle covers the same area. In the plot, all three parts lie on the
circuit board in the orientation from the placement plan: lengthwise,
crosswise and at $45°$. Their positions, however, deviate from the placement
sites by $3.2$ to $3.7\,\text{mm}$, as in Chapter 5.4, because the angles
$\alpha$ and $\beta$ come from the $1°$ grid. The gripper axis does not change
that; it only rotates the part about its center. The two-stage search from
Exercise 5.8 gives more accurate angles.

**Closing question:** $\mathbf{T}_\gamma$ rotates about the point
$(0.7, 0)$, where the gripper is only in the home position. The matrix must
therefore act while arm 1 and arm 2 are still in the home position, i.e. on
the far right of the chain. In the same way, $\mathbf{T}_\beta$ rotates about
the position of joint 2 in the home position and is to the right of
$\mathbf{T}_\alpha$. With
$\mathbf{T}_\gamma \cdot \mathbf{T}_\alpha \cdot \mathbf{T}_\beta$, the arm
would first move into its position, and only then would the part be rotated
about $(0.7, 0)$. But the gripper is no longer there, and the part would be
pulled away from the gripper, just as arm 2 came off with the swapped order in
Chapter 5.3.

For polarized parts such as diodes or electrolytic capacitors, the two ends
are not interchangeable. A half turn swaps plus and minus, and the part would
be mounted the wrong way around. The system would then have to supply the
part in the feeder already rotated by $180°$, for example, or use a gripper
axis with a larger range of rotation. If joint 2 were also allowed to bend
clockwise, the mirrored arm position from the closing question of
Chapter 5.4 would work as well. There, $\alpha + \beta \approx -10°$, and for
$P_1$, $\gamma \approx 10°$ is enough.
````
