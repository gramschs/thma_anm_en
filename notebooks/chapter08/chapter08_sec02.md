---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 8.2 Cooling Constant from Measured Data

In Chapter 8.1, operations management gave us a ready-made cost function. Now
you set up a cost function yourself. It measures how well a model fits
measured data, and gradient descent searches for the parameter for which the
model and the measurements agree best. Work through the parts in pairs if
possible, and in order.

## Project: When can the part be packed? (✩✩)

A company washes aluminum parts and then dries them in an oven at
$100\,°\text{C}$. The parts then cool on a fan-cooled conveyor belt in the
factory, where the air temperature is $20\,°\text{C}$. They must not be
wrapped in plastic film until they are below $40\,°\text{C}$, or condensation
will form inside the packaging. A thermocouple recorded the temperature of one
part every $5\,\text{s}$.

For the temperature $T$ at time $t$, we use **Newton's law of cooling**:

$$T(t) = T_\infty + (T_0 - T_\infty) \cdot e^{-\lambda t}.$$

| Symbol | Meaning | Value |
| --- | --- | --- |
| $T_0$ | temperature when leaving the oven | $100\,°\text{C}$ |
| $T_\infty$ | temperature in the factory | $20\,°\text{C}$ |
| $\lambda$ | **cooling constant**, depends on shape, material and air flow | unknown, in $1/\text{s}$ |
| limit | maximum temperature for packing | $40\,°\text{C}$ |

We are looking for the cooling constant $\lambda$ and the time the part has to
stay on the belt.

First run the following cell. It contains the functions `central()` and
`gradient_descent()` from Chapter 8.1, the known temperatures and the measured
data.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# functions from Chapter 8.1
def central(function, point, dx):
    """Central difference quotient of function at the given point."""
    return (function(point + dx) - function(point - dx)) / (2 * dx)

def gradient_descent(function, start, learning_rate, tolerance,
                     max_iterations):
    """Search for a minimum of function, starting at start.

    Returns all visited points as an array.
    """
    point = start
    history = [point]
    for k in range(max_iterations):
        slope = central(function, point, 1e-6)
        # stopping criterion: slope almost zero
        if abs(slope) < tolerance:
            break
        point = point - learning_rate * slope
        history.append(point)
    return np.array(history)

# known temperatures in °C
T_start = 100.0
T_ambient = 20.0

# measurement times in s and measured temperatures in °C
t_meas = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
T_meas = np.array([100.0, 82.6, 68.2, 56.9, 49.0, 41.9, 37.9, 35.2, 30.3,
                   27.8, 27.1, 25.5, 24.1])
```

## Part 1: Model and first estimate

Like `total_cost()` in Chapter 8.1, write a function `model(t, lam)` that
computes the temperature according to the law of cooling. Python reserves the
word `lambda` for something else, so the parameter is called `lam`.

Plot the measurements as points and the model for $\lambda = 0.03$ and
$\lambda = 0.08\,\text{1/s}$ as lines. To get smooth lines, evaluate the model
at 200 times between $0$ and $60\,\text{s}$.

Which of the two model curves cools down too slowly, and which too quickly?
Roughly where is the value of $\lambda$ we are looking for?

```{code-cell} python
# code cell
```

## Part 2: Cost function from the measured data

To measure how well a value of $\lambda$ fits, we look at the deviations
between the measurements and the model. We square each deviation and take
the mean over all $n$ measurements. This gives the **mean squared error**
(MSE):

$$C(\lambda) = \frac{1}{n} \sum_{i=1}^{n} \bigl(T_{\text{meas},i} - T(t_i)\bigr)^2.$$

Because we square the deviations, positive and negative deviations do not
cancel each other out, and large deviations count more than small ones.

Write a function `cost(lam)` that computes $C(\lambda)$ with `np.mean()`.
Evaluate it for 300 values of $\lambda$ between $0.01$ and
$0.12\,\text{1/s}$, and plot $C$ against $\lambda$. Unlike `total_cost()` in
Chapter 8.1, `cost()` only accepts a single number $\lambda$, because the
function already works with the array `t_meas` internally. So you compute the
300 values in a loop.

Roughly where is the minimum? What is the unit of $C$?

```{code-cell} python
# code cell
```

## Part 3: Gradient descent

Search for the minimum with `gradient_descent()`, starting at
$\lambda = 0.03\,\text{1/s}$, with a tolerance of $10^{-3}$ and at most 100
iterations.

The learning rate of 200 from Chapter 8.1 does not work here. First, use
`central()` to compute the slope of `cost()` at the starting value. The first
step should change $\lambda$ by about $0.02\,\text{1/s}$. Which learning rate
does this give?

Then compare the learning rates $10^{-6}$, $2 \cdot 10^{-6}$,
$5 \cdot 10^{-6}$ and $10^{-5}$. The code for the convergence plot is already
set up. You only need to fill in the gaps:

```python
# convergence plot for four learning rates
fig, ax = plt.subplots(figsize=(7, 4))
for learning_rate in [1e-6, 2e-6, 5e-6, 1e-5]:
    history = gradient_descent(___, ___, learning_rate, 1e-3, 100)
    n_iterations = len(history) - 1
    print(f'Learning rate {learning_rate:.0e}: {n_iterations} iterations, '
          f'λ = {history[-1]:.5f} 1/s')
    ax.plot(history, marker='.', label=f'learning rate {learning_rate:.0e}')
ax.set_xlabel('Iteration')
ax.set_ylabel('λ in 1/s')
ax.set_title('Convergence of gradient descent')
ax.legend()
ax.grid(True)
plt.show()
```

Which $\lambda$ do you find, and which learning rate needs the fewest
iterations?

```{code-cell} python
# code cell
```

## Part 4: Checking the result and computing the waiting time

After the loop in Part 3, `history` contains the result for the last learning
rate, which did not converge. So call `gradient_descent()` once more with the
fastest learning rate from Part 3. Store the $\lambda$ you find in a variable
`lam_best`, and plot the model with this value together with the measured
values.

Solving the law of cooling for $t$ gives the time at which the part reaches
the limit of $40\,°\text{C}$:

$$t_{40} = \frac{1}{\lambda} \cdot \ln \frac{T_0 - T_\infty}{40\,°\text{C} - T_\infty}.$$

`np.log()` computes the natural logarithm. How long does the part have to stay
on the belt?

```{code-cell} python
# code cell
```

## Closing question

1. The conveyor belt moves at $0.05\,\text{m/s}$. What is the minimum length
   of the cooling section?
2. The smallest value of the cost function is not zero, but
   $C = 0.36\,°\text{C}^2$. Why does gradient descent not find a $\lambda$ for
   which $C$ is zero? What does the square root of this value tell us about
   the fit?

## Bonus exercise: An outlier in the measurements (✩✩✩)

Because of a loose connection at the thermocouple, the reading at
$30\,\text{s}$ is $10\,°\text{C}$ too high. Create the data set with the faulty
reading using

```python
T_faulty = T_meas.copy()
T_faulty[6] = T_faulty[6] + 10
```

1. Write a cost function `cost_faulty(lam)` for the data with the faulty
   reading and determine $\lambda$ with `gradient_descent()`.
2. The differences between the measurements and the model are called
   **residuals**. Plot the residuals against time. How can you spot the
   outlier, and what do you notice about the other residuals?
3. `np.delete(array, 6)` returns a copy of the array without the entry at
   index 6. Remove the outlier from both arrays and determine $\lambda$ again.
   Compare the time to reach $40\,°\text{C}$ with and without the outlier.

```{code-cell} python
# code cell
```
