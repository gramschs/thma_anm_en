---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Excursus: Modeling a Wheatstone Bridge

This chapter is an optional excursus. It uses an electrical circuit to show
that the path from the physical equations to the matrix is always the same,
and it introduces the **rank** as the general criterion for the solvability
of a system of equations.

In Chapter 3.3 we set up a system of equations from energy balances. For
electrical circuits we instead use **Kirchhoff's laws**. As an example we
model a **Wheatstone bridge**: three resistors are known reference
resistors, the fourth, $R_4$, is a measuring resistor whose value changes
due to a physical influence, for example strain in a strain gauge. If all
four resistors are in a certain ratio, the bridge current $I$ through the
bridge resistor $R_B$ is zero, and the bridge is **balanced**. Any deviation
produces a measurable current.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can turn Kirchhoff's current law and voltage law into an LSE
  $\mathbf{A} \cdot \vec{x} = \vec{b}$.
* [ ] You can use `np.linalg.matrix_rank` to determine the rank of a matrix
  and read off from it whether an LSE has exactly one, no, or infinitely
  many solutions.
* [ ] You can carry out a parameter study over a resistor and determine the
  balance point of the bridge.
```

## From Kirchhoff's laws to the system of equations

```{figure} pics/wheatstone_bruecke.svg
:alt: Wheatstone bridge circuit with current directions marked
:align: center
:width: 75%

Wheatstone bridge with the four resistors $R_1, R_2, R_3, R_4$, the bridge
resistor $R_B$ and the voltage source $U_0$. The arrows show the assumed
reference directions of the six currents.
(Source: own figure; license [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0))
```

The bridge has six unknown currents:
$\vec{x} = (I_0,\ I_1,\ I_2,\ I_3,\ I_4,\ I)^\top$. So we need six equations.

**Kirchhoff's current law** (conservation of charge) says: at every node,
the sum of the currents flowing in equals the sum of the currents flowing
out. The three nodes give:

$$I_0 - I_1 - I_3 = 0 \qquad
I_1 - I_2 - I = 0 \qquad
I_3 + I - I_4 = 0$$

**Kirchhoff's voltage law** (conservation of energy) says: around any
closed loop, the sum of the voltage drops $R \cdot I$ equals the source
voltage. The two outer loops and the cross loop give:

$$R_1 I_1 + R_2 I_2 = U_0 \qquad
R_3 I_3 + R_4 I_4 = U_0 \qquad
R_1 I_1 - R_3 I_3 - R_B I = 0$$

We turn these six equations into a matrix. We wrap this directly into a
function, so that we can vary $R_4$ easily later on.

```{code-cell} python
import numpy as np

R1 = 100.0   # ohm
R2 = 100.0   # ohm
R3 = 100.0   # ohm
RB = 10.0    # ohm (bridge resistor)
U0 = 10.0    # V

def solve_bridge(R4):
    """Solves the 6x6 system of equations of the Wheatstone bridge.

    R4: measuring resistor in ohm
    Returns: solution vector [I0, I1, I2, I3, I4, I] in amperes
    """
    A = np.array([
        [+1.0, -1.0,  0.0, -1.0,  0.0,  0.0],   # node 1
        [ 0.0, +1.0, -1.0,  0.0,  0.0, -1.0],   # node 2
        [ 0.0,  0.0,  0.0, +1.0, -1.0, +1.0],   # node 3
        [ 0.0,   R1,   R2,  0.0,  0.0,  0.0],   # loop 1
        [ 0.0,  0.0,  0.0,   R3,   R4,  0.0],   # loop 2
        [ 0.0,   R1,  0.0,  -R3,  0.0,  -RB],   # cross loop
    ])
    b = np.array([0.0, 0.0, 0.0, U0, U0, 0.0])
    return np.linalg.solve(A, b)

x = solve_bridge(R4=200.0)
I0, I1, I2, I3, I4, I = x

print(f'Total current I0 = {I0 * 1000:.2f} mA')
print(f'Bridge current I = {I * 1000:.4f} mA')
```

At $R_4 = 200\,\Omega$ a bridge current of about −15.6 mA flows. The
negative sign means that the current flows opposite to the assumed
reference direction.

```{admonition} Mini-exercise (✩)
:class: tip
1. Call `solve_bridge(R4=50.0)` and print the bridge current.
2. Answer without further code: at $R_4 = 200\,\Omega$ the bridge current
   is negative, at $R_4 = 50\,\Omega$ it is positive. What evidently
   happens for a value in between, and what does that mean for the bridge?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
x = solve_bridge(R4=50.0)
print(f'Bridge current I = {x[5] * 1000:.4f} mA')
```
At $R_4 = 50\,\Omega$ the bridge current is positive at about +22.7 mA,
while at $R_4 = 200\,\Omega$ it was negative. Somewhere in between it
changes sign and is zero at that point. At that value of $R_4$ the bridge
is balanced. We determine this point precisely further below.
````

## When does an LSE have no unique solution? The rank

For the six unknown currents we took exactly six equations: three nodes and
three loops. *What would have happened if we had added another loop
equation?* It would not have been new information, but a combination of the
existing ones. The system of equations would then have had more rows than
unknowns, without being any better determined.

How many equations really carry independent information is measured by the
**rank** of a matrix. In Chapter 3.1 we checked solvability using the
determinant. The rank is the more general criterion: it is also defined for
non-square matrices and additionally tells us whether a system that has no
unique solution has *no* solution or *infinitely many*.

For this we need, besides $\mathbf{A}$, also the **augmented coefficient
matrix** $[\mathbf{A} \mid \vec{b}]$: the matrix $\mathbf{A}$ with $\vec{b}$
as an extra column. In NumPy, `np.column_stack` appends it.

```{code-cell} python
# A uniquely solvable system
A = np.array([
    [2.0, 1.0, 1.0],
    [1.0, 3.0, 1.0],
    [1.0, 1.0, 4.0],
])
b = np.array([1.0, 2.0, 3.0])

Ab = np.column_stack((A, b))

n = A.shape[1]   # number of unknowns
print('Rank of A:      ', np.linalg.matrix_rank(A))
print('Rank of [A | b]:', np.linalg.matrix_rank(Ab))
print('Number of unknowns:', n)
```

For a system with $n$ unknowns, three cases apply:

| $\text{rank}(\mathbf{A})$ | $\text{rank}([\mathbf{A} \mid \vec{b}])$ | Solvability |
| :---: | :---: | :--- |
| $= n$ | $= n$ | exactly one solution |
| $< n$ | $= \text{rank}(\mathbf{A})$ | infinitely many solutions |
| $< n$ | $> \text{rank}(\mathbf{A})$ | no solution |

We look at the two non-unique cases using a matrix whose second row is
twice the first:

```{code-cell} python
A = np.array([
    [1.0, 2.0, 1.0],
    [2.0, 4.0, 2.0],   # = 2 * row 1, no new information
    [0.0, 1.0, 1.0],
])

b_contradictory = np.array([3.0, 7.0, 2.0])   # b[1] should be 2*b[0] = 6, but is 7
b_consistent = np.array([3.0, 6.0, 2.0])      # b[1] = 6 = 2*b[0], matches row 2 = 2*row 1

print('rank A:', np.linalg.matrix_rank(A))
print('with b_contradictory: rank [A|b] =',
      np.linalg.matrix_rank(np.column_stack((A, b_contradictory))))
print('with b_consistent:    rank [A|b] =',
      np.linalg.matrix_rank(np.column_stack((A, b_consistent))))
```

With `b_contradictory` the rank of the augmented matrix rises to 3, while
$\text{rank}(\mathbf{A}) = 2$ stays the same: the system has **no
solution**, the equations contradict each other. With `b_consistent` the
rank stays at 2: the system has **infinitely many solutions**, one unknown
remains freely choosable. We saw the same contradictory case in the bonus
exercise of Chapter 3.2: a beam without horizontal restraint.

```{admonition} Mini-exercise (✩)
:class: tip
Given

$$\mathbf{A} = \begin{pmatrix} 1 & 1 & 2 \\ 3 & 3 & 6 \\ 1 & 0 & 1 \end{pmatrix},
\qquad \vec{b} = \begin{pmatrix} 4 \\ 12 \\ 1 \end{pmatrix}.$$

1. Answer without code: which two rows of $\mathbf{A}$ are dependent on
   each other?
2. Determine $\text{rank}(\mathbf{A})$ and
   $\text{rank}([\mathbf{A} \mid \vec{b}])$ with `np.linalg.matrix_rank`.
   Which of the three cases applies?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([
    [1.0, 1.0, 2.0],
    [3.0, 3.0, 6.0],
    [1.0, 0.0, 1.0],
])
b = np.array([4.0, 12.0, 1.0])

n = A.shape[1]
rank_A = np.linalg.matrix_rank(A)
rank_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))

print(f'rank A = {rank_A}, rank [A|b] = {rank_Ab}, n = {n}')
```
Output: `rank A = 2, rank [A|b] = 2, n = 3`.

The second row of $\mathbf{A}$ is three times the first. Since
$b[1] = 3 \cdot b[0]$ also holds, nothing contradicts:
$\text{rank}(\mathbf{A}) = \text{rank}([\mathbf{A} \mid \vec{b}]) = 2 < 3$.
The system has infinitely many solutions.
````

## Parameter study: finding the balance point

Now we vary $R_4$ systematically and look for the value at which the bridge
current becomes zero. For each value of $R_4$ we solve a separate system of
equations.

```{code-cell} python
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

r4_values = np.linspace(10.0, 300.0, 500)
i_values = np.zeros(500)
p_values = np.zeros(500)

for k, r4 in enumerate(r4_values):
    current = solve_bridge(r4)[5]
    i_values[k] = current
    p_values[k] = RB * current**2   # power dissipation P = R_B * I^2

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(7, 7), sharex=True)

ax[0].plot(r4_values, i_values * 1000)
ax[0].axhline(0, color='gray', linestyle='dashed', linewidth=1)
ax[0].set_ylabel('Bridge current in mA')
ax[0].set_title('Wheatstone bridge: bridge current and power dissipation')
ax[0].grid(True)

ax[1].plot(r4_values, p_values * 1000)
ax[1].set_xlabel('Measuring resistor R4 in ohm')
ax[1].set_ylabel('Power dissipation in mW')
ax[1].grid(True)

plt.tight_layout()
plt.show()
```

The bridge current crosses the zero line, and the power dissipation touches
the x-axis there. We find the zero crossing with `np.argmin` over the
absolute value and compare it with the known balance condition
$R_4^\ast = R_2 \cdot R_3 / R_1$.

```{code-cell} python
k_zero = np.argmin(np.abs(i_values))
r4_balance = r4_values[k_zero]

r4_analytical = R2 * R3 / R1

print(f'numerical:  R4* = {r4_balance:.1f} ohm')
print(f'analytical: R4* = {r4_analytical:.1f} ohm')
```

The numerical value deviates slightly from the analytical one, because
`np.linspace` does not hit the root exactly. A finer grid reduces the
deviation.

```{admonition} Mini-exercise (✩)
:class: tip
1. In the parameter study, increase the number of sample points from 500
   to 2000. How does the numerically found balance value $R_4^\ast$
   change?
2. Answer without code: why does the power dissipation touch the x-axis at
   the root instead of crossing it?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
r4_fine = np.linspace(10.0, 300.0, 2000)
i_fine = np.array([solve_bridge(r4)[5] for r4 in r4_fine])
print(f'R4* with 2000 sample points: {r4_fine[np.argmin(np.abs(i_fine))]:.2f} ohm')
```
With more sample points, the value found lies closer to the analytical
100 ohm. The power dissipation $P = R_B \cdot I^2$ contains the current
squared. A square is never negative, so $P$ cannot cross the x-axis. At the
root of the current, $P$ becomes exactly zero and touches the axis.
````

## Summary

The model of the Wheatstone bridge consists of six Kirchhoff equations for
six unknown currents. The **rank** of $\mathbf{A}$ and the augmented matrix
$[\mathbf{A} \mid \vec{b}]$ tells us whether a system of equations has
exactly one, no, or infinitely many solutions, and is therefore more
general than the determinant test. With a parameter study over $R_4$ and
`np.argmin` we determined the balance point of the bridge and confirmed it
with the analytical formula.

The second excursus, in Chapter 3.7, shifts perspective: there we
investigate how the runtime of `np.linalg.solve` grows with the size of the
system of equations.
