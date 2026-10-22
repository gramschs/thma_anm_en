---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 5.3 Homogeneous Coordinates for a Robot Arm

In Chapter 5.1 we kept joint 2 of the SCARA robot straight, so the gripper
could only reach points on a circle of radius $0.7\,\text{m}$, just like the
swivel arm from Chapter 5.2. To place a part anywhere on the circuit board,
joint 2 has to rotate as well. *Where is the gripper when joint 1 rotates by
30° and joint 2 by 60°?*

The rotation matrix alone cannot answer this question, because it rotates
only about the origin. Joint 2, however, sits at the end of arm 1. In this
chapter we build a rotation about another point from shifts and a rotation
about the origin. Then we append a third coordinate with the value 1 to every
point. With these **homogeneous coordinates** we combine rotation and
translation in a single matrix and compute the position of the whole arm.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can build a rotation about any point from shifting, rotating and
  shifting back.
* [ ] You can convert points to **homogeneous coordinates** and build a
  **homogeneous transformation matrix** from a rotation and a translation.
* [ ] You can chain several transformations by matrix multiplication and know
  why the order matters.
```

## How does joint 2 rotate?

We reuse the arm, the part and the function `rotation_matrix` from
Chapter 5.1. First run the following two cells: the first contains the given
plotting function, the second the function and the data from Chapter 5.1.

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

# points of the straight arm in the home position in m, row = [x, y]
arm = np.array([
    [0.0, 0.0],   # joint 1: axis of rotation at the base
    [0.4, 0.0],   # joint 2: end of arm 1
    [0.7, 0.0],   # gripper: end of arm 2
])

# corners of the part in the gripper in m, home position, row = [x, y]
part = np.array([
    [0.66, -0.02],
    [0.74, -0.02],
    [0.74,  0.02],
    [0.66,  0.02],
])
```

For now, we keep joint 1 in the home position, i.e. $\alpha = 0$, and rotate
only joint 2 by $\beta = 90°$. Arm 2 should then point straight up. Joint 2
stays at $(0.4, 0)$, and the gripper should end up $0.3\,\text{m}$ above it at
$(0.4, 0.3)$. First, we try the rotation matrix from Chapter 5.1.

```{code-cell} python
# first attempt: rotate the gripper by 90 degrees with the rotation matrix
R = rotation_matrix(np.deg2rad(90))
print('Gripper after the rotation in m:', np.round(R @ arm[2], 4))
```

The gripper ends up at $(0, 0.7)$ instead of $(0.4, 0.3)$. The rotation
matrix rotates about the origin, and that is where joint 1 is. So we rotated
the gripper as if joint 1 had rotated. *How do we rotate about joint 2
instead?* We shift the arm so that joint 2 lies at the origin. Then the
rotation matrix rotates about the right point. Afterward, we shift everything
back:

1. Shift: we subtract the position of joint 2 from every point.
2. Rotate: we multiply by the rotation matrix.
3. Shift back: we add the position of joint 2 again.

```{code-cell} python
joint2 = arm[1]

# step 1: shift so that joint 2 lies at the origin
gripper_shifted = arm[2] - joint2
# step 2: rotate about the origin, where joint 2 now lies
gripper_rotated = R @ gripper_shifted
# step 3: shift back
gripper_new = gripper_rotated + joint2

print('After step 1:', np.round(gripper_shifted, 4))
print('After step 2:', np.round(gripper_rotated, 4))
print('After step 3:', np.round(gripper_new, 4))
```

After step 1, the gripper is at $(0.3, 0)$, i.e. $0.3\,\text{m}$ to the right
of the shifted joint 2. Step 2 rotates it to $(0, 0.3)$, and step 3 moves it
to the correct position $(0.4, 0.3)$.

We treat the part the same way. If we subtract a vector with two entries from
an array of shape `(4, 2)`, NumPy subtracts it from every row. This way we
shift all four corners at once. Joint 1 and joint 2 do not move during this
rotation, so we copy them unchanged into the new arm.

```{code-cell} python
# rotate all corners of the part about joint 2 in three steps
part_new = (R @ (part - joint2).T).T + joint2

# joint 1 and joint 2 stay in place, only the gripper moves
arm_new = np.array([arm[0], arm[1], gripper_new])

print('Part after the rotation in m:')
print(np.round(part_new, 4))

plot_robot([arm, arm_new], parts=[part, part_new],
           labels=['Home position', 'β = 90°'],
           title='Joint 2 rotates by 90°')
```

Arm 2 is now perpendicular to arm 1. The part has rotated by 90° along with
the gripper, and its long edge extends from $y = 0.26$ to $y = 0.34$. By
shifting, rotating and shifting back, we can therefore rotate about any
point, not just about the origin. This is the approach we promised at the end
of Chapter 5.2 for the tilted lid.

```{admonition} Mini-exercise (✩)
:class: tip
1. Answer without code: where is the gripper if joint 2 rotates by
   $\beta = -90°$ and joint 1 stays in the home position?
2. Use the three steps to rotate the gripper and the part by $\beta = 45°$,
   and plot the home position and the new position with `plot_robot`.
3. Answer without code: what happens at $\beta = 90°$ if we forget step 3?
   Where does the gripper end up, and where would arm 2 be?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# task 2: rotate the gripper and the part by 45 degrees about joint 2
R_45 = rotation_matrix(np.deg2rad(45))
gripper_45 = R_45 @ (arm[2] - joint2) + joint2
part_45 = (R_45 @ (part - joint2).T).T + joint2
arm_45 = np.array([arm[0], arm[1], gripper_45])
print('Gripper at β = 45° in m:', np.round(gripper_45, 4))

plot_robot([arm, arm_45], parts=[part, part_45],
           labels=['Home position', 'β = 45°'],
           title='Joint 2 rotates by 45°')
```
At $\beta = -90°$, arm 2 rotates clockwise and points straight down, and the
gripper is at $(0.4, -0.3)$. At $\beta = 45°$, it is at $(0.612, 0.212)$,
i.e. $0.3\,\text{m} \cdot \cos 45° \approx 0.212\,\text{m}$ to the right of
joint 2 and the same distance above it. Without step 3, the gripper ends up
at $(0, 0.3)$. Arm 2 would be rotated correctly, but with its joint at the
origin. It would then be attached to the base instead of to the end of
arm 1.
````

## Translation as a matrix

Our calculation works, but it mixes two kinds of operations: shifting is an
addition, rotating is a matrix multiplication. Each additional joint adds
three more steps. An industrial robot with six joints would need a long chain
of additions and multiplications. It would be more convenient to write each
step as a matrix and combine all the matrices into a single one. *Can a
translation be written as a 2×2 matrix?*

Unfortunately not. A matrix $\mathbf{M}$ that shifts every point by
$\vec{t} = (t_x, t_y)^\top$ would also have to shift the origin, i.e. satisfy
$\mathbf{M} \cdot \vec{0} = \vec{t}$. However, the product of a matrix and
the zero vector is always the zero vector, because each entry of the product
is a sum of multiples of 0. A 2×2 matrix therefore always leaves the origin
where it is.

The solution is a trick: we append a third coordinate with the value 1 to
every point. $(x, y)$ becomes $(x, y, 1)$. This notation is called
**homogeneous coordinates**. The third coordinate is not a height $z$ in
space but merely a computational device for translations. For points, it
always has the value 1. Now a 3×3 matrix can translate, because the 1 in the
third coordinate adds the translation to the result:

$$\begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix}
\begin{pmatrix} x \\ y \\ 1 \end{pmatrix}
= \begin{pmatrix} 1 \cdot x + 0 \cdot y + t_x \cdot 1 \\
0 \cdot x + 1 \cdot y + t_y \cdot 1 \\
0 \cdot x + 0 \cdot y + 1 \cdot 1 \end{pmatrix}
= \begin{pmatrix} x + t_x \\ y + t_y \\ 1 \end{pmatrix}.$$

If we replace the ones and zeros in the top left with the rotation matrix, we
get the **homogeneous transformation matrix**

$$\mathbf{T} = \begin{pmatrix} \cos\varphi & -\sin\varphi & t_x \\
\sin\varphi & \cos\varphi & t_y \\ 0 & 0 & 1 \end{pmatrix}
= \left(\begin{array}{c|c} \mathbf{R}(\varphi) & \vec{t} \\ \hline
\vec{0}^\top & 1 \end{array}\right).$$

It first rotates a point about the origin and then shifts it by $\vec{t}$.
The last row $(0, 0, 1)$ ensures that the third coordinate keeps the value 1
after the transformation. With $\varphi = 0$, $\mathbf{T}$ is a pure
translation; with $\vec{t} = \vec{0}$, it is a pure rotation. The pure
rotation looks exactly like $\mathbf{R}_z(\varphi)$ from Chapter 5.1. Both
matrices leave the third coordinate unchanged, except that there it is the
height and here it is the 1 of the homogeneous coordinates.

We check this with steps 2 and 3 from the previous section. After step 1, the
gripper is at $(0.3, 0)$. A single matrix now rotates by $90°$ and shifts
back by $(0.4, 0)$:

$$\begin{pmatrix} 0 & -1 & 0.4 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}
\begin{pmatrix} 0.3 \\ 0 \\ 1 \end{pmatrix}
= \begin{pmatrix} 0 \cdot 0.3 + (-1) \cdot 0 + 0.4 \cdot 1 \\
1 \cdot 0.3 + 0 \cdot 0 + 0 \cdot 1 \\
0 \cdot 0.3 + 0 \cdot 0 + 1 \cdot 1 \end{pmatrix}
= \begin{pmatrix} 0.4 \\ 0.3 \\ 1 \end{pmatrix}.$$

If we drop the third coordinate, the gripper is at $(0.4, 0.3)$, as
expected.

```{admonition} Homogeneous coordinates in robotics
:class: note
In 3D space, we append a fourth coordinate 1 to $(x, y, z)$ and work with
4×4 matrices made up of a 3×3 rotation matrix and a translation vector. Robot
controllers describe each joint this way, and the position of the gripper
follows from the product of all the matrices.
```

In Python we write $\mathbf{T}$ as a function
`transformation_matrix(angle, tx, ty)`.

```{code-cell} python
def transformation_matrix(angle, tx, ty):
    """Homogeneous matrix: rotate by angle (radians), then shift by (tx, ty)."""
    return np.array([
        [np.cos(angle), -np.sin(angle), tx],
        [np.sin(angle),  np.cos(angle), ty],
        [0.0,            0.0,           1.0],
    ])

# step 1 as a matrix: pure translation, joint 2 moves to the origin
T_to_origin = transformation_matrix(0, -0.4, 0)
# steps 2 and 3 in one matrix: rotate by 90 degrees, then shift back
T_rot_back = transformation_matrix(np.deg2rad(90), 0.4, 0)

print('T_rot_back:')
print(np.round(T_rot_back, 4))
```

To transform many points at once, we use the ready-made helper function
`transform(T, points)`. It appends the 1 to every point, multiplies as in
Chapter 5.1 with `(T @ points_hom.T).T` and drops the third coordinate again
at the end. The comments explain how it does this step by step.

```{code-cell} python
# Given helper function: just run it, the details are in the comments.
def transform(T, points):
    """Applies the homogeneous matrix T to all points, row = [x, y]."""
    # array of ones: one row per point, three columns
    points_hom = np.ones((len(points), 3))
    # enter x and y into columns 0 and 1 using slicing from Chapter 4.1
    points_hom[:, 0:2] = points
    # transform all points at once as in Chapter 5.1
    result = (T @ points_hom.T).T
    # drop the third coordinate again
    return result[:, 0:2]
```

```{code-cell} python
# apply first T_to_origin, then T_rot_back to the part
part_shifted = transform(T_to_origin, part)
part_new = transform(T_rot_back, part_shifted)
print('Part after the rotation about joint 2 in m:')
print(np.round(part_new, 4))
```

In `T_rot_back`, the rotation matrix $\mathbf{R}(90°)$ is in the top left,
and the translation vector $(0.4, 0)$ is in the right column. The corners of the
part end up in the same places as in the first section. Instead of a
subtraction, a multiplication and an addition, we now need only two matrix
multiplications. The next section shows how to combine these two into one
matrix as well.

```{admonition} Mini-exercise (✩)
:class: tip
1. Answer without code: what does the matrix
   `transformation_matrix(0, 0.1, -0.2)` look like? Where does it move the
   gripper in the home position?
2. Use `transformation_matrix` and `transform` to rotate the whole arm by
   $30°$ about joint 1. Compare with the result from Chapter 5.1.
3. Answer without code: what would happen if the third coordinate of a point
   were 0 instead of 1?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# task 2: pure rotation about joint 1, i.e. without translation
T_30 = transformation_matrix(np.deg2rad(30), 0, 0)
arm_30 = transform(T_30, arm)
print('Arm after the rotation by 30° in m:')
print(np.round(arm_30, 4))
```
With $\varphi = 0$, $\cos 0 = 1$ and $\sin 0 = 0$, so the matrix is

$$\begin{pmatrix} 1 & 0 & 0.1 \\ 0 & 1 & -0.2 \\ 0 & 0 & 1 \end{pmatrix}.$$

It shifts the gripper from $(0.7, 0)$ to $(0.8, -0.2)$. The pure rotation by
$30°$ moves joint 2 to $(0.346, 0.200)$ and the gripper to $(0.606, 0.350)$,
exactly like the rotation matrix in Chapter 5.1. With $\vec{t} = \vec{0}$,
$\mathbf{T}$ therefore contains the rotation matrix unchanged. If the third
coordinate were 0, the right column would be multiplied by 0. The point would
only be rotated, not shifted. For directions, this is exactly what we want:
the direction of arm 2, for example, changes when the arm rotates, but not
when it is shifted. In homogeneous coordinates, points therefore get a 1 and
directions a 0.
````

## Chaining transformations

We transformed the part with two matrices, one after the other. For a point
$\tilde{p} = (x, y, 1)^\top$ in homogeneous coordinates, we may move the
parentheses in the matrix product:

$$\mathbf{T}_2 \cdot (\mathbf{T}_1 \cdot \tilde{p})
= (\mathbf{T}_2 \cdot \mathbf{T}_1) \cdot \tilde{p}.$$

The product $\mathbf{T}_2 \cdot \mathbf{T}_1$ is a single matrix that
performs both steps at once. Combining transformations in this way is called
**composition**. The matrix that acts first is on the right, just as with the
rotations in the bonus exercise of Chapter 5.2. For a rotation about any
point, we chain the three steps in the function `rotation_about_point`.

```{code-cell} python
def rotation_about_point(angle, center):
    """Homogeneous matrix: rotation about the point center, angle in radians."""
    T_to_origin = transformation_matrix(0, -center[0], -center[1])
    T_rot = transformation_matrix(angle, 0, 0)
    T_back = transformation_matrix(0, center[0], center[1])
    # the matrix applied first is on the right
    return T_back @ T_rot @ T_to_origin

# rotation about joint 2 by 90 degrees as a single matrix
T_joint2 = rotation_about_point(np.deg2rad(90), arm[1])
print(np.round(T_joint2, 4))
```

The top left again contains $\mathbf{R}(90°)$, and the right column the
translation $(0.4, -0.4)$. This is not the position of joint 2 but exactly
the translation that brings joint 2 back to its place after the rotation: the
rotation sends $(0.4, 0)$ to $(0, 0.4)$, and $(0, 0.4) + (0.4, -0.4)$ gives
$(0.4, 0)$ again. Every composition of rotations and translations again has
the form of $\mathbf{T}$.

Now both joints rotate. Arm 2 is attached to the end of arm 1. When joint 1
rotates, it carries arm 2 along. Arm 2 therefore follows both rotations,
while arm 1 follows only the rotation of joint 1. So we first bend arm 2
about joint 2 while arm 1 is still in the home position and we know that
joint 2 is at $(0.4, 0)$. Then we rotate everything about joint 1:

* We transform joint 1 and joint 2 with $\mathbf{T}_\alpha$.
* We transform the gripper and the part with
  $\mathbf{T}_\alpha \cdot \mathbf{T}_\beta$.

With the slice `arm[0:2]` we select the rows of joint 1 and joint 2, and with
`arm[1:3]` the rows of joint 2 and the gripper.

```{code-cell} python
# joint 1 rotates by 30 degrees about the origin
T_alpha = transformation_matrix(np.deg2rad(30), 0, 0)
# joint 2 rotates by 60 degrees about where it sits in the home position
T_beta = rotation_about_point(np.deg2rad(60), arm[1])
# arm 2 follows both rotations: first T_beta, then T_alpha
T_arm2 = T_alpha @ T_beta

# arm 1 (joints 1 and 2) only with T_alpha, arm 2 (joint 2 and gripper) with T_arm2
arm1_new = transform(T_alpha, arm[0:2])
arm2_new = transform(T_arm2, arm[1:3])
part_new = transform(T_arm2, part)

print('Arm 1 in m:')
print(np.round(arm1_new, 4))
print('Arm 2 in m:')
print(np.round(arm2_new, 4))

# combine joint 1, joint 2 and the gripper into one arm
arm_new = np.array([arm1_new[0], arm1_new[1], arm2_new[1]])
plot_robot([arm, arm_new], parts=[part, part_new],
           labels=['Home position', 'α = 30°, β = 60°'],
           title='Both joints rotate')
```

This answers the question from the beginning: the gripper is at
$(0.346, 0.500)$. Joint 2 appears in both results and ends up at
$(0.346, 0.200)$ both times. The two arms therefore stay connected, because
$\mathbf{T}_\beta$ leaves joint 2 in place. Arm 2 is rotated by
$30° + 60° = 90°$ relative to the $x$-axis and points straight up.

*Does the order of $\mathbf{T}_\alpha$ and $\mathbf{T}_\beta$ even matter?*
In the bonus exercise of Chapter 5.2, we were allowed to swap two rotations
because both were about the same joint. Here, the matrices rotate about
different points. Let us try it out.

```{code-cell} python
# swapped order: first T_alpha, then T_beta
T_wrong = T_beta @ T_alpha
arm2_wrong = transform(T_wrong, arm[1:3])
part_wrong = transform(T_wrong, part)

print('Arm 2 with swapped order in m:')
print(np.round(arm2_wrong, 4))

plot_robot([arm_new, arm2_wrong], parts=[part_new, part_wrong],
           labels=['correct: T_alpha @ T_beta', 'swapped: T_beta @ T_alpha'],
           title='Order swapped')
```

With the order swapped, arm 2 comes off: its joint ends up at
$(0.200, 0.054)$ instead of $(0.346, 0.200)$. The reason is the center of
rotation of $\mathbf{T}_\beta$. This matrix rotates about the point
$(0.4, 0)$, where joint 2 sits in the home position. After
$\mathbf{T}_\alpha$, however, joint 2 is no longer there, and
$\mathbf{T}_\beta$ rotates about a point where there is no joint at all. The
matrix product is therefore not commutative in general, and when we chain
transformations, we have to pay close attention to the order.

```{admonition} Mini-exercise (✩)
:class: tip
1. Answer without code: where are joint 2 and the gripper at
   $\alpha = 90°$ and $\beta = -90°$?
2. Check your answer with `transformation_matrix`, `rotation_about_point` and
   `transform`, and plot the position.
3. Answer without code: why do we apply
   $\mathbf{T}_\alpha \cdot \mathbf{T}_\beta$ only to arm 2 and the part, and
   not to joint 1?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# task 2: position for alpha = 90 degrees and beta = -90 degrees
T_alpha_90 = transformation_matrix(np.deg2rad(90), 0, 0)
T_arm2_90 = T_alpha_90 @ rotation_about_point(np.deg2rad(-90), arm[1])

arm1_90 = transform(T_alpha_90, arm[0:2])
arm2_90 = transform(T_arm2_90, arm[1:3])
part_90 = transform(T_arm2_90, part)
arm_90 = np.array([arm1_90[0], arm1_90[1], arm2_90[1]])
print(np.round(arm_90, 4))

plot_robot([arm, arm_90], parts=[part, part_90],
           labels=['Home position', 'α = 90°, β = -90°'],
           title='Arm 1 pointing up, arm 2 pointing right')
```
Arm 1 points up, and joint 2 is at $(0, 0.4)$. Arm 2 bends by $90°$
clockwise and points in the $x$-direction again; the gripper is at
$(0.3, 0.4)$. As in the home position, the part is aligned with the
$x$-axis, because in total it is rotated by $90° - 90° = 0°$. As for task 3:
$\mathbf{T}_\beta$ rotates about joint 2. Joint 1 does not lie at this center
of rotation and would be rotated along with the rest, for example to
$(0.346, -0.200)$ at $\alpha = 30°$ and $\beta = 60°$. Joint 1, however, is
firmly mounted in the base. Joint 2 moves only what comes after it, i.e.
arm 2, the gripper and the part.
````

## Summary and outlook

A rotation matrix rotates only about the origin. To rotate about another
point, we shift this point to the origin, rotate there and shift back. A
translation cannot be written as a 2×2 matrix, because every matrix keeps the
origin in place. Homogeneous coordinates solve this problem: with a third
coordinate 1, the homogeneous transformation matrix $\mathbf{T}$ combines
rotation and translation in a 3×3 matrix. We chain several transformations by
matrix multiplication, with the matrix applied first on the right. A rotation
about any point is thus the composition
$\mathbf{T}_\text{back} \cdot \mathbf{T}_\text{rot} \cdot \mathbf{T}_\text{to origin}$.
In the SCARA robot, arm 2 follows every motion of arm 1. We therefore
transform its points with $\mathbf{T}_\alpha \cdot \mathbf{T}_\beta$, and the
points of arm 1 only with $\mathbf{T}_\alpha$. If we swap the order, joint 2
rotates about a point where it no longer is.

So far we have used the joint angles to compute where the gripper is. In the
assembly cell, the opposite question usually arises: a part has to go to a
specific spot on the circuit board. Which angles does the controller have to
set for this? We explore this question in the project in Chapter 5.4.

In this chapter we rotated and shifted all points within one common
coordinate system. In Chapter 6 we will look at a second perspective: there,
each body has its own coordinate system, and we convert points between these
coordinate systems. This is also how most robot controllers describe their
arms.
