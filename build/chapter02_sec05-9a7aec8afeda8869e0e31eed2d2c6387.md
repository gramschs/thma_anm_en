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

````{admonition} Exercise 2.1 (✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

t = np.linspace(0, 10, 5)
placeholder = np.zeros(3)
counter = np.array([2, 4, 6])
measurement = np.array([2, 4, 6.0])

print(t)
print(t.shape)
print(placeholder.dtype)
print(counter.dtype)
print(measurement.dtype)
```
Output:
```
[ 0.   2.5  5.   7.5 10. ]
(5,)
float64
int64
float64
```
`t` contains five evenly distributed values from 0 to 10, `t.shape` is
`(5,)`, that is, one dimension with five elements. `np.zeros()` and
`np.linspace()` always generate floating-point numbers. `counter` contains
only whole numbers, so NumPy chooses `int64`. In `measurement`, the single
decimal number `6.0` forces all values to be stored as `float64`, because an
array has exactly one data type.
````

````{admonition} Exercise 2.2 (✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

measurements_1 = np.array([2.0, 4.0, 6.0, 8.0])
measurements_2 = np.array([1.0, 2.0, 3.0, 4.0])
angle = np.array([0.0, np.pi / 2, np.pi])

print(measurements_1 + measurements_2)
print(measurements_1 * measurements_2)
print(measurements_1 / measurements_2)
print(measurements_2 ** 2)
print(np.sin(angle))
```
Output:
```
[ 3.  6.  9. 12.]
[ 2.  8. 18. 32.]
[2. 2. 2. 2.]
[ 1.  4.  9. 16.]
[0.0000000e+00 1.0000000e+00 1.2246468e-16]
```
All basic arithmetic operations act element-wise; each element is combined
with the element at the same position. `np.sin(np.pi)` does not yield exactly
`0`, but a tiny value on the order of `1e-16`. This is a rounding error of
floating-point arithmetic, because $\pi$ cannot be stored exactly in the
computer.
````

````{admonition} Exercise 2.3 (✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

pressure = np.array([4.9, 5.1, 5.0, 4.8, 5.2, 5.0, 4.95, 5.05])

print(np.mean(pressure))
print(np.std(pressure))
print(np.max(pressure) - np.min(pressure))
```
Output:
```
5.0
0.11456439237389597
0.40000000000000036
```
The mean is exactly 5.0 bar. The standard deviation is about 0.11 bar and
thus close to 0.1, because all measured values lie close to the mean, in the
band between 4.8 and 5.2 bar. `np.max(pressure) - np.min(pressure)` is the
range, that is, the distance between the largest and smallest measured value,
here 0.4 bar.
````

````{admonition} Exercise 2.4 (✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
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
1. The upper curve is dashed (`linestyle='dashed'`) and shows three full
   oscillations, since the frequency is 3 Hz and the range is one second
   long.
2. Nothing. `label='3 Hz'` only stores the label internally. Only
   `ax[0].legend()` would turn it into a visible legend.
3. `plt.subplots(nrows=2, ncols=1)` creates two subplots one below the other.
   The lower one is addressed with `ax[1]`, the upper one with `ax[0]`.
````

````{admonition} Exercise 2.5 (✩✩)
:class: tip
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
force_n = np.array([812, 798, 825, 803, 819, 807, 830, 815])
lower_limit = 780
upper_limit = 840

# Processing
mean = np.mean(force_n)
spread = np.std(force_n)
force_min = np.min(force_n)
force_max = np.max(force_n)
force_kn = force_n / 1000

# Output
print(f"Mean:               {mean:.1f} N")
print(f"Standard deviation: {spread:.1f} N")
print(f"Minimum:            {force_min} N")
print(f"Maximum:            {force_max} N")

if force_min >= lower_limit and force_max <= upper_limit:
    print("All measured values within the tolerance range.")
else:
    print("Tolerance range exceeded!")

print(f"Measurement series in kN: {force_kn}")
```
Output:
```
Mean:               813.6 N
Standard deviation: 10.2 N
Minimum:            798 N
Maximum:            830 N
All measured values within the tolerance range.
Measurement series in kN: [0.812 0.798 0.825 0.803 0.819 0.807 0.83  0.815]
```
The smallest value is 798 N, the largest 830 N. Both lie within the limits of
780 N and 840 N, so the joint is acceptable. The division by 1000 acts as a
vector operation on every element.
````

````{admonition} Exercise 2.6 (✩✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Input
def component_temperature(time, t_ambient, t_start, tau):
    """Computes the cooling curve of a component in still air.

    time:      time axis as a NumPy array in s
    t_ambient: ambient temperature in degrees Celsius
    t_start:   initial temperature of the component in degrees Celsius
    tau:       time constant of the cooling in s
    Returns:   temperature as a NumPy array in degrees Celsius
    """
    return t_ambient + (t_start - t_ambient) * np.exp(-time / tau)

time = np.linspace(0, 600, 100)

# Processing
temperature = component_temperature(time, 20, 200, 150)

# Output
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(time, temperature)
ax.set_xlabel('Time in s')
ax.set_ylabel('Temperature in degrees Celsius')
ax.set_title('Cooling of a component in still air')
ax.grid(True)
plt.show()
```
After 600 s the temperature has fallen to about 23 degrees Celsius and is
thus almost at ambient level. The curve falls steeply at the start and
becomes flatter and flatter as the temperature difference decreases.
````

````{admonition} Exercise 2.7 (✩✩)
:class: tip
The same component is cooled once in still air (`tau = 200`) and once with a
fan (`tau = 80`). In both cases the ambient temperature is 20 degrees Celsius
and the initial temperature is 200 degrees Celsius.

1. Compute both temperature curves for a time axis from 0 to 600 s with 100
   points. Use the formula from exercise 2.6.
2. Plot both curves in a common diagram, with a legend, axis labels, title
   and grid.

Structure your code with IPO comments (input, processing, output).
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Input
time = np.linspace(0, 600, 100)
t_ambient = 20
t_start = 200

# Processing
temperature_still_air = t_ambient + (t_start - t_ambient) * np.exp(-time / 200)
temperature_fan = t_ambient + (t_start - t_ambient) * np.exp(-time / 80)

# Output
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(time, temperature_still_air, label='Still air')
ax.plot(time, temperature_fan, label='With fan')
ax.set_xlabel('Time in s')
ax.set_ylabel('Temperature in degrees Celsius')
ax.set_title('Cooling with and without a fan')
ax.legend()
ax.grid(True)
plt.show()
```
With a fan the time constant is smaller, the component cools down
considerably faster. After 240 s it is almost at ambient temperature with a
fan, while in still air it is still over 70 degrees Celsius hot.
````

````{admonition} Exercise 2.8 (✩✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Input
rpm = np.array([500, 1000, 1500, 2000, 2500, 3000])
efficiency = np.array([0.89, 0.93, 0.95, 0.96, 0.94, 0.91])
efficiency_std = np.array([0.010, 0.008, 0.006, 0.006, 0.009, 0.012])

# Processing
i_best = np.argmax(efficiency)

# Output
fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(rpm, efficiency, yerr=efficiency_std,
            fmt='o', capsize=4, label='Measurement')
ax.scatter(rpm[i_best], efficiency[i_best],
           marker='*', s=200, color='red', zorder=5, label='Best efficiency')
ax.set_xlabel('Rotational speed in 1/min')
ax.set_ylabel('Efficiency')
ax.set_title('Gearbox efficiency with measurement uncertainty')
ax.legend()
ax.grid(True)
plt.show()
```
The best efficiency is at 2000 1/min with 0.96. Between 1500 and 2500 1/min
the curve is almost flat, so the gearbox works with good efficiency over a
wide rotational-speed range.
````

`````{admonition} Exercise 2.9 (✩✩✩) Mini-project: Characteristic curve of a centrifugal pump
:class: tip
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
`````

```{code-cell} python
# code cell
```

`````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Input
flow_rate = np.array([2, 4, 6, 8, 10, 12, 14, 16])
head = np.array([48, 47, 45, 42, 38, 33, 26, 18])
power_input = np.array([2700, 3550, 4080, 4520,
                        4970, 5400, 5760, 6280])

print(flow_rate.shape, head.shape, power_input.shape)

# Processing
flow_rate_m3s = flow_rate / 1000
p_hydraulic = 1000 * 9.81 * flow_rate_m3s * head
efficiency = p_hydraulic / power_input

flow_rate_best_efficiency = flow_rate[np.argmax(efficiency)]
mean_power = np.mean(p_hydraulic)
power_spread = np.std(p_hydraulic)
max_power = np.max(p_hydraulic)

# Output: scatter plot
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(flow_rate, head)
ax.set_xlabel('Volume flow rate in l/s')
ax.set_ylabel('Delivery head in m')
ax.set_title('Measured delivery head over the volume flow rate')
ax.grid(True)
plt.show()

# Output: characteristic map
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 8))

ax[0].plot(flow_rate, head)
ax[0].set_ylabel('Delivery head in m')

ax[1].plot(flow_rate, p_hydraulic)
ax[1].set_ylabel('Hydraulic power in W')

ax[2].plot(flow_rate, efficiency)
ax[2].set_ylabel('Efficiency')
ax[2].set_ylim(0, 1)

for single_axis in ax:
    single_axis.set_xlabel('Volume flow rate in l/s')
    single_axis.grid(True)

ax[0].set_title('Characteristic map of the centrifugal pump')
plt.tight_layout()
plt.show()

# Output: text report
print(f"Best efficiency at {flow_rate_best_efficiency} l/s")
print(f"Hydraulic power: mean {mean_power:.0f} W, "
      f"spread {power_spread:.0f} W, maximum {max_power:.0f} W")
```
Output:
```
(8,) (8,) (8,)
Best efficiency at 10 l/s
Hydraulic power: mean 2842 W, spread 952 W, maximum 3885 W
```
The best efficiency of about 0.75 is at 10 l/s, the largest hydraulic power
of about 3885 W only at 12 l/s.

**Closing question:** For continuous operation, the pump is designed for the
volume flow rate with the best efficiency, that is, about 10 l/s. There, the
least drive power is lost as losses. The falling delivery head means that the
pump can build up less and less pressure at higher flow. If the system
suddenly demands more volume flow, the delivery head drops, and beyond a
certain point the pressure is no longer sufficient to supply the system
against its resistance.
`````
