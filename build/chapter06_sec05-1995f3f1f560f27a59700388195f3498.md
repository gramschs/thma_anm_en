---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 6.5 Exercises

These exercises are meant for self-study at home and review the material of
Chapters 6.1 to 6.4. Allow about 90 minutes for them. Before starting the
exercises, run the following two cells. They contain the plotting function,
the functions from Chapter 5.3, and the outline, the warehouse map and the
transfer station from Chapter 6.1.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 10 min)
* ✩✩ Application: write your own code and interpret results (approx. 25 min)

```{code-cell} python
:tags: [hide-input]
# Given plotting function: just run it, you do not need to understand it.
def plot_warehouse(vehicles=None, coordinate_systems=None, scan_points=None,
                   scanner=None, protective_field=None, targets=None, path=None,
                   surroundings=None, labels=None, title='',
                   limits=(0, 10, 0, 8)):
    """Plots a section of the warehouse in top view.

    vehicles: corners of a vehicle outline as an array, row = [x, y], the
              first two corners form the front edge, or a list of such
              arrays for several vehicles (optional)
    coordinate_systems: homogeneous 3x3 matrix of a coordinate system or a
              list of such matrices, the x-axis (red) and the y-axis (blue)
              are drawn 0.8 m long (optional)
    scan_points: scan points as an array, row = [x, y], drawn as red dots
                 (optional)
    scanner: position [x, y] of the scanner, draws the laser beams from the
             scanner to the scan points as thin red lines (optional)
    protective_field: corners of a protective field as an array, row = [x, y],
                      filled in yellow with a dashed outline (optional)
    targets: target points as an array, row = [x, y], marked as crosses (optional)
    path: path points as an array, row = [x, y], drawn as a dashed line with
          dots on top of the vehicles (optional)
    surroundings: corners of areas such as racks or pallets as an array or a
                  list of arrays, filled in gray (optional)
    labels: legend entries, one per vehicle; without labels, all vehicles
            are outlined in blue (optional)
    title: plot title
    limits: visible section (x_min, x_max, y_min, y_max) in m
    """
    blue, red, orange, gray = '#005A94', '#E60000', '#E87846', '#484949'
    colors = [blue, red, orange, gray]
    if isinstance(vehicles, np.ndarray):
        vehicles = [vehicles]
    if isinstance(coordinate_systems, np.ndarray):
        coordinate_systems = [coordinate_systems]
    if isinstance(surroundings, np.ndarray):
        surroundings = [surroundings]
    fig, ax = plt.subplots(figsize=(7, 6))

    # surroundings: racks, pallets, pillars
    if surroundings is not None:
        for area in surroundings:
            ax.fill(area[:, 0], area[:, 1], facecolor='#DDDEDE',
                    edgecolor=gray, linewidth=1, zorder=0)

    # protective field filled in yellow with a dashed outline
    if protective_field is not None:
        ax.fill(protective_field[:, 0], protective_field[:, 1],
                facecolor='#FFEC7F', edgecolor=orange, linestyle='--',
                linewidth=1.5, label='Protective field', zorder=1)

    # path as a dashed line with dots, on top of the vehicles
    if path is not None:
        ax.plot(path[:, 0], path[:, 1], color=gray, linestyle='--', linewidth=1,
                marker='o', markersize=3, label='Path', zorder=4)

    # vehicles: outline filled in light blue, front edge (corner 0 to corner 1) orange
    if vehicles is not None:
        for k in range(len(vehicles)):
            color = blue if labels is None else colors[k % len(colors)]
            corners = vehicles[k]
            label = None if labels is None else labels[k]
            ax.fill(corners[:, 0], corners[:, 1], facecolor='#CCDEE9',
                    edgecolor=color, linewidth=2, label=label, zorder=2)
            ax.plot(corners[0:2, 0], corners[0:2, 1], color=orange, linewidth=4,
                    solid_capstyle='butt', zorder=3)

    # coordinate systems: x-axis red, y-axis blue, each 0.8 m long
    if coordinate_systems is not None:
        for T in coordinate_systems:
            origin = T[0:2, 2]
            for column, color, name in [(0, red, 'x'), (1, blue, 'y')]:
                tip = origin + 0.8 * T[0:2, column]
                ax.annotate('', xy=tip, xytext=origin, zorder=4,
                            arrowprops=dict(arrowstyle='-|>', color=color, lw=2))
                label_position = origin + 1.0 * T[0:2, column]
                ax.text(label_position[0], label_position[1], name, color=color,
                        ha='center', va='center', fontsize=11, zorder=4)
            ax.scatter(origin[0], origin[1], s=25, color=gray, zorder=5)

    # scan points as red dots, optionally with laser beams from the scanner
    if scan_points is not None:
        scan_points = np.atleast_2d(scan_points)
        if scanner is not None:
            for point in scan_points:
                ax.plot([scanner[0], point[0]], [scanner[1], point[1]], color=red,
                        linewidth=0.8, alpha=0.6, zorder=4)
        ax.scatter(scan_points[:, 0], scan_points[:, 1], s=25, color=red,
                   zorder=5, label='Scan points')

    # target points as crosses
    if targets is not None:
        targets = np.atleast_2d(targets)
        ax.scatter(targets[:, 0], targets[:, 1], marker='x', s=80, color=gray,
                   linewidth=2, zorder=5, label='Target')

    if (labels is not None or scan_points is not None or targets is not None
            or path is not None or protective_field is not None):
        ax.legend(loc='upper left')
    ax.set_xlim(limits[0], limits[1])
    ax.set_ylim(limits[2], limits[3])
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

# corners of the AGV in the vehicle coordinate system in m, row = [x, y]
outline = np.array([
    [ 0.6, -0.4],   # front right
    [ 0.6,  0.4],   # front left
    [-0.6,  0.4],   # rear left
    [-0.6, -0.4],   # rear right
])

# warehouse map from Chapter 6.1: corners of the rack, the pallet and the
# pillar in m
rack = np.array([[0.5, 6.5], [9.5, 6.5], [9.5, 7.5], [0.5, 7.5]])
pallet = np.array([[5.6, 4.0], [6.8, 4.0], [6.8, 4.8], [5.6, 4.8]])
pillar = np.array([[6.3, 0.3], [6.7, 0.3], [6.7, 0.7], [6.3, 0.7]])
warehouse = [rack, pallet, pillar]

# transfer station from Chapter 6.1 in warehouse coordinates in m
station = np.array([[8.0, 2.5]])
```

````{admonition} Exercise 6.1 (✩)
:class: tip
The fleet manager does not report the pose of an AGV as three numbers but
directly as the matrix $\mathbf{T}_{WV}$. Given the following code:

```python
import numpy as np

T_WV = np.array([
    [ 0.0, 1.0, 6.0],
    [-1.0, 0.0, 3.0],
    [ 0.0, 0.0, 1.0],
])
print(np.rad2deg(np.arctan2(T_WV[1, 0], T_WV[0, 0])))
print(np.linalg.det(T_WV))

# measurement of the scanner at the vehicle center: distance 2 m, angle 90 degrees
r = 2.0
phi = np.deg2rad(90)
scan_point_V = np.array([[r * np.cos(phi), r * np.sin(phi)]])
print(np.round(scan_point_V, 4))
print(np.round(transform(T_WV, scan_point_V), 4))
```

Write down your guess in a Markdown cell before you run the code.

1. Where is the vehicle center, and in which direction of the warehouse does
   the $x_V$-axis point? What yaw angle does the first `print` line output?
2. What does `np.linalg.det(T_WV)` output? Explain your answer.
3. The scanner reports an object at a distance of $2\,\text{m}$ at the angle
   $\varphi = 90°$. Where is it in the vehicle coordinate system? In which
   direction of the warehouse does the $y_V$-axis point, and where is the
   object in the warehouse?
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

T_WV = np.array([
    [ 0.0, 1.0, 6.0],
    [-1.0, 0.0, 3.0],
    [ 0.0, 0.0, 1.0],
])
print(np.rad2deg(np.arctan2(T_WV[1, 0], T_WV[0, 0])))
print(np.linalg.det(T_WV))

r = 2.0
phi = np.deg2rad(90)
scan_point_V = np.array([[r * np.cos(phi), r * np.sin(phi)]])
print(np.round(scan_point_V, 4))
print(np.round(transform(T_WV, scan_point_V), 4))
```
Output:

```text
-90.0
1.0
[[0. 2.]]
[[8. 3.]]
```

The third column of $\mathbf{T}_{WV}$ is the position of the vehicle center,
i.e. $(6, 3)$. The first column contains the direction of the $x_V$-axis in
warehouse coordinates, here $(0, -1)$. So the AGV points in the negative
$y_W$-direction, toward the warehouse wall. As in Chapter 6.3, `np.arctan2`
receives first the $y$- and then the $x$-component of this direction and
returns $\psi = -90°$. The determinant is 1, as for every homogeneous
transformation matrix that only rotates and shifts.

In the vehicle coordinate system, the object is at $(0, 2)$, i.e.
$2\,\text{m}$ to the left of the vehicle center. `np.round` removes the tiny
remainder of $\cos 90° \approx 6 \cdot 10^{-17}$. The second column $(1, 0)$
shows that the $y_V$-axis points in the $x_W$-direction: if you face the
negative $y_W$-direction, the positive $x_W$-direction is on your left. The
object is therefore $2\,\text{m}$ further in the $x_W$-direction than the
vehicle center, at $(8, 3)$.
````

````{admonition} Exercise 6.2 (✩)
:class: tip
The AGV is at $(4, 2)$ and points in the $y_W$-direction with $\psi = 90°$.
In Chapter 6.1 we computed the conversion from warehouse to vehicle
coordinates with `np.linalg.inv`. The following code contains three
attempts to build the inverse matrix from a rotation and a translation
without `np.linalg.inv`:

```python
import numpy as np

T_WV = transformation_matrix(np.deg2rad(90), 4, 2)
T_VW = np.linalg.inv(T_WV)

T_a = transformation_matrix(np.deg2rad(-90), -4, -2)
T_b = transformation_matrix(0, -4, -2) @ transformation_matrix(np.deg2rad(-90), 0, 0)
T_c = transformation_matrix(np.deg2rad(-90), 0, 0) @ transformation_matrix(0, -4, -2)

print(np.allclose(T_a, T_VW))
print(np.allclose(T_b, T_VW))
print(np.allclose(T_c, T_VW))
print(np.round(T_VW, 4))
```

Write down your guess in a Markdown cell before you run the code.

1. In `T_b`, which acts first, the rotation or the translation? And in
   `T_c`? Two of the three attempts give the same matrix. Which ones?
2. Which attempt equals `T_VW`? Explain your answer using the order in which
   $\mathbf{T}_{WV}$ rotates and shifts.
3. The right column of `T_VW` contains the point to which `T_VW` moves the
   point $(0, 0)$. So where is the origin of the warehouse from the vehicle's
   point of view: in front or behind, to the left or to the right, and how
   far in each case?
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

T_WV = transformation_matrix(np.deg2rad(90), 4, 2)
T_VW = np.linalg.inv(T_WV)

T_a = transformation_matrix(np.deg2rad(-90), -4, -2)
T_b = transformation_matrix(0, -4, -2) @ transformation_matrix(np.deg2rad(-90), 0, 0)
T_c = transformation_matrix(np.deg2rad(-90), 0, 0) @ transformation_matrix(0, -4, -2)

print(np.allclose(T_a, T_VW))
print(np.allclose(T_b, T_VW))
print(np.allclose(T_c, T_VW))
print(np.round(T_VW, 4))
```
Output:

```text
False
False
True
[[ 0.  1. -2.]
 [-1.  0.  4.]
 [ 0.  0.  1.]]
```

In a matrix product, the matrix on the right acts first. So `T_b` rotates
first and then shifts, just like `transformation_matrix` itself. That is why
`T_a` and `T_b` are the same matrix, the tempting but wrong inverse from
Chapter 6.1. `T_c` shifts first and then rotates. $\mathbf{T}_{WV}$ rotated
first and shifted last. The inverse has to undo the steps in reverse order:
first the translation, then the rotation. Only `T_c` does this.

The right column of `T_VW` contains $(-2, 4)$. From the vehicle's point of
view, the origin of the warehouse is therefore $2\,\text{m}$ behind and
$4\,\text{m}$ to the left of the vehicle center. This makes sense: the AGV
points in the $y_W$-direction, and the origin is $2\,\text{m}$ lower, i.e.
behind it. For a vehicle pointing in the $y_W$-direction, the negative
$x_W$-direction is to the left, and the origin is $4\,\text{m}$ away in
that direction. The right column is therefore not simply $(-4, -2)$,
because the reverse rotation also rotates the translation vector.
````

````{admonition} Exercise 6.3 (✩)
:class: tip
An AGV also has a scanner at the rear. It sits $0.6\,\text{m}$ behind the
vehicle center and looks backward, so its $x_S$-axis points opposite to the
$x_V$-axis. Given the following code:

```python
import numpy as np

T_WV = transformation_matrix(np.deg2rad(90), 4, 2)
# rear scanner: 0.6 m behind the vehicle center, rotated by 180 degrees
T_VS = transformation_matrix(np.deg2rad(180), -0.6, 0)

# measurement of the rear scanner: distance 1 m, angle 0 degrees
scan_point_S = np.array([[1.0, 0.0]])

print(np.round(transform(T_VS, scan_point_S), 4))
print(np.round(transform(T_WV @ T_VS, scan_point_S), 4))
print(np.round(transform(T_VS @ T_WV, scan_point_S), 4))
print(np.round((T_WV @ T_VS)[0:2, 2], 4))
```

Write down your guess in a Markdown cell before you run the code.

1. Where is the scan point in the vehicle coordinate system? How far is it
   from the rear of the AGV?
2. Which of the two matrix products correctly converts from the scanner to
   the warehouse? Explain your answer using the subscripts. Where is the
   scan point in the warehouse?
3. What does the output of the last line mean?
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

T_WV = transformation_matrix(np.deg2rad(90), 4, 2)
T_VS = transformation_matrix(np.deg2rad(180), -0.6, 0)

scan_point_S = np.array([[1.0, 0.0]])

print(np.round(transform(T_VS, scan_point_S), 4))
print(np.round(transform(T_WV @ T_VS, scan_point_S), 4))
print(np.round(transform(T_VS @ T_WV, scan_point_S), 4))
print(np.round((T_WV @ T_VS)[0:2, 2], 4))
```
Output:

```text
[[-1.6  0. ]]
[[4.  0.4]]
[[-4.6 -3. ]]
[4.  1.4]
```

$\mathbf{T}_{VS}$ first rotates the scan point by $180°$ to $(-1, 0)$ and
then shifts it by $(-0.6, 0)$. So it is at $(-1.6, 0)$, $1.6\,\text{m}$
behind the vehicle center. The rear of the AGV is at $x_V = -0.6\,\text{m}$,
so the object is $1\,\text{m}$ away from the rear, exactly the measured
distance.

$\mathbf{T}_{WV} \cdot \mathbf{T}_{VS}$ is correct. As in Chapter 6.2, the
subscripts interlock like the links of a chain: $\mathbf{T}_{VS}$ converts
from S to V, and $\mathbf{T}_{WV}$ from V to W. The AGV points in the
$y_W$-direction, so behind it is the negative $y_W$-direction, and the scan
point is at $(4, 2 - 1.6) = (4, 0.4)$. In
$\mathbf{T}_{VS} \cdot \mathbf{T}_{WV}$, the inner subscripts S and W do not
match. The product first applies $\mathbf{T}_{WV}$ to the scanner
coordinates as if they were vehicle coordinates, and then $\mathbf{T}_{VS}$
to warehouse coordinates as if they were scanner coordinates. The point
$(-4.6, -3)$ is not even inside the warehouse. The last line prints the
third column of $\mathbf{T}_{WS}$, i.e. the position of the rear scanner in
the warehouse. It is at $(4, 1.4)$, $0.6\,\text{m}$ behind the vehicle
center.
````

````{admonition} Exercise 6.4 (✩)
:class: tip
After the handover, the AGV drives back to the left from the station at
$(8, 2.5)$ on a fairly flat path. As in Chapter 6.3, the following code
computes the yaw angles at the path points and the turns between
neighboring path points:

```python
import numpy as np

path = np.array([[8.0, 2.5], [7.0, 2.7], [6.0, 2.7], [5.0, 2.5]])

psi_deg = np.zeros(len(path))
for k in range(len(path) - 1):
    direction = path[k + 1] - path[k]
    psi_deg[k] = np.rad2deg(np.arctan2(direction[1], direction[0]))
psi_deg[-1] = psi_deg[-2]
print(np.round(psi_deg, 1))

turns = np.zeros(len(path) - 1)
for k in range(len(path) - 1):
    turns[k] = psi_deg[k + 1] - psi_deg[k]
print(np.round(turns, 1))
```

Write down your guess in a Markdown cell before you run the code.

1. In roughly which direction of the warehouse does the AGV point during
   the whole drive? Which values do you expect in `psi_deg`? Keep in mind
   that `np.arctan2` returns angles from $-180°$ to $180°$. Hint: the slope
   $0.2$ corresponds to the angle $11.3°$.
2. Sketch the path. Does the AGV turn left or right from segment to segment,
   and by how many degrees?
3. Which values does the second `print` line output? Does the AGV really
   turn that far between path point 1 and path point 2? How can the value
   be corrected?
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

path = np.array([[8.0, 2.5], [7.0, 2.7], [6.0, 2.7], [5.0, 2.5]])

psi_deg = np.zeros(len(path))
for k in range(len(path) - 1):
    direction = path[k + 1] - path[k]
    psi_deg[k] = np.rad2deg(np.arctan2(direction[1], direction[0]))
psi_deg[-1] = psi_deg[-2]
print(np.round(psi_deg, 1))

turns = np.zeros(len(path) - 1)
for k in range(len(path) - 1):
    turns[k] = psi_deg[k + 1] - psi_deg[k]
print(np.round(turns, 1))
```
Output:

```text
[ 168.7  180.  -168.7 -168.7]
[  11.3 -348.7    0. ]
```

The AGV drives to the left and therefore points roughly in the negative
$x_W$-direction, i.e. at about $180°$. The first segment $(-1, 0.2)$ rises
slightly, which gives $180° - 11.3° = 168.7°$. The second segment runs
exactly to the left, $180°$. The third segment $(-1, -0.2)$ falls slightly.
Its direction is at $180° + 11.3° = 191.3°$. Because `np.arctan2` only
returns values up to $180°$, we get $-168.7°$ instead. Both angles describe
the same direction; they differ by a full turn.

From segment to segment, the AGV turns left by $11.3°$: when you drive to
the left, the negative $y_W$-direction is on your left, and that is where
the path bends. Between path point 1 and 2, however, the calculation
reports $-348.7°$, almost a full turn to the right. The value is off by
$360°$ because the yaw angle jumps from $180°$ to $-168.7°$. If a turn is
below $-180°$, we add $360°$; if it is above $180°$, we subtract $360°$.
Here this gives $-348.7° + 360° = 11.3°$. In Chapters 6.3 and 6.4 the
problem did not occur, because the paths there never led in the negative
$x_W$-direction.
````

```{admonition} Exercise 6.5 (✩✩)
:class: tip
A box is waiting at the transfer station `station`. Three AGVs are currently
available in the warehouse:

| AGV | Pose $(x, y, \psi)$ |
| --- | --- |
| AGV 1 | $(4.0, 2.0, 30°)$ |
| AGV 2 | $(9.0, 5.0, -90°)$ |
| AGV 3 | $(6.5, 3.0, 180°)$ |

The fleet manager sends the AGV that can get to the station fastest. All
three have a **differential drive**: their drive wheels on the left and
right are driven independently. If the wheels turn in opposite directions,
the AGV turns on the spot, provided the chassis and the load allow it. For
its estimate, the fleet manager assumes that each AGV first turns on the
spot toward the station at $45°$ per second and then drives straight to the
station at $1\,\text{m/s}$.

1. Write a function `target_from_vehicle(T_WV, target)` with a docstring. It
   should convert a target from warehouse to vehicle coordinates and also
   return its distance $d$ from the vehicle center and the angle $\varphi$
   in degrees at which the target lies, measured from the $x_V$-axis. $d$
   and $\varphi$ are the polar coordinates from Chapter 6.1, only computed
   in the opposite direction. Hint: use the Pythagorean theorem and
   `np.arctan2`.
2. For each AGV, compute $d$, $\varphi$ and the estimated time. Which AGV
   does the fleet manager send?
3. Plot the three AGVs with the station and the warehouse map.
4. Answer without code: we could also compute the distance $d$ directly in
   warehouse coordinates. Why? We could determine the angle $\varphi$
   without the inverse matrix as the difference of two angles. How, and
   which difficulty from Exercise 6.4 occurs for AGV 3?

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
def target_from_vehicle(T_WV, target):
    """Converts a target from warehouse to vehicle coordinates.

    T_WV: homogeneous matrix of the AGV's pose
    target: target in warehouse coordinates as an array of shape (1, 2)
    Returns: target in vehicle coordinates, distance d in m, angle phi in degrees
    """
    target_V = transform(np.linalg.inv(T_WV), target)[0]
    d = np.sqrt(target_V[0]**2 + target_V[1]**2)
    phi_deg = np.rad2deg(np.arctan2(target_V[1], target_V[0]))
    return target_V, d, phi_deg

# poses of the three AGVs, row = [x in m, y in m, yaw angle in degrees]
poses = np.array([
    [4.0, 2.0,  30],
    [9.0, 5.0, -90],
    [6.5, 3.0, 180],
])
turn_rate = 45.0   # turning on the spot in degrees per second
speed = 1.0        # driving straight ahead in m/s

# Processing: station from the point of view of each AGV and estimated time
vehicles = []
times = np.zeros(len(poses))
for k in range(len(poses)):
    T_WV_k = transformation_matrix(np.deg2rad(poses[k, 2]), poses[k, 0], poses[k, 1])
    vehicles.append(transform(T_WV_k, outline))
    station_V, d, phi_deg = target_from_vehicle(T_WV_k, station)
    times[k] = np.abs(phi_deg) / turn_rate + d / speed
    print(f'AGV {k + 1}: station at {np.round(station_V, 3)} m, d = {d:.2f} m, '
          f'φ = {phi_deg:.1f}°, time {times[k]:.2f} s')

k_best = np.argmin(times)

# Output
print(f'The fleet manager sends AGV {k_best + 1}.')
plot_warehouse(vehicles, targets=station, surroundings=warehouse,
               labels=['AGV 1', 'AGV 2', 'AGV 3'],
               title='Which AGV takes the job?')
```
Output:

```text
AGV 1: station at [ 3.714 -1.567] m, d = 4.03 m, φ = -22.9°, time 4.54 s
AGV 2: station at [ 2.5 -1. ] m, d = 2.69 m, φ = -21.8°, time 3.18 s
AGV 3: station at [-1.5  0.5] m, d = 1.58 m, φ = 161.6°, time 5.17 s
The fleet manager sends AGV 2.
```

AGV 3 is closest to the station, but the station is behind it ($x_V < 0$).
It would have to turn by $161.6°$ and would need $3.6\,\text{s}$ for that
alone. AGV 2 already points almost toward the station, turns only $21.8°$
to the right and gets there after $3.18\,\text{s}$. We know AGV 1 from
Chapter 6.1: for the station at $(3.714, -1.567)$, it turns by a similarly
small amount, but it is the farthest away. The fleet manager sends AGV 2.

Rotations and translations do not change distances, as we saw in
Chapter 5.1. Therefore $d$ is the same in both coordinate systems, for
example for AGV 3: $\sqrt{(8 - 6.5)^2 + (2.5 - 3)^2} = 1.58\,\text{m}$. We
could compute the angle as the direction to the station in the warehouse
minus the yaw angle. For AGV 3, `np.arctan2(-0.5, 1.5)` gives the direction
$-18.4°$, and $-18.4° - 180° = -198.4°$. That is the same direction as
$161.6°$, but outside the range from $-180°$ to $180°$. As in
Exercise 6.4, we would have to add $360°$; otherwise the fleet manager would
calculate with a turn of more than $198°$. In vehicle coordinates, on the
other hand, `np.arctan2` returns the angle directly in the correct range.
````

````{admonition} Exercise 6.6 (✩✩)
:class: tip
In the aisle from Chapter 6.4, the AGV has picked up a box. It is in the
middle of the aisle at $(5.0, 5.0)$ and points deeper into the aisle with
$\psi = 90°$. For the way back, it is supposed to turn on the spot until it
points toward the main aisle with $\psi = 270°$. The two racks to the left
and right of the aisle are:

```python
rack_2 = np.array([[3.0, 2.4], [4.3, 2.4], [4.3, 7.5], [3.0, 7.5]])
rack_3 = np.array([[5.7, 2.4], [7.0, 2.4], [7.0, 7.5], [5.7, 7.5]])
```

1. Compute the outline of the AGV for the yaw angles
   $90°, 100°, \ldots, 270°$ and collect the outlines in a list. For each
   yaw angle, also collect the smallest and the largest $x$-coordinate of
   the four corners in two more lists. Plot all outlines with the two racks
   and `limits=(3.5, 6.5, 3.5, 6.5)`.
2. How far does the AGV extend to the left and to the right at most while
   turning, and at which yaw angle? Does it hit one of the racks?
3. Answer without code: how far is each corner from the vehicle center? How
   wide does an aisle have to be at least so that the AGV can turn around
   in it with $0.1\,\text{m}$ of safety clearance on both sides?
4. Answer without code: in Chapter 6.4 we checked the distance to the rack
   corner in the vehicle coordinate system. Why do we check in warehouse
   coordinates here?

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
rack_2 = np.array([[3.0, 2.4], [4.3, 2.4], [4.3, 7.5], [3.0, 7.5]])
rack_3 = np.array([[5.7, 2.4], [7.0, 2.4], [7.0, 7.5], [5.7, 7.5]])
psi_deg = np.linspace(90, 270, 19)

# Processing: outline for each yaw angle, smallest and largest x of the corners
vehicles = []
x_left = []
x_right = []
for k in range(len(psi_deg)):
    T_WV_k = transformation_matrix(np.deg2rad(psi_deg[k]), 5.0, 5.0)
    corners = transform(T_WV_k, outline)
    vehicles.append(corners)
    x_left.append(np.min(corners[:, 0]))
    x_right.append(np.max(corners[:, 0]))

k_left = np.argmin(x_left)
k_right = np.argmax(x_right)

# Output
print(f'Farthest left:  x = {x_left[k_left]:.3f} m at ψ = {psi_deg[k_left]:.0f}°')
print(f'Farthest right: x = {x_right[k_right]:.3f} m at ψ = {psi_deg[k_right]:.0f}°')
# even touching counts as a collision
print('Hits rack 2:', x_left[k_left] <= 4.3)
print('Hits rack 3:', x_right[k_right] >= 5.7)
plot_warehouse(vehicles, surroundings=[rack_2, rack_3],
               title='Turning around in the aisle', limits=(3.5, 6.5, 3.5, 6.5))
```
Output:

```text
Farthest left:  x = 4.280 m at ψ = 150°
Farthest right: x = 5.720 m at ψ = 150°
Hits rack 2: True
Hits rack 3: True
```

In our list, the AGV extends farthest at $\psi = 150°$, and equally far
again at $\psi = 210°$. However, these are only the extreme values of our
$10°$ grid. Each corner is $\sqrt{0.6^2 + 0.4^2} = 0.721\,\text{m}$ away
from the vehicle center. When the AGV turns on the spot, the corners
therefore sweep a circle with this radius. They reach farthest out when a
diagonal of the AGV is exactly horizontal. The diagonals are inclined by
$33.7°$ to the $x_V$-axis, because $\tan 33.7° = 0.4 / 0.6$. They are
therefore horizontal at $\psi = 180° - 33.7° = 146.3°$ and at
$\psi = 180° + 33.7° = 213.7°$. Then the corners reach exactly to
$x = 5 - 0.721 = 4.279\,\text{m}$ and $x = 5 + 0.721 = 5.721\,\text{m}$. So
the AGV sticks $2.1\,\text{cm}$ into the racks on both sides and cannot
turn around in the aisle. The aisle would have to be at least
$2 \cdot 0.721\,\text{m} = 1.44\,\text{m}$ wide, or $1.64\,\text{m}$ with
the safety clearance. Our aisle is only $1.4\,\text{m}$ wide. The AGV has to
back out of the aisle or leave it at the other end. Even touching counts as
a collision, which is why we compare with `<=` and `>=`.

The sides of the racks are the lines $x = 4.3$ and $x = 5.7$, parallel to
the $y_W$-axis. In warehouse coordinates, comparing the $x$-coordinates is
therefore enough. However, this only holds here because the AGV stays
entirely within the $y$-range of the racks while turning: its corners lie
between $y = 4.28\,\text{m}$ and $y = 5.72\,\text{m}$, and the racks extend
from $y = 2.4\,\text{m}$ to $y = 7.5\,\text{m}$. At the end of a rack, we
would also have to check whether the AGV and the rack overlap in the
$y$-direction. In the vehicle coordinate system, the sides of the racks
would be oblique and different for every yaw angle. In Chapter 6.4 it was
the other way around: the rack corner is a single point, and the sides of
the vehicle are parallel to the axes in the vehicle coordinate system. So we
always check in the coordinate system in which the boundary is parallel to
the axes.
````
