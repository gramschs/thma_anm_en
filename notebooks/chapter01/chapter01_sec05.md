---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.5 Exercises

These exercises are intended for self-study at home and review the material
of chapters 1.1 to 1.4. Expect around two hours of working time.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 5 min)
* ✩✩ Application: write your own code and interpret results (approx. 10 min)
* ✩✩✩ Mini-project: combine several concepts of the part (approx. 30 min)

## Exercise 1.1 (✩)

Which data type is present? Write your guess after the arrow before you run
the code.

* `7` -->
* `-7` -->
* `'steel'` -->
* `7.0` -->
* `7,0` -->
* `7**2` -->
* `7**(1/2)` -->
* `7 == 7.0` -->

Then check each line with `type()` in a code cell.

```{code-cell} python
# code cell
```

## Exercise 1.2 (✩✩)

A spring obeys the spring law `force = spring_constant * displacement`.
Compute the spring force for a spring constant of 250 N/m and a displacement
of 0.12 m. Print the result with an f-string and the unit newton, rounded to
two decimal places.

```{code-cell} python
# code cell
```

## Exercise 1.3 (✩)

What do the following expressions return? Note `True` or `False` before you
run the code.

* `5 > 3` -->
* `5 >= 5` -->
* `'Steel' == 'steel'` -->
* `not (5 > 3)` -->
* `(5 > 3) and (2 > 4)` -->
* `(5 > 3) or (2 > 4)` -->

```{code-cell} python
# code cell
```

## Exercise 1.4 (✩✩)

A material has a measured tensile strength of `tensile_strength_mpa = 420`.
Write an `if`/`elif`/`else` branch that prints the following categories:

* below 300 MPa: `'low-strength'`
* from 300 to 600 MPa (both inclusive): `'medium-strength'`
* above 600 MPa: `'high-strength'`

```{code-cell} python
# code cell
```

## Exercise 1.5 (✩✩)

Write a for loop that prints the value in Fahrenheit for the temperatures 0,
20, 40, 60, 80 and 100 degrees Celsius. Use the formula
`fahrenheit = celsius * 9/5 + 32` for this.

Hint: `range(start, stop, step)` generates numbers with a step size other
than 1. The value `stop` itself no longer belongs to the range, so choose it
suitably larger.

```{code-cell} python
# code cell
```

## Exercise 1.6 (✩✩)

A component cools down from 180 degrees Celsius by 12 degrees in each time
step. Write a for loop with `range(15)` that computes and prints the
temperature for each time step. Add an `if` check in the loop body that
additionally prints `below 20 degrees` as soon as the temperature falls below
the mark of 20 degrees Celsius.

```{code-cell} python
# code cell
```

## Exercise 1.7 (✩)

The list `my_list = [15, 8, 23, 4, 16, 42]` is given. Note down your guess
first, before you run the code.

* `my_list[0]` -->
* `my_list[2]` -->
* `my_list[-1]` -->
* `my_list[-3]` -->
* `len(my_list)` -->

```{code-cell} python
# code cell
```

## Exercise 1.8 (✩✩)

The list `measurement_series = [15.2, 8.7, 23.1, 4.4, 16.9, 42.0]` with force
readings in newtons is given. Determine the smallest and largest value of the
list with a for loop, without using the built-in functions `min()` and
`max()`.

```{code-cell} python
# code cell
```

## Exercise 1.9 (✩✩)

Create a dictionary `part` for a shaft with the following information:

* designation: `'Shaft_A1'`
* diameter_mm: 25.0
* material: `'42CrMo4'`
* max_torque_nm: 180

Then print: "Shaft_A1 made of 42CrMo4 (diameter 25.0 mm) withstands a maximum
of 180 Nm."

```{code-cell} python
# code cell
```

## Exercise 1.10 (✩✩)

Write a function `stress(force_n, cross_section_mm2=100)` that computes and
returns the mechanical stress `sigma = force_n / cross_section_mm2` in N/mm²
(MPa). Give the function a docstring. Call the function once with
`force_n = 5000` and the default cross section, and once with `force_n = 5000`
and `cross_section_mm2 = 50`. Compare the two results in one sentence.

```{code-cell} python
# code cell
```

## Exercise 1.11 (✩✩✩, mini-project)

In a tensile test, a sample with the constant cross section
`cross_section_mm2 = 19.6` is loaded step by step. The measured forces are
`forces_n = [1200, 3400, 5800, 7200, 8100, 6500]`. Implement the following
steps.

**Part 1:** Write a function `stress(force_n, cross_section_mm2)` that returns
the stress in MPa.

**Part 2:** Create a dictionary `test` with the keys `material` (`'S235JR'`),
`cross_section_mm2` (19.6) and `yield_strength_mpa` (235.0).

**Part 3:** Iterate over `forces_n` with a for loop. Compute the stress for
each value with your function and print for each measured value whether the
yield strength from the dictionary is exceeded (`'In the elastic range'` or
`'Yield strength exceeded'`). Also keep track of the force at which the yield
strength is first exceeded.

**Part 4:** Determine the maximum stress of the entire measurement series
without `max()` and print it at the end.

**Closing question:** At which force from the list is the yield strength first
exceeded, and what does that mean physically for the material sample?

```{code-cell} python
# code cell
```

