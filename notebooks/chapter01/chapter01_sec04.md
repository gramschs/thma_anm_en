---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.4 In-depth Practice (Part 2)

The following exercises build on the code-along from chapter 1.3. Exercises
with one star (✩) and two stars (✩✩) are compulsory. The exercise with three
stars (✩✩✩) is a bonus exercise for anyone who finishes early. Work in pairs
if possible. If you want to look up a term, the cheat sheet at the end of
Part 1 will help.

## Warm-up exercise (✩)

An acceleration test delivers the speeds `72`, `88` and `95` km/h. Create
them as a list `speeds_kmh`. Print the first and the last element, and the
number of elements with `len()`.

```{code-cell} python
# code cell
```

## Exercise A (✩)

The list `speeds_kmh = [72, 88, 95, 60, 110, 130]` is given. Note down your
guess first, before you run the code.

* `speeds_kmh[0]` -->
* `speeds_kmh[2]` -->
* `speeds_kmh[-1]` -->
* `len(speeds_kmh)` -->

Then check each line in a code cell.

```{code-cell} python
# code cell
```

## Exercise B (✩)

The following code is given. Note down which lines it prints and which value
`count` has at the end, before you run it.

```python
speeds_kmh = [72, 88, 95, 60, 110, 130]
count = 0

for speed in speeds_kmh:
    if speed > 90:
        print(f'{speed} km/h: fast')
        count = count + 1

print(f'Number of fast measurements: {count}')
```

```{code-cell} python
# code cell
```

## Exercise C (✩✩)

Complete the code at the `___` places. Create a dictionary `vehicle` with the
details of the test vehicle and print the sentence. The mass is 1200 kg.

```python
vehicle = {
    'name': 'test_car_3',
    'mass_kg': ___,
    'year': 2021,
}

print(f'{vehicle[___]} (year {vehicle["year"]}) weighs '
      f'{vehicle["mass_kg"]} kg.')
```

```{code-cell} python
# code cell
```

## Exercise D (✩✩)

Complete the function and the call at the `___` places. The function
`kmh_to_ms` should convert a speed from km/h to m/s by dividing by 3.6. Then
it is called in a loop for each measurement.

```python
def kmh_to_ms(speed_kmh):
    return speed_kmh ___ 3.6

speeds_kmh = [72, 88, 95, 60, 110, 130]

for speed_kmh in speeds_kmh:
    speed_ms = ___(speed_kmh)
    print(f'{speed_kmh} km/h corresponds to {speed_ms:.1f} m/s')
```

```{code-cell} python
# code cell
```

## Exercise E (✩✩✩, mini-project)

An acceleration test delivers the measurement series
`speeds_kmh = [72, 88, 95, 60, 110, 130]` in km/h. Implement the following
steps.

**Part 1:** Write a function
`kinetic_energy(speed_kmh, mass=1200)` that first converts internally to m/s
and then returns the kinetic energy in joules.

**Part 2:** Iterate over `speeds_kmh` with a for loop. Compute the kinetic
energy for each measured value and keep the largest value computed so far in
a variable `max_energy` (hint: start with `max_energy = 0` before the loop
and compare in each pass with an `if` check).

**Part 3:** Print the largest energy value found after the loop.

**Closing question:** At which speed from the measurement series does this
maximum value occur, and why can we guess this even without running the code?

```{code-cell} python
# code cell
```

