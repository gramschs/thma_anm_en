---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 7.2 How Small Can the Step Size Be?

In Chapter 7.1, the AGV started accelerating abruptly and stopped
accelerating just as abruptly. The load feels such jumps in acceleration as a
jolt. The rate of change of the acceleration, i.e. its derivative with respect
to time, is called **jerk**. That is why the fleet manager plans a smoother
start: the velocity rises from $0$ to $0.8\,\text{m/s}$ in $2\,\text{s}$
without a kink. With $t$ in seconds and $s$ in meters, the distance is

$$s(t) = 0.4 \left(t - \frac{2}{\pi} \sin\left(\frac{\pi t}{2}\right)\right)
\quad \text{for } 0 \le t \le 2.$$

Unlike with measured values, we can now evaluate $s$ at any point and choose the
step size freely. There is no measurement noise either. In Chapter 7.1, the
noise was the reason why a small step size was not always better. *Without
measurement noise, does the derivative get more and more accurate as the step
size gets smaller?*

Since we know the exact derivative, we can measure the error precisely. In
Chapter 8, we use the step size that proves best here for functions whose
derivative we do not want to work out as a formula.

## How accurate is the difference quotient?

First, we write the formula as a Python function `motion_profile(t)`. For
comparison, we also program its derivative, the exact velocity
$s'(t) = v(t) = 0.4 \left(1 - \cos\left(\frac{\pi t}{2}\right)\right)$.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# model of the smooth start: distance and exact velocity
def motion_profile(t):
    """Distance in m for the smooth start, t in s from 0 to 2."""
    return 0.4 * (t - 2 / np.pi * np.sin(np.pi * t / 2))

def velocity(t):
    """Exact velocity in m/s, the derivative of motion_profile."""
    return 0.4 * (1 - np.cos(np.pi * t / 2))
```

To compare the smooth start with the start from Chapter 7.1, we compute both
velocities at 101 times from $0$ to $2\,\text{s}$. In Chapter 7.1, the
velocity increased uniformly at $0.4\,\text{m/s}^2$, so $v = 0.4\,t$ there.
Since `velocity()` computes with NumPy functions, we can pass it the whole
array of times at once.

```{code-cell} python
# 101 times from 0 s to 2 s
t = np.linspace(0, 2, 101)

# velocity in m/s: uniform start from Chapter 7.1, smooth start
v_uniform = 0.4 * t
v_smooth = velocity(t)
```

The plot compares the two starts.

```{code-cell} python
# plot: velocity of the two starts
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(t, v_uniform, color='gray', linestyle='--',
        label='start from Chapter 7.1')
ax.plot(t, v_smooth, label='smooth start')
ax.set_xlabel('Time in s')
ax.set_ylabel('Velocity in m/s')
ax.set_title('Two ways to accelerate to 0.8 m/s')
ax.legend()
ax.grid(True)
plt.show()
```

Both starts reach a velocity of $0.8\,\text{m/s}$ after $2\,\text{s}$. The
curve of the smooth start, however, is flat at the beginning and at the end.
So the acceleration builds up gradually and tapers off gradually.

For the difference quotients, we write two functions. They take the function
they are supposed to differentiate as their first parameter `function`. In
Python, we can pass a function to another function just like a number. We
write its name without parentheses, because we pass the function itself and
not a function value. In the call `forward(motion_profile, 1.5, 0.1)`,
`function` stands for `motion_profile`, and `function(t + dt)` computes
`motion_profile(1.6)`.

```{code-cell} python
# difference quotients for any function
def forward(function, t, dt):
    """Forward difference quotient of function at the point t."""
    # TODO: ???   return the forward difference quotient of function at t with step size dt

def central(function, t, dt):
    """Central difference quotient of function at the point t."""
    # TODO: ???   return the central difference quotient of function at t with step size dt
```

We evaluate at $t = 1.5\,\text{s}$, shortly before the AGV reaches its final
velocity, and try three step sizes. As the error, we take the absolute value
of the deviation from the exact value.

```{code-cell} python
# point of evaluation in s and exact velocity there
t_0 = 1.5
exact = velocity(t_0)
print(f'Exact velocity at t = {t_0} s: {exact:.6f} m/s')

# error = absolute value of the deviation from the exact value,
# motion_profile without parentheses: we pass the function itself
for dt in [0.1, 0.01, 0.001]:
    # TODO: ???   compute the error of the forward difference quotient of motion_profile at t_0 and store it in error_forward
    # TODO: ???   compute the error of the central difference quotient of motion_profile at t_0 and store it in error_central
    print(f'dt = {dt:5}:  error forward {error_forward:.2e} m/s, '
          f'central {error_central:.2e} m/s')
```

The notation `2.10e-02` stands for $2.10 \cdot 10^{-2}$. When the step size
gets ten times smaller, the error of the forward difference quotient drops to
a tenth, and the error of the central difference quotient drops to a
hundredth. So the error is roughly proportional to $\Delta t$ and to
$\Delta t^2$, respectively. We call the exponent the **order of accuracy**:
the forward difference quotient has order of accuracy 1, the central one has
order of accuracy 2. Even at $\Delta t = 0.1\,\text{s}$, the central
difference quotient is more accurate than the forward difference quotient at
$\Delta t = 0.01\,\text{s}$.

## How do we read off the order of accuracy?

Three step sizes show the trend, but a plot shows it more clearly. For this,
we need many step sizes spanning several powers of ten.
`np.logspace(-1, -4, 31)` generates 31 numbers from $10^{-1}$ to $10^{-4}$,
ten per power of ten. For each step size, we compute both errors in a loop
and collect them in arrays that we create beforehand with `np.zeros()`.

```{code-cell} python
# 31 step sizes from 0.1 to 0.0001, ten per power of ten
dt_values = np.logspace(-1, -4, 31)

# errors of both difference quotients for each step size
error_forward = np.zeros(len(dt_values))
error_central = np.zeros(len(dt_values))
for k in range(len(dt_values)):
    error_forward[k] = abs(forward(motion_profile, t_0, dt_values[k]) - exact)
    error_central[k] = abs(central(motion_profile, t_0, dt_values[k]) - exact)
```

`ax.loglog()` plots like `ax.plot()` but uses logarithmic scales on both
axes: every power of ten gets the same amount of space on the axis.
`ax.grid(True, which='both')` also draws the fine grid lines between the
powers of ten.

In such a **log-log plot**, the relationship
$\text{error} = C \cdot \Delta t^p$ becomes a straight line with slope $p$.
So the order of accuracy is the slope of the line. We read it off in powers
of ten: by how many powers of ten does the error change when the step size
changes by one power of ten? We used the same tool for the runtime in the
excursus in Chapter 3.7, where the slope was 3.

```{code-cell} python
# plot: error against step size, log-log
fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(dt_values, error_forward, marker='.', label='forward')
ax.loglog(dt_values, error_central, marker='.', label='central')
ax.set_xlabel('Step size in s')
ax.set_ylabel('Error in m/s')
ax.set_title('Error of the difference quotients at t = 1.5 s')
ax.legend()
ax.grid(True, which='both')
plt.show()
```

As usual, the step size increases to the right along the axis, so the small
step sizes are on the left. Both curves are straight lines. Over three powers
of ten of the step size, the error of the forward difference quotient drops by
three powers of ten, from about $2 \cdot 10^{-2}$ to about $2 \cdot 10^{-5}$.
So the slope is 1. The error of the central difference quotient drops twice
as steeply, from about $10^{-3}$ to about $10^{-9}$, so the slope is 2. *Why
is the central difference quotient so much more accurate?*

## Math refresher: Taylor expansion

The **Taylor expansion** writes a function value near $t$ as a sum of powers
of the step size:

$$s(t + \Delta t) = s(t) + \Delta t \cdot s'(t) + \frac{\Delta t^2}{2}
\cdot s''(t) + \frac{\Delta t^3}{6} \cdot s'''(t) + \ldots$$

If we substitute this into the forward difference quotient, the largest error
term left besides $s'(t)$ is $\frac{\Delta t}{2} \cdot s''(t)$, which is
proportional to $\Delta t$. In the expansion of $s(t - \Delta t)$, the odd
powers of $\Delta t$ change sign. That is why the terms with $s''(t)$ cancel
in the central difference quotient. The largest error term is then
$\frac{\Delta t^2}{6} \cdot s'''(t)$, which is proportional to $\Delta t^2$.

For the start, $s''$ is the acceleration $a$. So the largest error term
$a \cdot \Delta t / 2$ of the forward difference quotient is roughly the
change in velocity over half a step. This matches Chapter 7.1: the forward
difference quotient gives approximately the velocity at the midpoint of the
interval, half a step too late. $s'''$ is the jerk. In Chapter 7.1, the
acceleration was constant and the jerk was zero. That is why the central
difference quotient was exact there, except at the kink at $t = 2\,\text{s}$.
At a kink, the Taylor expansion does not hold, and the central difference
quotient can even be worse than the forward difference quotient. At
$t = 2\,\text{s}$, the forward difference quotient gives exactly the planned
velocity, $(1.2 - 0.8)/0.5 = 0.8\,\text{m/s}$, but the central one only
$0.75\,\text{m/s}$. So the orders of accuracy assume that the function can be
differentiated often enough, and they describe the error for small step
sizes.

## What happens with tiny step sizes?

According to the Taylor expansion, the error should keep decreasing as the
step size gets smaller. We check this and reduce the step size down to
$10^{-15}$. The calculation is the same as in the previous section, only with
141 step sizes.

```{code-cell} python
# 141 step sizes from 0.1 to 1e-15, ten per power of ten
dt_values = np.logspace(-1, -15, 141)

# errors of both difference quotients for each step size
error_forward = np.zeros(len(dt_values))
error_central = np.zeros(len(dt_values))
for k in range(len(dt_values)):
    error_forward[k] = abs(forward(motion_profile, t_0, dt_values[k]) - exact)
    error_central[k] = abs(central(motion_profile, t_0, dt_values[k]) - exact)
```

We draw the plot as in the previous section, only without markers.

```{code-cell} python
# plot: error down to very small step sizes, log-log
fig, ax = plt.subplots(figsize=(7, 5))
ax.loglog(dt_values, error_forward, label='forward')
ax.loglog(dt_values, error_central, label='central')
ax.set_xlabel('Step size in s')
ax.set_ylabel('Error in m/s')
ax.set_title('Error at very small step sizes')
ax.legend()
ax.grid(True, which='both')
plt.show()
```

At first, the curves follow the lines from the previous section. They reach
their minimum at about $2 \cdot 10^{-8}$ for the forward difference quotient
and at about $5 \cdot 10^{-6}$ for the central one. Below that, the error
rises again and becomes erratic. At $\Delta t = 10^{-15}$, it is even larger
than at $\Delta t = 0.1$. *Where does this additional error come from?*

Python stores a floating-point number with about 16 significant digits and
rounds off the rest. This deviation is called **rounding error**. We can see
what it does in the two function values for $\Delta t = 10^{-10}$. We print
them to 17 decimal places with the format `:.17f`.

```{code-cell} python
# two function values a distance dt = 1e-10 s apart
dt = 1e-10
s_right = motion_profile(t_0 + dt)
s_left = motion_profile(t_0)

# difference and forward difference quotient
difference = s_right - s_left
v_forward = difference / dt

# output with 17 decimal places, exact velocity for comparison
print(f's(t_0 + dt) = {s_right:.17f} m')
print(f's(t_0)      = {s_left:.17f} m')
print(f'difference  = {difference:.17f} m')
print(f'forward     = {v_forward:.17f} m/s')
print(f'exact       = {exact:.17f} m/s')
```

The two function values agree in the first nine decimal places. When we
subtract, these digits turn into zeros, and of the roughly 16 significant
digits, only about six are left. This loss of significant digits is called
**cancellation**. That is why the difference quotient also agrees with the
exact velocity in only six digits.

The **machine epsilon** eps tells us how accurately Python computes. It is
the smallest relative gap between $1$ and the next number that Python can
store. For quantities around 1, every function value has a rounding error of
about eps. Like the measurement noise in Chapter 7.1, the difference quotient
divides it by the step size. So the rounding error in the result is about
$\text{eps} / \Delta t$, which is why the erratic parts of the curves on the
left have a slope of roughly $-1$.

The best step size is the one at which the error from the Taylor expansion and
the rounding error are about the same size. Ignoring the factors $C$, the
forward difference quotient gives $\Delta t \approx \text{eps} / \Delta t$,
which leads to the rule of thumb $\Delta t \approx \sqrt{\text{eps}}$. For the
central one, $\Delta t^2 \approx \text{eps} / \Delta t$, so
$\Delta t \approx \sqrt[3]{\text{eps}}$. NumPy provides eps as
`np.finfo(float).eps`, and we compute the cube root as `eps ** (1 / 3)`.

```{code-cell} python
# machine epsilon
eps = np.finfo(float).eps

# rules of thumb for the best step size
dt_forward = np.sqrt(eps)
dt_central = eps ** (1 / 3)

# output of the rules of thumb
print(f'Machine epsilon eps:          {eps:.1e}')
print(f'forward, square root of eps:  {dt_forward:.1e} s')
print(f'central, cube root of eps:    {dt_central:.1e} s')
```

The rules of thumb $1.5 \cdot 10^{-8}$ and $6.1 \cdot 10^{-6}$ match the
minima in the plot well. However, they only apply to quantities around 1, like
the time around $1.5\,\text{s}$ and the distance around $0.4\,\text{m}$ here.
If the variable is typically much larger or smaller, the best step size grows
or shrinks with it, for the central difference quotient to roughly
$\sqrt[3]{\text{eps}}$ times the typical size of the variable. The function
itself also plays a role. So the rules of thumb only give the order of
magnitude.

## Summary and outlook

If a function is available as a Python function, we pass it to `forward()` or
`central()` and choose the step size freely. If the function can be
differentiated often enough, the forward difference quotient has order of
accuracy 1 for small step sizes, and the central difference quotient has
order of accuracy 2. In a log-log plot, the order of accuracy appears as the
slope, and the Taylor expansion explains it. Very small step sizes do harm
because of rounding errors and cancellation, since the rounding error grows
like $\text{eps} / \Delta t$. For quantities around 1, step sizes of about
$\sqrt{\text{eps}} \approx 10^{-8}$ for the forward difference quotient and
$\sqrt[3]{\text{eps}}$, i.e. $10^{-5}$ to $10^{-6}$, for the central
difference quotient work well.

The exercises in Chapter 7.3 review both chapters, including an emergency
stop of an AGV. In Chapter 8.1, we search for the parameter of a model that
best fits measured data. The derivative shows us the direction, and we
compute it with the central difference quotient and the step size $10^{-6}$.

## Mini-exercises

### Mini-exercise 1

1. Write a function `backward(function, t, dt)` for the backward difference
   quotient. For $\Delta t = 0.1\,\text{s}$ at $t = 1.5\,\text{s}$, compute
   the deviation from the exact value with its sign, i.e. without `abs()`, for
   the forward and the backward difference quotient.
2. Answer without code: why is the forward difference quotient above the
   exact velocity and the backward difference quotient below it?
3. Answer without code: how large is the error of the central difference
   quotient for the start from Chapter 7.1 with $s(t) = 0.2\,t^2$ during the
   acceleration?

```{code-cell} python
# code cell
```

### Mini-exercise 2

1. Read off the plot: what step size does each of the two difference
   quotients need to keep the error below
   $1\,\text{mm/s} = 10^{-3}\,\text{m/s}$? Check your reading with
   `forward()` and `central()`.
2. Answer without code: at $t = 1.5\,\text{s}$, the AGV is accelerating at
   $0.444\,\text{m/s}^2$. Use the Taylor expansion to estimate the error of
   the forward difference quotient for $\Delta t = 0.01\,\text{s}$, and
   compare your estimate with the output in the previous section.

```{code-cell} python
# code cell
```

### Mini-exercise 3

1. In Chapter 8, we use the central difference quotient with the step size
   $10^{-6}$. Compute the error at $t = 1.5\,\text{s}$ for this step size and
   compare it with the smallest error in the plot.
2. Answer without code: a classmate uses the central difference quotient and
   chooses $\Delta t = 10^{-12}$ to make the derivative as accurate as
   possible. What do you tell them? Use the plot.

```{code-cell} python
# code cell
```
