---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 5.2 Swivel Arm at a Conveyor Belt

In Chapter 5.1 we used the rotation matrix to compute where the arm of a SCARA
robot ends up after a rotation. In this chapter we apply it to a packaging
line in which a swivel arm with only one joint does the work. Work through the
parts in pairs if possible, and in order, since each part builds on the
previous one.

## Project: Swivel arm at a conveyor belt (✩✩)

On a packaging line, housing lids arrive on a conveyor belt. A swivel arm
picks up each lid from the belt and places it in a box. The arm has a single
rotary joint at the origin and is $L = 0.6\,\text{m}$ long from the joint to
the gripper. In the home position $\alpha = 0$, it points along the
$x$-axis, and the gripper is over the lid on the belt. The arm can swivel
counterclockwise from $0°$ to $180°$.

```{figure} pics/chap05_schwenkarm_EN.svg
:alt: Top view of a swivel arm with its joint at the origin; in the home position it is over a lid on a conveyor belt, and it swivels by the angle alpha along a dashed circular path to a box
:align: center

The swivel arm from above: it picks up the lid from the conveyor belt and
swivels it along a circular path into the box.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

| Object | Position and size |
| --- | --- |
| Joint | at the origin $(0, 0)$ |
| Gripper in the home position | at $(0.6, 0)$ |
| Lid | $10\,\text{cm} \times 6\,\text{cm}$, centered under the gripper, long edge along the arm |
| Conveyor belt | $20\,\text{cm}$ wide, from $x = 0.5\,\text{m}$ to $x = 0.7\,\text{m}$ |
| Box | inside dimensions $16\,\text{cm} \times 16\,\text{cm}$, center at $(-0.46, 0.39)$, edges parallel to the axes |

First run the following two cells. The first contains the given plotting
function from Chapter 5.1. Two of its parameters were not needed there:
`surroundings` draws areas such as the conveyor belt and the box, and `path`
draws a sequence of gripper positions. The second cell contains the imports,
the function `rotation_matrix` from Chapter 5.1 and the points from the
table.

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

# swivel arm in the home position in m, row = [x, y]
arm = np.array([
    [0.0, 0.0],   # joint
    [0.6, 0.0],   # gripper
])

# corners of the lid under the gripper in m
lid = np.array([
    [0.55, -0.03],
    [0.65, -0.03],
    [0.65,  0.03],
    [0.55,  0.03],
])

# corners of the conveyor belt and the box (inside dimensions) in m
conveyor = np.array([[0.5, -0.8], [0.7, -0.8], [0.7, 0.8], [0.5, 0.8]])
box = np.array([[-0.54, 0.31], [-0.38, 0.31], [-0.38, 0.47], [-0.54, 0.47]])
box_center = np.array([-0.46, 0.39])

plot_robot(arm, parts=lid, targets=box_center,
           surroundings=[conveyor, box], title='Swivel arm in the home position')
```

## Part 1: Plot the arm in several swivel positions

Rotate the arm and the lid by $45°$, $90°$ and $135°$. Collect the arms in a
list `arms` and the lids in a list `lids`, each starting with the home
position. Inside a loop, `append()` from Chapter 1.3 adds an element to the
end of a list. Plot all four positions with

`plot_robot(arms, parts=lids, surroundings=[conveyor, box], labels=[...])`.

Estimate from the plot: at roughly which angle is the gripper over the
center of the box?

```{code-cell} python
# code cell
```

## Part 2: Compute the placement angle

Instead of estimating, we try out all angles. Use `np.linspace` to create the
angles from $0°$ to $180°$ in steps of $1°$. In a loop, compute the gripper
position for each angle and, with the Pythagorean theorem, its distance to the
center of the box. Store the distances in an array `distances` that you
create beforehand with `np.zeros`.

`np.argmin` works like `np.argmax` from Chapter 2.4 but returns the index of
the smallest value. Use it to determine the placement angle. How far from the
center of the box is the gripper at that angle? Plot the arm in the place
position with the center of the box as the target.

```{code-cell} python
# code cell
```

## Part 3: Does the lid fit in the box?

Rotate the lid by the placement angle and store the result in `lid_place`.
Then check whether all four corners lie inside the box. `lid_place[:, 0]`
returns column 0, i.e. the $x$-coordinates of all corners, and
`lid_place[:, 1]` the $y$-coordinates. Compare the smallest and largest
coordinates of the lid with those of the box.

What is the smallest gap between the lid and the walls of the box? Plot the
pick position and the place position with the lid in one plot.

```{code-cell} python
# code cell
```

## Part 4: How long is the gripper's path?

For the cycle time of the line, we need the length of the path that the
gripper travels from the belt to the box. We approximate the circular arc
with straight segments. To do this, write two functions:

1. `gripper_path(num_points)` uses `np.linspace` to create evenly spaced
   angles from $0°$ to the placement angle and returns the gripper positions as
   an array of shape `(num_points, 2)`.
2. `path_length(path)` adds up the straight-line distances between
   consecutive points of the path, each computed with the Pythagorean
   theorem.

Compute the path length for 8, 29 and 141 points, i.e. for angle steps of
$20°$, $5°$ and $1°$. Compare with the exact length of the circular arc
$L \cdot \alpha$, where the angle $\alpha$ must be in radians. Add the path
with 8 points to the plot using the parameter `path`.

Why is the path made of straight segments always shorter than the circular
arc?

```{code-cell} python
# code cell
```

## Closing question

1. The center of the box is $0.603\,\text{m}$ from the joint. What would
   happen if the box were closer to the base, for example with its center at
   $(-0.30, 0.30)$?
2. The lid lies at an angle in the box. For stacking, its long edge should be
   parallel to the $x$-axis. Why is the swivel arm unable to do this, and
   what additional motion would it need?

## Bonus exercise: Stop at the inspection camera (✩✩✩)

On its way to the box, the arm stops at $60°$, where a camera inspects the
lid. The swivel motion then consists of two rotations: first
$\mathbf{R}_1 = \mathbf{R}(60°)$ from the belt to the camera, then
$\mathbf{R}_2 = \mathbf{R}(80°)$ from the camera to the box. If
$\mathbf{R}_1$ is applied first and then $\mathbf{R}_2$, we have
$\mathbf{R}_2 \cdot (\mathbf{R}_1 \cdot \vec{p}) = (\mathbf{R}_2 \cdot \mathbf{R}_1) \cdot \vec{p}$.
The rotation applied first therefore appears on the right.

1. Compute the gripper position at the camera.
2. Compute the product $\mathbf{R}_2 \cdot \mathbf{R}_1$ and use
   `np.allclose` to compare it with $\mathbf{R}(140°)$.
3. Swap the order to $\mathbf{R}_1 \cdot \mathbf{R}_2$. Does the result
   change?
4. Explain without code why the order does not matter here.

```{code-cell} python
# code cell
```
