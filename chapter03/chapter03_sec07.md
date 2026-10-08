---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Excursus: Runtime and Scaling

This chapter is an optional excursus. So far we have used `np.linalg.solve`
for systems with 3 or 6 unknowns. In engineering practice, a finite-element
simulation produces systems with thousands to millions of unknowns. *How
fast does the runtime grow with the system size, and where does
`np.linalg.solve` reach its limits?*

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can use `np.random` to generate a random, uniquely solvable
  system of equations of any size.
* [ ] You can use `time.perf_counter()` to measure the runtime of an
  operation.
* [ ] You can plot the runtime against the system size in a log-log plot
  and estimate the scaling exponent with `np.polyfit`.
* [ ] You can explain the theoretical $O(n^3)$ scaling, compare it with the
  measurement and estimate its consequences for large systems.
```

## Generating random test systems

For the timing measurements we need test problems: matrices and
right-hand sides of any size that form a uniquely solvable system. We fill
them with random numbers: `np.random.default_rng(seed)` creates a random
number generator, which we store in `rng`. The same `seed` always yields the
same random numbers. `rng.standard_normal(shape)` then fills an array of the
given shape with normally distributed random numbers. A random matrix is
almost always solvable, but it can be **ill-conditioned**: small rounding
errors then have a large effect on the solution. We counter this by
strengthening the diagonal: we add $n$ times the identity matrix, which
NumPy creates with `np.eye(n)`.

```{code-cell} python
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

def generate_linear_system(n, seed=0):
    """Generates a random, uniquely solvable n x n system of equations.

    n:    size of the system
    seed: random seed for reproducible results
    Returns: matrix A and right-hand side b
    """
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((n, n))
    A = A + n * np.eye(n)          # strengthen the diagonal -> well-conditioned
    b = rng.standard_normal(n)
    return A, b

A, b = generate_linear_system(5)
print('Shape of A:  ', A.shape)
print('Determinant:', round(float(np.linalg.det(A)), 1))
```

Each diagonal element thus grows by $n$. The factor $n$ matters: a matrix is
**diagonally dominant** if, in every row, the diagonal element is larger in
magnitude than the sum of the magnitudes of the other entries. Such a matrix
is always solvable. For an $n \times n$ random matrix
this sum grows roughly like $0.8 \cdot n$. Adding $n$ therefore makes most
rows dominant and the matrix well-conditioned with high probability,
although it does not guarantee dominance in every row. A fixed increment
would not be enough for large $n$.

```{admonition} Mini-exercise (✩)
:class: tip
1. Call `generate_linear_system(5, seed=0)` twice and use `np.allclose` to
   check whether both calls give the same matrix.
2. Answer without code: why does it make sense, when measuring runtimes,
   to always use the same `seed`?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
A1, _ = generate_linear_system(5, seed=0)
A2, _ = generate_linear_system(5, seed=0)
print('same matrix:', np.allclose(A1, A2))
```
Both calls give the same matrix, because the `seed` fixes the starting
state of the random generator. A fixed `seed` makes the measurement
reproducible: if we repeat it, on the same or on another computer, we solve
exactly the same systems of equations. Differences in runtime then come from
the computer, not from different matrices.
````

## Measuring and plotting runtime

`time.perf_counter()` returns a point in time in seconds. The difference
between two calls is the elapsed time. We measure how long
`np.linalg.solve` takes for various system sizes.

```{code-cell} python
def measure_runtime(n):
    """Generates an n x n system, solves it, and returns the runtime in s."""
    A, b = generate_linear_system(n)
    start = time.perf_counter()
    np.linalg.solve(A, b)
    return time.perf_counter() - start

n_values = np.array([100, 200, 400, 700, 1000, 1500, 2000])
t_values = np.zeros(len(n_values))

for i, n in enumerate(n_values):
    t_values[i] = measure_runtime(n)
    print(f'n = {n:5d}:  {t_values[i] * 1000:7.2f} ms')
```

The absolute times depend on the hardware and fluctuate somewhat from run
to run. To study the scaling, we plot the times against the system size
using `ax.loglog`: both axes are logarithmic. A power law
$t \propto n^\alpha$ then appears as a straight line whose slope is the
exponent $\alpha$. With `marker='o'` each measured point is additionally
marked with a circle. For comparison we draw a reference line that grows
exactly with $n^3$ and starts at the first measured point.
`grid(True, which='both')` also draws grid lines between the powers of ten.

```{code-cell} python
# reference line for O(n^3), fitted to the first data point
t_reference = t_values[0] * (n_values / n_values[0])**3

fig, ax = plt.subplots(figsize=(7, 4))
ax.loglog(n_values, t_values, marker='o', label='measured')
ax.loglog(n_values, t_reference, linestyle='dashed', label='slope 3 (O(n³))')
ax.set_xlabel('System size n')
ax.set_ylabel('Runtime in s')
ax.set_title('Runtime of np.linalg.solve')
ax.legend()
ax.grid(True, which='both')
plt.show()
```

The measured points lie below the reference line, because the line starts
at the first point, where a fixed overhead per call still dominates the
runtime. For large $n$ both run almost parallel: there the runtime grows
roughly with $n^3$.

```{admonition} Mini-exercise (✩)
:class: tip
1. Plot the same data additionally with `ax.plot` instead of `ax.loglog`.
2. Answer without code: in which of the two plots is the scaling exponent
   easier to read off, and why?
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(n_values, t_values, marker='o')
ax.set_xlabel('System size n')
ax.set_ylabel('Runtime in s')
ax.set_title('Runtime, linear axes')
ax.grid(True)
plt.show()
```
In the linear plot, the steep rise at large $n$ dominates the whole
picture, and small $n$ are compressed and indistinguishable. In the
log-log plot, a power law appears as a straight line whose slope can be
read off directly as the exponent. For the scaling analysis, the log-log
plot is therefore better suited.
````

## Determining the scaling exponent

In log-log space, $\log t = \alpha \cdot \log n + \text{const}$. The
exponent $\alpha$ is therefore the slope of a line through the points
$(\log n,\ \log t)$. This slope is provided by `np.polyfit`. To use only
the upper half of the points, we compute the middle index with the integer
division `//`, which rounds the result down to a whole number.

```{code-cell} python
log_n = np.log(n_values)
log_t = np.log(t_values)

# np.polyfit(x, y, 1) fits a line through the points and returns
# [slope, intercept]. We use only the upper half of the data points,
# since for small n the fixed overhead distorts the measurement.
# log_n[middle:] selects the entries from index middle to the end.
middle = len(n_values) // 2
slope = np.polyfit(log_n[middle:], log_t[middle:], 1)[0]

print(f'estimated exponent: {slope:.2f}')
print('theoretical value:  3.00')
```

The measured exponent typically lies between about 2.5 and 3, and the exact
number fluctuates from measurement to measurement. The theory predicts
$O(n^3)$: internally, `np.linalg.solve` decomposes the matrix into a product
of two triangular matrices (LU decomposition), and this step costs on the
order of $n^3$ arithmetic operations. That the measured value often lies
somewhat below 3 has a practical reason: for medium-sized systems, the
library manages more arithmetic operations per second the larger the matrix
is, because it makes better use of several processor cores and the
processor's cache. Only for very large $n$ does the $n^3$ growth show in
full. If we then double the system size, the runtime increases by a factor
of $2^3 = 8$.

```{admonition} Mini-exercise (✩)
:class: tip
1. Using $t(n) \approx t(n_0) \cdot (n / n_0)^3$, estimate the runtime for
   $n = 20\,000$, where $n_0$ and $t(n_0)$ come from the largest measured
   point (`n_values[-1]` and `t_values[-1]`).
2. Answer without code: a finite-element simulation often has
   $n = 10^6$ unknowns. Is `np.linalg.solve` suitable for that? Look up the
   terms *sparse matrix* and *iterative solver*.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
n0 = n_values[-1]
t0 = t_values[-1]
n_new = 20000
t_new = t0 * (n_new / n0)**3
print(f'estimated runtime for n = {n_new}: {t_new:.1f} s ({t_new / 60:.1f} min)')
```
For $n = 20\,000$, this gives anywhere from a few seconds to minutes,
depending on the computer. For $n = 10^6$, the runtime with
`np.linalg.solve` would no longer be practical, and the memory needed for
a full $10^6 \times 10^6$ matrix would be enormous. In practice, the
matrices of large engineering problems are **sparse**, meaning almost all
entries are zero. Special iterative solvers exist for this (for example in
`scipy.sparse.linalg`), which store only the nonzero entries and need far
fewer arithmetic operations.
````

## Summary

In theory, the runtime of `np.linalg.solve` grows with the third power of the
system size, $O(n^3)$, because internally an LU decomposition is carried out.
For medium-sized systems, the measured exponent is often somewhat smaller.
For small and medium systems up to a few thousand unknowns, this is not a
problem. For the large, sparse systems of engineering practice, we need
specialized iterative solvers.

This concludes Part 3. In Part 4 we use the same tool to solve a larger
mechanical engineering problem: the deformation of a truss.
