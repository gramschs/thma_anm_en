---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 4.3 Displacements and Forces in a Truss

In Chapter 4.1 we assembled the stiffness matrix of the swing set, and in
Chapter 4.2 that of a wall bracket. Both times the matrix was singular,
because the supports were still missing from the system of equations. In
this chapter we add the supports and solve the system of equations. *How
far does the apex of the swing set sink under the load, and can the
structure carry the load at all?*

## Adding supports and solving the system of equations

We reuse the swing set and the function `assemble_stiffness_matrix`
from Chapter 4.1. The first cell again contains the given plotting
function.

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

```{code-cell} python
# swing set from Chapter 4.1
node_pos = np.array([
    [0.0, 0.0],   # node 0: left foot
    [1.0, 2.0],   # node 1: apex, the top beam rests here
    [2.0, 0.0],   # node 2: right foot
])
num_nodes = len(node_pos)
support_indices = [0, 2]
members = np.array([
    [0, 1],   # member 0
    [1, 2],   # member 1
])
force_vector = np.zeros(2 * num_nodes)
force_vector[3] = -2000.0   # Fy at node 1: 2000 N downward

youngs_modulus = 2.1e11                  # steel in N/m²
diameter = 0.01                          # in m
area = np.pi * diameter**2 / 4           # in m²

K = assemble_stiffness_matrix(node_pos, members, youngs_modulus, area)
```

The system of equations $\mathbf{K} \cdot \vec{u} = \vec{F}$ has six
equations, one for each degree of freedom. For the support nodes, however,
we already know the displacement, namely zero. We therefore replace the
equations of the constrained degrees of freedom with exactly this condition.

```{code-cell} python
# make copies so that K and force_vector stay unchanged
K_supported = K.copy()
force_supported = force_vector.copy()

# replace the equations of the constrained degrees of freedom with u_d = 0
for n in support_indices:
    for d in [2 * n, 2 * n + 1]:
        # TODO: ???   set the whole row d of K_supported to zero
        # TODO: ???   set the diagonal entry of row d to one: 1 * u_d ...
        # TODO: ???   set entry d of the right-hand side to zero: ... = 0

print('K_supported in kN/mm:')
print(np.round(K_supported * 1e-6, 2))
print('Row 0 of K_supported in N/m:', K_supported[0])
print(f'Determinant of K_supported: {np.linalg.det(K_supported):.4e}')
```

In `K_supported`, rows 0, 1, 4 and 5 are replaced. Each of these rows now
contains only a one on the diagonal, and the right-hand side is zero. So
the row simply says $u_d = 0$. In the matrix printed in kN/mm, the ones
appear as `0.`, because we multiply all entries by $10^{-6}$. The last
output shows row 0 in N/m. The determinant is no longer zero, so the system
is solvable. Because we only replaced rows, `K_supported` is no longer
symmetric. For `np.linalg.solve` this does not matter.

The method `.copy()` is important. Without it, `K_supported` and `K` would
refer to the same array, and we would overwrite the original stiffness
matrix. But we still need it shortly for the support reactions.

```{code-cell} python
# TODO: ???   solve the system with supports and store the displacements in u

print('Displacements in mm:')
for n in range(num_nodes):
    print(f'  Node {n}: ux = {u[2*n] * 1000:8.4f} mm,  uy = {u[2*n + 1] * 1000:8.4f} mm')
```

The apex sinks by $0.17\,\text{mm}$ and does not move sideways. This is
consistent with the symmetry: both members are identical and mirror images
of each other, and the load points straight down. We can even check the
value by hand. In
Chapter 4.1 we saw that the block of node 1 has entries only on the
diagonal. In the $y$-direction the apex has the stiffness
$11.80\,\text{kN/mm}$. So
$u_y = -2\,\text{kN} / 11.80\,\text{kN/mm} = -0.17\,\text{mm}$.

We need these steps again for every truss. We therefore combine them in a
function.

```{code-cell} python
def compute_displacements(K, force_vector, support_indices):
    """Solves K * u = F for a truss with pin supports.

    K: stiffness matrix in N/m
    force_vector: external node forces in N
    support_indices: list of supported nodes, where ux = uy = 0
    Returns: displacement vector u in m
    """
    K_supported = K.copy()
    force_supported = force_vector.copy()
    for n in support_indices:
        for d in [2 * n, 2 * n + 1]:
            K_supported[d, :] = 0.0
            K_supported[d, d] = 1.0
            force_supported[d] = 0.0
    return np.linalg.solve(K_supported, force_supported)

u = compute_displacements(K, force_vector, support_indices)
print('Displacement vector in mm:', np.round(u * 1000, 4))
```

## Which forces act in the supports and in the members?

We now know the displacements. If we substitute them into the original
equation $\vec{F} = \mathbf{K} \cdot \vec{u}$, we get the external forces
at all nodes.

```{code-cell} python
# node forces from the original stiffness matrix
# TODO: ???   compute the node forces and store them in node_forces

print('Node forces in N:')
for n in range(num_nodes):
    print(f'  Node {n}: Fx = {node_forces[2*n]:8.1f} N,  Fy = {node_forces[2*n + 1]:8.1f} N')

print(f'Sum Fx: {np.sum(node_forces[0::2]):.1f} N')
print(f'Sum Fy: {np.sum(node_forces[1::2]):.1f} N')
```

At node 1 we get exactly the load we prescribed. That is our check. At the
support nodes 0 and 2 we find the **support reactions**, i.e. the forces
with which the supports hold the truss in place. Each support carries half
of the load upward. In addition, the left support pushes to the right with
$500\,\text{N}$ and the right one to the left with $500\,\text{N}$. All
forces together add up to zero, so the truss is in equilibrium like the
beam in Chapter 3.2. The expression `node_forces[0::2]` selects every
second entry starting at index 0, i.e. all $x$-forces.

For the design we want to know how heavily each individual member is
loaded. The **member force** $N$ follows directly from the spring equation
of Chapter 4.1: $N = k \cdot \Delta L$. As in the
[figure on splitting the displacement](#fig_chap04_projektion) from
Chapter 4.1, the change in length $\Delta L$ is the component of the
displacement in the direction of the member. This time, however, both ends
of the member can move. What counts is therefore the displacement of
node $j$ relative to node $i$, i.e. $\vec{u}_j - \vec{u}_i$.

```{code-cell} python
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
        # TODO: ???   compute the displacement of node j relative to node i and store it in u_relative

        # change in length = component along the member, member force N = k * delta_l
        # TODO: ???   compute the change in length of member s and store it in delta_l
        member_forces[s] = k * delta_l
    return member_forces

member_forces = compute_member_forces(node_pos, members, youngs_modulus,
                                      area, u)

for s in range(len(members)):
    if abs(member_forces[s]) < 1e-6:   # below 1 µN: just a rounding error
        kind = 'zero force'
    elif member_forces[s] > 0:
        kind = 'tension'
    else:
        kind = 'compression'
    print(f'Member {s}: N = {member_forces[s]:8.1f} N  ({kind})')
```

Both members carry $1118\,\text{N}$ in **compression**. A positive member
force means tension: the member gets longer. A negative member force means
compression: the member gets shorter. The result is plausible: the load
pushes the apex down, the apex moves closer to the two supports, and both
members are compressed. The member force is larger than half the load
because the members are inclined. Each member has to carry $1000\,\text{N}$
in the vertical direction. Of its force, however, only the fraction
$\sin\varphi = 2/\sqrt{5} \approx 0.894$ points upward. The member force is
therefore larger: $1000\,\text{N} / 0.894 \approx 1118\,\text{N}$.

## Will the swing set hold?

First we show the result graphically. At less than one millimeter, the
displacements are much smaller than the members, which are over two meters
long. So that we can see anything at all, we magnify the displacements in
the plot by an **exaggeration factor**, here 2000. The calculation itself
does not change.

```{code-cell} python
plot_truss(node_pos, members, support_indices, force_vector=force_vector,
           displacement=u, scale=2000, member_forces=member_forces,
           title='Swing set, displacements exaggerated by a factor of 2000')
```

The dashed lines show the initial shape, the solid lines the exaggerated
deformed shape. Both members are red, so they are in compression.

Can the steel withstand these forces? To find out, we compute the
**stress** $\sigma = N/A$ and compare it with the yield strength. For
structural steel S235 it is $R_e = 235\,\text{N/mm}^2$.

```{code-cell} python
yield_strength = 235.0   # structural steel S235 in N/mm²

# stress sigma = N / A, converted from N/m² to N/mm²
# TODO: ???   compute the stresses of all members in N/mm² and store them in stresses

for s in range(len(members)):
    utilization = abs(stresses[s]) / yield_strength
    print(f'Member {s}: sigma = {stresses[s]:6.1f} N/mm²,  '
          f'utilization {utilization * 100:4.1f} %')
```

The stress is only about $14\,\text{N/mm}^2$, i.e. about 6 % of the yield
strength. Is the swing set therefore safe? *No, because for compression
members the stress alone is not a sufficient check.* A slender member under
compression can deflect sideways: it **buckles** long before the steel
starts to yield. From mechanics of materials we know the Euler buckling
load for this. For a member that is pinned at both ends, it is

$$F_\text{cr} = \frac{\pi^2\,E\,I}{L^2} \qquad \text{with} \qquad
I = \frac{\pi\,d^4}{64}$$

for a circular cross-section.

```{code-cell} python
# area moment of inertia of the circular cross-section in m^4
# TODO: ???   compute the area moment of inertia and store it in moment_of_inertia

# Euler buckling load for member 0 (both members have the same length)
length = np.sqrt(1.0**2 + 2.0**2)   # Pythagorean theorem with dx = 1 m, dy = 2 m
# TODO: ???   compute the Euler buckling load of member 0 and store it in buckling_load

print(f'Euler buckling load:         {buckling_load:8.1f} N')
print(f'Compressive force in member: {abs(member_forces[0]):8.1f} N')
```

The buckling load is only about $203\,\text{N}$, and the compressive force
is more than five times as large. The members with a diameter of
$1\,\text{cm}$ would therefore buckle, even though the stress is far below
the yield strength. The design of a truss therefore always requires both
checks: the stress for all members and buckling for all compression
members.

## Summary and outlook

We add the supports by replacing the equations of the constrained degrees of
freedom with $u_d = 0$. After that, the system of equations is solvable, and
`np.linalg.solve` gives all displacements. Substituting them into
$\mathbf{K} \cdot \vec{u}$ gives the support reactions at the supports. The
member forces follow from the change in length of each member: positive
means tension and negative means compression. For the design we compare the
stress with the yield strength and also check all compression members for
buckling.

All steps are now contained in three functions: `assemble_stiffness_matrix`,
`compute_displacements` and `compute_member_forces`. In the next chapter,
working in pairs, we use them to analyze and evaluate the roof truss of a
steel building under snow load.

## Mini-exercises

### Mini-exercise 1

1. Answer without code: which rows of `K_supported` would be replaced if
   only node 0 were supported?
2. When people swing, a lateral force of $1200\,\text{N}$ to the right acts
   at the apex in addition to the load. Create a new force vector
   `force_vector_side` and compute the displacements with
   `compute_displacements`.
3. Answer without code: the apex moves farther sideways than downward, even
   though the lateral force is smaller than the load. Why?

```{code-cell} python
# code cell
```

### Mini-exercise 2

1. Answer without code: why does the left support push to the right and not
   to the left?
2. Compute the member forces for the force vector with the lateral force
   from the last mini-exercise (load of $2000\,\text{N}$ downward and
   $1200\,\text{N}$ to the right at node 1). Which member is loaded more
   heavily? What do you notice about member 0?
3. Also compute the support reactions for this case. Which vertical force
   does the left support transmit? What does that mean for the swing set?

```{code-cell} python
# code cell
```

### Mini-exercise 3

1. Answer without code: what would you see in the plot if you chose
   `scale=1`?
2. We use members with a diameter of $2\,\text{cm}$. Use the three functions
   to recompute the stiffness matrix, the displacements and the member
   forces. Also compute the stress and the buckling load. Will the swing set
   hold now?
3. Answer without code: the deflection of the apex has dropped to a
   quarter, but the member forces have stayed the same. Why?

```{code-cell} python
# code cell
```
