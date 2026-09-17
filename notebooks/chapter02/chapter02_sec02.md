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

## Project: Test-rig run of a wind turbine (✩✩)

A test run measures the wind speed at eight points in time during a 70-second
start-up phase (in m/s):

```text
3.2, 5.1, 6.8, 7.5, 6.2, 4.9, 5.5, 6.0
```

From these measured values we determine step by step the electrical power
that the generator delivers, and then characterize the test run
statistically.

## Part 1: Create data and time axis

Create the wind speeds as an array `wind_speed`. Also create a time axis
`time` with eight evenly distributed values between 0 and 70 s, without
writing down the values one by one. Print the shape and data type of both
arrays.

```{code-cell} python
# code cell
```

## Part 2: Compute the rotor power

The rotor power can be computed in simplified form as $P = k \cdot v^3$, with
$k = 1.2$. Compute `rotor_power` in watts from `wind_speed`.

```{code-cell} python
# code cell
```

## Part 3: Efficiency of the generator

The generator needs a start-up time to reach its full efficiency. The
efficiency at time $t$ follows approximately

$$\eta(t) = \eta_{max} \cdot \left(1 - e^{-t/\tau}\right)$$

with $\eta_{max} = 0.95$ and $\tau = 20\,\text{s}$. Compute `efficiency` for
the points in time from `time`.

```{code-cell} python
# code cell
```

## Part 4: Electrical power

Compute the electrical power actually delivered, `electrical_power`, from
`rotor_power` and `efficiency`.

```{code-cell} python
# code cell
```

## Part 5: Characterize the test run

Determine the mean, minimum and maximum delivered power, as well as the
scatter of the power around the mean.

```{code-cell} python
# code cell
```

## Closing question

Answer in your own words, without further code:

1. The wind speed in the test run only fluctuates between about 3 and 8 m/s.
   Why does the rotor power nevertheless fluctuate so much more strongly?
2. What does the large scatter of the electrical power mean for the operation
   of the turbine? Name one practical consequence.

## Bonus exercise: Second site (✩✩✩)

A second test run at a windier site delivers the following wind speeds (m/s)
at the same eight points in time:

```text
7.5, 8.1, 6.9, 9.2, 8.8, 7.6, 8.4, 9.0
```

Carry out the calculation from Part 1 to Part 5 for this second site. The
time axis and the efficiency curve depend only on the start-up time, not on
the site, and therefore remain unchanged. Which site delivers more power on
average? Which delivers the more even power relative to the mean?

```{code-cell} python
# code cell
```
