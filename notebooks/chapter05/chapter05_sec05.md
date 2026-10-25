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

## Exercise 5.1 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.2 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.3 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.4 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.5 (✩✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.6 (✩✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.7 (✩✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.8 (✩✩)

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

```{code-cell} python
# code cell
```

## Exercise 5.9 (✩✩✩) Mini-project: A rotary axis at the gripper

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

```{code-cell} python
# code cell
```
