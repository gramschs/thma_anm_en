---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 4.2 Stiffness Matrix of a Wall Bracket

In Chapter 4.1 we described the swing set on the computer and assembled its
stiffness matrix. In this chapter we apply the same approach to a larger
truss with five nodes and six members. Work through the parts in pairs if
possible, and in order.

````{admonition} Project: Stiffness matrix of a wall bracket (✩✩)
:class: tip
A bracket made of steel bars is attached to the wall of a factory building.
A pipe hangs from its tip and pulls downward with $3000\,\text{N}$. The two
nodes on the wall are pin supports.

```{figure} pics/chap04_wandkonsole_EN.svg
:alt: Wall bracket made of six members with five nodes, two pin supports on the wall and a load at the tip
:align: center

The wall bracket with node numbers, member numbers and the load at node 4.
(Source: figure by the author; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

| Node | $x$ in m | $y$ in m | Note |
| --- | --- | --- | --- |
| 0 | 0.0 | 0.0 | pin support |
| 1 | 0.0 | 1.0 | pin support |
| 2 | 1.0 | 0.0 | free |
| 3 | 1.0 | 1.0 | free |
| 4 | 2.0 | 0.0 | free, the pipe hangs here |

| Member | connects nodes | Component |
| --- | --- | --- |
| 0 | 0 and 2 | bottom chord, inner |
| 1 | 2 and 4 | bottom chord, outer |
| 2 | 1 and 3 | top chord |
| 3 | 2 and 3 | vertical |
| 4 | 1 and 2 | diagonal |
| 5 | 3 and 4 | inclined member |

All members are made of steel ($E = 2.1 \cdot 10^{11}\,\text{N/m}^2$) and
have a circular cross-section with a diameter of $1\,\text{cm}$.
````

First run the following two cells. The first contains the given plotting
function, the second the imports and the function `assemble_stiffness_matrix`
from Chapter 4.1.

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
```

```{admonition} Part 1: Describe and plot the truss
:class: tip
Create `node_pos`, `support_indices`, `members` and `force_vector`. Keep the
order from the table in the member list. Plot the truss with `plot_truss`
and compare the plot with the sketch.

Also answer: how many degrees of freedom does the bracket have if we leave
out the supports for now, and at which index of `force_vector` is the load?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 1
:class: tip
:class: dropdown
```python
# node coordinates in m: row n contains [x, y] of node n
node_pos = np.array([
    [0.0, 0.0],   # node 0: pin support at the bottom of the wall
    [0.0, 1.0],   # node 1: pin support at the top of the wall
    [1.0, 0.0],   # node 2
    [1.0, 1.0],   # node 3
    [2.0, 0.0],   # node 4: tip with the pipe
])
num_nodes = len(node_pos)

support_indices = [0, 1]

# member list in the order of the table
members = np.array([
    [0, 2],   # member 0: bottom chord, inner
    [2, 4],   # member 1: bottom chord, outer
    [1, 3],   # member 2: top chord
    [2, 3],   # member 3: vertical
    [1, 2],   # member 4: diagonal
    [3, 4],   # member 5: inclined member
])

# load at node 4 in the y-direction: index 2 * 4 + 1 = 9
force_vector = np.zeros(2 * num_nodes)
force_vector[9] = -3000.0

print('Number of degrees of freedom:', 2 * num_nodes)
plot_truss(node_pos, members, support_indices, force_vector=force_vector,
           title='Wall bracket')
```
The bracket has five nodes with two degrees of freedom each, i.e. ten
degrees of freedom. The two pin supports constrain four of them, leaving six
free degrees of freedom. We will need this in Chapter 4.3. The load acts at
node 4 in the $y$-direction and is therefore at index
$2 \cdot 4 + 1 = 9$. The minus sign means that the force points downward.
````

```{admonition} Part 2: Print a member table
:class: tip
Define Young's modulus and the cross-sectional area. Then write a loop over
all members that prints, for each member, the member number, the two nodes,
the length in m and the stiffness $k$ in kN/mm. A loop of the form
`for s in range(len(members)):` gives the member number `s`, and with
`i, j = members[s]` you get the two nodes.

Which members are the most flexible, and why?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
youngs_modulus = 2.1e11                    # steel in N/m²
diameter = 0.01                            # in m
area = np.pi * diameter**2 / 4             # circular area in m²

print('Member  Nodes  Length in m  k in kN/mm')
for s in range(len(members)):
    i, j = members[s]
    difference = node_pos[j] - node_pos[i]
    length = np.sqrt(difference[0]**2 + difference[1]**2)
    k = youngs_modulus * area / length
    print(f'{s:6d}  {i} - {j}  {length:11.4f}  {k * 1e-6:10.2f}')
```
Output:

```text
Member  Nodes  Length in m  k in kN/mm
     0  0 - 2       1.0000       16.49
     1  2 - 4       1.0000       16.49
     2  1 - 3       1.0000       16.49
     3  2 - 3       1.0000       16.49
     4  1 - 2       1.4142       11.66
     5  3 - 4       1.4142       11.66
```

The two inclined members 4 and 5 are the most flexible. All members have the
same material and the same cross-section, so the stiffness $k = EA/L$
depends only on the length. At $\sqrt{2}\,\text{m}$, the inclined members
are the longest.
````

```{admonition} Part 3: Assemble the stiffness matrix
:class: tip
Assemble the stiffness matrix `K` with the function
`assemble_stiffness_matrix`. Print its shape and the matrix in kN/mm,
rounded to one decimal place.

Then use `np.allclose(K, K.T)` to check whether `K` is symmetric. `K.T` is
the **transposed** matrix, in which rows and columns are swapped. Why must
the stiffness matrix be symmetric?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
K = assemble_stiffness_matrix(node_pos, members, youngs_modulus, area)

print('Shape of K:', K.shape)
print('K in kN/mm:')
print(np.round(K * 1e-6, 1))
print('K is symmetric:', np.allclose(K, K.T))
```
`K` has the shape `(10, 10)`, one row and one column for each degree of
freedom. The matrix is symmetric because of two properties of each member.
First, its stiffness block is itself symmetric, because the top right and
the bottom left both contain $k\,e_x e_y$. Second, the function adds the
block symmetrically: $-\mathbf{b}$ appears both at nodes $i$ and $j$ and at
nodes $j$ and $i$.
````

```{admonition} Part 4: Read the block structure
:class: tip
1. First predict without code which of the following blocks are zero:
   `K[0:2, 8:10]`, `K[4:6, 8:10]` and `K[2:4, 4:6]`. Which nodes does each
   block belong to? Then print the three blocks in kN/mm and check your
   prediction.
2. Print the diagonal block of node 4. The entry for the $x$-direction is
   much larger than the one for the $y$-direction. Which members contribute
   to the two entries? What does that mean for the pipe?
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 4
:class: tip
:class: dropdown
```python
print('K[0:2, 8:10], nodes 0 and 4, in kN/mm:')
print(np.round(K[0:2, 8:10] * 1e-6, 2))
print('K[4:6, 8:10], nodes 2 and 4, in kN/mm:')
print(np.round(K[4:6, 8:10] * 1e-6, 2))
print('K[2:4, 4:6], nodes 1 and 2, in kN/mm:')
print(np.round(K[2:4, 4:6] * 1e-6, 2))

# diagonal block of node 4: rows and columns 8 and 9
print('K[8:10, 8:10], node 4, in kN/mm:')
print(np.round(K[8:10, 8:10] * 1e-6, 2))
```
Output:

```text
K[0:2, 8:10], nodes 0 and 4, in kN/mm:
[[0. 0.]
 [0. 0.]]
K[4:6, 8:10], nodes 2 and 4, in kN/mm:
[[-16.49   0.  ]
 [  0.     0.  ]]
K[2:4, 4:6], nodes 1 and 2, in kN/mm:
[[-5.83  5.83]
 [ 5.83 -5.83]]
K[8:10, 8:10], node 4, in kN/mm:
[[22.32 -5.83]
 [-5.83  5.83]]
```

Only the block of node 0 and node 4 is zero, because there is no member
between these two nodes. Nodes 2 and 4 are connected by the horizontal
member 1, so there is only one entry, in the top left. Nodes 1 and 2 are
connected by the diagonal, so all four entries are filled.

In the diagonal block of node 4, the contributions of members 1 and 5 add
up. In the $x$-direction both act: member 1 with $16.49\,\text{kN/mm}$ and
the inclined member with $5.83\,\text{kN/mm}$. In the $y$-direction only the
inclined member acts, because the horizontal member 1 cannot carry a
vertical force. The diagonal block, however, describes node 4 on its own, as
if all other nodes were held in place. Under this assumption, the tip yields
more easily in the $y$-direction than in the $x$-direction, i.e. in the
direction in which the pipe pulls. How far the tip actually moves we compute
in Exercise 4.5. There the supports are part of the system of equations, and
all free nodes can move.
````

```{admonition} Closing question
:class: tip
The stiffness matrix of the bracket is singular, even though we specified
the supports in `support_indices`. Why? Name motions of the whole bracket
that produce no force.
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
The function `assemble_stiffness_matrix` is not even given
`support_indices`. The matrix `K` therefore describes the bracket as if it
were not attached to the wall. We can shift such a free bracket as a whole
to the right or left, shift it up or down, or rotate it a little. None of
these motions changes a member length, so no force is produced either. For a
given load there is then no unique displacement, and that is exactly what
the zero determinant indicates.

This bracket has a fourth such motion. Only the horizontal member 0 is
attached to node 0, so node 0 can move a little vertically without any
member length changing. The pin support at node 0 will prevent this later.
In Chapter 4.3 we add the supports to the system of equations.
````

```{admonition} Bonus exercise: Rotating without producing a force (✩✩✩)
:class: tip
We rotate the free bracket by a small angle $\alpha = 0.001$ about node 0.
For a small rotation, node $n$ with the coordinates $(x_n, y_n)$ moves by

$$u_{nx} = -\alpha\, y_n, \qquad u_{ny} = \alpha\, x_n.$$

1. Use a loop over all nodes to create the displacement vector
   `u_rotation`. Compute `K @ u_rotation`.
2. For comparison, move only node 4 down by $1\,\text{mm}$ and compute the
   forces as well. What do you notice?
3. Plot the rotated bracket with
   `plot_truss(..., displacement=u_rotation, scale=100)`.
   The displacements are shown exaggerated by a factor of 100.
```

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
```python
# task 1: displacement vector of the small rotation about node 0
alpha = 0.001   # rotation angle in rad
u_rotation = np.zeros(2 * num_nodes)
for n in range(num_nodes):
    u_rotation[2 * n] = -alpha * node_pos[n, 1]      # x-displacement
    u_rotation[2 * n + 1] = alpha * node_pos[n, 0]   # y-displacement

print('Forces for the rotation in N:')
print(np.round(K @ u_rotation, 6))

# task 2: only node 4 moves down by 1 mm
u_node4 = np.zeros(2 * num_nodes)
u_node4[9] = -0.001
print('Forces for the displacement of node 4 in N:')
print(np.round(K @ u_node4, 1))

# task 3: rotated bracket, exaggerated by a factor of 100
plot_truss(node_pos, members, support_indices, displacement=u_rotation,
           scale=100, title='Small rotation of the free bracket')
```
For the rotation, all forces are zero. The output `-0.` is a tiny negative
rounding error that was rounded to zero. For the displacement of node 4, on
the other hand, forces of several thousand newtons arise at nodes 3 and 4.
The reason: during the rotation, the two ends of each member move relative
to each other only perpendicular to the member axis. Therefore all member
lengths stay the same, and no member is stretched or compressed. Besides the
two shifts in $x$ and $y$, the rotation is the third motion that a plane
truss without supports can perform as a whole without any force. In the
plot we also see how the bracket comes loose from its supports: the matrix
`K` does not know anything about the wall yet.
````
