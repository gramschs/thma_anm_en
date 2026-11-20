---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 8.4 Calibrating a Force Sensor

In Chapter 8.3, we used gradient descent to find the two coordinates of a
location. Now you will look for the two parameters of a model that should fit
measured data, as in Chapter 8.2. Work through the parts in pairs if possible,
and in order.

## Project: How accurately does the load cell measure? (✩✩)

On a filling line, a **load cell** weighs every container. It outputs a
voltage that increases with the force on the cell. According to the datasheet,
the **characteristic curve** is

$$U = m \cdot F + b$$

with the sensitivity $m = 2.0\,\text{V/kN}$ and the zero offset
$b = 0\,\text{V}$. Since every cell is slightly different, it is **calibrated**
after installation. To do this, a technician uses test weights to apply known
loads from $0$ to $2\,\text{kN}$ and records the voltage.

| Symbol | Meaning | Unit |
| --- | --- | --- |
| $F$ | force on the load cell | kN |
| $U$ | output voltage | V |
| $m$ | sensitivity, slope of the characteristic curve | V/kN |
| $b$ | zero offset, voltage without load | V |

We want to find the actual values of $m$ and $b$, and how far off a
measurement is when it is based on the characteristic curve from the
datasheet.

First run the following cell. It contains the functions `gradient()` and
`gradient_descent_2d()` from Chapter 8.3, the measured data and the
characteristic curve from the datasheet.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# functions from Chapter 8.3
def gradient(function, point, dx):
    """Gradient of function at point = [x, y].

    Each partial derivative with the central difference quotient.
    """
    shift_x = np.array([dx, 0.0])
    shift_y = np.array([0.0, dx])
    derivative_x = (function(point + shift_x)
                    - function(point - shift_x)) / (2 * dx)
    derivative_y = (function(point + shift_y)
                    - function(point - shift_y)) / (2 * dx)
    return np.array([derivative_x, derivative_y])

def gradient_descent_2d(function, start, learning_rate, tolerance,
                        max_iterations):
    """Search for a minimum of function, starting at start = [x, y].

    Returns all visited points as an array, row = [x, y].
    """
    point = start
    history = [point]
    for k in range(max_iterations):
        slope = gradient(function, point, 1e-6)
        # stopping criterion: length of the gradient almost zero
        if np.linalg.norm(slope) < tolerance:
            break
        point = point - learning_rate * slope
        history.append(point)
    return np.array(history)

# calibration: force of the test weights in kN and measured voltage in V
force = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
voltage = np.array([0.121, 0.437, 0.904, 1.293, 1.703, 2.116, 2.488,
                    2.931, 3.327, 3.818, 4.165])

# characteristic curve according to the datasheet: [m in V/kN, b in V]
datasheet = np.array([2.0, 0.0])
```

## Part 1: Measured data and datasheet

Write a function `characteristic(force, parameters)` that computes the voltage
according to the characteristic curve. Just like the location in Chapter 8.3,
`parameters` is an array with two entries, here `[m, b]`.

The following template plots the measurements as points and the
characteristic curve from the datasheet as a line. Fill in the gap:

```python
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(force, voltage, color='black', label='measurements')
ax.plot(force, ___, label='datasheet')
ax.set_xlabel('Force in kN')
ax.set_ylabel('Voltage in V')
ax.set_title('Calibration of the load cell')
ax.legend()
ax.grid(True)
plt.show()
```

Does the datasheet match the installed cell? Which of the two parameters is
probably off?

```{code-cell} python
# code cell
```

## Part 2: Cost function and contour plot

As in Part 2 of Chapter 8.2, write a function `cost(parameters)` that computes
the mean squared error between the measured voltage and the characteristic
curve. What is the mean squared error for the datasheet parameters?

Then, as in the first section of Chapter 8.3, draw a contour plot of the cost
function for $m$ from $1.8$ to $2.3\,\text{V/kN}$ and $b$ from $-0.2$ to
$0.3\,\text{V}$. The horizontal axis shows $m$, and the vertical axis shows
$b$. So the rows of the matrix correspond to $b$ and the columns to $m$. The
code is already set up. You only need to fill in the gaps:

```python
# cost on a grid, row = b, column = m
m_values = np.linspace(1.8, 2.3, 101)
b_values = np.linspace(-0.2, 0.3, 101)
cost_values = np.zeros((len(b_values), len(m_values)))
for i in range(len(b_values)):
    for j in range(len(m_values)):
        parameters = np.array([___, ___])
        cost_values[i, j] = ___

# contour plot with the datasheet
fig, ax = plt.subplots(figsize=(7, 6))
lines = ax.contour(m_values, b_values, cost_values,
                   levels=[0.002, 0.005, 0.01, 0.02, 0.05])
ax.clabel(lines, fontsize=8)
ax.scatter(datasheet[0], datasheet[1], marker='x', s=80, color='red',
           label='datasheet')
ax.set_xlabel('m in V/kN')
ax.set_ylabel('b in V')
ax.set_title('Mean squared error in V²')
ax.legend()
plt.show()
```

Roughly where is the minimum? What shape does the valley have?

```{code-cell} python
# code cell
```

## Part 3: Gradient descent and comparison with NumPy

Determine $m$ and $b$ with `gradient_descent_2d()`. Use the datasheet
parameters as the starting point, with a learning rate of $0.3$, a tolerance of
$10^{-4}$ and at most 1000 iterations. Draw the path of the method in the
contour plot. To do this, copy the code for the contour plot from Part 2 and
add a line with `ax.plot()` before `ax.legend()`.

For a straight line, there is a formula that minimizes the mean squared error
directly. NumPy provides it as `np.polyfit(force, voltage, 1)`. The `1` stands
for a polynomial of degree one, i.e. a straight line. The function returns the
slope and the intercept as an array. Compare them with your result.

Finally, run the following code. It tries out the learning rates $0.45$ and
$0.5$ and stores the result in `history_test`, so that your result in
`history` is not overwritten. What happens? Was the tolerance reached in each
case, or only the limit of 1000 iterations?

```python
# larger learning rates
for learning_rate in [0.45, 0.5]:
    history_test = gradient_descent_2d(cost, datasheet, learning_rate,
                                       1e-4, 1000)
    n_test = len(history_test) - 1
    print(f'Learning rate {learning_rate}: {n_test} iterations, '
          f'[m, b] = {np.round(history_test[-1], 4)}')
```

```{code-cell} python
# code cell
```

## Part 4: What does the calibration achieve?

During operation, the load cell reads $2.73\,\text{V}$. Solve the
characteristic curve for the force:

$$F = \frac{U - b}{m}.$$

Compute the force once with the datasheet and once with the calibrated
parameters from Part 3. By how many newtons and by what percentage does the
force based on the datasheet differ from the calibrated value?

```{code-cell} python
# code cell
```

## Closing question

Why is the valley in the contour plot narrow and slanted? Think about the
data points: what happens to the straight line if we increase $m$ a
little and decrease $b$ a little at the same time?

To find out, calculate in your head the voltage of the line with
$[m, b] = [2.0, 0.12]$ and with $[m, b] = [2.1, 0.02]$ at $0$, $1$ and
$2\,\text{kN}$, and compare the results with the measurements.

## Bonus exercise: Force in newtons instead of kilonewtons (✩✩✩)

A colleague prefers to work in newtons, multiplies the forces by 1000 and
starts from the datasheet values, which are now $m = 0.002\,\text{V/N}$ and
$b = 0\,\text{V}$.

1. Write the characteristic curve and the cost function for the force in
   newtons. Compute the gradient at the datasheet parameters and compare
   its two components with the gradient in kilonewtons.
2. Start gradient descent with a learning rate of $0.3$. Then search for the
   largest learning rate of the form $1 \cdot 10^{-k}$ or $4 \cdot 10^{-k}$
   for which the method does not blow up, and let it run for 2000 iterations.
   Compare the result with `np.polyfit()`.
3. Explain why the choice of unit determines whether the method succeeds or
   fails, even though the straight line is the same.

```{code-cell} python
# code cell
```
