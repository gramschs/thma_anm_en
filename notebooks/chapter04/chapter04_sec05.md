---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 4.5 Exercises

These exercises are meant for self-study at home and review the material of
Chapters 4.1 to 4.4. Plan for about 90 minutes of working time.
Before starting the exercises, run the following two cells. They contain
the plotting function and the three functions from Chapters 4.1, 4.3 and
4.4.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 5 min)
* ✩✩ Application: write your own code and interpret results (approx. 10 min)
* ✩✩✩ Mini-project: combine several concepts from this chapter (approx. 30 min)

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

# function from Chapter 4.4, with roller supports
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

## Exercise 4.1 (✩)

Given the following code:

```python
import numpy as np

node_pos = np.array([
    [0.0, 0.0],
    [1.5, 0.0],
    [1.5, 1.0],
    [0.0, 1.0],
])
members = np.array([[0, 1], [1, 2], [2, 3], [3, 0], [0, 2]])
num_nodes = len(node_pos)

force_vector = np.zeros(2 * num_nodes)
force_vector[5] = -800.0
```

Write down your guess in a Markdown cell before you run the code.

1. How many degrees of freedom does the truss have, and what is the shape of
   its stiffness matrix?
2. Which nodes does `members[4]` connect? How long is this member?
3. At which node and in which direction does the force of $800\,\text{N}$
   act?
4. Which of the two blocks `K[0:2, 6:8]` and `K[2:4, 6:8]` is zero?
5. Run the code, assemble the stiffness matrix with
   `assemble_stiffness_matrix` for steel with a diameter of $1\,\text{cm}$,
   and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 4.2 (✩)

Given the following code for a vertical steel member:

```python
import numpy as np

youngs_modulus = 2.1e11
area = np.pi * 0.01**2 / 4

node_i = np.array([0.0, 0.0])
node_j = np.array([0.0, 0.5])

difference = node_j - node_i
length = np.sqrt(difference[0]**2 + difference[1]**2)
k = youngs_modulus * area / length
e = difference / length

block = k * np.array([
    [e[0] * e[0], e[0] * e[1]],
    [e[1] * e[0], e[1] * e[1]],
])
print('e:', e)
print('Block in kN/mm:')
print(np.round(block * 1e-6, 2))
```

Write down your guess in a Markdown cell before you run the code.

1. What is the value of the unit vector `e`?
2. Which entries of the block are zero, and which one is not?
3. A $1\,\text{m}$ long member with the same cross-section has the stiffness
   $16.49\,\text{kN/mm}$. What is $k$ for this member?
4. The upper node moves a small distance horizontally. What force does this
   produce in the member?
5. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 4.3 (✩)

Given the following code:

```python
import numpy as np

K = np.array([
    [ 4.0, -2.0],
    [-2.0,  4.0],
])
K_supported = K
K_supported[0, :] = 0.0
K_supported[0, 0] = 1.0

print('K_supported:')
print(K_supported)
print('K:')
print(K)
```

Write down your guess in a Markdown cell before you run the code.

1. What does `print(K_supported)` output?
2. What does `print(K)` output? Why?
3. How must the line `K_supported = K` be changed so that `K` stays
   unchanged?
4. A truss has a pin support at node 1 and a roller support at node 3.
   Which rows of the stiffness matrix does `compute_displacements` replace?
5. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 4.4 (✩)

Given the following code with the results of a truss analysis:

```python
import numpy as np

member_forces = np.array([2500.0, -2500.0, -2500.0, -800.0])   # in N
lengths = np.array([1.0, 1.0, 2.0, 2.0])                       # in m

youngs_modulus = 2.1e11
diameter = 0.014
moment_of_inertia = np.pi * diameter**4 / 64

for s in range(len(member_forces)):
    if member_forces[s] < 0:
        buckling_load = np.pi**2 * youngs_modulus * moment_of_inertia / lengths[s]**2
        print(f'Member {s}: buckling load {buckling_load:6.0f} N, compressive force {-member_forces[s]:6.0f} N')
```

Write down your guess in a Markdown cell before you run the code.

1. For which members does the loop print a line? Why not for member 0?
2. A $1\,\text{m}$ long member with this diameter has a buckling load of
   about $3900\,\text{N}$. What is the buckling load of the $2\,\text{m}$
   long members?
3. Which of members 1, 2 and 3 buckle?
4. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 4.5 (✩✩)

We analyze the wall bracket from Chapter 4.2. The two nodes on the wall are
pin supports, and a pipe with $3000\,\text{N}$ hangs from the tip. All
members are made of steel with a diameter of $1\,\text{cm}$.

| Node | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| $x$ in m | 0.0 | 0.0 | 1.0 | 1.0 | 2.0 |
| $y$ in m | 0.0 | 1.0 | 0.0 | 1.0 | 0.0 |

Member list: `[[0, 2], [2, 4], [1, 3], [2, 3], [1, 2], [3, 4]]`, pin
supports at nodes 0 and 1, load at node 4 pointing downward.

1. Compute the displacements and print the displacement of the tip in mm.
2. Compute the support reactions at nodes 0 and 1. Which of the two wall
   connections is loaded in tension, i.e. pulled out of the wall?
3. Compute the member forces. Check the forces in members 1 and 5 by hand
   with the equilibrium at node 4: only the horizontal member 1, the
   inclined member 5 and the load meet at this node.

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 4.6 (✩✩)

At which height does the apex of the swing set from Chapter 4.1 sink the
least? The feet stay at $(0, 0)$ and $(2\,\text{m}, 0)$, and the apex is at
$(1\,\text{m}, h)$. The load is $2000\,\text{N}$ downward, and the members
are made of steel with a diameter of $1\,\text{cm}$.

1. Use `np.linspace` to create twelve heights from $0.25\,\text{m}$ to
   $3.0\,\text{m}$. In a loop, compute the force in member 0 and the
   deflection of the apex for each height.
2. Plot both quantities over $h$ in two subplots.
3. At which height is the deflection smallest? Use `np.argmin`.
4. Why does the member force become so large for small heights? Why does
   the deflection increase again for large heights, even though the member
   force keeps decreasing?
5. Our swing set is $2\,\text{m}$ high and therefore not at its stiffest.
   Why do we still build it this high?

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 4.7 (✩✩✩) Mini-project: Maintenance walkway in a factory

A maintenance walkway in a factory spans $3\,\text{m}$. It is built as
a truss of equilateral triangles with a side length of $1\,\text{m}$. The
walkway deck rests on the bottom chord. Two technicians with tools load
nodes 1 and 2 with $3000\,\text{N}$ each, pointing downward. On the left the
walkway rests on a pin support, on the right on a roller support. The
height of the truss is $h = \sqrt{3}/2\,\text{m} \approx 0.866\,\text{m}$.

| Node | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $x$ in m | 0.0 | 1.0 | 2.0 | 3.0 | 0.5 | 1.5 | 2.5 |
| $y$ in m | 0.0 | 0.0 | 0.0 | 0.0 | $h$ | $h$ | $h$ |

Member list:
`[[0, 1], [1, 2], [2, 3], [4, 5], [5, 6], [0, 4], [1, 4], [1, 5], [2, 5], [2, 6], [3, 6]]`

The members are round bars made of S235 with
$E = 2.1 \cdot 10^{11}\,\text{N/m}^2$ and $R_e = 235\,\text{N/mm}^2$.

**Part 1:** Create the truss and plot it with the pin support, the roller
support and the loads.

**Part 2:** For a diameter of $12\,\text{mm}$, compute the displacements,
the support reactions and the member forces. Plot the truss with member
forces and displacements exaggerated by a factor of 200.

**Part 3:** Check all members for stress and all compression members for
buckling. Which members fail?

**Part 4:** Round bars are available with diameters of 12, 16, 20 and
25 mm. Use a loop to print, for each diameter, how many members fail at
least one of the two checks. What is the smallest diameter for which all
members pass both checks?

**Closing question:** The two diagonals 7 and 8, which lead from the bottom
chord to the middle node 5, carry no force. Why? And why do the member
forces not change when we change the diameter?

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```
