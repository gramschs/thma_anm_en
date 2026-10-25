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

````{admonition} Project: Swivel arm at a conveyor belt (✩✩)
:class: tip
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
````

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

```{admonition} Part 1: Plot the arm in several swivel positions
:class: tip
Rotate the arm and the lid by $45°$, $90°$ and $135°$. Collect the arms in a
list `arms` and the lids in a list `lids`, each starting with the home
position. Inside a loop, `append()` from Chapter 1.3 adds an element to the
end of a list. Plot all four positions with

`plot_robot(arms, parts=lids, surroundings=[conveyor, box], labels=[...])`.

Estimate from the plot: at roughly which angle is the gripper over the
center of the box?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 1
:class: tip
:class: dropdown
```python
# home position as the first element, then append three rotated positions
arms = [arm]
lids = [lid]
for angle in [45, 90, 135]:
    R = rotation_matrix(np.deg2rad(angle))
    arms.append((R @ arm.T).T)
    lids.append((R @ lid.T).T)
    print(f'{angle:3d}°: gripper at {np.round(arms[-1][1], 4)} m')

plot_robot(arms, parts=lids, surroundings=[conveyor, box],
           labels=['0°', '45°', '90°', '135°'],
           title='Swivel arm in four positions')
```
The gripper moves on a circle of radius $0.6\,\text{m}$ via
$(0.424, 0.424)$ and $(0, 0.6)$ to $(-0.424, 0.424)$. At $135°$ it is already
over the box, but still about $5\,\text{cm}$ from the center, offset toward
the upper right corner. A little further counterclockwise, it gets closer to
the center. The placement angle is therefore slightly more than $135°$. The lid
rotates along with the arm: at $90°$, its long edge is parallel to the
$y$-axis.
````

```{admonition} Part 2: Compute the placement angle
:class: tip
Instead of estimating, we try out all angles. Use `np.linspace` to create the
angles from $0°$ to $180°$ in steps of $1°$. In a loop, compute the gripper
position for each angle and, with the Pythagorean theorem, its distance to the
center of the box. Store the distances in an array `distances` that you
create beforehand with `np.zeros`.

`np.argmin` works like `np.argmax` from Chapter 2.4 but returns the index of
the smallest value. Use it to determine the placement angle. How far from the
center of the box is the gripper at that angle? Plot the arm in the place
position with the center of the box as the target.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
# swivel angles from 0 to 180 degrees in steps of 1 degree
angles_deg = np.linspace(0, 180, 181)
distances = np.zeros(len(angles_deg))

for k in range(len(angles_deg)):
    gripper = rotation_matrix(np.deg2rad(angles_deg[k])) @ arm[1]
    difference = gripper - box_center
    distances[k] = np.sqrt(difference[0]**2 + difference[1]**2)

# the index of the smallest distance gives the placement angle
k_best = np.argmin(distances)
place_angle = angles_deg[k_best]
print(f'Placement angle: {place_angle:.0f}°')
print(f'Remaining distance to the box center: {distances[k_best] * 1000:.1f} mm')

R_place = rotation_matrix(np.deg2rad(place_angle))
arm_place = (R_place @ arm.T).T
plot_robot(arm_place, targets=box_center, surroundings=[conveyor, box],
           title=f'Place position at {place_angle:.0f}°')
```
Output:

```text
Placement angle: 140°
Remaining distance to the box center: 4.3 mm
```
At $140°$, the gripper is at $(-0.460, 0.386)$, $4.3\,\text{mm}$ from the
center of the box. This remaining distance has two different causes that we
need to distinguish:

* **Error due to the grid:** $140°$ is only the best angle on the $1°$ grid,
  not the exact best angle. A very fine grid gives $139.7°$, where the
  remaining distance is $3.1\,\text{mm}$. The grid therefore costs a little
  over $1\,\text{mm}$, and with smaller steps this part can be made
  arbitrarily small. An error that arises only because we try a finite
  number of angles instead of all of them is called a **discretization
  error**.
* **Geometric mismatch:** The center of the box is $0.603\,\text{m}$ from
  the joint, but the gripper moves on a circle of radius $0.6\,\text{m}$. The
  gripper cannot reach the center of the box. Even at the exact best angle,
  $3.1\,\text{mm}$ therefore remains, and no grid, however fine, changes
  that.

For the packaging line, a remaining distance of $4.3\,\text{mm}$ is not
critical, because the lid only has to fit into the box. We check this in
Part 3.
````

```{admonition} Part 3: Does the lid fit in the box?
:class: tip
Rotate the lid by the placement angle and store the result in `lid_place`.
Then check whether all four corners lie inside the box. `lid_place[:, 0]`
returns column 0, i.e. the $x$-coordinates of all corners, and
`lid_place[:, 1]` the $y$-coordinates. Compare the smallest and largest
coordinates of the lid with those of the box.

What is the smallest gap between the lid and the walls of the box? Plot the
pick position and the place position with the lid in one plot.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
# lid in the place position
lid_place = (R_place @ lid.T).T

# smallest and largest coordinates of the lid
x_min = np.min(lid_place[:, 0])
x_max = np.max(lid_place[:, 0])
y_min = np.min(lid_place[:, 1])
y_max = np.max(lid_place[:, 1])

# smallest and largest coordinates of the box
box_x_min = np.min(box[:, 0])
box_x_max = np.max(box[:, 0])
box_y_min = np.min(box[:, 1])
box_y_max = np.max(box[:, 1])

fits = (x_min >= box_x_min and x_max <= box_x_max
        and y_min >= box_y_min and y_max <= box_y_max)
print('Lid lies completely inside the box:', fits)

# gaps to the four walls of the box: left, right, bottom, top
gaps = np.array([x_min - box_x_min, box_x_max - x_max,
                 y_min - box_y_min, box_y_max - y_max])
print(f'Smallest gap to a wall: {np.min(gaps) * 100:.1f} cm')

plot_robot([arm, arm_place], parts=[lid, lid_place],
           surroundings=[conveyor, box], labels=['Pick', 'Place'],
           title='Lid in the box')
```
Output:

```text
Lid lies completely inside the box: True
Smallest gap to a wall: 2.1 cm
```
The lid fits into the box, with $2.1\,\text{cm}$ of space left at the bottom
wall. Comparing the smallest and largest coordinates is enough here because
the walls of the box are parallel to the axes. Notice the orientation of the
lid: it has rotated by $140°$ along with the arm and lies at an angle in the
box.
````

```{admonition} Part 4: How long is the gripper's path?
:class: tip
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
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 4
:class: tip
:class: dropdown
```python
def gripper_path(num_points):
    """Gripper positions while swiveling from 0 degrees to the placement angle."""
    angles = np.linspace(0, place_angle, num_points)
    path = np.zeros((num_points, 2))
    for k in range(num_points):
        path[k] = rotation_matrix(np.deg2rad(angles[k])) @ arm[1]
    return path

def path_length(path):
    """Sum of the straight-line distances between consecutive points."""
    length = 0.0
    for k in range(len(path) - 1):
        difference = path[k + 1] - path[k]
        length += np.sqrt(difference[0]**2 + difference[1]**2)
    return length

# exact arc length: radius times angle in radians
arc_length = 0.6 * np.deg2rad(place_angle)
print(f'Exact circular arc: {arc_length:.5f} m')

for num in [8, 29, 141]:
    length = path_length(gripper_path(num))
    print(f'{num:3d} points: {length:.5f} m, error {(arc_length - length) * 1000:.2f} mm')

plot_robot([arm, arm_place], parts=[lid, lid_place],
           path=gripper_path(8), surroundings=[conveyor, box],
           labels=['Pick', 'Place'], title='Gripper path with 8 points')
```
Output:

```text
Exact circular arc: 1.46608 m
  8 points: 1.45864 m, error 7.43 mm
 29 points: 1.46561 m, error 0.47 mm
141 points: 1.46606 m, error 0.02 mm
```
The gripper travels just under $1.47\,\text{m}$. Each straight segment is a
chord of the circle and therefore shorter than the corresponding arc, so the
sum is always slightly too small. With smaller angle steps, the approximation
improves quickly: if the step size is divided by four, from $20°$ to $5°$,
the error drops from $7.43\,\text{mm}$ to $0.47\,\text{mm}$, i.e. to about
one sixteenth. The error decreases with the square of the step size. We will
look at this order of the error more closely in later chapters on numerical
differentiation and integration.
````

```{admonition} Closing question
:class: tip
1. The center of the box is $0.603\,\text{m}$ from the joint. What would
   happen if the box were closer to the base, for example with its center at
   $(-0.30, 0.30)$?
2. The lid lies at an angle in the box. For stacking, its long edge should be
   parallel to the $x$-axis. Why is the swivel arm unable to do this, and
   what additional motion would it need?
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
1. The arm has only one joint. The gripper therefore always moves on a circle
   of radius $0.6\,\text{m}$ around the joint, and its position is determined
   by the angle $\alpha$ alone. A box center at $(-0.30, 0.30)$ is only
   $0.424\,\text{m}$ from the joint. The gripper would never get closer to it
   than $0.6\,\text{m} - 0.424\,\text{m} = 0.176\,\text{m}$ and would miss
   the box. To reach points in a whole area, the arm needs a second joint at
   the end of the first arm, like the SCARA robot from Chapter 5.1.
2. The orientation of the lid is rigidly coupled to the swivel angle: when the
   arm swivels by $140°$, the lid also rotates by $140°$. To place it
   straight, the lid would also have to be rotated about its own center;
   because of its symmetry, $40°$ is enough. Real packaging lines have a
   rotating gripper for this. Our rotation matrix, however, rotates only about
   the origin. A rotation about another point is made up of a rotation and
   translations. In Chapter 5.3 we will learn how to describe both in a
   single matrix.
````

```{admonition} Bonus exercise: Stop at the inspection camera (✩✩✩)
:class: tip
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
```

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
```python
R_1 = rotation_matrix(np.deg2rad(60))   # from the belt to the camera
R_2 = rotation_matrix(np.deg2rad(80))   # from the camera to the box

# task 1: gripper at the camera
gripper_camera = R_1 @ arm[1]
print('Gripper at the camera in m:', np.round(gripper_camera, 4))

# task 2: both rotations combined
R_total = R_2 @ R_1
print('R_2 R_1 equals R(140°):', np.allclose(R_total, rotation_matrix(np.deg2rad(140))))

# task 3: order swapped
print('R_1 R_2 equals R_2 R_1:', np.allclose(R_1 @ R_2, R_2 @ R_1))
```
Output:

```text
Gripper at the camera in m: [0.3    0.5196]
R_2 R_1 equals R(140°): True
R_1 R_2 equals R_2 R_1: True
```
At the camera, the gripper is at $(0.300, 0.520)$. Two consecutive rotations
combine into a single rotation by the sum of the angles,
$60° + 80° = 140°$. Both rotations are about the same point, the joint.
Since the order of the terms does not matter in a sum,
$\mathbf{R}_1 \cdot \mathbf{R}_2 = \mathbf{R}_2 \cdot \mathbf{R}_1$ as well.
This is a special property of rotations about the same point in the plane. In
general, matrix multiplication is not commutative. In Chapter 5.3,
translations come into play, and then the order does matter.
````
