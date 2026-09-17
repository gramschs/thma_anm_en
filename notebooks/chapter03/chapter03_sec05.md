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

## Exercise 3.1 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 3.2 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 3.3 (✩)

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

```{code-cell} python
# code cell
```

## Exercise 3.4 (✩✩)

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

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 3.5 (✩✩)

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

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 3.6 (✩✩)

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

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 3.7 (✩✩✩) Mini-project: Electricity tariffs

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

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

