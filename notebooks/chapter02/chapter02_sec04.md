---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.4 Test-rig Report for an Electric Motor

In chapters 2.1 to 2.3 we computed NumPy arrays, analyzed them statistically
and plotted them with Matplotlib. In this chapter we apply these tools
together and analyze a complete test-rig run of the electric motor from
chapter 2.3. Work through the sub-tasks in pairs if possible and in order,
because each part builds on the results of the previous one.

## Project: Test-rig report for the electric motor (✩✩)

On the test rig, the rotational speed of the motor was increased in twelve
steps from 250 to 3000 1/min. At each step, the torque at the shaft and the
electrical power input were measured. The measured values are already stored
as arrays in the first code cell. From them we create the figures and key
figures for the test-rig report.

## Part 1: Read in the measurement data and compute characteristic quantities

In the code cell, the measured values are already stored as arrays `rpm`,
`torque` and `power_input`.

1. Check with `.shape` that all three arrays are the same length.
2. Compute the angular velocity `omega = 2 * np.pi * rpm / 60` in rad/s.
3. Compute the mechanical power `p_mech = torque * omega` in watts.
4. Compute the efficiency `efficiency = p_mech / power_input` and print the
   array.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

rpm = np.array([250, 500, 750, 1000, 1250, 1500,
                1750, 2000, 2250, 2500, 2750, 3000])           # 1/min
torque = np.array([7.4, 6.7, 6.1, 5.4, 4.7, 4.1,
                   3.4, 2.9, 2.3, 1.7, 1.1, 0.5])              # Nm
power_input = np.array([1350, 1660, 1720, 1520, 1230, 980,
                        800, 720, 660, 600, 560, 470])         # W

# Add: check shapes, compute omega, p_mech and efficiency
```

## Part 2: Characteristic map as subplots

Create a Figure with three subplots one below the other (`nrows=3`). Show the
torque at the top, the mechanical power in the middle and the efficiency at
the bottom, each over the rotational speed. Label each subplot with its
y-axis and give the efficiency subplot the full scale with `set_ylim(0, 1)`.
Set the x-axis label and the grid via a `for` loop over `ax`. The top subplot
gets a title. Align the Figure with `plt.tight_layout()`.

```{code-cell} python
# code cell
```

## Part 3: Determine operating points

The function `np.argmax(array)` returns the index of the largest value in the
array. With `rpm[np.argmax(p_mech)]` you therefore find the rotational speed
at which the mechanical power is largest.

1. Determine the rotational speed at which the mechanical power is maximal.
2. Determine the rotational speed at which the efficiency is maximal.
3. Compute the mean, standard deviation and maximum of the mechanical power
   over the entire run.
4. Print the results as a short text report with f-strings.

```{code-cell} python
# code cell
```

## Part 4: Efficiency with measurement uncertainty

Each efficiency value is the mean of three repeat measurements. The standard
deviation of these repeats is given:

```python
efficiency_std = np.array([0.015, 0.018, 0.020, 0.022, 0.025, 0.024,
                           0.022, 0.020, 0.019, 0.018, 0.028, 0.030])
```

1. Plot the efficiency over the rotational speed with `ax.errorbar()` and
   error bars in the y-direction (`fmt='o'`, `capsize=4`).
2. Highlight the operating point with the best efficiency by drawing it with
   a second `ax.scatter()` call as a large star (`marker='*'`, `s=200`).
3. Label the axes and title and show a legend.

```{code-cell} python
# code cell
```

## Closing question

Answer in your own words, without further code:

1. The motor delivers its largest mechanical power at 1500 1/min, but works
   most efficiently at 2000 1/min. For which rotational speed would you design
   the motor for continuous operation? Justify.
2. At which measured points is the relative measurement uncertainty of the
   efficiency largest? What follows from this for planning further
   measurements?

## Bonus exercise: Second test-rig run with a warm motor (✩✩✩)

After an hour of continuous running, the motor is warm. A second test-rig run
at the same rotational speeds and the same torque delivers a higher power
input, because the winding resistances rise with temperature:

```python
power_input_warm = np.array([1420, 1780, 1880, 1680, 1370, 1100,
                             910, 830, 770, 710, 660, 560])   # W
```

1. Compute the efficiency `efficiency_warm` for the warm run. The torque, and
   thus `p_mech`, stay unchanged.
2. Plot both efficiency curves, cold and warm, in a common diagram, with a
   legend.
3. Compare: how much does the peak efficiency drop? Does the rotational speed
   of the best operating point shift?

```{code-cell} python
# code cell
```

