---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 6.4 Turning into an Aisle

In Chapter 6.3 we plotted the AGV along a path. Now it turns into an aisle
between racks, and we check whether the curve leaves enough clearance to the
racks. Work through the parts in pairs if possible, and in order.

## Project: Does the AGV clear the rack corner? (✩✩)

The AGV is supposed to fetch a box from the aisle between rack 2 and rack 3.
It drives to the right in the main aisle and turns left into the aisle on a
quarter circle with a radius of $2\,\text{m}$. There must always be at least
$0.1\,\text{m}$ of clearance between the AGV and the racks. The critical
point is the **rack corner** $E$ that the AGV drives around.

```{figure} pics/chap06_regalgang_EN.svg
:alt: Top view of the main aisle and the aisle between rack 2 and rack 3, the AGV in the main aisle and the dashed path that goes straight and then turns left into the 1.4 m wide aisle on a quarter circle with radius 2 m around the center M, plus the rack corner E at the lower right corner of rack 2
:align: center

Main aisle and aisle with the planned path, the center $M$ of the quarter
circle and the rack corner $E$.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

| Object | Position and size |
| --- | --- |
| AGV | $1.2\,\text{m} \times 0.8\,\text{m}$ |
| Racks | $y$ from $2.4\,\text{m}$ to $7.5\,\text{m}$, rack 2 at $x$ from $3.0$ to $4.3\,\text{m}$, rack 3 at $x$ from $5.7$ to $7.0\,\text{m}$ |
| Aisle | $1.4\,\text{m}$ wide, center at $x = 5.0\,\text{m}$ |
| Path | straight line at $y = 1.2\,\text{m}$, quarter circle around $M = (3, 3.2)$ with $R = 2\,\text{m}$, straight line at $x = 5\,\text{m}$ up to $y = 6.2\,\text{m}$ |
| Rack corner $E$ | $(4.3, 2.4)$ |
| Safety clearance | $0.1\,\text{m}$ |

First run the following two cells: the plotting function from Chapter 6.1
and a cell with the functions and the outline from Chapters 5.3 and 6.1, the
four racks, the rack corner and the path. The cell assembles the path from
three pieces and computes the points of the quarter circle with polar
coordinates around the center.

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

# warehouse map: four racks in warehouse coordinates in m
rack_1 = np.array([[0.3, 2.4], [1.6, 2.4], [1.6, 7.5], [0.3, 7.5]])
rack_2 = np.array([[3.0, 2.4], [4.3, 2.4], [4.3, 7.5], [3.0, 7.5]])
rack_3 = np.array([[5.7, 2.4], [7.0, 2.4], [7.0, 7.5], [5.7, 7.5]])
rack_4 = np.array([[8.4, 2.4], [9.7, 2.4], [9.7, 7.5], [8.4, 7.5]])
warehouse = [rack_1, rack_2, rack_3, rack_4]

# rack corner: lower right corner of rack 2, as an array of shape (1, 2)
corner = np.array([[4.3, 2.4]])

# path into the aisle: path points in warehouse coordinates in m, row = [x, y]
# center of the quarter circle: the curve starts in the main aisle at y = 1.2 m
# and ends in the middle of the aisle at x = 5 m, so for radius = 2 at (3.0, 3.2)
radius = 2.0
center_x = 5.0 - radius
center_y = 1.2 + radius
path_points = []
# piece 1: straight line in the main aisle at y = 1.2 m
for x_W in np.linspace(1.0, center_x - 0.5, 4):
    path_points.append([x_W, 1.2])
# piece 2: quarter circle around (center_x, center_y), one point every 10 degrees
for angle in np.deg2rad(np.linspace(-90, 0, 10)):
    x_W = center_x + radius * np.cos(angle)
    y_W = center_y + radius * np.sin(angle)
    path_points.append([x_W, y_W])
# piece 3: straight line in the aisle at x = 5 m
for y_W in np.linspace(center_y + 0.5, 6.2, 6):
    path_points.append([5.0, y_W])
path = np.array(path_points)
print('Number of path points:', len(path))

# AGV at the start of the path, yaw angle 0
outline_start = transform(transformation_matrix(0, 1.0, 1.2), outline)
plot_warehouse(outline_start, path=path, targets=path[-1], surroundings=warehouse,
               title='Initial situation: path into the aisle')
```

## Part 1: Yaw angle along the path

As in the second section of Chapter 6.3, compute the yaw angle `psi` at
every path point, print it in degrees and plot it against the number of the
path point.

What is the yaw angle of the AGV on the straight lines, and by how many
degrees does it turn from one circle point to the next? Why does it already
point $5°$ to the left at the start of the quarter circle, at path point 4?

```{code-cell} python
# code cell
```

## Part 2: The AGV along the path

As in the third section of Chapter 6.3, plot the outline at every path
point, collected in a list `vehicles`, with `limits=(2, 7, 0, 4.5)`.

Where does the AGV come closest to a rack? How much space is left on the
left and right when it drives in the middle of the aisle?

```{code-cell} python
# code cell
```

## Part 3: Distance to the rack corner

We calculate the gap in the vehicle coordinate system, as we did for the
protective field check in Chapter 6.2. There, the AGV is the same
axis-aligned rectangle at every path point, and its left side is always at
$y_V = 0.4$. The rack is oblique there, but only the corner $E$ matters for
the gap:

```{figure} pics/chap06_regalecke_fahrzeug_EN.svg
:alt: The AGV as an axis-aligned rectangle in the vehicle coordinate system, above it on the left the rack corner E of an oblique rack, in between the gap y_V - 0.4 to the left side of the vehicle at y_V = 0.4, below it the range -0.6 to 0.6 in the x_V-direction
:align: center

The rack corner in the vehicle coordinate system.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

For every path point, use $\mathbf{T}_{WV}^{-1}$ as in Chapter 6.1 to
convert the corner to vehicle coordinates. If it lies to the left of the
AGV, i.e. at $-0.6 \leq x_V \leq 0.6$ and $y_V \geq 0$, then $y_V - 0.4$ is
the gap. A negative gap would mean that the corner sticks into the AGV.
Collect the gaps and the numbers of the path points in two lists.

How small does the gap get at the checked path points, and at which path
point? Does the curve keep the safety clearance of $0.1\,\text{m}$ there?
Plot the AGV at this path point with `limits=(3.5, 6, 1, 3.5)`.

```{code-cell} python
# code cell
```

## Closing question

1. In the aisle, $0.3\,\text{m}$ remain free on each side. Why does the gap
   become so much smaller in the curve? Compare the $y$-coordinate of $M$
   with where the racks begin.
2. Should the fleet manager increase or decrease the radius? What speaks in
   favor of a large radius?

## Bonus exercise: Dead reckoning in the curve (✩✩✩)

How does the AGV's controller know its pose while driving? Our AGV has a
**differential drive**: its two drive wheels on the left and right are
driven independently, and the controller counts the revolutions of each
wheel. From these counts, it computes after each segment of travel how far
the AGV has moved and by how much it has turned, from the vehicle's own
point of view. This method is called **dead reckoning**.

On the quarter circle, the wheel measurement reports the same segment nine
times: a circular arc with radius $R = 2\,\text{m}$ on which the AGV turns by
$\Delta\psi = 10°$. In the vehicle coordinate system before the segment, the
center of the circle is at $(0, R)$. The AGV therefore ends up at
$(R \sin\Delta\psi,\ R\,(1 - \cos\Delta\psi))$ and is rotated by
$\Delta\psi$. Like the position of the scanner in Chapter 6.2, this
describes a new vehicle coordinate system relative to the old one:
`T_step = transformation_matrix(dpsi, radius * np.sin(dpsi), radius * (1 - np.cos(dpsi)))`.
The controller therefore gets the new pose the same way as
$\mathbf{T}_{WS}$ in Chapter 6.2, by multiplying from the right:

$$\mathbf{T}_{WV,\text{new}} = \mathbf{T}_{WV,\text{old}} \cdot \mathbf{T}_{\text{step}}.$$

1. Start with the pose $(3, 1.2, 0°)$ at the start of the quarter circle and
   apply the segment nine times in a loop. Use `np.allclose` to check
   whether the computed matrix matches the pose $(5, 3.2, 90°)$ at the end
   of the quarter circle.
2. One drive wheel slips a little in the curve. We simplify the slip as
   follows: the controller still assumes a circular arc with
   $R = 2\,\text{m}$ for each segment, but computes $\Delta\psi = 10.2°$
   instead of $10°$. This makes both the computed yaw angle and the computed
   path of each segment wrong. Real slip would also change the computed
   radius. Repeat the calculation with the reported value. Then append the
   straight line in the aisle as a single segment of $3\,\text{m}$,
   `transformation_matrix(0, 3, 0)`, to both the computed and the true pose.
   How far apart are the computed and the true end positions? What yaw angle
   does the controller compute? `np.arctan2` gives you the yaw angle from
   the first column of the matrix, because it contains the direction of the
   $x_V$-axis.
3. Answer without code: on the straight line, the wheel measurement is
   correct. Why does the distance between the computed and the true position
   still keep growing there? What can the controller do about it?

```{code-cell} python
# code cell
```
