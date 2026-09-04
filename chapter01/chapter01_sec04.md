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

```{admonition} Warm-up exercise (✩)
:class: tip
An acceleration test delivers the speeds `72`, `88` and `95` km/h. Create
them as a list `speeds_kmh`. Print the first and the last element, and the
number of elements with `len()`.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
speeds_kmh = [72, 88, 95]

print(speeds_kmh[0])
print(speeds_kmh[-1])
print(len(speeds_kmh))
```
`speeds_kmh[0]` is `72`, the first element, `speeds_kmh[-1]` is `95`, the
last. `len(...)` is `3`, the number of elements.
````

```{admonition} Exercise A (✩)
:class: tip
The list `speeds_kmh = [72, 88, 95, 60, 110, 130]` is given. Note down your
guess first, before you run the code.

* `speeds_kmh[0]` -->
* `speeds_kmh[2]` -->
* `speeds_kmh[-1]` -->
* `len(speeds_kmh)` -->

Then check each line in a code cell.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
speeds_kmh = [72, 88, 95, 60, 110, 130]
print(speeds_kmh[0])
print(speeds_kmh[2])
print(speeds_kmh[-1])
print(len(speeds_kmh))
```
`speeds_kmh[0]` is `72`, the first element. `speeds_kmh[2]` is `95`, the
element at index 2. `speeds_kmh[-1]` is `130`, the last element. `len(...)`
is `6`, the number of elements.
````

````{admonition} Exercise B (✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
speeds_kmh = [72, 88, 95, 60, 110, 130]
count = 0

for speed in speeds_kmh:
    if speed > 90:
        print(f'{speed} km/h: fast')
        count = count + 1

print(f'Number of fast measurements: {count}')
```
The `if` check is only true for the values 95, 110 and 130, so exactly these
three lines are printed with `fast`. The variable `count` is increased by 1
in exactly these three passes and has the value `3` at the end.
````

````{admonition} Exercise C (✩✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
vehicle = {
    'name': 'test_car_3',
    'mass_kg': 1200,
    'year': 2021,
}

print(f'{vehicle["name"]} (year {vehicle["year"]}) weighs '
      f'{vehicle["mass_kg"]} kg.')
```
The first gap is the value `1200`, the second one the key `"name"` in
quotation marks. The output is `test_car_3 (year 2021) weighs 1200 kg.` An
f-string may be spread over several lines, as long as each substring starts
with an `f`.
````

````{admonition} Exercise D (✩✩)
:class: tip
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
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def kmh_to_ms(speed_kmh):
    return speed_kmh / 3.6

speeds_kmh = [72, 88, 95, 60, 110, 130]

for speed_kmh in speeds_kmh:
    speed_ms = kmh_to_ms(speed_kmh)
    print(f'{speed_kmh} km/h corresponds to {speed_ms:.1f} m/s')
```
The first gap is the division operator `/`, the second one the function name
`kmh_to_ms`. Since the function is defined once, we can call it as often as we
like with different arguments, without writing out the conversion formula
each time.
````

```{admonition} Exercise E (✩✩✩, mini-project)
:class: tip
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
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def kinetic_energy(speed_kmh, mass=1200):
    speed_ms = speed_kmh / 3.6
    return 0.5 * mass * speed_ms**2

speeds_kmh = [72, 88, 95, 60, 110, 130]

max_energy = 0
for speed_kmh in speeds_kmh:
    energy = kinetic_energy(speed_kmh)
    if energy > max_energy:
        max_energy = energy

print(f'Maximum kinetic energy: {max_energy:.1f} joules')
```
The maximum value occurs at 130 km/h, the largest value in the measurement
series. Since the kinetic energy grows with the square of the speed and the
mass stays constant over the entire measurement series, the maximum of the
energy is always at the highest measured speed. We can therefore derive this
from the formula alone, without running the code.
````
