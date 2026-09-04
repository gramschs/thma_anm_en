---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.2 Support Reactions of a Beam

In Chapter 3.1 we wrote a system of equations as a matrix equation, checked
its solvability, and solved it with `np.linalg.solve`. In this chapter we
apply the same approach to a problem from engineering mechanics: the support
reactions of a loaded beam. Work through the parts in pairs if possible, and
in order, since each part builds on the previous one.

We consider the following beam with a pin support and a roller support, on
which a cable force and a load act.

```{figure} pics/traeger_auflagerkraefte_EN.svg
:width: 75%
:align: center

Beam with pin support and roller support, cable force and load $F$.
```

```{admonition} Project: Support reactions of a beam (✩✩)
:class: tip
A horizontal beam of length $L = 4\,\text{m}$ is supported on the left at
point A by a **pin support** and on the right at point B by a **roller
support**. The pin support can carry a horizontal force $A_x$ and a vertical
force $A_y$, the roller support only a vertical force $B_y$. The x-axis
points to the right, the y-axis upward, and the origin is at A.

The beam is loaded by:

* a **cable force** at a distance of $1\,\text{m}$ from A, with components
  $6\,\text{kN}$ to the right and $8\,\text{kN}$ upward,
* a **load** $F = 12\,\text{kN}$ vertically downward at a distance of
  $3\,\text{m}$ from A.

We want to find the three support reactions $A_x$, $A_y$ and $B_y$.
```

```{admonition} Part 1: Set up the equilibrium conditions
:class: tip
For a rigid beam, three equilibrium conditions hold: the sum of all
horizontal forces is zero, the sum of all vertical forces is zero, and the
sum of all moments about point A is zero.

Set up the three equations with the numerical values from the project
statement. Use the sign convention: forces to the right and upward are
positive, moments counterclockwise are positive. The cable force acts at
the height of the beam axis, so its horizontal component produces no moment
about A.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 1
:class: tip
:class: dropdown
Sum of horizontal forces:

$$A_x + 6 = 0$$

Sum of vertical forces:

$$A_y + B_y + 8 - 12 = 0 \quad\Longrightarrow\quad A_y + B_y = 4$$

Sum of moments about A (lever arm times force, counterclockwise positive):

$$4 \cdot B_y + 1 \cdot 8 - 3 \cdot 12 = 0 \quad\Longrightarrow\quad 4\,B_y = 28$$

The vertical cable component ($8\,\text{kN}$ upward at a distance of
$1\,\text{m}$) produces a positive moment, the load ($12\,\text{kN}$
downward at a distance of $3\,\text{m}$) a negative one.
````

```{admonition} Part 2: Bring into matrix form and check solvability
:class: tip
Combine the three equations from Part 1 into the matrix equation
$\mathbf{A} \cdot \vec{x} = \vec{b}$, with the vector of unknowns
$\vec{x} = (A_x,\ A_y,\ B_y)^\top$. Create `A` as a two-dimensional array
and `b` as a one-dimensional array, and use the determinant to check
whether the system has a unique solution.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
import numpy as np

# unknowns: x = [A_x, A_y, B_y]
A = np.array([
    [1, 0, 0],   # sum Fx:  1*A_x + 0*A_y + 0*B_y = -6
    [0, 1, 1],   # sum Fy:  0*A_x + 1*A_y + 1*B_y =  4
    [0, 0, 4],   # sum M_A: 0*A_x + 0*A_y + 4*B_y = 28
], dtype=float)

b = np.array([-6.0, 4.0, 28.0])

det_A = np.linalg.det(A)
print(f'Determinant: {det_A:.1f}')
print('uniquely solvable:', not np.isclose(det_A, 0.0))
```
The determinant is 4.0 and therefore not zero. The system has exactly one
solution. The beam is **statically determinate**: it has exactly as many
support reactions as are needed to constrain it.
````

```{admonition} Part 3: Solve and check
:class: tip
Solve the system with `np.linalg.solve` and verify the result with a check.
Print the three support reactions in kN.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
x = np.linalg.solve(A, b)

print(f'A_x = {x[0]:.1f} kN')
print(f'A_y = {x[1]:.1f} kN')
print(f'B_y = {x[2]:.1f} kN')

print('Check passed:', np.allclose(A @ x, b))
```
The solution is $A_x = -6.0\,\text{kN}$, $A_y = -3.0\,\text{kN}$,
$B_y = 7.0\,\text{kN}$. The check passes.
````

```{admonition} Part 4: Interpret the result
:class: tip
Answer in your own words:

1. What does the negative sign of $A_x$ mean for the direction of the
   horizontal support reaction?
2. $A_y$ is also negative. In which direction does the vertical support
   reaction at the pin support point, and how does that fit with the cable
   force acting on the beam?
```

````{admonition} Solution Part 4
:class: tip
:class: dropdown
1. We had assumed $A_x$ to be a force pointing to the right. The result
   $A_x = -6\,\text{kN}$ means that the actual support reaction points to
   the left with $6\,\text{kN}$. It balances the horizontal cable
   component.
2. $A_y = -3\,\text{kN}$ means that the vertical support reaction at the
   pin support points downward. So the pin support is holding the beam
   down at this point. The reason is the cable force: it pulls upward with
   $8\,\text{kN}$, which near A is more than needed for equilibrium, so
   without the pin support the beam would lift off at this point.
````

```{admonition} Closing question
:class: tip
Suppose that at A there were a roller support instead of the pin support,
one that can only carry a vertical force **upward** (it can push, but not
pull). What would happen to the beam? Use your result from Part 3.
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
From Part 3 we know that the vertical support reaction at A points
downward ($A_y = -3\,\text{kN}$). A roller support that can only push is
not able to provide that. The beam would lift off at A and rotate about
support B until it hits another component or falls down. It would no
longer be in equilibrium. The mathematical model with three unknowns
therefore silently assumes that the pin support can carry forces in both
directions.
````

````{admonition} Bonus exercise: A beam without horizontal restraint (✩✩✩)
:class: tip
Now **both** supports are roller supports that can carry only vertical
forces. There are therefore only two unknown support reactions, $A_y$ and
$B_y$, but still three equilibrium conditions. The loading stays unchanged.

1. Write the three equations with the two unknowns as
   $\mathbf{A} \cdot \vec{x} = \vec{b}$. The matrix `A` then has three rows
   and two columns.
2. Try to solve the system with `np.linalg.solve`. What does Python report?
3. Consider the first equation ($\sum F_x = 0$) on its own. Can it be
   satisfied?
4. Explain physically why this beam cannot be in equilibrium.
````

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
```python
import numpy as np

# unknowns: x = [A_y, B_y]
A = np.array([
    [0, 0],   # sum Fx:  0*A_y + 0*B_y = -6
    [1, 1],   # sum Fy:  1*A_y + 1*B_y =  4
    [0, 4],   # sum M_A: 0*A_y + 4*B_y = 28
], dtype=float)

b = np.array([-6.0, 4.0, 28.0])

print('Shape of A:', A.shape)

try:
    x = np.linalg.solve(A, b)
except np.linalg.LinAlgError as error:
    print('solve fails:', error)
```
`np.linalg.solve` requires a square matrix and terminates with a
`LinAlgError` for the shape `(3, 2)`.

The first equation reads $0 \cdot A_y + 0 \cdot B_y = -6$, i.e. $0 = -6$.
That is a contradiction; no choice of $A_y$ and $B_y$ can satisfy it. The
system has **no solution**.

Physically this means: the horizontal cable component exerts a force of
$6\,\text{kN}$ to the right on the beam, but neither roller support can
provide a horizontal counterforce. The beam would slide away to the right;
it is a **kinematically unstable system** and not in equilibrium. For the
static analysis we need at least one support that can carry horizontal
forces.
````
