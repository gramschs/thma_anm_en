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

## Exercise 6.1 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 6.2 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 6.3 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 6.4 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 6.5 (✩✩)

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

```{code-cell} python
# code cell
```

## Exercise 6.6 (✩✩)

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

```{code-cell} python
# code cell
```
