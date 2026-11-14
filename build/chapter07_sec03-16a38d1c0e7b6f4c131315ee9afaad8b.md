---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 7.3 Exercises

These exercises are meant for self-study at home and review the material of
Chapters 7.1 and 7.2. Allow about 45 minutes for them. Before starting the
exercises, run the following cell. It contains the function `derivative()`
from Chapter 7.1 and the functions `motion_profile()` and `velocity()` of the
smooth start from Chapter 7.2.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 7 min)
* ✩✩ Application: write your own code and interpret results (approx. 25 min)

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# function from Chapter 7.1
def derivative(values, dt):
    """Derivative of a measurement series with step size dt.

    Central difference quotient at the interior points, forward at the
    first point, backward at the last point.
    """
    n = len(values)
    result = np.zeros(n)
    result[0] = (values[1] - values[0]) / dt
    result[-1] = (values[-1] - values[-2]) / dt
    for k in range(1, n - 1):
        result[k] = (values[k + 1] - values[k - 1]) / (2 * dt)
    return result

# functions from Chapter 7.2
def motion_profile(t):
    """Distance in m for the smooth start, t in s from 0 to 2."""
    return 0.4 * (t - 2 / np.pi * np.sin(np.pi * t / 2))

def velocity(t):
    """Exact velocity in m/s, the derivative of motion_profile."""
    return 0.4 * (1 - np.cos(np.pi * t / 2))
```

````{admonition} Exercise 7.1 (✩)
:class: tip
With **average speed enforcement** on highways, cameras photograph every
vehicle at several checkpoints. From the distance between two checkpoints and
the time between the two photos, the system computes the speed. The following
code is given for a car that passes three checkpoints:

```python
import numpy as np

# location of the checkpoints in km and passing times in min
location = np.array([0.0, 6.0, 15.0])
time = np.array([0.0, 2.5, 7.0])

# speed on each section in km/h
v_section = np.zeros(len(location) - 1)
for k in range(len(location) - 1):
    v_section[k] = (location[k + 1] - location[k]) / (time[k + 1] - time[k]) * 60
print(v_section)

# speed over the entire route in km/h
v_total = (location[-1] - location[0]) / (time[-1] - time[0]) * 60
print(round(v_total, 1))
```

Write down your guess in a Markdown cell before you run the code.

1. What do the two `print()` lines output? What is the factor `60` for?
2. The speed limit is $130\,\text{km/h}$. Does the driver get a speeding
   ticket if the system evaluates both sections separately? And if it only
   evaluates the entire route?
3. On the second section, the result is $120\,\text{km/h}$. Could the driver
   still have driven faster than $130\,\text{km/h}$ there? Explain your answer
   using the terms difference quotient and derivative.
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

location = np.array([0.0, 6.0, 15.0])
time = np.array([0.0, 2.5, 7.0])

v_section = np.zeros(len(location) - 1)
for k in range(len(location) - 1):
    v_section[k] = (location[k + 1] - location[k]) / (time[k + 1] - time[k]) * 60
print(v_section)

v_total = (location[-1] - location[0]) / (time[-1] - time[0]) * 60
print(round(v_total, 1))
```
Output:

```text
[144. 120.]
128.6
```

1. The first line prints the speeds on the two sections, the second the speed
   over the entire route. Each value is a difference quotient as in
   Chapter 7.1: distance divided by time. Since the time is given in minutes,
   the result is in kilometers per minute, and the factor 60 converts it to
   kilometers per hour.
2. On the first section, the car covers $6\,\text{km}$ in $2.5\,\text{min}$,
   i.e. $144\,\text{km/h}$ on average. If the system evaluates the sections
   separately, the driver gets a speeding ticket. Over the entire route, the
   result is only $128.6\,\text{km/h}$, and the first section, where the car
   was too fast, no longer stands out in the average. This is not the mean
   $(144 + 120)/2 = 132\,\text{km/h}$ of the two sections. The car spends
   $4.5\,\text{min}$ on the slower section, but only $2.5\,\text{min}$ on the
   faster one. That is why the slower section carries more weight.
3. Yes. The $120\,\text{km/h}$ on the second section is also an average
   speed, a difference quotient over $4.5\,\text{min}$. The instantaneous
   speed, the derivative of the distance with respect to time, may have been
   considerably higher in between. Average speed enforcement does not detect
   this.
````

````{admonition} Exercise 7.2 (✩)
:class: tip
The AGV is recharging at its charging station. Every $10\,\text{min}$, the
charging station logs the state of charge of the battery in percent. The
following code is given:

```python
# state of charge in percent at 0, 10, 20, 30 and 40 min
dt = 10
state_of_charge = np.array([50.0, 65.0, 80.0, 90.0, 95.0])
print(derivative(state_of_charge, dt))
```

Write down your guess in a Markdown cell before you run the code.

1. Which difference quotient does `derivative()` use for the first, the
   second and the last value? What does the `print()` line output, and in
   what unit?
2. Which point in time does the last value fit best?
3. What does the trend of the values tell us about the charging?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
dt = 10
state_of_charge = np.array([50.0, 65.0, 80.0, 90.0, 95.0])
print(derivative(state_of_charge, dt))
```
Output:

```text
[1.5  1.5  1.25 0.75 0.5 ]
```

1. The first value is the forward difference quotient
   $(65 - 50)/10 = 1.5$, the second is the central difference quotient
   $(80 - 50)/20 = 1.5$, and the last is the backward difference quotient
   $(95 - 90)/10 = 0.5$. The values tell us by how many percentage points the
   state of charge rises per minute, so the unit is percentage points per
   minute. When the state of charge rises from 50 to 65 percent, that is 15
   percentage points, but the charge stored in the battery grows by 30
   percent. The first two values are equal because the state of charge rises
   by 15 percentage points in each of the two intervals of the first
   $20\,\text{min}$.
2. The last value is the average charging rate from $30$ to $40\,\text{min}$.
   So it fits $35\,\text{min}$ best, the midpoint of the interval, and not
   $40\,\text{min}$. This holds exactly if the charging rate changes uniformly
   in this interval. We do not know how it behaves between the measurements.
3. The computed charging rates decrease as the battery fills up. This is
   typical: from about 80 percent on, the charging electronics reduce the
   charging current to protect the battery.
````

````{admonition} Exercise 7.3 (✩)
:class: tip
The following code is given for the smooth start from Chapter 7.2:

```python
def backward(function, t, dt):
    """Backward difference quotient of function at the point t."""
    return (function(t) - function(t - dt)) / dt

t_0 = 1.0
exact = velocity(t_0)
for dt in [0.1, 0.05, 0.025]:
    deviation = backward(motion_profile, t_0, dt) - exact
    print(f'dt = {dt:5}: deviation {deviation:+.5f} m/s')
```

Write down your guess in a Markdown cell before you run the code.

1. Expand $s(t - \Delta t)$ with the Taylor expansion from Chapter 7.2 up to
   the term with $\Delta t^2$. To do so, replace $\Delta t$ with $-\Delta t$
   everywhere in the expansion of $s(t + \Delta t)$. Substitute the result
   into the backward difference quotient
   $(s(t) - s(t - \Delta t))/\Delta t$. Which error term is the largest one
   left?
2. At $t = 1\,\text{s}$, the acceleration reaches its maximum of
   $s''(1) = 0.628\,\text{m/s}^2$. Which deviations, including their signs,
   do you predict for the three step sizes?
3. By what factor does the deviation change from line to line?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def backward(function, t, dt):
    """Backward difference quotient of function at the point t."""
    return (function(t) - function(t - dt)) / dt

t_0 = 1.0
exact = velocity(t_0)
for dt in [0.1, 0.05, 0.025]:
    deviation = backward(motion_profile, t_0, dt) - exact
    print(f'dt = {dt:5}: deviation {deviation:+.5f} m/s')
```
Output:

```text
dt =   0.1: deviation -0.03135 m/s
dt =  0.05: deviation -0.01570 m/s
dt = 0.025: deviation -0.00785 m/s
```

1. With $-\Delta t$ instead of $\Delta t$, the odd powers of $\Delta t$
   change sign:

   $$s(t - \Delta t) = s(t) - \Delta t \cdot s'(t) + \frac{\Delta t^2}{2}
   \cdot s''(t) - \ldots$$

   Substituting this into the backward difference quotient gives

   $$\frac{s(t) - s(t - \Delta t)}{\Delta t} = s'(t) - \frac{\Delta t}{2}
   \cdot s''(t) + \ldots$$

   The largest error term is $-\frac{\Delta t}{2} \cdot s''(t)$. It has the
   same absolute value as for the forward difference quotient, but the
   opposite sign.
2. With $s''(1) = 0.628\,\text{m/s}^2$, the error term predicts the
   deviations $-0.0314$, $-0.0157$ and $-0.0079\,\text{m/s}$. The computed
   values agree with them almost exactly. At $t = 1\,\text{s}$, the jerk is
   zero, so the next term of the Taylor expansion vanishes as well. The
   negative sign matches Chapter 7.1: the backward difference quotient
   averages over the time before $t = 1\,\text{s}$, when the AGV was still
   slower.
3. When the step size is halved, the deviation is halved as well. So the error
   is proportional to $\Delta t$, and the order of accuracy is 1, as for the
   forward difference quotient.
````

````{admonition} Exercise 7.4 (✩✩)
:class: tip
An AGV drives straight through the warehouse. At $t = 0.4\,\text{s}$, the
safety scanner from Chapter 6.2 detects an obstacle in the protective field,
and the AGV brakes as hard as it can. An unsecured steel wire mesh container
stands on its load platform. With a coefficient of static friction of
$\mu = 0.2$, the container slides as soon as the deceleration exceeds
$\mu \cdot g = 0.2 \cdot 9.81\,\text{m/s}^2 \approx 1.96\,\text{m/s}^2$.
During the drive, the AGV logged its position ten times per second:

```python
# step size in s and times 0.0, 0.1, ..., 1.5 s
dt = 0.1
t = np.linspace(0, 1.5, 16)
# distance traveled in m, rounded to millimeters
s = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.488, 0.55, 0.588,
              0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
```

1. Use `derivative()` to compute the velocity. How fast was the AGV moving
   before it braked? How long is the braking distance from the start of
   braking at $t = 0.4\,\text{s}$ until the AGV stops?
2. Compute the acceleration and plot velocity and acceleration in two
   subplots, one above the other. Draw the limit above which the container
   slides as a horizontal line, like the planned acceleration in Chapter 7.1.
   Determine the largest deceleration with `np.min()`. Does the container
   slide?
3. Answer without code: the AGV brakes as hard as it can, abruptly and with
   constant deceleration. Why does the computed deceleration nevertheless rise
   gradually over several points in time and then drop again?
4. With constant deceleration $a$, the braking distance is $v_0^2 / (2a)$.
   Check the formula with your results from tasks 1 and 2. The fleet manager
   is supposed to limit the deceleration to $1.96\,\text{m/s}^2$ so that the
   container does not slide. How long will the braking distance be then, and
   what does that mean for the protective field?

Structure your code with IPO comments (input, processing, output).
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
# Input: log of the drive and limit for the container
dt = 0.1
t = np.linspace(0, 1.5, 16)
s = np.array([0.0, 0.1, 0.2, 0.3, 0.4, 0.488, 0.55, 0.588,
              0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6])
limit = 0.2 * 9.81    # largest deceleration without sliding in m/s²

# Processing: velocity and braking distance from t = 0.4 s (index 4)
v = derivative(s, dt)
v_0 = v[0]
braking_dist = s[-1] - s[4]

# Processing: acceleration and largest deceleration
a = derivative(v, dt)
decel_max = -np.min(a)

# Processing: braking distance from the formula, measured and limited
braking_dist_formula = v_0**2 / (2 * decel_max)
braking_dist_limited = v_0**2 / (2 * limit)

# Output
print(f'Velocity before braking: {v_0:.2f} m/s')
print(f'Braking distance: {braking_dist:.3f} m')
print(f'Largest deceleration: {decel_max:.2f} m/s²')
if decel_max > limit:
    print('The container slides.')
else:
    print('The container stays in place.')
print(f'Braking distance at {decel_max:.2f} m/s²: {braking_dist_formula:.3f} m')
print(f'Braking distance at {limit:.2f} m/s²: {braking_dist_limited:.3f} m')

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(7, 6))
ax[0].plot(t, v, marker='o')
ax[0].set_ylabel('Velocity in m/s')
ax[1].plot(t, a, marker='o', label='from measurement')
# limit as a line from t = 0 s to t = 1.5 s
ax[1].plot([0, 1.5], [-limit, -limit], color='gray', linestyle='--',
           label='limit: container slides')
ax[1].set_ylabel('Acceleration in m/s²')
ax[1].legend()
for single_axis in ax:
    single_axis.set_xlabel('Time in s')
    single_axis.grid(True)
ax[0].set_title('Emergency stop of the AGV')
plt.tight_layout()
plt.show()
```
Output:

```text
Velocity before braking: 1.00 m/s
Braking distance: 0.200 m
Largest deceleration: 2.50 m/s²
The container slides.
Braking distance at 2.50 m/s²: 0.200 m
Braking distance at 1.96 m/s²: 0.255 m
```

1. Before braking, the AGV moves at $1.00\,\text{m/s}$. The braking distance
   is the distance from the start of braking at index 4 until the AGV stops,
   i.e. $0.200\,\text{m}$.
2. The largest deceleration is $2.50\,\text{m/s}^2$, which is above the limit
   of $1.96\,\text{m/s}^2$. So the unsecured container slides. In the plot,
   the acceleration is below the gray line at $0.5$, $0.6$ and
   $0.7\,\text{s}$. As with the planned acceleration in Chapter 7.1, we draw
   the line with `ax.plot()` through two points.
3. Each value of the velocity uses the positions $0.1\,\text{s}$ before and
   after, so each value of the acceleration uses positions from
   $0.2\,\text{s}$ before to $0.2\,\text{s}$ after. The braking lasts only
   $0.4\,\text{s}$. Only at $t = 0.6\,\text{s}$ does this window lie entirely
   within the braking, and only there does the full deceleration of
   $2.5\,\text{m/s}^2$ show up. At the other points in time, the window mixes
   driving and braking or braking and standstill, so the computed deceleration
   is smaller there. Differentiating twice smears out the jump in the
   acceleration, just like the kink in Chapter 7.1.
4. With $v_0 = 1\,\text{m/s}$ and $a = 2.5\,\text{m/s}^2$, the formula gives
   $0.200\,\text{m}$, exactly the braking distance from task 1. If the fleet
   manager limits the deceleration to $1.96\,\text{m/s}^2$, the braking
   distance increases to $0.255\,\text{m}$, a good $5\,\text{cm}$ more. So the
   AGV has to start braking earlier, and the protective field has to extend
   farther forward. The protective field from Chapter 6.2 extends
   $1\,\text{m}$ beyond the front edge. In our simplified model without
   reaction time, that is still enough.
````
