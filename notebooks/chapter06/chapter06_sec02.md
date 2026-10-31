---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 6.2 Safety Scanner and Protective Field

In Chapter 6.1 the scanner sat at the center of the vehicle. Now a second
scanner is added at the front of the vehicle. It makes sure that the AGV
stops in time. Work through the parts in pairs if possible, and in order.

## Project: Does the AGV have to stop? (✩✩)

The AGV from Chapter 6.1 is at $(4, 2)$ with $\psi = 30°$. A **safety
scanner** sits in the middle of its front edge. It has its own **scanner
coordinate system** S, whose axes point in the same directions as those of
the vehicle. As in Chapter 6.1, it measures the distance $r$ and the angle
$\varphi$, now measured from the $x_S$-axis, and it monitors the **protective
field** in front of the vehicle. In our simplified model, the rule is: if a
scan point lies inside the protective field, the AGV has to stop.

```{figure} pics/chap06_schutzfeld_EN.svg
:alt: Top view of the AGV with the vehicle coordinate system V at the vehicle center, the scanner coordinate system S 0.6 m further forward in the middle of the front edge and the yellow protective field, 1.0 m long and 1.0 m wide, in front of the vehicle, plus a beam with distance r and angle phi measured from the x_S-axis
:align: center

Vehicle coordinate system V, scanner coordinate system S and the protective
field of the safety scanner.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

| Object | Position and size |
| --- | --- |
| AGV | $1.2\,\text{m} \times 0.8\,\text{m}$, pose $(4, 2, 30°)$ |
| Safety scanner | at $(0.6, 0)$ in the vehicle coordinate system, not rotated |
| Scan | $-90°$ to $90°$ in steps of $5°$, range $5\,\text{m}$ |
| Protective field | $x_V$ from $0.6\,\text{m}$ to $1.6\,\text{m}$, $y_V$ from $-0.5\,\text{m}$ to $0.5\,\text{m}$ |
| Warehouse wall | at $y = 0$ along the bottom edge of the plot, not on the warehouse map |

First run the following two cells: the plotting function from Chapter 6.1,
whose parameter `protective_field` draws a protective field in yellow, and a
cell with the functions and data from Chapters 5.3 and 6.1, the corners of
the protective field and the scan. Beams that hit nothing within
$5\,\text{m}$ are missing from the scan.

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

# warehouse map: corners of the rack, the pallet and the pillar in warehouse
# coordinates in m
rack = np.array([[0.5, 6.5], [9.5, 6.5], [9.5, 7.5], [0.5, 7.5]])
pallet = np.array([[5.6, 4.0], [6.8, 4.0], [6.8, 4.8], [5.6, 4.8]])
pillar = np.array([[6.3, 0.3], [6.7, 0.3], [6.7, 0.7], [6.3, 0.7]])
warehouse = [rack, pallet, pillar]

# pose of the AGV as in Chapter 6.1: center at (4, 2) m, yaw angle 30 degrees
T_WV = transformation_matrix(np.deg2rad(30), 4, 2)
outline_W = transform(T_WV, outline)

# corners of the protective field in the vehicle coordinate system in m
protective_field = np.array([
    [0.6, -0.5],
    [1.6, -0.5],
    [1.6,  0.5],
    [0.6,  0.5],
])

# scan of the safety scanner: angle measured from the x_S-axis in degrees,
# distance in m
angles_deg = np.array([-90, -85, -80, -75, -70, -65, -60,
                       -35, -30, -25, -20, -15, -10,  -5,
                        10,  15,  20,  25,  30,  35,  40,  45,  50,
                        55,  60,  65,  70,  75,  80,  85,  90])
distances = np.array([2.66, 2.81, 3.00, 2.52, 2.49, 4.01, 4.60,
                      1.04, 0.88, 0.83, 0.89, 0.96, 1.06, 1.18,
                      2.64, 2.40, 2.22, 2.08, 2.16, 2.56, 4.47, 4.35, 4.26,
                      4.22, 4.20, 4.22, 4.26, 4.35, 4.47, 4.63, 4.85])

plot_warehouse(outline_W, coordinate_systems=T_WV, surroundings=warehouse,
               title='Initial situation')
```

## Part 1: The scan from the scanner's point of view

Convert the measurements to Cartesian coordinates as in the second section
of Chapter 6.1. Because the angles are measured from the $x_S$-axis, you get
scanner coordinates `points_S`, one row per measurement. Use `np.argmin` to
find the shortest distance and its angle. Plot the scan with

`plot_warehouse(scan_points=points_S, scanner=[0, 0], limits=(-1, 5, -4.5, 6), title='Scan in scanner coordinates')`.

Is the nearest object to the left or to the right? Does the figure tell you
where it is in the warehouse?

```{code-cell} python
# code cell
```

## Part 2: The scan in the warehouse

Use `transformation_matrix` to build the matrix $\mathbf{T}_{VS}$ that
converts from S to V. Convert the scan points in two steps: with
$\mathbf{T}_{VS}$ into `points_V`, then with $\mathbf{T}_{WV}$ into
`points_W`. As in Chapter 5.3, the two steps can be chained:

$$\mathbf{T}_{WS} = \mathbf{T}_{WV} \cdot \mathbf{T}_{VS}.$$

The subscripts interlock like the links of a chain: from S via V to W. Use
`np.allclose` to check whether `transform(T_WS, points_S)` gives the same
result as the two steps. Plot the vehicle, the scan and the warehouse map.
The position of the scanner is in the third column of $\mathbf{T}_{WS}$.

Which scan points do not match any object on the warehouse map, and where are
they?

```{code-cell} python
# code cell
```

## Part 3: Is a scan point inside the protective field?

The protective field moves with the vehicle and always has the same
boundaries in vehicle coordinates. A scan point lies inside it if it is
within all four boundaries:

```{figure} pics/chap06_schutzfeld_pruefung_EN.svg
:alt: The AGV and the yellow protective field in the vehicle coordinate system with the boundaries x_V = 0.6 and 1.6 and y_V = 0.5 and -0.5, a red scan point inside the protective field with its longitudinal distance x_V - 0.6 to the front edge, a point too far ahead and a point off to the side
:align: center

Checking the protective field in the vehicle coordinate system.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

Loop through `points_V` from Part 2. Count the points inside the protective
field, and for each of them, collect the **longitudinal distance**
$x_V - 0.6$, i.e. how far the point lies ahead of the front edge in the
direction of travel. What is the smallest longitudinal distance? Does the
AGV have to stop?

Finally, convert the corners of the protective field to warehouse
coordinates and draw them into the figure from Part 2 using the parameter
`protective_field`. Why don't all points of the unknown object lie inside
the protective field?

```{code-cell} python
# code cell
```

## Closing question

1. Why do we check the protective field in vehicle coordinates and not in
   warehouse coordinates? Which of the matrices $\mathbf{T}_{VS}$ and
   $\mathbf{T}_{WV}$ does the check need, and what follows if the controller
   has the wrong pose for the vehicle?
2. Two neighboring beams are $5°$ apart. How far apart are their scan points
   at a distance of $1\,\text{m}$? Would the scanner reliably detect a chair
   leg with a diameter of $4\,\text{cm}$ at this distance?

## Bonus exercise: Determining the yaw angle with a reflector (✩✩✩)

The AGV's controller continuously computes the pose from the rotations of
the wheels. Small measurement errors add up in the process, especially for
the yaw angle. To correct this, a **reflector** is mounted on the pillar, at
$(6.3, 0.7)$ according to the warehouse map. For localization, the
controller also evaluates the measurement data of the front scanner, with an
angular resolution of $1°$ instead of the $5°$ of our protective field scan.
In practice, a separate navigation scanner often takes over this task,
because not every safety scanner provides such data. The evaluation
recognizes the reflector by its particularly bright echo. It is at the
distance $r = 2.39\,\text{m}$ and the angle $\varphi = -72°$, both values
rounded. Assume that the vehicle center is at $(4, 2)$ and only the yaw
angle is unknown.

1. Try all yaw angles from $0°$ to $359°$ in steps of $1°$. For each angle,
   use $\mathbf{T}_{WV} \cdot \mathbf{T}_{VS}$ to compute where the reflector
   would be in the warehouse, and its distance to the position on the
   warehouse map.
2. Use `np.argmin` to find the yaw angle with the smallest distance. Plot the
   distance against the yaw angle.
3. Answer without code: why is a single reflector no longer enough if the
   position of the vehicle is also unknown?

```{code-cell} python
# code cell
```
