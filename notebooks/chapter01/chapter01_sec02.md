---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.2 In-depth Practice (Part 1)

The following exercises build on the code-along from chapter 1.1. Exercises
with one star (✩) and two stars (✩✩) are compulsory. The exercise with three
stars (✩✩✩) is a bonus exercise for anyone who finishes early. Work in pairs
if possible; this helps especially if Python is still new to you. If you want
to look up a term, the cheat sheet at the end of Part 1 will help.

## Warm-up exercise (✩)

A test vehicle travels at 27.8 m/s. Create a variable `speed_ms` with this
value and a variable `vehicle` with the value `'test_car_3'`. Print both with
`print()` and display the data type of `speed_ms` with `type()`.

```{code-cell} python
# code cell
```

## Exercise A (✩)

A test vehicle delivers various measured values. Which data type is present
in each case? Write down your guess first, before you run the code.

* `120` (number of measurements) -->
* `27.8` (speed in m/s) -->
* `'test_car_3'` (vehicle name) -->
* `120 / 4` -->
* `2 ** 8` -->
* `27.8 > 33.3` -->

Then check each line with `type()` in a code cell.

```{code-cell} python
# code cell
```

## Exercise B (✩)

The following code is given. Note down what it prints before you run it.

```python
speed_ms = 30.0
speed_limit_ms = 33.3

if speed_ms > speed_limit_ms:
    print('too fast')
elif speed_ms == speed_limit_ms:
    print('exactly at the limit')
else:
    print('within the limit')
```

What changes about the output if the first line reads `speed_ms = 33.3`?

```{code-cell} python
# code cell
```

## Exercise C (✩✩)

Complete the code at the places marked with `___`. A test vehicle travels at
`speed_kmh = 95`. The code should convert the speed to m/s and print whether
the speed limit of 33.3 m/s is exceeded.

```python
speed_kmh = 95
speed_limit_ms = 33.3

speed_ms = speed_kmh / ___

if speed_ms ___ speed_limit_ms:
    print(f'{speed_ms:.1f} m/s: speed limit exceeded')
else:
    print(f'{speed_ms:.1f} m/s: within the permitted range')
```

```{code-cell} python
# code cell
```

## Exercise D (✩✩)

Complete the for loop at the `___` places. An acceleration test runs over
seven time steps. In each time step the speed increases by 7 m/s. The code
should print the speed for each time step and additionally `too fast` as
soon as it is above the speed limit of 33.3 m/s.

```python
speed_limit_ms = 33.3

for time_step in range(7):
    speed_ms = time_step * ___
    print(f'Time step {time_step}: {speed_ms:.1f} m/s')
    if ___:
        print('too fast')
```

```{code-cell} python
# code cell
```

## Exercise E (✩✩✩, mini-project)

A test rig simulates an acceleration test over ten time steps. Implement the
following steps.

**Part 1:** Write a for loop with `range(10)` for the time steps 0 to 9. In
each time step the speed is `speed_ms = time_step * 5.0`. Print the time step
and speed with an f-string.

**Part 2:** Add an `if`/`else` check in the loop body that prints for each
time step whether the speed limit `speed_limit_ms = 33.3` is observed or
exceeded.

**Part 3:** Count in how many time steps the speed limit is exceeded. For
this, create a variable `count_too_fast = 0` before the loop and increase it
by 1 in the appropriate case. Print the number after the loop.

**Closing question:** From which time step onward is the speed limit
exceeded, and how does that relate to the chosen acceleration of 5.0 m/s per
time step?

```{code-cell} python
# code cell
```

