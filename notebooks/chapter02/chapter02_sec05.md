---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.5 Exercises

These exercises are intended for self-study at home and review the material
of chapters 2.1 to 2.4. Expect around 90 minutes of working time.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 5 min)
* ✩✩ Application: write your own code and interpret results (approx. 10 min)
* ✩✩✩ Mini-project: combine several concepts of the part (approx. 30 min)

## Exercise 2.1 (✩)

The following code is given:

```python
import numpy as np

t = np.linspace(0, 10, 5)
placeholder = np.zeros(3)
counter = np.array([2, 4, 6])
measurement = np.array([2, 4, 6.0])
```

Note down your guess before you run the code.

1. Which values does `t` contain and what does `t.shape` return?
2. What does `placeholder.dtype` return?
3. What does `counter.dtype` return and what does `measurement.dtype`? Why do
   the two differ, even though only one number is written differently?
4. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 2.2 (✩)

Two measurement series are given:

```python
import numpy as np

measurements_1 = np.array([2.0, 4.0, 6.0, 8.0])
measurements_2 = np.array([1.0, 2.0, 3.0, 4.0])
angle = np.array([0.0, np.pi / 2, np.pi])
```

Note down your guess before you run the code.

1. What do `measurements_1 + measurements_2`, `measurements_1 * measurements_2`
   and `measurements_1 / measurements_2` return?
2. What does `measurements_2 ** 2` return?
3. What does `np.sin(angle)` return? Why is the value not exactly `0` at the
   position of $\pi$?
4. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 2.3 (✩)

On a hydraulic test rig, the system pressure is measured eight times, in bar:

```python
import numpy as np

pressure = np.array([4.9, 5.1, 5.0, 4.8, 5.2, 5.0, 4.95, 5.05])
```

Answer first without code:

1. Is `np.mean(pressure)` closer to 5.0 or to 5.5?
2. Is `np.std(pressure)` closer to 0.1 or to 1.0? Justify with a look at the
   measured values.
3. What does `np.max(pressure) - np.min(pressure)` compute in terms of
   content?
4. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 2.4 (✩)

The following code is given:

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

t = np.linspace(0, 1, 500)

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
ax[0].plot(t, np.sin(2 * np.pi * 3 * t), linestyle='dashed', label='3 Hz')
ax[1].plot(t, np.exp(-2 * t))
plt.tight_layout()
plt.show()
```

Note down your guess before you run the code.

1. Which line style does the upper curve have and how many full oscillations
   does it show in the plotted range?
2. The upper `plot` call has `label='3 Hz'`, but there is no call to
   `ax[0].legend()`. What can be seen in the diagram as a result?
3. How many subplots does `plt.subplots(nrows=2, ncols=1)` create and how do
   you address the lower one?
4. Run the code and check your predictions.

```{code-cell} python
# code cell
```

## Exercise 2.5 (✩✩)

On a test rig, the holding force of a bolted joint is measured eight times,
in newtons:

```python
force_n = np.array([812, 798, 825, 803, 819, 807, 830, 815])
```

1. Compute the mean, standard deviation, minimum and maximum and print the
   results formatted.
2. The joint is considered acceptable if all measured values lie between
   780 N and 840 N. Check this with an `if` check over `np.min(force_n)` and
   `np.max(force_n)` and print a suitable message.
3. Convert the measurement series to kilonewtons (1 kN = 1000 N) and print
   the array `force_kn`.

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 2.6 (✩✩)

A hot component cools down in still air. The temperature follows the decay
law

$$T(t) = T_\text{ambient} + (T_\text{start} - T_\text{ambient}) \cdot e^{-t / \tau}$$

1. Write a function
   `component_temperature(time, t_ambient, t_start, tau)` that returns the
   temperature as a NumPy array. Give the function a docstring.
2. Call the function for a time axis from 0 to 600 s with 100 points, with
   `t_ambient = 20`, `t_start = 200` and `tau = 150`.
3. Plot the temperature curve as a line plot, with axis labels, title and
   grid.

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 2.7 (✩✩)

The same component is cooled once in still air (`tau = 200`) and once with a
fan (`tau = 80`). In both cases the ambient temperature is 20 degrees Celsius
and the initial temperature is 200 degrees Celsius.

1. Compute both temperature curves for a time axis from 0 to 600 s with 100
   points. Use the formula from exercise 2.6.
2. Plot both curves in a common diagram, with a legend, axis labels, title
   and grid.

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 2.8 (✩✩)

The efficiency of a gearbox is measured at six rotational speeds, each value
as the mean of several repeats with a standard deviation:

```python
rpm = np.array([500, 1000, 1500, 2000, 2500, 3000])
efficiency = np.array([0.89, 0.93, 0.95, 0.96, 0.94, 0.91])
efficiency_std = np.array([0.010, 0.008, 0.006, 0.006, 0.009, 0.012])
```

1. Plot the efficiency over the rotational speed with `ax.errorbar()` and
   error bars in the y-direction (`fmt='o'`, `capsize=4`).
2. Determine the point with the best efficiency with `np.argmax()` and draw
   it with a second `ax.scatter()` call as a large star (`marker='*'`,
   `s=200`).
3. Label the axes and title and show a legend.

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

## Exercise 2.9 (✩✩✩) Mini-project: Characteristic curve of a centrifugal pump

On a pump test rig, the volume flow rate is increased in eight steps. At each
step, the delivery head and the electrical power input are measured:

```python
flow_rate = np.array([2, 4, 6, 8, 10, 12, 14, 16])                # l/s
head = np.array([48, 47, 45, 42, 38, 33, 26, 18])                 # m
power_input = np.array([2700, 3550, 4080, 4520,
                        4970, 5400, 5760, 6280])                  # W
```

**Part 1:** Create the three measurement series as arrays and check with
`.shape` that they are all the same length. Plot the delivery head over the
volume flow rate as a scatter plot.

**Part 2:** Compute the hydraulic power
`p_hydraulic = 1000 * 9.81 * flow_rate_m3s * head`, where
`flow_rate_m3s = flow_rate / 1000` is the volume flow rate in m³/s. Compute
the efficiency `efficiency = p_hydraulic / power_input`.

**Part 3:** Create a Figure with three subplots one below the other: delivery
head, hydraulic power and efficiency, each over the volume flow rate. Give
the efficiency subplot the full scale with `set_ylim(0, 1)`. Set the x-axis
label and the grid via a `for` loop.

**Part 4:** Determine the volume flow rate with the best efficiency with
`np.argmax()`. Also compute the mean, standard deviation and maximum of the
hydraulic power. Print the results as a short text report with f-strings.

**Closing question:** The best efficiency and the largest hydraulic power
occur at different volume flow rates. For which volume flow rate should the
pump be designed for continuous operation, and what does the falling delivery
head mean for operation if suddenly more flow is demanded?

Structure your code with IPO comments (input, processing, output).

```{code-cell} python
# code cell
```

