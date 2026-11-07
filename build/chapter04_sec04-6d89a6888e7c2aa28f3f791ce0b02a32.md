---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 4.4 Roof Truss of a Steel Building Under Snow Load

In Chapter 4.3 we added the supports, computed displacements, support
reactions and member forces, and checked the swing set for stress and
buckling. In this chapter we use the three functions to analyze and
evaluate a roof truss. Work through the parts in pairs if possible, and in
order.

````{admonition} Project: Roof truss of a steel building (✩✩)
:class: tip
The roof of a small steel building rests on roof trusses with a span of
$6\,\text{m}$ and a ridge height of $2\,\text{m}$. After heavy snowfall, a
load of $2000\,\text{N}$ pushes down on each of the three upper nodes. The
truss rests on a pin support on the left and on a roller support on the
right, like the beam in Chapter 3.2.

```{figure} pics/chap04_dachbinder_EN.svg
:alt: Roof truss made of eleven members with seven nodes, a pin support on the left, a roller support on the right and three snow loads on the upper nodes
:align: center

The roof truss with node numbers, member numbers and the snow load.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

| Node | $x$ in m | $y$ in m | Note |
| --- | --- | --- | --- |
| 0 | 0.0 | 0.0 | pin support |
| 1 | 2.0 | 0.0 | free |
| 2 | 4.0 | 0.0 | free |
| 3 | 6.0 | 0.0 | roller support |
| 4 | 2.0 | 4/3 | free, snow load |
| 5 | 3.0 | 2.0 | free, snow load (ridge) |
| 6 | 4.0 | 4/3 | free, snow load |

| Member | connects nodes | Component |
| --- | --- | --- |
| 0, 1, 2 | 0 and 1, 1 and 2, 2 and 3 | bottom chord |
| 3, 4, 5, 6 | 0 and 4, 4 and 5, 5 and 6, 6 and 3 | top chord |
| 7, 8 | 1 and 4, 2 and 6 | verticals |
| 9, 10 | 1 and 5, 2 and 5 | diagonals |

All members are round bars made of structural steel S235 with a diameter of
$2\,\text{cm}$, $E = 2.1 \cdot 10^{11}\,\text{N/m}^2$ and the yield strength
$R_e = 235\,\text{N/mm}^2$.
````

First run the following two cells. The first contains the given plotting
function, the second the imports and the three functions from Chapters 4.1
and 4.3.

The function `compute_displacements` has an additional parameter
`roller_indices`. A roller support like support B in Chapter 3.2 holds the
node only in the vertical direction; horizontally, the node can move
freely. The function therefore replaces only the equation for $u_y$ at a
roller support. `plot_truss` also knows this parameter and draws roller
supports with an extra line.

```{code-cell} python
:tags: [hide-input]
# Given plotting function: just run it, you do not need to understand it.
def plot_truss(node_pos, members, support_indices, roller_indices=None,
               force_vector=None, displacement=None, scale=1.0,
               member_forces=None, title=''):
    """Plots a plane truss.

    node_pos: node coordinates in m, row n = [x_n, y_n]
    members: member list, row s = [i, j]
    support_indices: list of nodes with a pin support
    roller_indices: list of nodes with a roller support (optional)
    force_vector: external node forces in N, drawn as arrows (optional)
    displacement: displacement vector in m, draws the deformed shape (optional)
    scale: exaggeration factor for the displacements
    member_forces: member forces in N, blue = tension, red = compression, gray = zero force (optional)
    title: plot title
    """
    blue, red, orange, gray = '#005A94', '#E60000', '#E87846', '#484949'
    num_nodes = len(node_pos)
    extent = np.max(np.ptp(node_pos, axis=0))   # larger extent in x or y
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # node positions: initial shape or exaggerated deformed shape
    pos = node_pos.copy()
    if displacement is not None:
        pos = node_pos + scale * displacement.reshape(num_nodes, 2)
        for i, j in members:
            ax.plot(node_pos[[i, j], 0], node_pos[[i, j], 1],
                    color=gray, linestyle='--', linewidth=1)

    # members, colored and labeled if member forces are given
    for s in range(len(members)):
        i, j = members[s]
        color = blue
        if member_forces is not None:
            color = blue if member_forces[s] >= 0 else red
            if abs(member_forces[s]) <= 1e-6 * np.max(np.abs(member_forces)):
                color = '#A6A6A6'   # light gray: member without force (ignore rounding errors)
            mid = 0.5 * (pos[i] + pos[j])
            ax.text(mid[0], mid[1], f' {member_forces[s] / 1000:.2f} kN',
                    color=color, fontsize=9)
        ax.plot(pos[[i, j], 0], pos[[i, j], 1], color=color, linewidth=3)

    # supports as triangles below the nodes, roller supports with an extra line
    if roller_indices is None:
        roller_indices = []
    h = 0.06 * extent
    for n in list(support_indices) + list(roller_indices):
        x, y = node_pos[n]
        ax.fill([x, x - h, x + h], [y, y - 1.5 * h, y - 1.5 * h],
                color='#CCDEE9', edgecolor=gray, zorder=2)
        if n in roller_indices:
            ax.plot([x - h, x + h], [y - 2 * h, y - 2 * h], color=gray, linewidth=2)

    # nodes with numbers
    ax.scatter(pos[:, 0], pos[:, 1], color=orange, s=60, zorder=3)
    for n in range(num_nodes):
        ax.text(pos[n, 0], pos[n, 1], f'  N{n}', color=blue,
                fontsize=10, va='bottom')

    # external forces as arrows pointing at the nodes
    if force_vector is not None:
        forces = force_vector.reshape(num_nodes, 2)
        for n in range(num_nodes):
            magnitude = np.sqrt(forces[n, 0]**2 + forces[n, 1]**2)
            if magnitude > 0:
                direction = forces[n] / magnitude
                start = pos[n] - 0.15 * extent * direction
                ax.annotate('', xy=pos[n], xytext=start,
                            arrowprops=dict(color=gray, width=2, headwidth=8))
                ax.text(start[0], start[1], f' {magnitude:.0f} N', color=gray,
                        fontsize=9)
                ax.plot(start[0], start[1], alpha=0)   # keep the arrow inside the plot area

    if member_forces is not None:
        ax.plot([], [], color=blue, linewidth=3, label='Tension')
        ax.plot([], [], color=red, linewidth=3, label='Compression')
        ax.plot([], [], color='#A6A6A6', linewidth=3, label='Zero force')
        ax.legend(loc='upper right')

    ax.set_title(title)
    ax.set_xlabel('x in m')
    ax.set_ylabel('y in m')
    ax.set_aspect('equal')
    ax.margins(0.15)
    ax.grid(True)
    plt.show()
```

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# function from Chapter 4.1
def assemble_stiffness_matrix(node_pos, members, youngs_modulus, area):
    """Assembles the stiffness matrix of a plane truss.

    node_pos: node coordinates in m, row n = [x_n, y_n]
    members: member list, row s = [i, j]
    youngs_modulus: E in N/m², the same for all members
    area: A in m², the same for all members
    Returns: stiffness matrix K in N/m, shape (2 * number of nodes, 2 * number of nodes)
    """
    num_dofs = 2 * len(node_pos)
    K = np.zeros((num_dofs, num_dofs))

    for i, j in members:
        # geometry and stiffness of the member
        difference = node_pos[j] - node_pos[i]
        length = np.sqrt(difference[0]**2 + difference[1]**2)
        k = youngs_modulus * area / length
        e = difference / length

        # stiffness block of the member
        block = k * np.array([
            [e[0] * e[0], e[0] * e[1]],
            [e[1] * e[0], e[1] * e[1]],
        ])

        # add the block to K: +block at i-i and j-j, -block at i-j and j-i
        K[2*i : 2*i + 2, 2*i : 2*i + 2] += block
        K[2*j : 2*j + 2, 2*j : 2*j + 2] += block
        K[2*i : 2*i + 2, 2*j : 2*j + 2] -= block
        K[2*j : 2*j + 2, 2*i : 2*i + 2] -= block

    return K


# function from Chapter 4.3, extended to roller supports
def compute_displacements(K, force_vector, support_indices, roller_indices=None):
    """Solves K * u = F for a truss with pin and roller supports.

    K: stiffness matrix in N/m
    force_vector: external node forces in N
    support_indices: list of nodes with a pin support, where ux = uy = 0
    roller_indices: list of nodes with a roller support, where only uy = 0 (optional)
    Returns: displacement vector u in m
    """
    if roller_indices is None:
        roller_indices = []
    K_supported = K.copy()
    force_supported = force_vector.copy()
    for n in support_indices:
        for d in [2 * n, 2 * n + 1]:
            K_supported[d, :] = 0.0
            K_supported[d, d] = 1.0
            force_supported[d] = 0.0
    # new: at a roller support, replace only the equation for the y-direction
    for n in roller_indices:
        d = 2 * n + 1
        K_supported[d, :] = 0.0
        K_supported[d, d] = 1.0
        force_supported[d] = 0.0
    return np.linalg.solve(K_supported, force_supported)


# function from Chapter 4.3
def compute_member_forces(node_pos, members, youngs_modulus, area, u):
    """Computes the member forces of a truss from the displacements.

    node_pos: node coordinates in m, row n = [x_n, y_n]
    members: member list, row s = [i, j]
    youngs_modulus: E in N/m², the same for all members
    area: A in m², the same for all members
    u: displacement vector in m
    Returns: member forces in N, positive = tension, negative = compression
    """
    member_forces = np.zeros(len(members))
    for s in range(len(members)):
        i, j = members[s]
        # geometry and stiffness as in assemble_stiffness_matrix
        difference = node_pos[j] - node_pos[i]
        length = np.sqrt(difference[0]**2 + difference[1]**2)
        k = youngs_modulus * area / length
        e = difference / length

        # displacement of node j relative to node i
        u_relative = u[2*j : 2*j + 2] - u[2*i : 2*i + 2]

        # change in length = component along the member, member force N = k * delta_l
        delta_l = e[0] * u_relative[0] + e[1] * u_relative[1]
        member_forces[s] = k * delta_l
    return member_forces
```

```{admonition} Part 1: Describe and plot the roof truss
:class: tip
Define the material properties, `node_pos`, `support_indices` for the
pin support, `roller_indices` for the roller support, `members` and
`force_vector`. Keep the order of the member numbers in the member list.
Plot the truss with

`plot_truss(node_pos, members, support_indices, roller_indices=roller_indices, force_vector=force_vector)`

and compare the plot with the sketch.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 1
:class: tip
:class: dropdown
```python
# material: round bars made of S235 with a diameter of 2 cm
youngs_modulus = 2.1e11                  # in N/m²
diameter = 0.02                          # in m
area = np.pi * diameter**2 / 4           # in m²
yield_strength = 235.0                   # in N/mm²

# node coordinates in m
node_pos = np.array([
    [0.0, 0.0],       # node 0: pin support
    [2.0, 0.0],       # node 1
    [4.0, 0.0],       # node 2
    [6.0, 0.0],       # node 3: roller support
    [2.0, 4 / 3],     # node 4
    [3.0, 2.0],       # node 5: ridge
    [4.0, 4 / 3],     # node 6
])
num_nodes = len(node_pos)

support_indices = [0]   # pin support
roller_indices = [3]    # roller support

members = np.array([
    [0, 1], [1, 2], [2, 3],           # members 0 to 2: bottom chord
    [0, 4], [4, 5], [5, 6], [6, 3],   # members 3 to 6: top chord
    [1, 4], [2, 6],                   # members 7 and 8: verticals
    [1, 5], [2, 5],                   # members 9 and 10: diagonals
])

# snow load: Fy at nodes 4, 5 and 6 is at indices 9, 11 and 13
force_vector = np.zeros(2 * num_nodes)
force_vector[9] = -2000.0
force_vector[11] = -2000.0
force_vector[13] = -2000.0

plot_truss(node_pos, members, support_indices,
           roller_indices=roller_indices, force_vector=force_vector,
           title='Roof truss under snow load')
```
We write the coordinates of nodes 4 and 6 as `4 / 3`; Python then computes
the value accurately enough. The snow load at node $n$ is at index $2n + 1$,
i.e. at indices 9, 11 and 13.
````

```{admonition} Part 2: Predict, then compute
:class: tip
1. Think about it without code: is the bottom chord in tension or in
   compression? And the top chord? Write down your prediction.
2. Use the three functions to compute the stiffness matrix, the
   displacements and the member forces. Print the member forces together
   with tension or compression, and plot the truss with member forces and
   displacements exaggerated by a factor of 200. Was your prediction
   correct?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
K = assemble_stiffness_matrix(node_pos, members, youngs_modulus, area)
u = compute_displacements(K, force_vector, support_indices, roller_indices)
member_forces = compute_member_forces(node_pos, members, youngs_modulus,
                                      area, u)

for s in range(len(members)):
    if abs(member_forces[s]) < 1e-6:   # below 1 µN: just a rounding error
        kind = 'zero force'
    elif member_forces[s] > 0:
        kind = 'tension'
    else:
        kind = 'compression'
    print(f'Member {s:2d}: N = {member_forces[s]:8.1f} N  ({kind})')
print(f'Deflection of the ridge: {u[11] * 1000:.3f} mm')

plot_truss(node_pos, members, support_indices,
           roller_indices=roller_indices, force_vector=force_vector,
           displacement=u, scale=200, member_forces=member_forces,
           title='Roof truss, displacements exaggerated by a factor of 200')
```
Output:

```text
Member  0: N =   4500.0 N  (tension)
Member  1: N =   3500.0 N  (tension)
Member  2: N =   4500.0 N  (tension)
Member  3: N =  -5408.3 N  (compression)
Member  4: N =  -5408.3 N  (compression)
Member  5: N =  -5408.3 N  (compression)
Member  6: N =  -5408.3 N  (compression)
Member  7: N =  -2000.0 N  (compression)
Member  8: N =  -2000.0 N  (compression)
Member  9: N =   2236.1 N  (tension)
Member 10: N =   2236.1 N  (tension)
Deflection of the ridge: -0.817 mm
```

The bottom chord is in tension, the top chord in compression. The snow load
compresses the inclined top chord members, and these try to push the two
supports outward. The bottom chord holds the supports together like a tie.
The verticals carry the load of nodes 4 and 6 down into the bottom chord in
compression, and the diagonals carry it back up to the ridge in tension.
The ridge sinks by about $0.8\,\text{mm}$.
````

```{admonition} Part 3: Support reactions and equilibrium
:class: tip
Compute the node forces $\mathbf{K} \cdot \vec{u}$ and print the forces at
the support nodes 0 and 3.

1. Why does each support carry exactly half of the total snow load?
2. Why is the horizontal support reaction at the pin support zero?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
node_forces = K @ u

for n in [0, 3]:
    print(f'Node {n}: Fx = {node_forces[2*n]:8.1f} N,  '
          f'Fy = {node_forces[2*n + 1]:8.1f} N')
```
Output:

```text
Node 0: Fx =      0.0 N,  Fy =   3000.0 N
Node 3: Fx =      0.0 N,  Fy =   3000.0 N
```

The total snow load is $3 \cdot 2000\,\text{N} = 6000\,\text{N}$. The truss
and the load are symmetric about the center, so each support carries
$3000\,\text{N}$ upward. Horizontally, only support reactions act, because
the snow load points straight down. The roller support cannot carry a
horizontal force. For the sum of the horizontal forces to be zero, the
horizontal force at the pin support must also be zero, just as for the beam
in Chapter 3.2.
````

```{admonition} Part 4: Will the roof truss hold?
:class: tip
Check each member with a loop:

- Compute the stress $\sigma = N/A$ in N/mm² and the utilization
  $|\sigma| / R_e$.
- For each compression member, also compute the Euler buckling load
  $F_\text{cr} = \pi^2 E I / L^2$ with $I = \pi d^4 / 64$ and compare it
  with the magnitude of the compressive force.

Which members fail one of the two checks?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 4
:class: tip
:class: dropdown
```python
moment_of_inertia = np.pi * diameter**4 / 64   # in m^4

print('Member    N in N  sigma in N/mm²  Utilization  Buckling load in N  Buckles?')
for s in range(len(members)):
    i, j = members[s]
    difference = node_pos[j] - node_pos[i]
    length = np.sqrt(difference[0]**2 + difference[1]**2)

    # stress check for all members
    stress = member_forces[s] / area * 1e-6
    utilization = abs(stress) / yield_strength

    # buckling check only for compression members
    if member_forces[s] < 0:
        buckling_load = np.pi**2 * youngs_modulus * moment_of_inertia / length**2
        buckles = 'yes' if abs(member_forces[s]) > buckling_load else 'no'
        print(f'{s:6d}  {member_forces[s]:8.1f}  {stress:14.1f}  {utilization * 100:9.1f} %'
              f'  {buckling_load:18.1f}  {buckles}')
    else:
        print(f'{s:6d}  {member_forces[s]:8.1f}  {stress:14.1f}  {utilization * 100:9.1f} %'
              f'  {"(tension)":>18}')
```
Output:

```text
Member    N in N  sigma in N/mm²  Utilization  Buckling load in N  Buckles?
     0    4500.0            14.3        6.1 %           (tension)
     1    3500.0            11.1        4.7 %           (tension)
     2    4500.0            14.3        6.1 %           (tension)
     3   -5408.3           -17.2        7.3 %              2817.4  yes
     4   -5408.3           -17.2        7.3 %             11269.6  no
     5   -5408.3           -17.2        7.3 %             11269.6  no
     6   -5408.3           -17.2        7.3 %              2817.4  yes
     7   -2000.0            -6.4        2.7 %              9156.5  no
     8   -2000.0            -6.4        2.7 %              9156.5  no
     9    2236.1             7.1        3.0 %           (tension)
    10    2236.1             7.1        3.0 %           (tension)
```

All members pass the stress check by a wide margin; the highest utilization
is below ten percent. In the buckling check, however, the two outer top
chord members 3 and 6 fail: their buckling load is only half as large as the
compressive force. So the roof truss fails under the snow load.
````

```{admonition} Closing question
:class: tip
All four top chord members carry the same compressive force. Nevertheless,
only members 3 and 6 buckle. Why? And why don't we need to check the bottom
chord for buckling at all, even though its member forces are similar in
size? Suggest a design change that makes the truss hold.
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
The buckling load $F_\text{cr} = \pi^2 E I / L^2$ decreases with the square
of the member length. At $2.40\,\text{m}$, members 3 and 6 are twice as long
as members 4 and 5 at $1.20\,\text{m}$. Their buckling load is therefore
only a quarter as large, and that is no longer enough for the compressive
force of $5408\,\text{N}$.

The bottom chord is in tension. A member in tension is pulled straight and
cannot deflect sideways; buckling is only possible under compression.

One remedy is an additional node in the middle of members 3 and 6 that is
connected to the bottom chord by further members. This halves the buckling
length in the plane of the truss, and the buckling load quadruples.
Perpendicular to this plane, the new node must also be held in place, in a
real roof for example by a purlin. Alternatively, we use thicker bars
or tubes for the top chord. For the same cross-sectional area, a tube has a
much larger area moment of inertia $I$ than a solid bar, because the
material lies farther out.
````

```{admonition} Bonus exercise: Why does a roller support make sense? (✩✩✩)
:class: tip
We replace the roller support at node 3 by a second pin support, i.e.
`support_indices = [0, 3]` and no roller supports. Recompute the
displacements, member forces and support reactions, and compare them with
the previous supports.

1. How do the forces in the bottom chord change?
2. Which horizontal forces now occur at the supports? What does that mean
   for the walls of the building?
```

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
```python
# two pin supports, no roller support
u_pinned = compute_displacements(K, force_vector, [0, 3])
member_forces_pinned = compute_member_forces(node_pos, members, youngs_modulus,
                                             area, u_pinned)
node_forces_pinned = K @ u_pinned

# task 1: bottom chord in comparison
print('Bottom chord  pin + roller       pin + pin')
for s in [0, 1, 2]:
    print(f'Member {s}:   {member_forces[s]:12.1f} N  {member_forces_pinned[s]:12.1f} N')

# task 2: support reactions with two pin supports
for n in [0, 3]:
    print(f'Node {n}: Fx = {node_forces_pinned[2*n]:8.1f} N,  '
          f'Fy = {node_forces_pinned[2*n + 1]:8.1f} N')
```
Output:

```text
Bottom chord  pin + roller       pin + pin
Member 0:         4500.0 N         333.3 N
Member 1:         3500.0 N        -666.7 N
Member 2:         4500.0 N         333.3 N
Node 0: Fx =   4166.7 N,  Fy =   3000.0 N
Node 3: Fx =  -4166.7 N,  Fy =   3000.0 N
```

With two pin supports, the bottom chord carries almost no force; the middle
member is even in slight compression. The two supports now take over the
role of the tie: they push horizontally against each other with about
$4200\,\text{N}$. Conversely, the truss pushes the walls or columns of the
building outward with this force, and they would have to carry this force
in addition. Moreover, every change in temperature would produce additional
restraint forces, because the truss can no longer expand freely. That is
why a truss usually rests on a roller support on one side.

With two pin supports, the roof truss is **statically indeterminate**, as
described in Chapter 4.1. With a pin and a roller support, there are 14
unknowns, namely 11 member forces and 3 support reactions, and exactly 14
equilibrium conditions. The second pin support adds a fourth support
reaction. The horizontal support reaction of about $4200\,\text{N}$
therefore does not follow from equilibrium alone. It also depends on how the
members deform. Because the two supports cannot move apart, the changes in
length of the three bottom chord members must add up to zero. If, for
example, the middle bottom chord member were twice as stiff, the horizontal
support reaction would rise to $4300\,\text{N}$. The stiffness method takes
this into account automatically; we did not have to change our functions at
all.
````
