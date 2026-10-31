---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 6.3 Driving Along a Path

In Chapter 6.2 the AGV stopped in front of a box. The **fleet manager**, i.e.
the computer that coordinates all vehicles in the warehouse, now sends it a
**detour path**: a sequence of points that leads between the box and the
pillar to the transfer station. The path points tell the AGV where to go,
but not which way it has to point along the way. *How do we determine the
yaw angle from the path points?*

So far, the pose was always given. Now we compute the yaw angle from the
path and check in the figure whether the AGV gets past the box and the
pillar.

## In which direction does the AGV have to drive?

The detour path consists of nine path points from the vehicle center at
$(4, 2)$ to the transfer station at $(8, 2.5)$. At each path point, the AGV
should point toward the next path point.

First we run two cells: the plotting function from Chapter 6.1, whose
parameter `path` draws path points as a dashed line, and a cell with the
functions and data from Chapters 5.3 and 6.1. The warehouse map now also
contains the box, and the path points are stored row by row in the array
`path`.

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

# warehouse map: rack, pallet, pillar and the box from Chapter 6.2
# in warehouse coordinates in m
rack = np.array([[0.5, 6.5], [9.5, 6.5], [9.5, 7.5], [0.5, 7.5]])
pallet = np.array([[5.6, 4.0], [6.8, 4.0], [6.8, 4.8], [5.6, 4.8]])
pillar = np.array([[6.3, 0.3], [6.7, 0.3], [6.7, 0.7], [6.3, 0.7]])
box = np.array([[5.67, 2.14], [5.97, 2.66], [5.63, 2.86], [5.33, 2.34]])
warehouse = [rack, pallet, pillar, box]

# pose of the AGV as in Chapter 6.2: center at (4, 2) m, yaw angle 30 degrees
T_WV = transformation_matrix(np.deg2rad(30), 4, 2)
outline_W = transform(T_WV, outline)

# transfer station from Chapter 6.1 in warehouse coordinates in m
station = np.array([[8.0, 2.5]])

# detour path from the fleet manager: path points in warehouse coordinates
# in m, row = [x, y]
path = np.array([
    [4.0, 2.0 ],   # start: vehicle center
    [4.5, 1.72],
    [5.0, 1.55],
    [5.5, 1.47],
    [6.0, 1.45],
    [6.5, 1.69],
    [7.0, 2.17],
    [7.5, 2.5 ],
    [8.0, 2.5 ],   # goal: transfer station
])

plot_warehouse(outline_W, coordinate_systems=T_WV, path=path, targets=station,
               surroundings=warehouse,
               title='Initial situation: detour path to the station')
```

The direction to the next path point is the difference vector
`path[1] - path[0]` with the components $\Delta x$ and $\Delta y$. For its
angle $\psi$ measured from the $x_W$-axis, we have

$$\tan\psi = \frac{\Delta y}{\Delta x}.$$

So the obvious choice is the **arctangent** `np.arctan`. `np.rad2deg`, the
counterpart of `np.deg2rad`, converts its result from radians to degrees. We
try it out for the first segment and for the later return trip to the start.

```{code-cell} python
# direction from the first to the second path point
direction = path[1] - path[0]
# TODO: ???   compute the yaw angle with the arctangent of the quotient and store it in psi_out
print('Direction vector to the next path point in m:', direction)
print(f'Yaw angle with np.arctan: {np.rad2deg(psi_out):.1f}°')

# return trip: from the last path point (station) back to the first (start)
direction_back = path[0] - path[-1]
psi_back = np.arctan(direction_back[1] / direction_back[0])
print('Direction vector for the return trip in m:', direction_back)
print(f'Yaw angle with np.arctan: {np.rad2deg(psi_back):.1f}°')
```

For the first segment, $-29.2°$ matches the figure. The return trip, however,
leads to the left, and $7.1°$ points to the right, directly away from the
starting point. *Why does the arctangent get it wrong?*

## Math refresher: arctangent and quadrants

The arctangent only returns angles between $-90°$ and $90°$. The directions
$(4, 0.5)$ and $(-4, -0.5)$ have the same quotient $0.125$ and cannot be told
apart this way. For $\Delta x = 0$, the quotient is not even defined. The
function **arctan2** takes $\Delta y$ and $\Delta x$ separately, determines
the quadrant from their signs and returns angles from $-180°$ to $180°$.

NumPy provides it as `np.arctan2(dy, dx)`. As in the quotient, the
$y$-component comes first.

```{code-cell} python
# yaw angle with np.arctan2(dy, dx): first the y-component, then the x-component
# TODO: ???   compute the yaw angle with the quadrant-aware arctangent and store it in psi_start
psi_back = np.arctan2(direction_back[1], direction_back[0])
print(f'Yaw angle to the next path point: {np.rad2deg(psi_start):.1f}°')
print(f'Yaw angle for the return trip: {np.rad2deg(psi_back):.1f}°')
```

For the first segment, nothing changes, because $\Delta x > 0$ there. For the
return trip, `np.arctan2` now returns $-172.9°$, exactly $180°$ less than the
arctangent, i.e. the opposite direction.

## How does the AGV turn along the path?

Now we repeat the calculation for all segments: at path point `k`, the AGV
should point toward path point `k + 1`. Nine path points have eight
segments, so the loop runs over `range(len(path) - 1)`. As with the scan
points in Chapter 6.1, we collect the yaw angles in an array that we create
beforehand with `np.zeros`. The last path point has no successor and takes
over the second-to-last angle.

```{code-cell} python
# yaw angle at each path point: direction to the next path point
psi = np.zeros(len(path))
for k in range(len(path) - 1):
    # TODO: ???   compute the direction from path point k to k + 1 and store it in direction
    # TODO: ???   compute the yaw angle of this direction and store it in entry k of psi

# the last path point has no successor and keeps the last direction
psi[-1] = psi[-2]

psi_deg = np.rad2deg(psi)
print('Yaw angles in degrees:', np.round(psi_deg, 1))

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(range(len(path)), psi_deg, marker='o')
ax.set_xlabel('Path point k')
ax.set_ylabel('Yaw angle in degrees')
ax.set_title('Yaw angle along the detour path')
ax.grid(True)
plt.show()
```

The AGV starts with $-29.2°$ toward the lower right, first turns left, then
right again, and stands at the station with $0°$, parallel to the warehouse
wall.

`psi[k]` is the direction of the **secant**, i.e. the line segment from path
point `k` to path point `k + 1`. The direction of the path at the point
itself, on the other hand, is given by the **tangent**. At the lowest path
point `k = 4`, the path runs roughly horizontally, but the AGV already
points upward at $25.6°$. The slope $\Delta y / \Delta x$ of the secant is
called the **difference quotient**. In Chapter 7.1 we use it to approximate
derivatives.

## Does the AGV get past the box?

With `path[k]` and `psi[k]`, we know the pose at every path point. As in
Chapter 6.1, we use it to build $\mathbf{T}_{WV}$ and convert the outline to
warehouse coordinates, this time in a loop. As with the distances in Part 3
of Chapter 6.2, we collect the outlines in a list: before the loop, we create
an empty list, and `append` adds each new outline to the end. The parameter
`limits` shows only the section around the path.

```{code-cell} python
# empty list for the outlines at all path points
vehicles = []
for k in range(len(path)):
    # pose at path point k: position from the path, yaw angle from psi
    # TODO: ???   set up the transformation matrix for this pose and store it in T_WV_k
    # convert the outline to warehouse coordinates and append it to the list
    # TODO: ???   convert the outline and append it to vehicles

print('Number of outlines:', len(vehicles))
print('Corners at the lowest path point in m:')
print(np.round(vehicles[4], 3))

plot_warehouse(vehicles, path=path, targets=station, surroundings=warehouse,
               title='Driving along the detour path', limits=(3, 9, 0, 4))
```

Each outline is a snapshot of the AGV at one path point. It gets tight at
the box at path points 2 and 3, and at the pillar at path point 5. The AGV
touches neither of them, but the gaps are only a few tens of centimeters
wide. The figure does not show what happens between the path points, and we
only read off the gaps. We will calculate such gaps in the project in
Chapter 6.4.

## Summary and outlook

We compute the yaw angle between two path points with `np.arctan2(dy, dx)`.
Unlike `np.arctan`, this function determines the quadrant from the signs and
returns angles from $-180°$ to $180°$. In a loop, we get the yaw angle at
every path point, approximated by the direction of the secant. With the
position and the yaw angle, we build $\mathbf{T}_{WV}$ at every path point
and collect the outlines in a list.

In the project in Chapter 6.4, the AGV turns into an aisle on a quarter
circle. We use the inverse matrix from Chapter 6.1 to calculate how close it
comes to a rack corner. We will take a closer look at the difference quotient
in Chapter 7.1.

## Mini-exercises

### Mini-exercise 1

After the handover, the AGV continues from the station at $(8, 2.5)$. Three
possible targets are at $(8, 4.5)$, $(6, 2.5)$ and $(7, 1.5)$.

1. Answer without code: which yaw angle does the AGV need to drive to each
   of the three targets?
2. Check your answers with `np.arctan2` and `np.rad2deg`.
3. Answer without code: for which of the three drives does the arctangent of
   the quotient $\Delta y / \Delta x$ give a wrong angle or no angle at all?
   Explain.

```{code-cell} python
# code cell
```

### Mini-exercise 2

1. Answer without code: why does the array `psi` have nine entries even
   though the loop runs only eight times?
2. In a loop, compute by how many degrees the AGV turns between each pair of
   neighboring path points, i.e. `psi_deg[k + 1] - psi_deg[k]`. Use
   `np.argmax` and `np.argmin` to find the largest turn to the left and the
   largest turn to the right. Between which path points do they occur?
3. Answer without code: how do the turns between neighboring path points
   change if the fleet manager sends the same path with twice as many
   points?

```{code-cell} python
# code cell
```

### Mini-exercise 3

1. Plot only every second path point, but each with its vehicle coordinate
   system. To do this, collect the matrices $\mathbf{T}_{WV}$ in a second
   list and pass it to the parameter `coordinate_systems`. You get every
   second path point with `range(0, len(path), 2)` from Chapter 1.5.
2. Answer without code: path point 3 is $0.69\,\text{m}$ away from the box.
   How wide can the gap between the AGV and the box be there at most? Why?
3. Answer without code: look at the outline at path point 5 in the figure of
   the drive. Which corner of the AGV comes closest to the pillar? Why this
   one?

```{code-cell} python
# code cell
```
