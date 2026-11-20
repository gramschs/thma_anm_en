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

````{admonition} Project: When can the part be packed? (✩✩)
:class: tip
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
````

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

```{admonition} Part 1: Model and first estimate
:class: tip
Like `total_cost()` in Chapter 8.1, write a function `model(t, lam)` that
computes the temperature according to the law of cooling. Python reserves the
word `lambda` for something else, so the parameter is called `lam`.

Plot the measurements as points and the model for $\lambda = 0.03$ and
$\lambda = 0.08\,\text{1/s}$ as lines. To get smooth lines, evaluate the model
at 200 times between $0$ and $60\,\text{s}$.

Which of the two model curves cools down too slowly, and which too quickly?
Roughly where is the value of $\lambda$ we are looking for?
```

```{code-cell} python
# code cell
```

````{admonition} Hint Part 1
:class: tip
:class: dropdown
The function is built like `total_cost()` in Chapter 8.1. Since `np.exp()`
works with arrays, `model()` also works for an array of times. `ax.scatter()`
plots points.
```python
def model(t, lam):
    """Temperature in °C at the time t according to the law of cooling."""
    return ___

# 200 times for smooth model curves
t_fine = np.linspace(___, ___, 200)

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(t_meas, T_meas, color='black', label='measurements')
for lam in [0.03, 0.08]:
    ax.plot(t_fine, ___, label=f'model with λ = {lam} 1/s')
ax.set_xlabel('Time in s')
ax.set_ylabel('Temperature in °C')
ax.set_title('Cooling of an aluminum part')
ax.legend()
ax.grid(True)
plt.show()
```
````

````{admonition} Solution Part 1
:class: tip
:class: dropdown
```python
def model(t, lam):
    """Temperature in °C at the time t according to the law of cooling."""
    return T_ambient + (T_start - T_ambient) * np.exp(-lam * t)

# 200 times for smooth model curves
t_fine = np.linspace(0, 60, 200)

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(t_meas, T_meas, color='black', label='measurements')
for lam in [0.03, 0.08]:
    ax.plot(t_fine, model(t_fine, lam), label=f'model with λ = {lam} 1/s')
ax.set_xlabel('Time in s')
ax.set_ylabel('Temperature in °C')
ax.set_title('Cooling of an aluminum part')
ax.legend()
ax.grid(True)
plt.show()
```
With $\lambda = 0.03\,\text{1/s}$, the model curve lies above the
measurements, so the model cools down too slowly. With
$\lambda = 0.08\,\text{1/s}$, it lies below them, so the model cools down too
quickly. The larger $\lambda$, the faster the temperature approaches that of
the factory. So the value of $\lambda$ we are looking for lies between the two
estimates, at roughly
$0.05\,\text{1/s}$ by eye.
````

````{admonition} Part 2: Cost function from the measured data
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Hint Part 2
:class: tip
:class: dropdown
`model(t_meas, lam)` returns the model values at all 13 measurement times at
once. As in Chapter 7.1, we collect the 300 values of $C$ in an array that we
create beforehand with `np.zeros()`.
```python
def cost(lam):
    """Mean squared error in °C² between measurement and model."""
    deviation = ___
    return np.mean(___)

# C for 300 values of lambda
lam_values = np.linspace(___, ___, 300)
cost_values = np.zeros(len(lam_values))
for k in range(len(lam_values)):
    cost_values[k] = ___

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(lam_values, cost_values)
ax.set_xlabel('λ in 1/s')
ax.set_ylabel('C in °C²')
ax.set_title('Mean squared error')
ax.grid(True)
plt.show()
```
````

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
def cost(lam):
    """Mean squared error in °C² between measurement and model."""
    deviation = T_meas - model(t_meas, lam)
    return np.mean(deviation**2)

# C for 300 values of lambda
lam_values = np.linspace(0.01, 0.12, 300)
cost_values = np.zeros(len(lam_values))
for k in range(len(lam_values)):
    cost_values[k] = cost(lam_values[k])

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(lam_values, cost_values)
ax.set_xlabel('λ in 1/s')
ax.set_ylabel('C in °C²')
ax.set_title('Mean squared error')
ax.grid(True)
plt.show()
```
The cost function has a clear minimum at about $0.05\,\text{1/s}$. We average
squared temperature differences, so $C$ has the unit $°\text{C}^2$. The shape
resembles the curve in Chapter 8.1: to the left of the minimum, the curve
drops steeply, and to the right, it rises more gently.
````

````{admonition} Part 3: Gradient descent
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Hint Part 3
:class: tip
:class: dropdown
A step is the learning rate times the slope. For a step of
$0.02\,\text{1/s}$, we divide $0.02$ by the absolute value of the slope.
```python
# slope at the starting value and a suitable learning rate
slope_start = central(___, ___, 1e-6)
learning_rate_estimate = ___ / abs(slope_start)
print(f'Slope at the start: {slope_start:.0f} °C² s')
print(f'Estimated learning rate: {learning_rate_estimate:.1e}')
```
In the code for the convergence plot, fill in the cost function and the
starting value.
````

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
# slope at the starting value and a suitable learning rate
slope_start = central(cost, 0.03, 1e-6)
learning_rate_estimate = 0.02 / abs(slope_start)
print(f'Slope at the start: {slope_start:.0f} °C² s')
print(f'Estimated learning rate: {learning_rate_estimate:.1e}')

# convergence plot for four learning rates
fig, ax = plt.subplots(figsize=(7, 4))
for learning_rate in [1e-6, 2e-6, 5e-6, 1e-5]:
    history = gradient_descent(cost, 0.03, learning_rate, 1e-3, 100)
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
Output:

```text
Slope at the start: -19224 °C² s
Estimated learning rate: 1.0e-06
Learning rate 1e-06: 30 iterations, λ = 0.05038 1/s
Learning rate 2e-06: 15 iterations, λ = 0.05038 1/s
Learning rate 5e-06: 74 iterations, λ = 0.05038 1/s
Learning rate 1e-05: 100 iterations, λ = 0.12026 1/s
```
The slope is very large, but $\lambda$ itself is small. So for a step of only
a few hundredths, the learning rate has to be tiny. The estimate gives
$10^{-6}$. Three of the four learning rates find
$\lambda = 0.0504\,\text{1/s}$, and the fastest is $2 \cdot 10^{-6}$ with 15
iterations. With $5 \cdot 10^{-6}$, the first step jumps to
$0.126\,\text{1/s}$, far past the minimum, and the method takes a long time to
come back. With $10^{-5}$, it jumps back and forth erratically and does not
meet the stopping criterion within 100 iterations, so the result is useless.
````

````{admonition} Part 4: Checking the result and computing the waiting time
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Hint Part 4
:class: tip
:class: dropdown
The last entry of `history` is the $\lambda$ found by the method. The plot is
created as in Part 1, only with a single model curve.
```python
# best lambda from gradient descent
history = gradient_descent(cost, 0.03, ___, 1e-3, 100)
lam_best = ___

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(t_meas, T_meas, color='black', label='measurements')
ax.plot(t_fine, ___, label=f'model with λ = {lam_best:.4f} 1/s')
ax.set_xlabel('Time in s')
ax.set_ylabel('Temperature in °C')
ax.set_title('Fitted cooling model')
ax.legend()
ax.grid(True)
plt.show()

# time to reach 40 °C
t_40 = ___
print(f'Time to reach 40 °C: {t_40:.1f} s')
```
````

````{admonition} Solution Part 4
:class: tip
:class: dropdown
```python
# best lambda from gradient descent
history = gradient_descent(cost, 0.03, 2e-6, 1e-3, 100)
lam_best = history[-1]

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(t_meas, T_meas, color='black', label='measurements')
ax.plot(t_fine, model(t_fine, lam_best),
        label=f'model with λ = {lam_best:.4f} 1/s')
ax.set_xlabel('Time in s')
ax.set_ylabel('Temperature in °C')
ax.set_title('Fitted cooling model')
ax.legend()
ax.grid(True)
plt.show()

# time to reach 40 °C
t_40 = np.log((T_start - T_ambient) / (40 - T_ambient)) / lam_best
print(f'Time to reach 40 °C: {t_40:.1f} s')
```
Output:

```text
Time to reach 40 °C: 27.5 s
```
The model curve runs right through the middle of the data points, with
some points slightly above it and some slightly below. After $27.5\,\text{s}$,
the part has cooled down to $40\,°\text{C}$.
````

```{admonition} Closing question
:class: tip
1. The conveyor belt moves at $0.05\,\text{m/s}$. What is the minimum length
   of the cooling section?
2. The smallest value of the cost function is not zero, but
   $C = 0.36\,°\text{C}^2$. Why does gradient descent not find a $\lambda$ for
   which $C$ is zero? What does the square root of this value tell us about
   the fit?
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
1. In $27.5\,\text{s}$ at $0.05\,\text{m/s}$, the part travels
   $0.05\,\text{m/s} \cdot 27.5\,\text{s} \approx 1.38\,\text{m}$. Allowing
   for some margin, the cooling section should be at least $1.5\,\text{m}$
   long.
2. $C$ would only be zero if the model curve passed exactly through all 13
   data points. There are two reasons why it does not. First, the
   thermocouple does not measure exactly, and measurement noise pushes each
   reading a little up or down. Second, the law of cooling is a
   simplification. For example, it assumes that the part has the same
   temperature throughout and that the fan cools it evenly. A smooth curve
   with a single free parameter can follow neither the noise nor every detail
   of the real cooling process.

   The square root of the mean squared error is in $°\text{C}$ again. Here it
   is $\sqrt{0.36\,°\text{C}^2} = 0.6\,°\text{C}$. So a typical measurement
   lies about $0.6\,°\text{C}$ off the model curve. This is accurate enough for
   designing the cooling section. The value alone does not tell us how much of
   it is measurement noise and how much is model error. Only the deviations of
   the individual measurements from the curve reveal that. If they scatter
   up and down without a pattern, noise dominates. If they stay on the same
   side of the curve over longer stretches, the model does not describe the
   process accurately.
````

````{admonition} Bonus exercise: An outlier in the measurements (✩✩✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
1. The cost function is the same as in Part 2, only with `T_faulty`:

   ```python
   # task 1: lambda from the data with the faulty reading
   T_faulty = T_meas.copy()
   T_faulty[6] = T_faulty[6] + 10

   def cost_faulty(lam):
       """Mean squared error for the data with the faulty reading."""
       deviation = T_faulty - model(t_meas, lam)
       return np.mean(deviation**2)

   history = gradient_descent(cost_faulty, 0.03, 2e-6, 1e-3, 100)
   lam_faulty = history[-1]
   print(f'λ with outlier: {lam_faulty:.4f} 1/s')
   ```

   With the outlier, we get $\lambda = 0.0482\,\text{1/s}$ instead of
   $0.0504\,\text{1/s}$.
2. We compute the residuals with the $\lambda$ from task 1:

   ```python
   # task 2: residuals against time
   residuals = T_faulty - model(t_meas, lam_faulty)
   print('Residuals in °C:', np.round(residuals, 1))

   fig, ax = plt.subplots(figsize=(7, 4))
   ax.plot(t_meas, residuals, marker='o', linestyle='none')
   ax.axhline(0, color='gray')
   ax.set_xlabel('Time in s')
   ax.set_ylabel('Residual in °C')
   ax.set_title('Residuals with outlier')
   ax.grid(True)
   plt.show()
   ```

   Output:

   ```text
   Residuals in °C: [ 0.  -0.3 -1.2 -1.9 -1.5 -2.1  9.1  0.4 -1.3 -1.3 -0.1 -0.1 -0.3]
   ```

   At $9.1\,°\text{C}$, the residual at $30\,\text{s}$ is more than four times
   as large as any of the others. Notice also that the residuals from
   $10\,\text{s}$ to $25\,\text{s}$ are all negative. The outlier pulls the
   model curve upward, so near the outlier the curve lies above the correct
   measurements. Because the deviations are squared, a single large error
   carries a lot of weight.
3. We remove the entry at index 6 from both arrays:

   ```python
   # task 3: remove the outlier and determine lambda again
   t_clean = np.delete(t_meas, 6)
   T_clean = np.delete(T_faulty, 6)

   def cost_clean(lam):
       """Mean squared error without the outlier."""
       deviation = T_clean - model(t_clean, lam)
       return np.mean(deviation**2)

   history = gradient_descent(cost_clean, 0.03, 2e-6, 1e-3, 100)
   lam_clean = history[-1]

   # time to reach 40 °C with and without the outlier
   ratio = (T_start - T_ambient) / (40 - T_ambient)
   t_40_faulty = np.log(ratio) / lam_faulty
   t_40_clean = np.log(ratio) / lam_clean
   print(f'λ without outlier: {lam_clean:.4f} 1/s')
   print(f'Time to reach 40 °C with outlier:    {t_40_faulty:.1f} s')
   print(f'Time to reach 40 °C without outlier: {t_40_clean:.1f} s')
   ```

   Output:

   ```text
   λ without outlier: 0.0504 1/s
   Time to reach 40 °C with outlier:    28.8 s
   Time to reach 40 °C without outlier: 27.5 s
   ```

   Without the outlier, we again find $\lambda = 0.0504\,\text{1/s}$ and a time
   of $27.5\,\text{s}$ to reach $40\,°\text{C}$. A single bad reading increased
   the waiting time by more than a second. Here the error is harmless, because
   it leads to a longer cooling section and thus errs on the safe side. If the
   faulty reading had been $10\,°\text{C}$ too low, we would have
   underestimated the waiting time. That is why the residuals should be checked
   whenever a model is fitted to measured data.
````
