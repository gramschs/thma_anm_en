---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.5 Exercises

These exercises are meant for self-study at home and review the material of
Chapters 3.1 to 3.4. Plan for a good hour and a half of working time.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 5 min)
* ✩✩ Application: write your own code and interpret results (approx. 10 min)
* ✩✩✩ Mini-project: combine several concepts of the part (approx. 30 min)

````{admonition} Exercise 3.1 (✩)
:class: tip
Given the following code:

```python
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
b = np.array([1.0, 2.0, 3.0])
```

Write down your guess before running the code.

1. What does `A.shape` return?
2. What does `A[2, 0]` return?
3. What does `A[1, 2]` return?
4. Look closely at the three rows of `A`. Will `np.linalg.det(A)` be close
   to zero? Justify your answer.
5. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)

print(A.shape)
print(A[2, 0])
print(A[1, 2])
print(np.linalg.det(A))
```
Output:
```
(3, 3)
7.0
6.0
-9.51619735392994e-16
```
`A.shape` is `(3, 3)`, i.e. three rows and three columns. `A[2, 0]` is the
value in row 2, column 0, i.e. `7.0`. `A[1, 2]` sits in row 1, column 2 and
is `6.0`. On the computer the determinant is a tiny number close to zero,
because the third row is a combination of the first two:
$[7,8,9] = 2 \cdot [4,5,6] - [1,2,3]$. The system has no unique solution.
````

````{admonition} Exercise 3.2 (✩)
:class: tip
Given the following code:

```python
import numpy as np

A = np.array([[2, 1], [5, 3]], dtype=float)
b = np.array([8.0, 19.0])
```

Write down your guess before running the code.

1. Compute the determinant in your head: $\det = 2 \cdot 3 - 1 \cdot 5$.
   Does the system have a unique solution?
2. What does `np.linalg.solve(A, b)` return?
3. Substitute your solution into both equations by hand and check that it
   is correct.
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([[2, 1], [5, 3]], dtype=float)
b = np.array([8.0, 19.0])

print(np.linalg.det(A))
x = np.linalg.solve(A, b)
print(x)
print('Check:', np.allclose(A @ x, b))
```
Output:
```
1.0000000000000002
[ 5. -2.]
Check: True
```
The determinant is $2 \cdot 3 - 1 \cdot 5 = 1$, so it is not zero: exactly
one solution. `np.linalg.solve` returns $x = (5,\ -2)$. The check by hand:
$2 \cdot 5 + 1 \cdot (-2) = 8$ and $5 \cdot 5 + 3 \cdot (-2) = 19$, both
equations hold.
````

````{admonition} Exercise 3.3 (✩)
:class: tip
Given the following code:

```python
import numpy as np

A = np.array([[2, 4], [1, 2]], dtype=float)
b = np.array([10.0, 3.0])

try:
    x = np.linalg.solve(A, b)
    print('Solution:', x)
except np.linalg.LinAlgError:
    print('Matrix is singular.')
```

Write down your guess before running the code.

1. Compute `np.linalg.det(A)` in your head. What do you notice about the
   two rows of `A`?
2. Will the `try` branch or the `except` branch run? What gets printed?
3. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([[2, 4], [1, 2]], dtype=float)
b = np.array([10.0, 3.0])

print('Determinant:', np.linalg.det(A))

try:
    x = np.linalg.solve(A, b)
    print('Solution:', x)
except np.linalg.LinAlgError:
    print('Matrix is singular.')
```
Output:
```
Determinant: 0.0
Matrix is singular.
```
The second row is exactly half the first ($[1, 2] = 0.5 \cdot [2, 4]$), so
it carries no new information. The determinant is zero, `np.linalg.solve`
raises a `LinAlgError`, and the `except` branch prints `Matrix is
singular.`
````

```{admonition} Exercise 3.4 (✩✩)
:class: tip
Three people share the costs of a household. Over three months they pay
different shares of rent (R), electricity (E) and internet (I), and the
total amount is known:

| Month | Share R | Share E | Share I | Total in euros |
| --- | --- | --- | --- | --- |
| January | 0.50 | 0.30 | 0.20 | 980.00 |
| February | 0.40 | 0.35 | 0.25 | 960.00 |
| March | 0.45 | 0.25 | 0.30 | 970.00 |

We want to find the monthly total costs $R$, $E$, $I$ of the three items.

1. Write the system of equations as $\mathbf{A} \cdot \vec{x} = \vec{b}$
   with $\vec{x} = (R,\ E,\ I)^\top$.
2. Use the determinant to check solvability.
3. Solve the system with `np.linalg.solve` and print the three costs.
4. Run a check.

Structure your code with Input/Processing/Output comments.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

# Input
A = np.array([
    [0.50, 0.30, 0.20],
    [0.40, 0.35, 0.25],
    [0.45, 0.25, 0.30],
])
b = np.array([980.00, 960.00, 970.00])

# Processing
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

# Output
print(f'Determinant: {det_A:.5f}')
print(f'Rent:        {x[0]:.2f} euros')
print(f'Electricity: {x[1]:.2f} euros')
print(f'Internet:    {x[2]:.2f} euros')
print('Check passed:', np.allclose(A @ x, b))
```
Output:
```
Determinant: 0.00750
Rent:        1080.00 euros
Electricity: 880.00 euros
Internet:    880.00 euros
Check passed: True
```
The determinant is small at 0.0075, but not zero: the system has exactly
one solution. Rent costs 1080 euros a month, electricity and internet 880
euros each.
````

```{admonition} Exercise 3.5 (✩✩)
:class: tip
A horizontal beam of length $L = 6\,\text{m}$ is supported on the left at A
by a pin support, on the right at B by a roller support. The pin support
carries $A_x$ (horizontal) and $A_y$ (vertical), the roller support only
$B_y$. The beam is loaded by:

* a horizontal force $H = 3\,\text{kN}$ to the right at the height of the
  beam axis,
* a load $F_1 = 6\,\text{kN}$ vertically downward at a distance of
  $2\,\text{m}$ from A,
* a load $F_2 = 3\,\text{kN}$ vertically downward at a distance of
  $4\,\text{m}$ from A.

1. Set up the three equilibrium conditions ($\sum F_x = 0$,
   $\sum F_y = 0$, $\sum M_A = 0$; forces to the right and upward positive,
   moments counterclockwise positive).
2. Write them as $\mathbf{A} \cdot \vec{x} = \vec{b}$ with
   $\vec{x} = (A_x,\ A_y,\ B_y)^\top$, check the determinant, and solve the
   system.
3. Print the three support reactions and interpret the sign of $A_x$.

Structure your code with Input/Processing/Output comments.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

# Input
# sum Fx:  A_x + 3 = 0
# sum Fy:  A_y + B_y - 6 - 3 = 0   ->   A_y + B_y = 9
# sum M_A: 6*B_y - 6*2 - 3*4 = 0   ->   6*B_y = 24
A = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 1.0],
    [0.0, 0.0, 6.0],
])
b = np.array([-3.0, 9.0, 24.0])

# Processing
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

# Output
print(f'Determinant: {det_A:.1f}')
print(f'A_x = {x[0]:.1f} kN')
print(f'A_y = {x[1]:.1f} kN')
print(f'B_y = {x[2]:.1f} kN')
print('Check passed:', np.allclose(A @ x, b))
```
Output:
```
Determinant: 6.0
A_x = -3.0 kN
A_y = 5.0 kN
B_y = 4.0 kN
Check passed: True
```
The determinant is 6.0, the system is uniquely solvable. The negative sign
of $A_x$ means that the horizontal support reaction points to the left
with $3\,\text{kN}$, opposite to the assumed direction. It balances the
horizontal force $H$.
````

```{admonition} Exercise 3.6 (✩✩)
:class: tip
A meal plan is put together from three ingredients: rice (R), chicken (C)
and broccoli (B). The table shows the calorie, protein and carbohydrate
content per 100 g, as well as the target values per meal:

| Nutrient | Rice | Chicken | Broccoli | Target |
| --- | --- | --- | --- | --- |
| Calories | 130 | 165 | 34 | 600 |
| Protein in g | 2.7 | 31.0 | 2.8 | 55 |
| Carbohydrates in g | 28.0 | 0.0 | 7.0 | 80 |

We want to find the amount of each ingredient (in 100-g units) that gives
exactly these nutritional values.

1. Write the system of equations as $\mathbf{A} \cdot \vec{x} = \vec{b}$.
2. Check the determinant, solve the system, and print the amounts in
   grams.
3. Run a check.

Structure your code with Input/Processing/Output comments.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

# Input
# row = nutrient, column = ingredient [rice, chicken, broccoli]
A = np.array([
    [130.0, 165.0, 34.0],
    [  2.7,  31.0,  2.8],
    [ 28.0,   0.0,  7.0],
])
b = np.array([600.0, 55.0, 80.0])

# Processing
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

# Output
print(f'Determinant: {det_A:.1f}')
print(f'Rice:     {x[0] * 100:.0f} g')
print(f'Chicken:  {x[1] * 100:.0f} g')
print(f'Broccoli: {x[2] * 100:.0f} g')
print('Check passed:', np.allclose(A @ x, b))
```
Output:
```
Determinant: 8515.5
Rice:     227 g
Chicken:  136 g
Broccoli: 236 g
Check passed: True
```
The determinant is clearly not zero. The meal plan consists of about
227 g rice, 136 g chicken and 236 g broccoli. The check confirms that
these amounts hit the three target values exactly.
````

````{admonition} Exercise 3.7 (✩✩✩) Mini-project: Electricity tariffs
:class: tip
A household is billed for electricity under three tariffs: peak (P),
off-peak (O) and special (S). Over three months the consumption was
measured and the bills issued:

| Month | P in kWh | O in kWh | S in kWh | Amount in euros |
| --- | --- | --- | --- | --- |
| January | 210 | 180 | 40 | 105.00 |
| February | 190 | 160 | 35 | 94.25 |
| March | 230 | 200 | 50 | 116.50 |

**Part 1:** Set up the system of equations, check the determinant, and
compute the prices for P, O and S in cents per kWh.

**Part 2:** In April, 250 kWh P, 220 kWh O and 60 kWh S are consumed.
Compute the expected bill amount using the solution from Part 1. Hint: the
amount is the dot product of the consumption vector and the price vector,
i.e. `consumption_april @ x`.

**Part 3:** The P price rises by 10 percent. Create a new price vector (the
other two prices stay the same) and compute the new April amount, as well
as the absolute and percentage change.

**Closing question:** The P price rises by 10 percent, but the bill
amount rises by only about 6 percent. Why is that?

Structure your code with Input/Processing/Output comments.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

# Input
A = np.array([
    [210.0, 180.0, 40.0],
    [190.0, 160.0, 35.0],
    [230.0, 200.0, 50.0],
])
b = np.array([105.00, 94.25, 116.50])

# Processing Part 1: tariff prices
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

print(f'Determinant: {det_A:.1f}')
print(f'Peak price:     {x[0] * 100:.2f} ct/kWh')
print(f'Off-peak price: {x[1] * 100:.2f} ct/kWh')
print(f'Special price:  {x[2] * 100:.2f} ct/kWh')
print('Check passed:', np.allclose(A @ x, b))

# Processing Part 2: April forecast
consumption_april = np.array([250.0, 220.0, 60.0])
amount_april = consumption_april @ x
print(f'April bill: {amount_april:.2f} euros')

# Processing Part 3: peak price plus 10 percent
x_new = np.array([x[0] * 1.10, x[1], x[2]])
amount_new = consumption_april @ x_new
change_abs = amount_new - amount_april
change_pct = change_abs / amount_april * 100

print(f'April bill after peak price increase: {amount_new:.2f} euros')
print(f'Absolute change:   {change_abs:.2f} euros')
print(f'Percentage change: {change_pct:.2f} %')
```
Output:
```
Determinant: -3000.0
Peak price:     30.00 ct/kWh
Off-peak price: 20.00 ct/kWh
Special price:  15.00 ct/kWh
Check passed: True
April bill: 128.00 euros
April bill after peak price increase: 135.50 euros
Absolute change:   7.50 euros
Percentage change: 5.86 %
```
The three tariff prices are 30, 20 and 15 ct/kWh. The April bill rises from
128.00 to 135.50 euros.

**Closing question:** The peak price rises by 10 percent, but the peak
tariff only accounts for part of the bill. Of the 128 euros, $250 \cdot
0.30 = 75$ euros comes from the peak tariff, the rest from off-peak and
special, whose prices stay unchanged. 10 percent of 75 euros is 7.50 euros,
and relative to the total of 128 euros that is only about 6 percent.
````
