---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 5.4 Populating a Circuit Board

In Chapter 5.3 we used the two joint angles of the SCARA robot to compute
where the gripper and the part are. In this project we turn the question
around: which joint angles bring a part to a given spot on the circuit board?
Work through the parts in pairs if possible, and in order, since each part
builds on the previous one.

## Project: Populating a circuit board (✩✩)

The SCARA robot from Chapters 5.1 and 5.3 populates a circuit board with
parts. It picks up each part from a feeder in the home position
$\alpha = \beta = 0$ and puts it down at a placement site. The part is
centered under the gripper. Joint 1 rotates between $0°$ and $180°$. Joint 2
may only bend counterclockwise, i.e. between $0°$ and $150°$.

| Object | Position and size |
| --- | --- |
| Joint 1 | at the origin $(0, 0)$ |
| Arm 1 and arm 2 | $l_1 = 0.4\,\text{m}$ and $l_2 = 0.3\,\text{m}$ long |
| Part | $8\,\text{cm} \times 4\,\text{cm}$, lengthwise along the arm in the home position |
| Feeder | $x$ from $0.62\,\text{m}$ to $0.78\,\text{m}$, $y$ from $-0.06\,\text{m}$ to $0.06\,\text{m}$ |
| Circuit board | $x$ from $0.25\,\text{m}$ to $0.50\,\text{m}$, $y$ from $0.25\,\text{m}$ to $0.45\,\text{m}$ |
| Placement sites | $P_1 = (0.30, 0.35)$, $P_2 = (0.40, 0.40)$, $P_3 = (0.45, 0.30)$ |

First run the following two cells. The first contains the given plotting
function from Chapter 5.1. The second contains the imports, the three
functions `transformation_matrix`, `transform` and `rotation_about_point`
from Chapter 5.3 and the data from the table.

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

# corners of the feeder and the circuit board in m
feeder = np.array([[0.62, -0.06], [0.78, -0.06], [0.78, 0.06], [0.62, 0.06]])
board = np.array([[0.25, 0.25], [0.50, 0.25], [0.50, 0.45], [0.25, 0.45]])

# placement sites P1, P2, P3 in m, row = [x, y]
placement_sites = np.array([
    [0.30, 0.35],
    [0.40, 0.40],
    [0.45, 0.30],
])

plot_robot(arm, parts=part, targets=placement_sites,
           surroundings=[feeder, board], title='Assembly cell in the home position')
```

## Part 1: Compute the position of the robot

Write a function `robot_position(alpha, beta)` that, for the joint angles
$\alpha$ and $\beta$ in radians, returns the points of the arm as an array of
shape `(3, 2)` and the corners of the part as an array of shape `(4, 2)`.
Proceed as in Chapter 5.3: transform arm 1 with $\mathbf{T}_\alpha$, and
arm 2 and the part with $\mathbf{T}_\alpha \cdot \mathbf{T}_\beta$. A
function can return more than one result. `return arm_new, part_new` returns
both arrays, and `arm_new, part_new = robot_position(alpha, beta)` unpacks
them.

Test your function with the position $\alpha = 30°$, $\beta = 60°$ from
Chapter 5.3. The gripper should be at $(0.346, 0.500)$. Then plot the home
position and the positions $(30°, 60°)$ and $(60°, 90°)$ together with the
feeder and the circuit board.

Computing the position of the robot from the joint angles is called
**forward kinematics**. Why is it unique, i.e. why does each pair of angles
correspond to exactly one position?

```{code-cell} python
# code cell
```

## Part 2: Find the angles for a placement site

The controller knows only the placement site $P_1 = (0.30, 0.35)$ and has to
find the joint angles itself. Reversing forward kinematics in this way is
called **inverse kinematics**. As in Chapter 5.2, we solve it by trial and
error, but now for two angles.

Use two nested loops to go through all $\alpha$ from $0°$ to $180°$ and all
$\beta$ from $0°$ to $150°$ in steps of $1°$. For each pair of angles,
compute the position of the gripper with `robot_position` and its distance to
$P_1$ with the Pythagorean theorem. Use an `if` statement to keep track of
the smallest distance so far and the corresponding angles. Start with
`best_distance = 10.0`, i.e. a value larger than any possible distance.

Which angles does the search find, and how far from $P_1$ is the gripper at
these angles? Plot the resulting position with $P_1$ as the target.

```{code-cell} python
# code cell
```

## Part 3: Move to all placement sites

Wrap the search from Part 2 in a function `search_angles(target)` that
returns the best angles in degrees and the remaining distance. Use it in a
loop to determine the angles for all three placement sites. For each site,
print the angles, the remaining distance and the angle $\alpha + \beta$ by
which the part is rotated relative to the home position. Plot the three
positions with their parts in a single plot.

```{code-cell} python
# code cell
```

## Closing question

1. We allowed only angles between $0°$ and $150°$ for joint 2. Is there a
   second position that also brings the gripper to $P_1$? What does it look
   like, and why does the controller commit to one of the two?
2. Why is the robot, with its two joints, unable to set the position and the
   orientation of the part independently of each other?

## Bonus exercise: Does the gripper move in a straight line? (✩✩✩)

The controller moves the gripper from the feeder to $P_1$ by rotating both
joints simultaneously and uniformly. To model this, use `np.linspace` to
create 21 values each for $\alpha$ from $0°$ to $9°$ and for $\beta$ from
$0°$ to $99°$. For each pair of values, compute the position of the gripper
with `robot_position` and store it in an array `path` of shape `(21, 2)`.
Add the path to the plot with the parameter `path` of `plot_robot`.

Compare the length of the path with the length of the straight line between
its start and end points. Compute the path length as in Part 4 of
Chapter 5.2. Why does the gripper not move in a straight line?

```{code-cell} python
# code cell
```
