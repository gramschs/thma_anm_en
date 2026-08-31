---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.1 NumPy Basics

In measurement technology, thousands of measured values quickly accumulate.
An acceleration sensor monitoring a vibrating machine, for example, delivers
10,000 measured values per second. If we want to process this data with
Python lists, we need loops over thousands of elements: tedious to write and
slow to run. In this chapter we get to know NumPy, a library built for
exactly such tasks. Its central data type, the **array**, allows us to apply
mathematical operations and statistical measures directly to whole number
series, without writing a single loop.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You know what a **NumPy array** is and how it differs from a Python
  list.
* [ ] You can create an array with `np.array()`, `np.linspace()` and
  `np.zeros()`.
* [ ] You can apply **vector operations** (element-wise addition,
  multiplication, scaling) to arrays.
* [ ] You can apply mathematical functions such as `np.sin()` and `np.exp()`
  to arrays.
* [ ] You can compute statistical measures of an array with `np.mean()`,
  `np.std()`, `np.min()` and `np.max()`.
```

## What is a NumPy array?

NumPy (short for *Numerical Python*) is a library, that is, a collection of
ready-made functions that we can use in our own code without writing them
ourselves. Before we can use a library, we have to load it with `import`. For
NumPy a fixed abbreviation has become established, under which we refer to
the library in the rest of the code:

```{code-cell} python
import numpy as np
```

This line loads the `numpy` library and makes it available in the code under
the name `np`. From now on we call all functions from NumPy with this
abbreviation, for example `np.array()`. The abbreviation `np` is pure
convention; a different name would work just as well technically, but `np` is
so widespread in the Python world that practically every piece of NumPy code
uses it.

The central data type of NumPy is the **array**. It allows us to apply
mathematical operations directly to whole number series, without writing a
single loop, as we will see below.

The difference between a list and an array is seen most quickly with an
example. A sensor delivers five acceleration values in m/s^2:

```{code-cell} python
# accelerations in m/s^2 as a Python list
measurements_list = [0.3, 1.2, 2.5, 1.8, 0.7]

# accelerations in m/s^2 as a NumPy array
measurements_array = np.array([0.3, 1.2, 2.5, 1.8, 0.7])

print(measurements_list)
print(measurements_array)
```

At first glance, a list and an array look similar. A NumPy array, however, is
designed specifically for numerical data and mathematical calculations. This
lets us apply arithmetic operations directly to whole measurement series.
First, though, we look at further ways to create a NumPy array.

Besides `np.array()`, which converts an existing list into an array, NumPy
provides two more functions with which we create arrays directly, without
writing down the values one by one.

`np.linspace(start, stop, count)` generates `count` evenly distributed values
between `start` and `stop`. The end value `stop` is included by default. This
is suitable, for example, for time axes:

```{code-cell} python
t = np.linspace(0, 2, 5)    # 5 values between 0 and 2 seconds
print(t)
```

In the output there is a point after each whole number, that is, `0.` instead
of `0`. `np.linspace()` always generates the values as floating-point
numbers, even if we specify integer bounds. This is intentional, because the
evenly distributed intermediate values of an axis are generally not whole
numbers.

`np.zeros(count)` generates an array of all zeros. This is useful for
creating an array as a placeholder that is filled with values later:

```{code-cell} python
placeholder = np.zeros(5)   # placeholder with 5 zeros
print(placeholder)
```

With these three functions, `np.array()`, `np.linspace()` and `np.zeros()`,
we already cover most cases in which we need to create a new array: from
existing values, as an evenly distributed axis or as a placeholder.

Before we continue computing with the arrays we have created, we check their
basic properties: size and data type.

```{code-cell} python
print(measurements_array.shape)   # number of elements per dimension
print(measurements_array.dtype)   # data type of the stored values
```

`.shape` returns the dimensions of the array as a tuple. `(5,)` means: one
dimension with five elements. `.dtype` returns the common data type of all
elements, here typically `float64` for floating-point numbers. These two
attributes are the fastest way to inspect an unknown array.

```{admonition} Mini-exercise (✩)
:class: tip
A temperature sensor delivers four measured values in °C: `18.5`, `19.2`,
`18.9`, `20.1`.

1. Store the values in an array called `temperatures`.
2. Print the shape and data type of `temperatures`.
3. Create a time axis `time` with four evenly distributed values between 0
   and 3 seconds, without writing down the values one by one.
4. Create an array `calibration_values` with four zeros that is to serve
   later as a placeholder for calibration factors.
5. Answer without running: which data type does `time.dtype` return, even
   though you only specified the whole numbers 0 and 3 as bounds in
   `np.linspace()`? Justify your answer.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

temperatures = np.array([18.5, 19.2, 18.9, 20.1])
print(temperatures.shape)   # (4,)
print(temperatures.dtype)   # float64

time = np.linspace(0, 3, 4)
print(time)                 # [0. 1. 2. 3.]

calibration_values = np.zeros(4)
print(calibration_values)   # [0. 0. 0. 0.]
```
`time.dtype` returns `float64`. `np.linspace()` generates its values as
floating-point numbers by default, because the computed intermediate values
of an axis are generally not integers. That is why NumPy also stores the
incidentally integer values 0, 1, 2 and 3 as floats, recognizable by the
point in the output `[0. 1. 2. 3.]`.
````

## Vector operations and mathematical functions

In the last section we created arrays and looked at their structure with
`.shape` and `.dtype`. Now we see what really makes arrays useful:
arithmetic operations that act on whole number series, without writing a
single loop.

Suppose we want to compute the acting force from the acceleration values.
$F = m \cdot a$ holds, where the mass is $m = 5\,\mathrm{kg}$. With a Python
list we need a loop for this:

```{code-cell} python
# with the list: a manual loop is necessary
forces_list = []
for a in measurements_list:
    forces_list.append(5.0 * a)

print(forces_list)
```

With the NumPy array a single line is enough:

```{code-cell} python
forces_array = 5.0 * measurements_array
print(forces_array)
```

The multiplication by the scalar `5.0` is automatically applied to **every
element** of `measurements_array`. We call such operations on whole number
series **vector operations**. They avoid explicit loops and are therefore
usually considerably more efficient for large measurement series.

*Is this difference noticeable at all with five measured values?* With five
values, no. But as soon as a sensor delivers several thousand values per
second, the vector operation determines whether an analysis takes fractions
of a second or several minutes.

The same principle applies to the basic arithmetic operations `+`, `-`, `*`,
`/` and `**`. If we add two one-dimensional arrays of equal length, their
elements are added pairwise:

```{code-cell} python
sensor_a = np.array([0.3, 1.2, 2.5, 1.8, 0.7])
sensor_b = np.array([0.1, 0.2, 0.3, 0.1, 0.2])

total = sensor_a + sensor_b
print(total)
```

The first element of `sensor_a` is added to the first element of `sensor_b`,
the second to the second, and so on. Since both arrays contain five elements,
this pairing of partners is unambiguous.

For one-dimensional arrays, a pairwise operation is normally only possible if
both arrays have the same length. For multi-dimensional arrays, the shapes
(`.shape`) of the arrays must match each other. Under certain conditions,
NumPy can also combine differently shaped arrays; these rules are called
**broadcasting** and are covered later.

Besides the basic arithmetic operations, NumPy also provides mathematical
functions that act element-wise on arrays. We need two of them often:
`np.sin()` for trigonometric calculations and `np.exp()` for exponential
functions.

```{code-cell} python
angle = np.linspace(0, 2 * np.pi, 5)
print(np.sin(angle))
```

`np.sin()` applies the sine to each element of `angle` individually and
returns a new array of the same length. In the output it is noticeable that
for the angles $\pi$ and $2\pi$ the value is not exactly `0`, but a tiny
value on the order of `1e-16`. The exact sine would be zero at these points.
This small deviation is a **rounding error** of floating-point arithmetic
that we always have to reckon with in numerical calculations.

`np.exp()` works on the same principle:

```{code-cell} python
values = np.array([0.0, 1.0, 2.0, 3.0])
print(np.exp(values))
```

Python already comes with `math.sin()` and `math.exp()` in the `math` module,
but these only accept single numbers, not arrays. To apply them to several
values, we would again need a loop. The NumPy variants `np.sin()` and
`np.exp()` are built for arrays and are therefore the right choice in this
lecture.

````{admonition} Mini-exercise (✩)
:class: tip
On a crane, two ropes pull with the following forces in kN, measured at four
points in time:

```python
rope_1 = np.array([120.0, 135.0, 128.0, 140.0])
rope_2 = np.array([80.0, 75.0, 82.0, 78.0])
```

1. Compute the sum of the magnitudes of both rope tension forces at each
   point in time and store it in `total_rope_forces_kn`.
2. Convert `total_rope_forces_kn` to newtons and store the result in
   `total_rope_forces_newton` (1 kN = 1000 N).
3. Rope 1 is inclined relative to the horizontal. The angle at the four
   points in time is, in rad:

```python
   angle = np.array([0.50, 0.55, 0.52, 0.58])
```

   Compute the vertical component of the force in rope 1 and store it in
   `rope_1_vertical`.
4. Answer without running: how many elements does `rope_1 * np.sin(angle)`
   have, and which angle belongs to the third element of `rope_1`? Is the
   vertical component at each point in time larger or smaller than the total
   force in the rope?
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

rope_1 = np.array([120.0, 135.0, 128.0, 140.0])
rope_2 = np.array([80.0, 75.0, 82.0, 78.0])

total_rope_forces_kn = rope_1 + rope_2
print(total_rope_forces_kn)

total_rope_forces_newton = total_rope_forces_kn * 1000.0
print(total_rope_forces_newton)

angle = np.array([0.50, 0.55, 0.52, 0.58])
rope_1_vertical = rope_1 * np.sin(angle)
print(rope_1_vertical)
```
`rope_1 * np.sin(angle)` again has four elements, since NumPy multiplies the
two arrays element-wise. The third element of `rope_1` (128.0 kN) belongs to
the third angle (0.52 rad). The vertical component is smaller than the total
force in the rope at every point in time, because the sine yields values
between 0 and 1 for angles between 0 and $\pi/2$.
````

## Statistical measures

So far we have looked at individual values of an array or transformed the
whole array at once. Often, however, we are not interested in every single
value, but in a summarizing measure: how large is a measured value on
average? How much do the values fluctuate? NumPy provides functions for this
that compute a single number from an array.

As a data basis we take a measurement series: the peak acceleration that a
sensor recorded during twelve consecutive test runs of the same machine.

```{code-cell} python
peak_values = np.array([4.8, 5.1, 4.6, 5.3, 4.9, 5.0,
                        4.7, 5.2, 4.9, 5.4, 4.8, 5.0])
print(peak_values)
```

With the NumPy functions `np.mean()`, `np.min()` and `np.max()` we compute
the mean, minimum and maximum. `np.mean()` adds all values and divides by the
number of elements, just like computing a mean by hand, only without a loop.
`np.min()` and `np.max()` yield the smallest and largest value in the array
respectively.

```{code-cell} python
print(f"Mean:    {np.mean(peak_values):.2f} m/s^2")
print(f"Minimum: {np.min(peak_values):.2f} m/s^2")
print(f"Maximum: {np.max(peak_values):.2f} m/s^2")
```

The standard deviation describes how much the individual values deviate from
the mean on average. A small standard deviation means that the test runs
delivered very similar peak values. A large standard deviation shows that the
machine reacts noticeably differently from run to run. The standard deviation
is computed with `np.std()`.

```{code-cell} python
print(f"Standard deviation: {np.std(peak_values):.3f} m/s^2")
```

`np.mean()`, `np.std()`, `np.min()` and `np.max()` can also be called
directly as a method of the array: `peak_values.mean()` yields the same
result as `np.mean(peak_values)`. Both notations are common. In this script
we consistently use the function notation `np.function(array)`, because it
works regardless of whether we are working with an array or an ordinary
list.

With these four functions, every measurement series can be characterized at a
glance: a typical value through the mean, the scatter through the standard
deviation and the extreme values through minimum and maximum. These are the
first tools for deriving reliable statements about a measured system from
pure number series.

````{admonition} Mini-exercise (✩)
:class: tip
In a quality inspection, the tightening torque of ten screws is measured, in
Nm:

```python
torques = np.array([45.2, 44.8, 46.1, 45.5, 44.9,
                    45.8, 46.3, 44.6, 45.1, 45.9])
```

1. Determine the mean tightening torque and store it in `mean_torque`.
2. Determine how much the values scatter around this mean on average, and
   store the result in `spread`.
3. Determine the smallest and the largest measured torque and store them in
   `min_torque` and `max_torque`.
4. Compute the range of the measurement (difference between the largest and
   smallest value) from `min_torque` and `max_torque` and store it in
   `span`.
5. Estimate before running: is `spread` closer to 0.6 Nm or closer to 6 Nm?
   Justify with a look at the ten measured values.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
import numpy as np

torques = np.array([45.2, 44.8, 46.1, 45.5, 44.9,
                    45.8, 46.3, 44.6, 45.1, 45.9])

mean_torque = np.mean(torques)
print(f"Mean:    {mean_torque:.2f} Nm")

spread = np.std(torques)
print(f"Spread:  {spread:.3f} Nm")

min_torque = np.min(torques)
max_torque = np.max(torques)
print(f"Minimum: {min_torque:.2f} Nm")
print(f"Maximum: {max_torque:.2f} Nm")

span = max_torque - min_torque
print(f"Span:    {span:.2f} Nm")
```
All measured values lie close together between 44.6 Nm and 46.3 Nm, that is,
in a band only about 1.7 Nm wide. The standard deviation measures the average
deviation from the mean and is therefore considerably smaller than this
bandwidth, here about 0.6 Nm. A value of 6 Nm would be impossible, since no
single deviation is that large.
````

## Summary and outlook

We have got to know NumPy arrays as an alternative to Python lists, created
them with `np.array()`, `np.linspace()` and `np.zeros()` and examined them
with `.shape` and `.dtype`. We apply vector operations and functions such as
`np.sin()` and `np.exp()` directly to whole arrays, without writing loops.
With `np.mean()`, `np.std()`, `np.min()` and `np.max()` we summarize a
measurement series in a few key figures.

In the next chapter we apply these tools in a coherent project and analyze
the test-rig run of a wind turbine. After that we get to know Matplotlib in
order to plot whole measurement series. Two-dimensional arrays and systems of
linear equations follow in chapter 3.
