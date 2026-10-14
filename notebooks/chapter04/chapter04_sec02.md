---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 4.2 Stiffness Matrix of a Wall Bracket

In Chapter 4.1 we described the swing set in Python and assembled its
stiffness matrix. In this chapter we apply the same approach to a larger
truss with five nodes and six members. Work through the parts in pairs if
possible, and in order.

## Project: Stiffness matrix of a wall bracket (✩✩)

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

## Part 1: Describe and plot the truss

Create `node_pos`, `support_indices`, `members` and `force_vector`. Keep the
order from the table in the member list. Plot the truss with `plot_truss`
and compare the plot with the sketch.

Also answer: how many degrees of freedom does the bracket have if we leave
out the supports for now, and at which index of `force_vector` is the load?

```{code-cell} python
# code cell
```

## Part 2: Print a member table

Define Young's modulus and the cross-sectional area. Then write a loop over
all members that prints, for each member, the member number, the two nodes,
the length in m and the stiffness $k$ in kN/mm. A loop of the form
`for s in range(len(members)):` gives the member number `s`, and with
`i, j = members[s]` you get the two nodes.

Which members are the most flexible, and why?

```{code-cell} python
# code cell
```

## Part 3: Assemble the stiffness matrix

Assemble the stiffness matrix `K` with the function
`assemble_stiffness_matrix`. Print its shape and the matrix in kN/mm,
rounded to one decimal place.

Then use `np.allclose(K, K.T)` to check whether `K` is symmetric. `K.T` is
the **transposed** matrix, in which rows and columns are swapped. Why must
the stiffness matrix be symmetric?

```{code-cell} python
# code cell
```

## Part 4: Read the block structure

1. First predict without code which of the following blocks are zero:
   `K[0:2, 8:10]`, `K[4:6, 8:10]` and `K[2:4, 4:6]`. Which nodes does each
   block belong to? Then print the three blocks in kN/mm and check your
   prediction.
2. Print the diagonal block of node 4. The entry for the $x$-direction is
   much larger than the one for the $y$-direction. Which members contribute
   to the two entries? What does that mean for the pipe?

```{code-cell} python
# code cell
```

## Closing question

The stiffness matrix of the bracket is singular, even though we specified
the supports in `support_indices`. Why? Name motions of the whole bracket
that produce no force.

## Bonus exercise: Rotating without producing a force (✩✩✩)

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

```{code-cell} python
# code cell
```
