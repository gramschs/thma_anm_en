---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.3 Lists, Dictionaries and Functions

In chapter 1.1 we stored individual measured values in variables and used a
branch to check whether a speed limit is being observed. During an
acceleration test, however, a test vehicle delivers not just a single
measured value but a whole measurement series. A single variable is no longer
enough for that. In this chapter we therefore introduce the data structures
**list** and **dictionary**, with which we manage several values together.
Afterwards we encapsulate recurring calculations such as the conversion from
km/h to m/s in our own **functions**.

As in chapter 1.1, short videos are again embedded at the end of the sections
as preparation.

## Learning objectives

```{admonition} Learning objectives
:class: attention
* [ ] You can create **lists**, extend them with `append()` and access
  elements via the **index**.
* [ ] You can create, read and modify **dictionaries** with key-value pairs.
* [ ] You can write your own **functions** with `def`, use parameters and
  return a value with `return`.
* [ ] You know what a **default value** and a **docstring** are.
```

## How do we collect several measured values in a list?

Imagine an acceleration test in which a sensor records the speed at several
points in time. We collect these values in a **list**, recognizable by the
square brackets.

```{code-cell} python
speeds_kmh = [80, 95, 120, 60, 110]
print(speeds_kmh)
```

A list can contain any number of elements. With `len()` we display the
number of elements.

```{code-cell} python
num_measurements = len(speeds_kmh)
print(f'Number of measurements: {num_measurements}')
```

We access individual elements via the **index**. Python starts counting at 0.
With the index `-1` we conveniently access the last element.

```{code-cell} python
first_measurement = speeds_kmh[0]
last_measurement = speeds_kmh[-1]
print(f'First measurement: {first_measurement} km/h')
print(f'Last measurement: {last_measurement} km/h')
```

To add a new measurement at the end of the list, we use the `append()`
method.

```{code-cell} python
speeds_kmh.append(75)
print(speeds_kmh)
```

If we want to process every measured value in a list, we iterate over the
list directly with a for loop, without the detour via `range()` and the
index.

```{code-cell} python
for speed in speeds_kmh:
    print(f'Measured value: {speed} km/h')
```

```{admonition} Mini-exercise (✩)
:class: tip
Create a list `temperatures` with five temperature readings of your choice.
Append another reading with `append()` and then print the number of elements
with `len()`.

Also answer, without running the code: what does `temperatures[-2]` return
after you have appended the sixth value? Justify your answer.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
temperatures = [18.5, 19.2, 21.0, 22.4, 20.1]
temperatures.append(23.7)
count = len(temperatures)
print(f'Number of readings: {count}')
```
`temperatures[-2]` returns the second-to-last element of the list, that is,
the value `20.1`. The index `-1` points to the last element (`23.7`, the
value just appended), `-2` points to the element directly before it.
````

```{dropdown} Video "Listen in Python - Einführung" by Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/ihF8bZoauBs" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video "Zugriff auf Listen" by Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/_XzWPXvya2w?si=50tgXK-UUqOpQS8E"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "for-Schleife mit Listen" by Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/_XzWPXvya2w?si=50tgXK-UUqOpQS8E"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## How do we structure data with keys?

A list like `[200.0, 'test_rig_1', 'Sensor_A']` stores several values, but
*how do we keep track, in a longer list, of which value stands for what?* At
index 0 we would have to remember that the measuring range is there, at index
1 the location and at index 2 the name. For such cases the **dictionary** is
more suitable, since we access it via meaningful keys instead of a numeric
index.

```{code-cell} python
sensor = {
    'name': 'Sensor_A',
    'location': 'test_rig_1',
    'measuring_range_max': 200.0
}
print(sensor)
```

A value is accessed via the corresponding key in square brackets.

```{code-cell} python
print(f'Sensor: {sensor["name"]}')
print(f'Location: {sensor["location"]}')
```

We can change existing values or add new key-value pairs.

```{code-cell} python
sensor['measuring_range_max'] = 250.0
sensor['calibration_date'] = '2026-01-15'
print(sensor)
```

```{admonition} Mini-exercise (✩)
:class: tip
Create a dictionary `measurement` for a temperature reading with the keys
`temperature` (23.5), `location` (`'test_rig_2'`) and `timestamp`
(`'14:32'`). Print the temperature and location with suitable labels.

Also answer: why would a list `[23.5, 'test_rig_2', '14:32']` be less
suitable for this data than a dictionary? Phrase your answer in your own
words.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
measurement = {
    'temperature': 23.5,
    'location': 'test_rig_2',
    'timestamp': '14:32'
}
print(f'Temperature: {measurement["temperature"]} degrees Celsius')
print(f'Location: {measurement["location"]}')
```
With the list we would have to remember that index 0 contains the
temperature, index 1 the location and index 2 the timestamp. This mapping is
not obvious to others and is error-prone as soon as the order changes. The
dictionary makes the meaning of each value immediately visible via the key.
````

```{dropdown} Video "Dictionaries" by Pitrium
<iframe width="560" height="315"
src="https://www.youtube.com/embed/fQGQ4MIBKBY?si=w4hfWIM4n_PyuF5i"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## How do we encapsulate calculations in functions?

In chapter 1.1 we wrote out the formula `speed_kmh / 3.6` for the conversion
to m/s by hand several times. With our own **function** we encapsulate this
calculation, so that we only define it once and can reuse it as often as we
like.

```{code-cell} python
def kmh_to_ms(speed_kmh):
    speed_ms = speed_kmh / 3.6
    return speed_ms

speed_ms = kmh_to_ms(95)
print(speed_ms)
```

A function begins with the keyword `def`, followed by the function name and
the **parameters** in parentheses. Here too, the header ends with a colon `:`
and the function body is indented. The keyword `return` determines which
value is returned to the caller. Once the function is defined, we
call it as often as we like with different arguments, for example for every
measured value in our list.

```{code-cell} python
for speed in speeds_kmh:
    print(f'{speed} km/h corresponds to {kmh_to_ms(speed):.1f} m/s')
```

A function can have several parameters. If we write an `=` with a value after
a parameter, that is a **default value**: if we call the function without
this argument, Python automatically uses the default value.

```{code-cell} python
def kinetic_energy(speed_ms, mass=1200):
    return 0.5 * mass * speed_ms**2

print(f'{kinetic_energy(27.8):.1f} joules')            # mass = 1200
print(f'{kinetic_energy(27.8, mass=1500):.1f} joules')
```

Directly below the header of a function we can write a **docstring** in
triple quotation marks, a short sentence that describes what the function
does.

```{code-cell} python
def kmh_to_ms(speed_kmh):
    """Converts a speed from km/h to m/s."""
    return speed_kmh / 3.6
```

```{dropdown} Video "Funktionen selbst definieren" by Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/LQCfN5HS9xI" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

```{dropdown} Video "Funktionen mit Parametern" by Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/af9ORp1Pty0" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video "Funktionen mit Rückgabewert" by Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/ehSP-sYoKCY" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{admonition} Mini-exercise (✩)
:class: tip
Write a function `braking_distance(speed_kmh)` that returns the braking
distance according to the rule of thumb `(speed_kmh / 10) ** 2 / 2`. Call the
function for `speed_kmh = 100` and print the result.

Also answer, without running the code: what does the function call return if
you forget the keyword `return` in the function? Justify your answer.
```

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def braking_distance(speed_kmh):
    return (speed_kmh / 10) ** 2 / 2

print(f'Braking distance: {braking_distance(100):.1f} m')
```
Without `return`, the function automatically returns the value `None`. The
calculation inside the function would still be carried out, but the result
would be lost, since it is not returned to the caller.
````

## Summary and outlook

In this chapter we have learned how to collect several measured values in a
**list**, structure them with meaningful keys in a **dictionary** and
encapsulate recurring calculations in our own **functions** with parameters
and return values. With these we now have the tools to process the
measurement series from our acceleration tests.

We have deliberately left out some Python topics and will catch up on them
later, when we need them, for example error handling with `try` and `except`
in the numerical methods. In chapter 2 we use **NumPy** and **Matplotlib** to
process entire measurement series such as `speeds_kmh` all at once without our
own loop and to plot them.
