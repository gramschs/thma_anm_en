---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 4.1 From Truss to Stiffness Matrix

In Chapter 3.2 we computed the support reactions of a beam. We set up the
three equilibrium conditions by hand. That works well for a beam with two
supports. For a crane, a bridge or a roof structure with dozens of members,
it quickly becomes hard to keep track. *How do we get the computer to set up
the system of equations for an entire structure by itself?*

For this we consider **ideal plane trusses**. They consist of straight
members that are connected by pins at their ends. The connection points are
called **nodes**. External forces act only at the nodes. Therefore the
members are loaded only along their axis, in tension or compression, and not
in bending. In this chapter we describe a truss on the computer and use it
to build the matrix of the system of equations step by step.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can describe a plane truss on the computer by node coordinates,
  support nodes, a **member list** and a **force vector**.
* [ ] You can compute the **member stiffness** $k = EA/L$ and explain why a
  member transmits forces only in the direction of its axis.
* [ ] You can assemble the **stiffness matrix** of a truss with a function
  and explain why it is singular without supports.
```

## How do we describe a truss on the computer?

Our example is a swing set. The top beam, from which the swings hang, rests
at each end on an A-frame made of two inclined steel bars. We look at one of
these A-frames from the side. In this view, the swings also move back and
forth. The two bars meet at the top in node 1. There the top beam pushes
down with $2000\,\text{N}$, which already includes an allowance for the
swinging. The two feet, nodes 0 and 2, are held by fixed supports.

```{figure} pics/chap04_schaukelgestell_EN.svg
:alt: On the left, an A-frame of the swing set seen from the side with the top beam and a swinging swing; on the right, the model made of two members with three nodes, two supports and a load at the top node
:align: center
:label: fig_chap04_schaukelgestell

An A-frame of the swing set seen from the side and its model as a plane
truss with three nodes and two members.
(Source: own figure; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

For the calculation we need four pieces of information: Where are the nodes?
Which nodes are supported? Which nodes are connected by a member? Which
forces act? We translate this directly into Python.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# node coordinates in m: row n contains [x, y] of node n
node_pos = np.array([
    [0.0, 0.0],   # node 0: left foot
    [1.0, 2.0],   # node 1: apex, the top beam rests here
    [2.0, 0.0],   # node 2: right foot
])
num_nodes = len(node_pos)

# support nodes: these nodes cannot move
support_indices = [0, 2]

# member list: row s contains the numbers of the two nodes of member s
members = np.array([
    [0, 1],   # member 0 connects node 0 and node 1
    [1, 2],   # member 1 connects node 1 and node 2
])

# force vector in N: [F_0x, F_0y, F_1x, F_1y, F_2x, F_2y]
force_vector = np.zeros(2 * num_nodes)
force_vector[3] = -2000.0   # Fy at node 1: 2000 N downward

print('Number of nodes:  ', num_nodes)
print('Number of members:', len(members))
print('Force vector:     ', force_vector)
```

The node coordinates are stored in a 2D array with one row per node. With
`node_pos[1]` we get the whole row, i.e. both coordinates of node 1. The
**member list** `members` works the same way: each row is a member and
contains the numbers of the two nodes it connects.

We have to look more closely at the **force vector**. Each node can move in
the $x$- and in the $y$-direction. These two possible movements are called
**degrees of freedom**. Three nodes therefore have six degrees of freedom,
and the force vector has six entries. They are sorted node by node: first
$x$ and $y$ of node 0, then of node 1, and so on. In general:

- index $2n$ belongs to the $x$-direction of node $n$,
- index $2n+1$ belongs to the $y$-direction of node $n$.

The load at node 1 in the $y$-direction is therefore at index
$2 \cdot 1 + 1 = 3$. The minus sign means: the force points downward, i.e.
against the $y$-axis.

Before we compute anything, we plot the truss. That way, typos in the
coordinates or in the member list stand out immediately. The plotting
function is given. We simply run the cell and do not need to understand the
code in detail.

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
plot_truss(node_pos, members, support_indices, force_vector=force_vector,
           title='Swing set')
```

The plot matches the sketch: two members, two supports, one downward load at
node 1. We simplify as follows: both supports are **pin supports** like
support A in Chapter 3.2; they hold the node in place in the $x$- and in the
$y$-direction.

```{admonition} Mini-exercise (✩)
:class: tip
1. Answer without code: what does `node_pos[2]` return, and what does
   `members[1]` return? What do the values mean for the truss?
2. Answer without code: at which index of `force_vector` is the force in the
   $x$-direction at node 2?
3. When people swing, the top beam also pushes sideways. Create a new force
   vector `force_vector_new` in which a force of $1200\,\text{N}$ to the
   right acts at node 1 in addition to the load. Plot the truss with this
   force vector.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# task 3: lateral force from swinging in addition to the load at node 1
force_vector_new = np.zeros(2 * num_nodes)
force_vector_new[2] = 1200.0    # Fx at node 1: index 2 * 1 = 2
force_vector_new[3] = -2000.0   # Fy at node 1: index 2 * 1 + 1 = 3
print('New force vector:', force_vector_new)

plot_truss(node_pos, members, support_indices,
           force_vector=force_vector_new, title='Swing set while swinging')
```
`node_pos[2]` returns `[2. 0.]`, i.e. the coordinates of node 2:
$x = 2\,\text{m}$, $y = 0\,\text{m}$. `members[1]` returns `[1 2]`: member 1
connects node 1 with node 2. The $x$-force at node 2 is at index
$2 \cdot 2 = 4$. The lateral force at node 1 belongs at index
$2 \cdot 1 = 2$. In the plot, the force arrow now points diagonally down and
to the right, because it shows the sum of both forces. The label therefore
gives the magnitude $\sqrt{1200^2 + 2000^2}\,\text{N} \approx 2332\,\text{N}$.
````

## A member acts like a spring

So far our truss only describes the geometry and the load. With this
information we could even solve the swing set by hand: at each of the three
nodes, two equilibrium conditions hold. That gives six equations for six
unknowns, namely two member forces and four support reactions. For many
trusses, however, this is not enough. If a truss has more members or
supports than necessary, there are more unknowns than equilibrium
conditions. Such a truss is called **statically indeterminate**. In
addition, we want to know how far the apex sinks under the load. Both become
possible once we also take into account how the members deform.

How much a member deforms under load depends on the material. Under tension
or compression, a member behaves like a spring. From Hooke's law
$\sigma = E\,\varepsilon$ with the stress $\sigma = F/A$ and the strain
$\varepsilon = \Delta L/L$ it follows that

$$F = \frac{E\,A}{L} \cdot \Delta L = k \cdot \Delta L.$$

The **member stiffness** $k = EA/L$ is therefore the spring constant of the
member. A thick, short member made of a stiff material is a stiff spring.

```{figure} pics/chap04_federanalogie_EN.svg
:alt: A member with length L, cross-sectional area A and Young's modulus E next to a spring with spring constant k equal to EA over L
:align: center
:label: fig_chap04_federanalogie

A member under tension or compression behaves like a linear spring with the
spring constant $k = EA/L$.
(Source: own figure; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

Our members are made of steel and have a circular cross-section with a
diameter of $1\,\text{cm}$. For the stiffness we still need the member
length. We pick out member 0. We compute its length from the coordinates of
the two nodes it connects: first the difference vector, then the length
with Pythagoras, $L = \sqrt{\Delta x^2 + \Delta y^2}$.

```{figure} pics/chap04_stabgeometrie_EN.svg
:alt: Member 0 of the swing set with length L, angle phi and the components Delta x and Delta y
:align: center
:label: fig_chap04_stabgeometrie

The difference vector from node 0 to node 1 has the components $\Delta x$
and $\Delta y$, the length $L$ and the angle $\varphi$ to the $x$-axis.
(Source: own figure; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

```{code-cell} python
# material and cross-section, the same for all members
youngs_modulus = 2.1e11                    # steel in N/m²
diameter = 0.01                            # in m
area = np.pi * diameter**2 / 4             # circular area in m²

# member 0: get the node numbers from the member list
i, j = members[0]

# difference vector from node i to node j and member length (Pythagoras)
difference = node_pos[j] - node_pos[i]
length = np.sqrt(difference[0]**2 + difference[1]**2)

# member stiffness k = E * A / L
k = youngs_modulus * area / length

print(f'Member 0 connects nodes {i} and {j}')
print(f'Difference vector: {difference} m')
print(f'Member length:     {length:.4f} m')
print(f'Stiffness k:       {k:.4e} N/m = {k * 1e-6:.2f} kN/mm')
```

The line `i, j = members[0]` unpacks the two node numbers into two
variables, just as we unpacked the solution into `T_AB, T_BC, Q` in
Chapter 3.3.

Our steel member has $k \approx 7.38\,\text{kN/mm}$: to stretch it by one
millimeter, we need a force of about $7.4\,\text{kN}$.

Unlike a spring lying on a table, our member is inclined in the plane.
Nevertheless, it transmits forces only in the direction of its axis. The
reason: forces act on the member only at its two ends, because external
loads act only at the nodes, and the pins transmit no moment. For the member
to be in equilibrium, both forces must be equal in magnitude, opposite in
direction and lie on one line; otherwise they would rotate the member. This
line is the member axis. We describe its direction by the **unit vector**
$\vec{e}$, the difference vector divided by the member length.

What happens if node 1 moves down by $1\,\text{mm}$? Only the part of the
displacement in the direction of the member changes its length; the part
perpendicular to it merely rotates the member slightly. The following figure
shows this for our member 0, with the displacement greatly exaggerated.
Node 0 is fixed, and node 1 moves by $\vec{u}_1$ to the new position $1'$.
We split the displacement into the component $u^{\parallel}$ along the member
axis and the component $u^{\perp}$ perpendicular to it. Only $u^{\parallel}$
changes the member length, so it is exactly the change in length $\Delta L$.
Here $u^{\parallel}$ points against $\vec{e}$, so the member gets shorter.

```{figure} pics/chap04_projektion_EN.svg
:alt: Member 0 of the swing set with the downward displacement of node 1, split into a component along the member axis and a component perpendicular to it
:align: center
:label: fig_chap04_projektion

Only the component $u^{\parallel}$ of the displacement along the member axis
$\vec{e}$ changes the member length and produces a force.
(Source: own figure; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

The force $\vec{F}_1$ in the figure carries the index 1 because it acts at
node 1. For a displacement $\vec{u}_1 = (u_x, u_y)^\top$ of node 1, the dot
product with $\vec{e}$ gives the component in the direction of the member,
i.e. the change in length. The spring equation then gives the force in the
direction of the member:

$$\Delta L = e_x\,u_x + e_y\,u_y, \qquad \vec{F}_1 = k\,\Delta L\,\vec{e}.$$

```{code-cell} python
# unit vector in the direction of the member axis (length 1)
e = difference / length

# node 1 moves down by 1 mm, node 0 stays in place
displacement_node1 = np.array([0.0, -0.001])   # in m

# change in length: only the component of the displacement along the member counts
delta_l = e[0] * displacement_node1[0] + e[1] * displacement_node1[1]

# external force at node 1 that produces this displacement: magnitude k * delta_l, direction e
force_node1 = k * delta_l * e

print(f'Unit vector e:            {e}')
print(f'Change in length:         {delta_l * 1000:.4f} mm')
print(f'External force at node 1: {force_node1} N')
```

The member gets shorter by only about $0.89\,\text{mm}$, not by the full
millimeter, because the displacement points straight down, while the member
points diagonally upward. The force points along the member, down and to the
left: it compresses the member. That is why it also has an $x$-component,
even though the node does not move sideways at all. This is the external
force needed to displace node 1 in this way. The member exerts a force of
equal magnitude in the opposite direction on the node.

We could repeat this calculation for any displacement. It is easier with a
$2 \times 2$ matrix that contains the whole relationship at once. To get it,
we substitute $\Delta L$ into $\vec{F}_1$ and write the result as a matrix
times a vector:

$$\vec{F}_1 = k\,(e_x u_x + e_y u_y) \begin{pmatrix} e_x \\ e_y \end{pmatrix}
= k \begin{pmatrix} e_x e_x & e_x e_y \\ e_y e_x & e_y e_y \end{pmatrix}
\begin{pmatrix} u_x \\ u_y \end{pmatrix}.$$

We call this matrix the **stiffness block** $\mathbf{b}$ of the member. With
the angle $\varphi$ from the
[figure of the member geometry](#fig_chap04_stabgeometrie),
$\vec{e} = (\cos\varphi, \sin\varphi)^\top$, and the block reads

$$\mathbf{b} = k \begin{pmatrix}
\cos^2\varphi & \cos\varphi\,\sin\varphi \\
\cos\varphi\,\sin\varphi & \sin^2\varphi
\end{pmatrix}.$$

We never have to compute the angle itself, because the entries of `e`
already are $\cos\varphi$ and $\sin\varphi$. In the code we therefore build
the block directly from `e` and check whether it gives the same force as
before.

```{code-cell} python
# stiffness block of the member: converts a displacement into a force
block = k * np.array([
    [e[0] * e[0], e[0] * e[1]],
    [e[1] * e[0], e[1] * e[1]],
])

print('Stiffness block in kN/mm:')
print(np.round(block * 1e-6, 2))
print('block @ displacement:', block @ displacement_node1, 'N')
```

The product `block @ displacement_node1` gives exactly the force from above.
For our member, $\vec{e} \approx (0.447, 0.894)^\top$, so
$\cos^2\varphi = 0.2$, $\cos\varphi\,\sin\varphi = 0.4$ and
$\sin^2\varphi = 0.8$. The block therefore contains $0.2\,k$, $0.4\,k$ and
$0.8\,k$, i.e. $1.48$, $2.95$ and $5.90\,\text{kN/mm}$. The bottom-right
entry is the largest: the member is steep and therefore stiffest in the
$y$-direction.

```{admonition} Mini-exercise (✩)
:class: tip
1. Compute the length, the stiffness $k$ and the stiffness block for
   member 1.
2. Answer without code: why does the block of member 1 have a different sign
   on the off-diagonal than the block of member 0?
3. Answer without code: a horizontal member has the unit vector
   $\vec{e} = (1, 0)^\top$. Which entries of its stiffness block are zero?
   What does that mean for a displacement perpendicular to the member?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# task 1: length, stiffness and stiffness block of member 1
i_member1, j_member1 = members[1]
difference_member1 = node_pos[j_member1] - node_pos[i_member1]
length_member1 = np.sqrt(difference_member1[0]**2 + difference_member1[1]**2)
k_member1 = youngs_modulus * area / length_member1
e_member1 = difference_member1 / length_member1

block_member1 = k_member1 * np.array([
    [e_member1[0] * e_member1[0], e_member1[0] * e_member1[1]],
    [e_member1[1] * e_member1[0], e_member1[1] * e_member1[1]],
])

print(f'Member length: {length_member1:.4f} m')
print(f'Stiffness k:   {k_member1 * 1e-6:.2f} kN/mm')
print(f'Unit vector:   {e_member1}')
print('Stiffness block in kN/mm:')
print(np.round(block_member1 * 1e-6, 2))
```
Member 1 is just as long as member 0 and therefore has the same stiffness.
However, it points from node 1 diagonally down and to the right, so
$\vec{e} \approx (0.447, -0.894)^\top$. This makes the product $e_x e_y$ on
the off-diagonal negative; the diagonal stays positive because it contains
squares.

For the horizontal member, $e_y = 0$. So all entries are zero except the
top-left one, and the block reads $k \begin{pmatrix} 1 & 0 \\ 0 & 0
\end{pmatrix}$. A small displacement perpendicular to the member does not
change its length and therefore produces no force.
````

## From members to the stiffness matrix

Each member gives a stiffness block. Now we combine all blocks into one
large matrix that describes the whole truss, the **stiffness matrix**
$\mathbf{K}$. It has one row and one column for each degree of freedom, so
$6 \times 6$ entries for the swing set. It relates the displacements of all
nodes to the forces at all nodes:

$$\mathbf{K} \cdot \vec{u} = \vec{F}.$$

The displacement vector $\vec{u}$ is sorted in the same way as the force
vector: index $2n$ belongs to the $x$-displacement of node $n$, index $2n+1$
to the $y$-displacement.

So far node 0 stayed fixed, and only node 1 moved. In a truss, both end
nodes $i$ and $j$ of a member can move. The force in the member, however,
depends only on how far the two end nodes move *relative to each other*. If
both move the same distance in the same direction, the member length stays
the same, and no force arises. For the forces at nodes $i$ and $j$ we
therefore have

$$\vec{F}_i = \mathbf{b}\,(\vec{u}_i - \vec{u}_j), \qquad
\vec{F}_j = \mathbf{b}\,(\vec{u}_j - \vec{u}_i).$$

If node $i$ is fixed, i.e. $\vec{u}_i = \vec{0}$, then
$\vec{F}_j = \mathbf{b}\,\vec{u}_j$ remains. That is exactly our calculation
for member 0 from the last section. If we expand the parentheses, we see
where the block ends up in $\mathbf{K}$:

$$\begin{pmatrix} \vec{F}_i \\ \vec{F}_j \end{pmatrix} =
\begin{pmatrix} \mathbf{b} & -\mathbf{b} \\ -\mathbf{b} & \mathbf{b} \end{pmatrix}
\begin{pmatrix} \vec{u}_i \\ \vec{u}_j \end{pmatrix}.$$

Each member therefore adds $+\mathbf{b}$ to the two **diagonal blocks**
$(i, i)$ and $(j, j)$ and $-\mathbf{b}$ to the two **off-diagonal blocks**
$(i, j)$ and $(j, i)$.

To add the blocks, we need a new tool, **slicing**. The expression
`K[0:2, 2:4]` selects rows 0 and 1 and columns 2 and 3, i.e. a $2 \times 2$
block. As with `range`, the upper bound is not included. Member 0 connects
node 0 with node 1. Node 0 occupies rows and columns 0 and 1, node 1 rows
and columns 2 and 3. We first add the block of member 0 by hand.

```{code-cell} python
# empty matrix: one row and one column per degree of freedom
K_member0 = np.zeros((2 * num_nodes, 2 * num_nodes))

# member 0 connects node 0 (rows/columns 0:2) with node 1 (rows/columns 2:4)
K_member0[0:2, 0:2] += block   # diagonal block (0, 0)
K_member0[2:4, 2:4] += block   # diagonal block (1, 1)
K_member0[0:2, 2:4] -= block   # off-diagonal block (0, 1)
K_member0[2:4, 0:2] -= block   # off-diagonal block (1, 0)

print('Contribution of member 0 in kN/mm:')
print(np.round(K_member0 * 1e-6, 2))
```

Member 0 fills only the rows and columns of node 0 and node 1. Node 2 is not
attached to member 0, so its rows and columns remain zero. For member 1 we
would have to repeat the same with node 1 and node 2, i.e. with the ranges
`2:4` and `4:6`. For a truss with dozens of members this would be very
tedious. We therefore replace the fixed bounds: node $n$ occupies rows and
columns $2n$ and $2n+1$, i.e. the range `2*n : 2*n + 2`. With this we add
all members in a loop over the member list. Since we need this for every
truss, we write a function right away. In the loop we compute exactly what
we did by hand for member 0.

```{code-cell} python
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

K = assemble_stiffness_matrix(node_pos, members, youngs_modulus, area)

print('Stiffness matrix K in kN/mm:')
print(np.round(K * 1e-6, 2))
```

The first two rows match the contribution of member 0. In the rows and
columns of node 1, on the other hand, both members meet. Let us take a
closer look at the block of node 1.

```{code-cell} python
# the 2x2 block of node 1: rows 2 and 3, columns 2 and 3
print('K[2:4, 2:4] in kN/mm:')
print(np.round(K[2:4, 2:4] * 1e-6, 2))
```

In the block of node 1, the contributions of both members add up. That is
why the function uses `+=` and not `=`: with `=`, member 1 would overwrite
the contribution of member 0. The off-diagonal entries cancel because the
two members are mirror images of each other. What remains is a stiffness of
$2.95\,\text{kN/mm}$ in the $x$-direction and $11.80\,\text{kN/mm}$ in the
$y$-direction. Vertically, the apex is therefore four times as stiff as
horizontally, because both members are steep. Where no member connects two
nodes, a zero block remains.

```{figure} pics/chap04_blockstruktur_EN.svg
:alt: The stiffness matrix as a 3 by 3 grid of 2 by 2 blocks with diagonal blocks, off-diagonal blocks and two zero blocks
:align: center
:label: fig_chap04_blockstruktur

Block structure of the stiffness matrix of the swing set: there is no
member between node 0 and node 2, so these blocks are zero.
(Source: own figure; license [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0))
```

Can we now simply solve $\mathbf{K} \cdot \vec{u} = \vec{F}$ with
`np.linalg.solve`? We check solvability with the determinant, as in
Chapter 3.1. In addition, as a test, we shift the whole truss
$1\,\text{mm}$ to the right.

```{code-cell} python
print(f'Determinant of K: {np.linalg.det(K):.4e}')

# all three nodes move 1 mm to the right
u_rigid = np.array([0.001, 0.0, 0.001, 0.0, 0.001, 0.0])
print('K @ u_rigid:', K @ u_rigid, 'N')
```

The determinant is zero or, within rounding errors, tiny. So the matrix is
**singular**. The second calculation shows one reason: if we shift the whole
truss, no member length changes, and no force arises. The printed values on
the order of $10^{-14}\,\text{N}$ are rounding errors; physically, this is
zero. Shifting to the right is not the only such motion. We will meet more
of them in Chapter 4.2. Without supports, the truss could slide away, and
for a given load there would be no unique displacement. The supports are not
yet included in the system of equations. In Chapter 4.3 we prescribe zero
displacement at the support nodes.

```{admonition} Mini-exercise (✩)
:class: tip
1. Answer without code: why is the block `K[0:2, 4:6]` zero?
2. Answer without code: why does the block `K[0:2, 0:2]` match the
   stiffness block of member 0 exactly?
3. We close the triangle with a third member between node 0 and node 2.
   Create a new member list `members_new` for this, assemble the stiffness
   matrix again and print `K_new[0:2, 4:6]`. What has changed?
4. First answer without code: is `K_new` now nonsingular because the
   triangle is closed? Then check your answer with the determinant.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# task 3: third member between node 0 and node 2
members_new = np.array([
    [0, 1],
    [1, 2],
    [0, 2],   # new member between the two support nodes
])
K_new = assemble_stiffness_matrix(node_pos, members_new, youngs_modulus, area)

print('K_new[0:2, 4:6] in kN/mm:')
print(np.round(K_new[0:2, 4:6] * 1e-6, 2))

# task 4: check solvability with the closed triangle
print(f'Determinant of K_new: {np.linalg.det(K_new):.4e}')
```
The block `K[0:2, 4:6]` links the degrees of freedom of node 0 with those of
node 2. In the swing set there is no member between these nodes, so the
function adds nothing there. Only member 0 is attached to node 0, so its
diagonal block contains only the stiffness block of member 0.

With the new member, `K_new[0:2, 4:6]` is no longer zero. The member is
horizontal and $2\,\text{m}$ long, and its stiffness is
$k = 8.25\,\text{kN/mm}$. The block therefore contains only one entry, in
the top left, namely $-8.25\,\text{kN/mm}$. The minus sign comes from the
off-diagonal block.

`K_new` is also singular; the determinant is zero. The new member only
prevents node 0 and node 2 from moving relative to each other. We can still
shift the whole triangle to the right without any member length changing,
exactly as above with `u_rigid`. So the matrix is singular because of the
missing supports, not because of a missing member.
````

## Summary and outlook

We describe a plane truss by four data structures: the node coordinates, the
support nodes, the member list and the force vector. Each node has two
degrees of freedom; node $n$ occupies the indices $2n$ and $2n+1$. Each
member acts like a spring with the stiffness $k = EA/L$ and gives a
$2 \times 2$ stiffness block. The function `assemble_stiffness_matrix` uses
slicing to add each block to the stiffness matrix $\mathbf{K}$, positive on
the diagonal blocks and negative on the off-diagonal blocks. Without
supports, $\mathbf{K}$ is singular, because the truss can move without any
force arising.

In the next chapter we apply the function in pairs to a larger truss, a wall
bracket for a pipe. In Chapter 4.3 we then add the supports, solve the
system of equations and compute how far the apex of the swing set sinks and
whether it can carry the load.
