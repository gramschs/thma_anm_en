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

````{admonition} Project: Populating a circuit board (✩✩)
:class: tip
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
````

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

```{admonition} Part 1: Compute the position of the robot
:class: tip
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
```

```{code-cell} python
# code cell
```

````{admonition} Hint Part 1
:class: tip
:class: dropdown
The body of the function is almost complete in the last section of
Chapter 5.3. Replace the fixed angles there with `alpha` and `beta`. Collect
the positions in lists as in Part 1 of Chapter 5.2.
```python
def robot_position(alpha, beta):
    """Arm points and part corners for the joint angles in radians."""
    T_alpha = transformation_matrix(alpha, 0, 0)
    T_arm2 = T_alpha @ ___
    # arm 1 only with T_alpha, arm 2 and the part with both rotations
    arm1_new = transform(T_alpha, arm[0:2])
    arm2_new = ___
    arm_new = np.array([arm1_new[0], arm1_new[1], arm2_new[1]])
    part_new = ___
    return arm_new, part_new

# test with the position from Chapter 5.3
arm_test, part_test = robot_position(___, ___)
print('Gripper at (30°, 60°) in m:', np.round(arm_test[2], 4))

# collect and plot three positions
arms = []
parts = []
for angle_pair in [[0, 0], [30, 60], [60, 90]]:
    arm_new, part_new = robot_position(np.deg2rad(angle_pair[0]), ___)
    arms.append(arm_new)
    parts.append(___)

plot_robot(arms, parts=parts, surroundings=[feeder, board],
           labels=['Home position', '(30°, 60°)', '(60°, 90°)'],
           title='Three positions of the SCARA robot')
```
````

````{admonition} Solution Part 1
:class: tip
:class: dropdown
```python
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

# test with the position from Chapter 5.3
arm_test, part_test = robot_position(np.deg2rad(30), np.deg2rad(60))
print('Gripper at (30°, 60°) in m:', np.round(arm_test[2], 4))

# collect and plot three positions
arms = []
parts = []
for angle_pair in [[0, 0], [30, 60], [60, 90]]:
    arm_new, part_new = robot_position(np.deg2rad(angle_pair[0]), np.deg2rad(angle_pair[1]))
    arms.append(arm_new)
    parts.append(part_new)
    print(f'α = {angle_pair[0]:2d}°, β = {angle_pair[1]:2d}°: '
          f'gripper at {np.round(arm_new[2], 4)} m')

plot_robot(arms, parts=parts, surroundings=[feeder, board],
           labels=['Home position', '(30°, 60°)', '(60°, 90°)'],
           title='Three positions of the SCARA robot')
```
Output:

```text
Gripper at (30°, 60°) in m: [0.3464 0.5   ]
α =  0°, β =  0°: gripper at [0.7 0. ] m
α = 30°, β = 60°: gripper at [0.3464 0.5   ] m
α = 60°, β = 90°: gripper at [-0.0598  0.4964] m
```
For $(30°, 60°)$, the function returns the same gripper position as in
Chapter 5.3. At $(60°, 90°)$, the gripper is just to the left of the
$y$-axis, far away from the circuit board. Forward kinematics is unique
because every step of the calculation is unique: the angles yield exactly one
matrix $\mathbf{T}_\alpha$ and exactly one matrix $\mathbf{T}_\beta$, and
their product maps each point to exactly one location.
````

```{admonition} Part 2: Find the angles for a placement site
:class: tip
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
```

```{code-cell} python
# code cell
```

````{admonition} Hint Part 2
:class: tip
:class: dropdown
The outer loop runs over $\alpha$, the inner loop over $\beta$. Compute the
distance as in Part 2 of Chapter 5.2. The only new thing is that we do not
store all distances but use `if` to keep track of the best value so far.
`robot_position` expects the angles in radians.
```python
target = placement_sites[0]

# initial value larger than any possible distance
best_distance = 10.0
for alpha_deg in np.linspace(0, 180, 181):
    for beta_deg in np.linspace(0, 150, ___):
        arm_new, part_new = robot_position(___, ___)
        difference = arm_new[2] - target
        distance = ___
        # remember the smallest distance and the corresponding angles
        if ___:
            best_distance = distance
            best_alpha = alpha_deg
            best_beta = beta_deg

print(f'Angles found: α = {best_alpha:.0f}°, β = {best_beta:.0f}°')
print(f'Remaining distance to P1: {best_distance * 1000:.1f} mm')

arm_p1, part_p1 = robot_position(np.deg2rad(best_alpha), np.deg2rad(best_beta))
plot_robot(arm_p1, parts=part_p1, targets=target,
           surroundings=[feeder, board], title='Position for P1')
```
````

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
target = placement_sites[0]

# initial value larger than any possible distance
best_distance = 10.0
for alpha_deg in np.linspace(0, 180, 181):
    for beta_deg in np.linspace(0, 150, 151):
        arm_new, part_new = robot_position(np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
        difference = arm_new[2] - target
        distance = np.sqrt(difference[0]**2 + difference[1]**2)
        # remember the smallest distance and the corresponding angles
        if distance < best_distance:
            best_distance = distance
            best_alpha = alpha_deg
            best_beta = beta_deg

print(f'Angles found: α = {best_alpha:.0f}°, β = {best_beta:.0f}°')
print(f'Remaining distance to P1: {best_distance * 1000:.1f} mm')

arm_p1, part_p1 = robot_position(np.deg2rad(best_alpha), np.deg2rad(best_beta))
plot_robot(arm_p1, parts=part_p1, targets=target,
           surroundings=[feeder, board], title='Position for P1')
```
Output:

```text
Angles found: α = 9°, β = 99°
Remaining distance to P1: 3.2 mm
```
At $\alpha = 9°$ and $\beta = 99°$, the gripper misses $P_1$ by
$3.2\,\text{mm}$. Unlike the center of the box in Chapter 5.2, however, the
gripper can reach $P_1$ exactly: with the exact angles $\alpha \approx 9.4°$
and $\beta \approx 99.0°$, it would hit the point with no remaining distance.
Here, the remaining $3.2\,\text{mm}$ is therefore purely a discretization
error of the $1°$ grid. For a placement robot, this is far too inaccurate,
because parts have to be placed to within a fraction of a millimeter. A grid
ten times finer would help, but it would take much longer. We have already
computed $181 \cdot 151 = 27\,331$ positions. With steps of $0.1°$, there
would be $1801 \cdot 1501$, i.e. about 2.7 million positions, a hundred times
as many.

Grid search is just the simplest way to solve the inverse kinematics
numerically. For an arm with two joints, the angles can even be computed
exactly, using the law of cosines in the triangle formed by arm 1, arm 2 and
the line from the origin to the target. For more complex robots, such
formulas do not always exist. In Chapter 8 we will learn about gradient
descent, a numerical method that heads straight for the minimum instead of
trying out all combinations.
````

```{admonition} Part 3: Move to all placement sites
:class: tip
Wrap the search from Part 2 in a function `search_angles(target)` that
returns the best angles in degrees and the remaining distance. Use it in a
loop to determine the angles for all three placement sites. For each site,
print the angles, the remaining distance and the angle $\alpha + \beta$ by
which the part is rotated relative to the home position. Plot the three
positions with their parts in a single plot.
```

```{code-cell} python
# code cell
```

````{admonition} Hint Part 3
:class: tip
:class: dropdown
The body of `search_angles` is the nested loop from Part 2. The target
becomes the parameter, and instead of printing, `return` gives back the three
results. The loop over the placement sites works like the loop over the angle
pairs in Part 1.
```python
def search_angles(target):
    """Joint angles in degrees that bring the gripper closest to target."""
    best_distance = 10.0
    # insert the nested loop from Part 2 here
    ___
    return best_alpha, best_beta, best_distance

arms = []
parts = []
for k in range(len(placement_sites)):
    alpha_deg, beta_deg, distance = search_angles(___)
    arm_new, part_new = robot_position(np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
    arms.append(arm_new)
    parts.append(part_new)
    print(f'P{k + 1}: α = {alpha_deg:3.0f}°, β = {beta_deg:3.0f}°, '
          f'remaining {distance * 1000:.1f} mm, part rotated by {___:.0f}°')

plot_robot(arms, parts=parts, targets=placement_sites,
           surroundings=[feeder, board], labels=['P1', 'P2', 'P3'],
           title='All placement sites')
```
````

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
def search_angles(target):
    """Joint angles in degrees that bring the gripper closest to target."""
    best_distance = 10.0
    for alpha_deg in np.linspace(0, 180, 181):
        for beta_deg in np.linspace(0, 150, 151):
            arm_new, part_new = robot_position(np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
            difference = arm_new[2] - target
            distance = np.sqrt(difference[0]**2 + difference[1]**2)
            if distance < best_distance:
                best_distance = distance
                best_alpha = alpha_deg
                best_beta = beta_deg
    return best_alpha, best_beta, best_distance

arms = []
parts = []
for k in range(len(placement_sites)):
    alpha_deg, beta_deg, distance = search_angles(placement_sites[k])
    arm_new, part_new = robot_position(np.deg2rad(alpha_deg), np.deg2rad(beta_deg))
    arms.append(arm_new)
    parts.append(part_new)
    print(f'P{k + 1}: α = {alpha_deg:3.0f}°, β = {beta_deg:3.0f}°, '
          f'remaining {distance * 1000:.1f} mm, part rotated by {alpha_deg + beta_deg:.0f}°')

plot_robot(arms, parts=parts, targets=placement_sites,
           surroundings=[feeder, board], labels=['P1', 'P2', 'P3'],
           title='All placement sites')
```
Output:

```text
P1: α =   9°, β =  99°, remaining 3.2 mm, part rotated by 108°
P2: α =  14°, β =  74°, remaining 3.7 mm, part rotated by 88°
P3: α =   1°, β =  79°, remaining 3.2 mm, part rotated by 80°
```
All three parts land close to their placement sites and miss them by $3.2$ to
$3.7\,\text{mm}$. As in Part 2, this is a discretization error of the grid,
and it is too large for placing parts. In addition, the parts lie on the
circuit board at different angles. Our robot has no rotary axis
at the gripper, so the part is rigidly attached to arm 2. Its long axis
therefore always points in the direction of arm 2. Arm 1 is rotated by
$\alpha$ relative to the $x$-axis, and arm 2 bends by a further $\beta$. The
part is thus always rotated by $\alpha + \beta$. The angles that the
controller chooses therefore determine not only the position but also the
orientation of the part.
````

```{admonition} Closing question
:class: tip
1. We allowed only angles between $0°$ and $150°$ for joint 2. Is there a
   second position that also brings the gripper to $P_1$? What does it look
   like, and why does the controller commit to one of the two?
2. Why is the robot, with its two joints, unable to set the position and the
   orientation of the part independently of each other?
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
1. Yes. Joint 1, joint 2 and the gripper form a triangle with side lengths
   $0.4\,\text{m}$, $0.3\,\text{m}$ and $0.461\,\text{m}$. The third side is
   the distance from $P_1$ to the origin. This triangle can be mirrored
   across the line from the origin to $P_1$. In the mirrored position,
   joint 2 bends clockwise, at roughly $\alpha = 89°$ and $\beta = -99°$. If
   the controller allowed both signs of $\beta$, the search might find one
   position or the other, depending on the grid. The arm might then swing all
   the way over between two neighboring sites. That is why the controller of a
   SCARA robot works with one fixed arm configuration.
2. The part is always rotated by $\alpha + \beta$. The placement site already
   determines $\alpha$ and $\beta$, apart from the mirrored solution, and with
   them the orientation. A part in the plane, however, has three degrees of
   freedom: the two coordinates and the angle of rotation. To set all three
   independently, the robot needs a third rotary axis. Many SCARA robots have
   it directly at the gripper, where it rotates the part about its own
   center. With `rotation_about_point` from Chapter 5.3, we could add this
   rotation to the chain as a homogeneous matrix as well.
````

```{admonition} Bonus exercise: Does the gripper move in a straight line? (✩✩✩)
:class: tip
The controller moves the gripper from the feeder to $P_1$ by rotating both
joints simultaneously and uniformly. To model this, use `np.linspace` to
create 21 values each for $\alpha$ from $0°$ to $9°$ and for $\beta$ from
$0°$ to $99°$. For each pair of values, compute the position of the gripper
with `robot_position` and store it in an array `path` of shape `(21, 2)`.
Add the path to the plot with the parameter `path` of `plot_robot`.

Compare the length of the path with the length of the straight line between
its start and end points. Compute the path length as in Part 4 of
Chapter 5.2. Why does the gripper not move in a straight line?
```

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
```python
# rotate both joints uniformly from the home position to the angles for P1
alphas = np.linspace(0, 9, 21)
betas = np.linspace(0, 99, 21)

path = np.zeros((21, 2))
for k in range(21):
    arm_new, part_new = robot_position(np.deg2rad(alphas[k]), np.deg2rad(betas[k]))
    path[k] = arm_new[2]

# path length as in Chapter 5.2: add up the straight-line distances between the path points
length = 0.0
for k in range(len(path) - 1):
    difference = path[k + 1] - path[k]
    length += np.sqrt(difference[0]**2 + difference[1]**2)

# straight line between the start and end points of the path
difference = path[-1] - path[0]
straight = np.sqrt(difference[0]**2 + difference[1]**2)
print(f'Path of the gripper: {length:.3f} m')
print(f'Straight line:       {straight:.3f} m')

arm_start, part_start = robot_position(0, 0)
arm_end, part_end = robot_position(np.deg2rad(9), np.deg2rad(99))
plot_robot([arm_start, arm_end], parts=[part_start, part_end],
           targets=placement_sites[0], path=path, surroundings=[feeder, board],
           labels=['Pick', 'Place'], title='Path of the gripper')
```
Output:

```text
Path of the gripper: 0.603 m
Straight line:       0.528 m
```
The gripper travels $0.603\,\text{m}$, while the straight line is only
$0.528\,\text{m}$ long. The detour is therefore about 14%. We end the
straight line at the end point of the path, not at $P_1$, because the grid
puts this end point $3.2\,\text{mm}$ away from $P_1$. This way we compare two
paths between the same points, and the grid error does not affect the
detour.

The controller rotates the joints uniformly but does not move the gripper in
a straight line. Because $\beta$ changes eleven times as fast as $\alpha$, it
is mainly arm 2 that rotates about joint 2, and the gripper traces an arc
around this joint. In robotics, this kind of motion is called a **PTP
motion**, short for *point-to-point*. It is simple because the controller
only needs to know the angles at the start and at the target. If the gripper
has to move in a straight line, for example when inserting a part into a
hole, the controller must solve the inverse kinematics for many points along
the line. In Chapter 6 we will investigate how to move a body along a given
path.
````
