---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.1 Solving Linear Systems of Equations with NumPy

At a fruit stand, an apple, a banana and a clementine each cost a fixed
amount. On three days we buy different quantities and each time pay a total
amount. We no longer know the individual prices, only the quantities and the
receipts. *How do we work out the individual prices from that?*

That is the task of a **linear system of equations**, or **LSE** for short.
In this chapter we write an LSE as a matrix equation, use the determinant to
check whether it has a unique solution, and compute it with a single NumPy
function. The NumPy arrays from Chapter 2 are our tool here; the only thing
new is that we now work with two-dimensional arrays.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can write a linear system of equations in matrix form
  $\mathbf{A} \cdot \vec{x} = \vec{b}$.
* [ ] You can create a matrix as a two-dimensional NumPy array and access
  individual entries with `A[i, j]`.
* [ ] You can use `np.linalg.det()` to check whether an LSE has a unique
  solution, and catch a `LinAlgError` with `try`/`except`.
* [ ] You can solve an LSE with `np.linalg.solve()` and verify the result
  with a check.
```

## How do we write a system of equations as a matrix?

We arrange the purchase quantities from the three days in a table: each row
is a day, each column a type of fruit.

| | Apples | Bananas | Clementines |
| --- | --- | --- | --- |
| **Day 1** | 3 | 2 | 1 |
| **Day 2** | 2 | 3 | 0 |
| **Day 3** | 1 | 1 | 3 |

With the unknown unit prices $x_A$, $x_B$, $x_C$ and the amounts paid, each
day gives us one equation:

$$\begin{align}
3 x_A + 2 x_B + 1 x_C &= 1.80 \\
2 x_A + 3 x_B + 0 x_C &= 1.20 \\
1 x_A + 1 x_B + 3 x_C &= 2.00
\end{align}$$

All three left-hand sides have the same structure: numbers times unknowns,
summed up. We write these numbers, the **coefficients**, into a matrix
$\mathbf{A}$, and the unknowns into a vector $\vec{x}$:

$$\mathbf{A} = \begin{pmatrix} 3 & 2 & 1 \\ 2 & 3 & 0 \\ 1 & 1 & 3 \end{pmatrix},
\qquad
\vec{x} = \begin{pmatrix} x_A \\ x_B \\ x_C \end{pmatrix}$$

The product $\mathbf{A} \cdot \vec{x}$ is defined so that it produces exactly
the left-hand sides of our equations. For each row of $\mathbf{A}$ we
multiply entry by entry with $\vec{x}$ and add up:

$$\mathbf{A} \cdot \vec{x} =
\begin{pmatrix} 3 & 2 & 1 \\ 2 & 3 & 0 \\ 1 & 1 & 3 \end{pmatrix}
\cdot \begin{pmatrix} x_A \\ x_B \\ x_C \end{pmatrix}
=
\begin{pmatrix}
3 \cdot x_A + 2 \cdot x_B + 1 \cdot x_C \\
2 \cdot x_A + 3 \cdot x_B + 0 \cdot x_C \\
1 \cdot x_A + 1 \cdot x_B + 3 \cdot x_C
\end{pmatrix}$$

The first row of $\mathbf{A}$ meets $\vec{x}$ from top to bottom: $3$ times
$x_A$, plus $2$ times $x_B$, plus $1$ times $x_C$. That is exactly the
left-hand side of the first equation. The same holds for the second and
third rows.

If we set this product equal to the vector of receipts, row by row we get
back our original system of equations:

$$\begin{pmatrix} 3 & 2 & 1 \\ 2 & 3 & 0 \\ 1 & 1 & 3 \end{pmatrix}
\cdot \begin{pmatrix} x_A \\ x_B \\ x_C \end{pmatrix}
= \begin{pmatrix} 1.80 \\ 1.20 \\ 2.00 \end{pmatrix}$$

This is the **matrix equation** $\mathbf{A} \cdot \vec{x} = \vec{b}$. The
**coefficient matrix** $\mathbf{A}$ contains the purchase quantities, the
vector $\vec{x}$ the unknown prices, and the vector $\vec{b}$ the receipts.
Each row of $\mathbf{A}$ belongs to one equation, each column to one
unknown.

In NumPy we create $\mathbf{A}$ as a **two-dimensional array**: a list of
lists, where each inner list is one row.

```{code-cell} python
import numpy as np

# Coefficient matrix: each row is a shopping day,
# the columns stand for apples, bananas, clementines
A = np.array([
    [3, 2, 1],
    [2, 3, 0],
    [1, 1, 3],
], dtype=float)

b = np.array([1.80, 1.20, 2.00])

print(A)
print('Shape (rows, columns):', A.shape)
```

`A.shape` returns `(3, 3)`, i.e. three rows and three columns. We access a
single entry with two indices: first the row, then the column.

```{code-cell} python
print('Row 0, column 2:', A[0, 2])   # clementines on day 1
print('Row 1, column 0:', A[1, 0])   # apples on day 2
```

```{admonition} Mini-exercise (✩)
:class: tip
A company manufactures two products from steel and aluminum. With the
unknown quantities $n_1$ and $n_2$, the system of equations reads:

$$\begin{align}
3 n_1 + 2 n_2 &= 12 \qquad \text{(steel in kg)} \\
1 n_1 + 4 n_2 &= 9 \qquad \text{(aluminum in kg)}
\end{align}$$

1. Write the coefficient matrix `A` and the right-hand side `b` as
   NumPy arrays.
2. Print `A.shape`.
3. Answer without code: what do the entries `A[1, 0]` and `b[1]` mean in
   context?
4. Compute $\mathbf{A} \cdot \vec{n}$ by hand and check that, row by row,
   you get back the system of equations above.
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
    [3, 2],    # steel:     3 kg per unit of product 1, 2 kg per unit of product 2
    [1, 4],    # aluminum:  1 kg per unit of product 1, 4 kg per unit of product 2
], dtype=float)

b = np.array([12.0, 9.0])

print(A.shape)
```
`A.shape` is `(2, 2)`. The entry `A[1, 0]` sits in row 1 (aluminum) and
column 0 (product 1), so it is the aluminum required per unit of product 1,
here 1 kg. `b[1]` belongs to the second equation and is the total available
amount of aluminum, here 9 kg.

The product by hand:

$$\mathbf{A} \cdot \vec{n} =
\begin{pmatrix} 3 & 2 \\ 1 & 4 \end{pmatrix}
\cdot \begin{pmatrix} n_1 \\ n_2 \end{pmatrix}
= \begin{pmatrix} 3 n_1 + 2 n_2 \\ 1 n_1 + 4 n_2 \end{pmatrix}$$

Setting this equal to $\vec{b} = \begin{pmatrix} 12 \\ 9 \end{pmatrix}$ gives,
row by row, exactly the two original equations.
````

## Does the system have a unique solution?

Not every LSE has exactly one solution. Three cases are possible:

* exactly one solution (the normal case)
* no solution (the equations contradict each other)
* infinitely many solutions (one equation carries no new information)

For square systems, i.e. as many equations as unknowns, we check this with
the **determinant** $\det(\mathbf{A})$. The rule is: if the determinant is
not zero, the system has exactly one solution.

```{code-cell} python
det_A = np.linalg.det(A)
print(f'Determinant: {det_A:.4f}')

# np.isclose checks whether a value is close to zero.
# This is more reliable than == 0, because floating-point numbers are never exact.
if np.isclose(det_A, 0.0):
    print('det(A) = 0: no unique solution.')
else:
    print('det(A) not equal to 0: exactly one solution.')
```

For comparison, here is a matrix whose third row is the sum of the first
two and therefore carries no new information:

```{code-cell} python
A_singular = np.array([
    [3, 2, 1],
    [2, 3, 0],
    [5, 5, 1],   # row 3 = row 1 + row 2
], dtype=float)

print(f'Determinant: {np.linalg.det(A_singular):.2e}')
```

The result is not exactly zero, but a tiny number on the order of `1e-16`.
Floating-point numbers are stored on the computer only approximately, and
every computation accumulates small rounding errors. That is exactly why we
compare with `np.isclose` and not with `== 0`.

````{admonition} What happens with a singular matrix?
:class: warning
If we pass a singular matrix to the solver function `np.linalg.solve`, the
program terminates with a `LinAlgError`. We catch such errors with `try`
and `except` instead of letting the program crash:

```python
try:
    x = np.linalg.solve(A_singular, b)
except np.linalg.LinAlgError:
    print('Matrix is singular, the system has no unique solution.')
```
````

If the determinant is zero, the system has either no solution or infinitely
many. Which case applies, and how to check solvability even when there are
more equations than unknowns, we clarify with the **rank** in the excursus
on the Wheatstone bridge.

```{admonition} Mini-exercise (✩)
:class: tip
Given the matrix

$$\mathbf{A} = \begin{pmatrix} 2 & 1 & 1 \\ 4 & 2 & 2 \\ 1 & 0 & 3 \end{pmatrix}.$$

1. Answer without code: will `np.linalg.det(A)` be close to zero? Look
   closely at the first two rows.
2. Create the matrix and check your guess with `np.linalg.det()` and
   `np.isclose()`.
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
    [2, 1, 1],
    [4, 2, 2],
    [1, 0, 3],
], dtype=float)

det_A = np.linalg.det(A)
print(f'Determinant: {det_A:.2e}')
print('close to zero:', np.isclose(det_A, 0.0))
```
The second row is exactly twice the first row and therefore carries no new
information. The determinant is therefore zero; on the computer it shows up
as a tiny number close to zero. `np.isclose` returns `True`, so the system
has no unique solution.
````

## Solving the system and checking the result

If the determinant is not zero, we compute the solution with
`np.linalg.solve`. The function expects the matrix first, then the
right-hand side.

```{code-cell} python
x = np.linalg.solve(A, b)

print(f'Price apple:      {x[0]:.2f} euros')
print(f'Price banana:     {x[1]:.2f} euros')
print(f'Price clementine: {x[2]:.2f} euros')
```

*How do we know this result is correct?* If $\vec{x}$ is the correct
solution, the matrix product $\mathbf{A} \cdot \vec{x}$ must again give the
vector $\vec{b}$. That is the **check**. For the matrix product we use the
`@` operator, not `*`.

```{code-cell} python
b_check = A @ x

print('A @ x:', b_check)
print('b:    ', b)

# np.allclose checks whether all entries agree up to tiny rounding errors
print('Check passed:', np.allclose(b_check, b))
```

```{admonition} Mini-exercise (✩)
:class: tip
A café sells coffee, tea and ice cream on three days and records the daily
revenue in euros:

| Day | Coffee | Tea | Ice cream | Revenue |
| --- | --- | --- | --- | --- |
| Mon | 5 | 2 | 3 | 25.60 |
| Tue | 3 | 4 | 1 | 17.60 |
| Wed | 4 | 2 | 3 | 23.30 |

1. Create `A` and `b`, check the determinant, solve with
   `np.linalg.solve` and verify the result with a check.
2. Answer without code: the check `np.allclose(A @ x, b)` returns `True`.
   Does that mean `A` and `b` were guaranteed to be set up correctly?
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
    [5, 2, 3],
    [3, 4, 1],
    [4, 2, 3],
], dtype=float)

b = np.array([25.60, 17.60, 23.30])

print(f'Determinant: {np.linalg.det(A):.2f}')

x = np.linalg.solve(A, b)
print(f'Coffee:    {x[0]:.2f} euros')
print(f'Tea:       {x[1]:.2f} euros')
print(f'Ice cream: {x[2]:.2f} euros')

print('Check passed:', np.allclose(A @ x, b))
```
The determinant is 10.0, so the system has a unique solution: coffee 2.30
euros, tea 1.80 euros, ice cream 3.50 euros. The check only confirms that
`x` fits the `A` and `b` we set up, not that `A` and `b` themselves are
correct. A typo in `A` would still produce a solution that passes the
check. That is why it is worth printing and reviewing `A` and `b` once more
before solving.
````

## Summary and outlook

We write a linear system of equations as the matrix equation
$\mathbf{A} \cdot \vec{x} = \vec{b}$. We create the coefficient matrix
$\mathbf{A}$ as a two-dimensional NumPy array, and the right-hand side
$\vec{b}$ as a one-dimensional array. With `np.linalg.det()` and
`np.isclose()` we check in advance whether a unique solution exists, and we
catch the `LinAlgError` with `try`/`except`. The solution itself comes from
`np.linalg.solve(A, b)` in a single line, verified by the check
`np.allclose(A @ x, b)`.

In the next chapter we leave the fruit stand behind and set up an LSE from a
mechanical engineering problem: the static equilibrium of a loaded beam.
The approach stays the same, only the equations now come from mechanics.
