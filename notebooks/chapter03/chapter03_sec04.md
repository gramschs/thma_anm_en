---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.4 How Much Does Thicker Insulation Help?

In Chapter 3.3 we computed the temperatures and the heat flow in a
three-layer wall. In this chapter we add an insulation layer to the wall and
use a parameter study to investigate how much the heat flow drops as we
increase the insulation. Work through the parts in pairs if possible, and in
order.

## Project: Parameter study on insulation thickness (✩✩)

An exterior wall consists of four layers. Inside it is
$T_{LA} = 293\,\text{K}$ (20 °C), outside $T_{DR} = 263\,\text{K}$ (−10 °C).

| Layer | Component | $R$ in K/W |
| --- | --- | --- |
| A | Interior plaster | 0.04 |
| B | Masonry | 0.5 |
| C | Insulation | $R_C$ (variable) |
| D | Exterior plaster | 0.04 |

The unknowns are the three interface temperatures $T_{AB}$, $T_{BC}$,
$T_{CD}$ and the heat flow $Q$. As in Chapter 3.3, $Q = \Delta T_i / R_i$
holds for each layer.

## Part 1: Set up the system of equations

Rearrange the four layer equations so that all unknowns are on the left
(multiply each by its $R_i$). Write the result as the matrix equation
$\mathbf{A} \cdot \vec{x} = \vec{b}$ with
$\vec{x} = (T_{AB},\ T_{BC},\ T_{CD},\ Q)^\top$. The matrix has the same
structure as in Chapter 3.3, just with one more row and one more column.

```{code-cell} python
# code cell
```

## Part 2: Solve for a fixed insulation value

Create `A` and `b` as NumPy arrays for $R_C = 1.0\,\text{K/W}$. Check the
determinant, solve with `np.linalg.solve`, and print the three interface
temperatures (in °C) and the heat flow. Verify the result with a check.

```{code-cell} python
# code cell
```

## Part 3: Parameter study and plot

Investigate how the heat flow depends on the insulation thickness. Vary
$R_C$ with

```python
r_c_values = np.linspace(0.0, 3.0, 31)
```

Solve the system of equations for each value, store the heat flow in an
array `q_values`, and plot `q_values` against `r_c_values` as a line plot
(axis labels, title, grid).

```{code-cell} python
# code cell
```

## Part 4: Evaluate the plot

Answer in your own words:

1. How does the heat flow change when $R_C$ rises from 0 to 0.5 K/W, and
   how does it change when it rises from 2.5 to 3.0 K/W?
2. What does the shape of the curve imply for the question of whether ever
   thicker insulation is worthwhile?

## Bonus exercise: Halving the heat flow (✩✩✩)

Determine from the parameter study at which $R_C$ the heat flow has dropped
to half the value without insulation ($R_C = 0$).

1. The value without insulation is `q_values[0]`. Form the target
   `q_target = q_values[0] / 2`.
2. Find the index of the `q_values` entry closest to `q_target`, using
   `np.argmin(np.abs(q_values - q_target))`.
3. Print the corresponding $R_C$ and mark the point in the plot from Part 3
   with a second `ax.scatter()` call.

```{code-cell} python
# code cell
```

