---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.3 Heat Transfer Through a Multilayer Wall

In Chapter 3.1 we solved linear systems of equations with NumPy, and in
Chapter 3.2 we computed the support reactions of a beam. Both times we set up
the equations by hand. Now we apply the same tool to a classic mechanical
engineering problem: an exterior wall made of three layers with different
thermal resistances. *What is the temperature at the interfaces, and how
large is the heat flow?*

We will see that the path from the physical equations to the matrix is
always the same: all unknowns on the left-hand side, all known quantities on
the right.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can rearrange physical balance equations so that all unknowns are
  on the left-hand side.
* [ ] You can read off the coefficient matrix $\mathbf{A}$ and the vector
  $\vec{b}$ from the rearranged equations.
* [ ] You can solve the LSE with `np.linalg.solve` and interpret the result
  physically, including a negative sign.
```

## The physical model

We consider a wall made of three layers A, B, C with thermal resistances
$R_A$, $R_B$, $R_C$ in K/W. On the left the temperature is $T_{LA}$, on the
right $T_{CR}$.

```{figure} pics/waermeuebertragung_mehrschichtwand_EN.svg
:alt: Cross-section of a three-layer wall with temperature profile and heat flow
:align: center
:label: fig_waermeuebertragung_mehrschichtwand

Temperature profile of a multilayer wall in the steady state (schematic
representation with equal geometric layer thickness). Since the heat flow
through all layers is the same, the slope of the temperature profile is
proportional to the thermal resistance of each layer, steepest in layer C
and flattest in layer B. (Source: own figure; license [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0))
```

In the **steady state** the heat flow $Q$ is the same through all layers.
The **heat transfer law**, analogous to Ohm's law, reads for each layer

$$Q = \frac{\Delta T_i}{R_i},$$

where $\Delta T_i$ is the temperature difference across the layer. With the
two unknown interface temperatures $T_{AB}$, $T_{BC}$ and the unknown heat
flow $Q$, this gives three equations:

$$\frac{T_{LA} - T_{AB}}{R_A} = Q \qquad (1)$$

$$\frac{T_{AB} - T_{BC}}{R_B} = Q \qquad (2)$$

$$\frac{T_{BC} - T_{CR}}{R_C} = Q \qquad (3)$$

```{admonition} Mini-exercise (✩)
:class: tip
1. Answer without code: why is the heat flow $Q$ the same in all three
   layers in the steady state? What would it mean if $Q$ in layer B were
   larger than in layer A?
2. For a single wall without intermediate layers,
   $Q = (T_{LA} - T_{CR}) / R_\text{total}$ with
   $R_\text{total} = R_A + R_B + R_C$. Compute this value for
   $R_A = 0.5$, $R_B = 0.3$, $R_C = 0.7$ (all in K/W), $T_{LA} = 293$ K and
   $T_{CR} = 273$ K.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
R_total = 0.5 + 0.3 + 0.7
Q = (293 - 273) / R_total
print(f'Total resistance: {R_total} K/W')
print(f'Heat flow Q:       {Q:.4f} W')
```
The heat flow is the same everywhere because in the steady state heat
neither accumulates nor disappears anywhere: whatever flows into a layer
must also flow back out. If $Q$ in layer B were larger than in layer A,
heat would continually disappear at the A-B interface, the temperature
there would drop, and the state would not be steady. The total resistance
is 1.5 K/W, and the heat flow is about 13.33 W. The system of equations
gives the same result right away.
````

## From the equations to matrix form

The three equations contain the unknowns in fractions. We bring all
unknowns to the left-hand side by multiplying each equation by $R_i$ and
rearranging:

$$T_{AB} + R_A \cdot Q = T_{LA} \qquad (1')$$

$$-T_{AB} + T_{BC} + R_B \cdot Q = 0 \qquad (2')$$

$$-T_{BC} + R_C \cdot Q = -T_{CR} \qquad (3')$$

Now we read off the coefficient matrix row by row. The solution vector is
$\vec{x} = (T_{AB},\ T_{BC},\ Q)^\top$:

$$\begin{pmatrix}
+1 &  0 & R_A \\
-1 & +1 & R_B \\
 0 & -1 & R_C
\end{pmatrix}
\cdot
\begin{pmatrix} T_{AB} \\ T_{BC} \\ Q \end{pmatrix}
=
\begin{pmatrix} T_{LA} \\ 0 \\ -T_{CR} \end{pmatrix}$$

Each rearranged equation gives one row of $\mathbf{A}$ and one entry in
$\vec{b}$. The coefficient of the $j$-th unknown in the $i$-th equation sits
in $A_{ij}$. Unknowns that do not appear in an equation get the coefficient
0.

```{admonition} Mini-exercise (✩)
:class: tip
Answer without code:

1. In the coefficient matrix, row 2, column 1 holds the value $-1$. Which
   equation does this entry come from, and why is it negative?
2. Why is the second entry of the right-hand side, $b[1]$, equal to zero?
   What does that mean physically?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
1. The entry $A_{21} = -1$ comes from equation (2'), which arises by
   rearranging $(T_{AB} - T_{BC}) / R_B = Q$. The temperature difference
   across layer B is $T_{AB} - T_{BC}$, where $T_{AB}$ has a positive sign.
   After multiplying by $R_B$ and sorting all unknowns to the left,
   $-T_{AB}$ remains, so the coefficient is $-1$.
2. $b[1] = 0$ because equation (2') contains no known temperature. The
   middle layer only borders the two interfaces, whose temperatures are
   themselves unknown. There is no externally given boundary condition for
   this equation.
````

## Implementation and solution

```{code-cell} python
import numpy as np

# given quantities
R_A = 0.5    # thermal resistance layer A in K/W
R_B = 0.3    # thermal resistance layer B in K/W
R_C = 0.7    # thermal resistance layer C in K/W
T_LA = 293.0    # temperature left side (inside) in K
T_CR = 273.0    # temperature right side (outside) in K

# coefficient matrix, unknowns x = [T_AB, T_BC, Q]
A = np.array([
    [+1.0,  0.0, R_A],   # equation (1'):  T_AB + R_A*Q = T_LA
    [-1.0, +1.0, R_B],   # equation (2'): -T_AB + T_BC + R_B*Q = 0
    [ 0.0, -1.0, R_C],   # equation (3'): -T_BC + R_C*Q = -T_CR
])
b = np.array([T_LA, 0.0, -T_CR])

# check solvability
det_A = np.linalg.det(A)
print(f'Determinant: {det_A:.4f}')

# solve
x = np.linalg.solve(A, b)
T_AB, T_BC, Q = x   # unpack the result into three variables

print(f'T_AB = {T_AB:.2f} K   (interface A-B)')
print(f'T_BC = {T_BC:.2f} K   (interface B-C)')
print(f'Q    = {Q:.4f} W   (heat flow)')

print('Check passed:', np.allclose(A @ x, b))
```

The heat flow $Q$ is positive. This matches our setup: the positive
direction points from left to right, and heat flows from the warmer left
side ($T_{LA} = 293$ K) to the colder right side ($T_{CR} = 273$ K). A
negative value would mean that the heat flows in the other direction.

As a check, we compute the temperature difference across each layer. Layer
C has the largest resistance and should therefore show the largest
temperature jump, just as the largest resistance in an electrical circuit
produces the largest voltage drop.

```{code-cell} python
delta_A = T_AB - T_LA
delta_B = T_BC - T_AB
delta_C = T_CR - T_BC

print(f'Temperature difference layer A (R = {R_A} K/W): {delta_A:.2f} K')
print(f'Temperature difference layer B (R = {R_B} K/W): {delta_B:.2f} K')
print(f'Temperature difference layer C (R = {R_C} K/W): {delta_C:.2f} K')
print(f'Sum: {delta_A + delta_B + delta_C:.2f} K '
      f'(must equal T_CR - T_LA = {T_CR - T_LA:.1f} K)')
```

```{admonition} Mini-exercise (✩)
:class: tip
A cold-storage wall keeps the inside at $T_\text{inside} = 268$ K (−5 °C),
while outside it is $T_\text{outside} = 293$ K (20 °C). The left side is the
inside ($T_{LA} = T_\text{inside}$), the right side the outside
($T_{CR} = T_\text{outside}$).

| Layer | Material | $R$ in K/W |
| --- | --- | --- |
| A | Concrete | 0.2 |
| B | Polyurethane foam | 1.8 |
| C | Sheet steel | 0.05 |

1. Answer without code: which layer will have the largest temperature drop?
2. Set up `A` and `b` with the new values, solve the system, and print
   $T_{AB}$, $T_{BC}$ and $Q$.
3. The heat flow comes out negative. Why?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

R_A = 0.2
R_B = 1.8
R_C = 0.05
T_LA = 268.0    # inside (cold)
T_CR = 293.0    # outside (warm)

A = np.array([
    [+1.0,  0.0, R_A],
    [-1.0, +1.0, R_B],
    [ 0.0, -1.0, R_C],
])
b = np.array([T_LA, 0.0, -T_CR])

x = np.linalg.solve(A, b)
T_AB, T_BC, Q = x

print(f'T_AB = {T_AB:.2f} K  ({T_AB - 273.15:.1f} °C)')
print(f'T_BC = {T_BC:.2f} K  ({T_BC - 273.15:.1f} °C)')
print(f'Q    = {Q:.4f} W')
print('Check passed:', np.allclose(A @ x, b))

print(f'Temperature drop layer A (concrete): {abs(T_AB - T_LA):.2f} K')
print(f'Temperature drop layer B (foam):     {abs(T_BC - T_AB):.2f} K')
print(f'Temperature drop layer C (steel):    {abs(T_CR - T_BC):.2f} K')
```
The largest temperature drop occurs in layer B, the polyurethane foam, at
about 22 K. Its thermal resistance, $R_B = 1.8$ K/W, is by far the largest.
That is exactly the point of thermal insulation: it takes on almost the
entire temperature difference between inside and outside.

The heat flow is negative (about −12.2 W) because we chose the positive
direction from left (inside) to right (outside), but the heat actually
flows from the warm outside into the cold storage room. Magnitude and sign
together are correct.
````

## Summary and outlook

The approach is always the same: rearrange the physical balance equations,
move all unknowns to the left, all known quantities to the right, then read
off $\mathbf{A}$ and $\vec{b}$ row by row. `np.linalg.solve` provides the
solution, `np.allclose` verifies it, and we interpret the sign of the result
through the chosen direction convention.

In the next chapter we extend this example: we add a fourth layer to the
wall and use a parameter study to investigate how much additional
insulation reduces the heat flow.
