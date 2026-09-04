---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.2 Test Rig for a Wind Turbine

In chapter 2.1 we created NumPy arrays, processed them with vector operations
and functions such as `np.exp()` and summarized them into key figures with
`np.mean()` and `np.std()`. In this chapter we apply these tools to a
coherent case: the analysis of a test-rig run for a wind turbine. Work
through the sub-tasks in pairs if possible and in order, because each part
builds on the results of the previous one.

````{admonition} Project: Test-rig run of a wind turbine (✩✩)
:class: tip
A test run measures the wind speed at eight points in time during a 70-second
start-up phase (in m/s):

```text
3.2, 5.1, 6.8, 7.5, 6.2, 4.9, 5.5, 6.0
```

From these measured values we determine step by step the electrical power
that the generator delivers, and then characterize the test run
statistically.
````

```{admonition} Part 1: Create data and time axis
:class: tip
Create the wind speeds as an array `wind_speed`. Also create a time axis
`time` with eight evenly distributed values between 0 and 70 s, without
writing down the values one by one. Print the shape and data type of both
arrays.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 1
:class: tip
:class: dropdown
```python
import numpy as np

wind_speed = np.array([3.2, 5.1, 6.8, 7.5, 6.2, 4.9, 5.5, 6.0])
time = np.linspace(0, 70, 8)

print(wind_speed.shape, wind_speed.dtype)
print(time.shape, time.dtype)
```
Both arrays have the shape `(8,)` and the data type `float64`.
`np.linspace(0, 70, 8)` generates the points in time 0, 10, 20 up to 70 s, so
the interval between two measurements is 10 s.
````

```{admonition} Part 2: Compute the rotor power
:class: tip
The rotor power can be computed in simplified form as $P = k \cdot v^3$, with
$k = 1.2$. Compute `rotor_power` in watts from `wind_speed`.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 2
:class: tip
:class: dropdown
```python
k = 1.2
rotor_power = k * wind_speed**3
print(rotor_power)
```
The power `**3` and the multiplication by `k` act element-wise on the whole
array. Because the power grows with the third power of the wind speed, the
fastest measured value (7.5 m/s) already delivers about thirteen times as
much (around 506 W) as the slowest (3.2 m/s, around 39 W).
````

```{admonition} Part 3: Efficiency of the generator
:class: tip
The generator needs a start-up time to reach its full efficiency. The
efficiency at time $t$ follows approximately

$$\eta(t) = \eta_{max} \cdot \left(1 - e^{-t/\tau}\right)$$

with $\eta_{max} = 0.95$ and $\tau = 20\,\text{s}$. Compute `efficiency` for
the points in time from `time`.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 3
:class: tip
:class: dropdown
```python
eta_max = 0.95
tau = 20.0
efficiency = eta_max * (1 - np.exp(-time / tau))
print(efficiency)
```
`np.exp()` acts element-wise on `-time / tau`. At time 0 s the efficiency is
0, after which it approaches the limit value 0.95. After 70 s, that is, three
and a half time constants, about 97 percent of this limit value is reached.
````

```{admonition} Part 4: Electrical power
:class: tip
Compute the electrical power actually delivered, `electrical_power`, from
`rotor_power` and `efficiency`.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 4
:class: tip
:class: dropdown
```python
electrical_power = rotor_power * efficiency
print(electrical_power)
```
Both arrays have eight elements, so NumPy multiplies them pairwise: at each
point in time the rotor power is weighted by the corresponding efficiency. At
the first point in time the result is 0 W, because the generator has not yet
started up.
````

```{admonition} Part 5: Characterize the test run
:class: tip
Determine the mean, minimum and maximum delivered power, as well as the
scatter of the power around the mean.
```

```{code-cell} python
# code cell
```

````{admonition} Solution Part 5
:class: tip
:class: dropdown
```python
mean_power = np.mean(electrical_power)
min_power = np.min(electrical_power)
max_power = np.max(electrical_power)
spread = np.std(electrical_power)

print(f"Mean:    {mean_power:.1f} W")
print(f"Minimum: {min_power:.1f} W")
print(f"Maximum: {max_power:.1f} W")
print(f"Spread:  {spread:.1f} W")
```
The minimum of 0 W comes from the first point in time, at which the generator
is still at rest. The scatter is of the same order of magnitude as the mean,
so the test run delivers a very uneven power. This is due both to the
start-up phase of the generator and to the fluctuating wind speed.
````

```{admonition} Closing question
:class: tip
Answer in your own words, without further code:

1. The wind speed in the test run only fluctuates between about 3 and 8 m/s.
   Why does the rotor power nevertheless fluctuate so much more strongly?
2. What does the large scatter of the electrical power mean for the operation
   of the turbine? Name one practical consequence.
```

````{admonition} Solution closing question
:class: tip
:class: dropdown
1. The rotor power grows with the third power of the wind speed
   ($P = k \cdot v^3$). Through the third power, the ratio of about 8 to 3
   between the two wind speeds becomes a ratio of about 19 to 1 in the rotor
   power. Even moderate changes in wind speed therefore have a
   disproportionate effect on the power.
2. A strongly fluctuating electrical power stresses the power grid and the
   power electronics of the turbine. In practice, the turbine must cushion
   the fluctuations, for example by controlling the rotor blades, by buffer
   storage or by feeding into the grid only above a minimum wind speed.
````

````{admonition} Bonus exercise: Second site (✩✩✩)
:class: tip
A second test run at a windier site delivers the following wind speeds (m/s)
at the same eight points in time:

```text
7.5, 8.1, 6.9, 9.2, 8.8, 7.6, 8.4, 9.0
```

Carry out the calculation from Part 1 to Part 5 for this second site. The
time axis and the efficiency curve depend only on the start-up time, not on
the site, and therefore remain unchanged. Which site delivers more power on
average? Which delivers the more even power relative to the mean?
````

```{code-cell} python
# code cell
```

````{admonition} Solution bonus exercise
:class: tip
:class: dropdown
```python
wind_speed_2 = np.array([7.5, 8.1, 6.9, 9.2, 8.8, 7.6, 8.4, 9.0])

# k and efficiency come from Part 2 and Part 3 and apply unchanged.
rotor_power_2 = k * wind_speed_2**3
electrical_power_2 = rotor_power_2 * efficiency

mean_power_2 = np.mean(electrical_power_2)
spread_2 = np.std(electrical_power_2)

print(f"Site 1: {mean_power:.1f} W (spread {spread:.1f} W)")
print(f"Site 2: {mean_power_2:.1f} W (spread {spread_2:.1f} W)")

print(f"Spread/mean site 1: {spread / mean_power:.2f}")
print(f"Spread/mean site 2: {spread_2 / mean_power_2:.2f}")
```
Site 2 delivers a considerably higher mean power, because the wind speeds are
consistently higher and the power grows with the third power. The absolute
scatter is also larger at site 2. More meaningful is the ratio of scatter to
mean: this value is smaller at site 2, so the power there is more even in
relative terms.
````
