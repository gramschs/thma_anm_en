---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 8.5 Exercises

These exercises are meant for self-study at home and review the material of
Chapters 8.1 to 8.4. Allow about 90 minutes for them. Before starting the
exercises, run the following cell. It contains the functions `central()` and
`gradient_descent()` from Chapter 8.1 as well as `gradient()` and
`gradient_descent_2d()` from Chapter 8.3. Several exercises use the same
names, for example `cost`. If you go back to an earlier exercise, run its cells
again in order. Also keep in mind that the methods also stop when
`max_iterations` is reached, and that a small slope alone does not prove a
minimum.

The difficulty level is given in the title of each exercise:

* ✩ Comprehension: predict and explain code and outputs (approx. 5 min)
* ✩✩ Application: write your own code and interpret results (approx. 10 min)
* ✩✩✩ Mini-project: combine several concepts from this chapter (approx. 30 min)

These times are for working on the exercises only. Add time for reading,
checking your results and debugging.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# functions from Chapter 8.1
def central(function, point, dx):
    """Central difference quotient of function at the given point."""
    return (function(point + dx) - function(point - dx)) / (2 * dx)

def gradient_descent(function, start, learning_rate, tolerance,
                     max_iterations):
    """Search for a minimum of function, starting at start.

    Returns all visited points as an array.
    """
    point = start
    history = [point]
    for k in range(max_iterations):
        slope = central(function, point, 1e-6)
        # stopping criterion: slope almost zero
        if abs(slope) < tolerance:
            break
        point = point - learning_rate * slope
        history.append(point)
    return np.array(history)

# functions from Chapter 8.3
def gradient(function, point, dx):
    """Gradient of function at point = [x, y].

    Each partial derivative with the central difference quotient.
    """
    shift_x = np.array([dx, 0.0])
    shift_y = np.array([0.0, dx])
    derivative_x = (function(point + shift_x)
                    - function(point - shift_x)) / (2 * dx)
    derivative_y = (function(point + shift_y)
                    - function(point - shift_y)) / (2 * dx)
    return np.array([derivative_x, derivative_y])

def gradient_descent_2d(function, start, learning_rate, tolerance,
                        max_iterations):
    """Search for a minimum of function, starting at start = [x, y].

    Returns all visited points as an array, row = [x, y].
    """
    point = start
    history = [point]
    for k in range(max_iterations):
        slope = gradient(function, point, 1e-6)
        # stopping criterion: length of the gradient almost zero
        if np.linalg.norm(slope) < tolerance:
            break
        point = point - learning_rate * slope
        history.append(point)
    return np.array(history)
```

````{admonition} Exercise 8.1 (✩)
:class: tip
In milling, the cost per part depends on the **feed rate**, i.e. on how fast
the tool moves through the material. If the feed rate is low, machining takes
a long time. If it is high, the tool wears out quickly. In simplified form, we
describe the cost in € per part by $C(v) = (v - 4)^2 + 10$ with the feed rate
$v$ in m/min. The model only applies near $4\,\text{m/min}$, and the starting
value $v = 0$ in the code only serves to illustrate the method. The following
code is given:

```python
def cost(feed):
    """Cost in € per part for the feed rate in m/min."""
    return (feed - 4)**2 + 10

# three steps of gradient descent for three learning rates
for learning_rate in [0.25, 0.5, 1.0]:
    feed = 0.0
    history = [feed]
    for k in range(3):
        slope = central(cost, feed, 1e-6)
        feed = feed - learning_rate * slope
        history.append(feed)
    print(learning_rate, np.round(history, 2))
```

Write down your guess in a Markdown cell before you run the code.

1. At which feed rate is the cost lowest, and how high is it there?
2. The derivative is $C'(v) = 2 \cdot (v - 4)$. How large is the slope at the
   start $v = 0$?
3. Which three feed rates does the code compute for each of the three learning
   rates? What do you notice about the learning rate $1.0$?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def cost(feed):
    """Cost in € per part for the feed rate in m/min."""
    return (feed - 4)**2 + 10

for learning_rate in [0.25, 0.5, 1.0]:
    feed = 0.0
    history = [feed]
    for k in range(3):
        slope = central(cost, feed, 1e-6)
        feed = feed - learning_rate * slope
        history.append(feed)
    print(learning_rate, np.round(history, 2))
```
Output:

```text
0.25 [0.  2.  3.  3.5]
0.5 [0. 4. 4. 4.]
1.0 [0. 8. 0. 8.]
```

1. The expression $(v - 4)^2$ is never negative and becomes zero at
   $v = 4\,\text{m/min}$. There, the cost is €10 per part.
2. The slope at the start is $2 \cdot (0 - 4) = -8$ € per (m/min). It is
   negative, so the first step goes toward higher feed rates.
3. With the learning rate $0.25$, the first step is $0.25 \cdot 8 = 2$ long.
   Each further step halves the distance to the minimum: $2$, $3$, $3.5$. With
   $0.5$, the very first step lands exactly at $4$. After that, the slope is
   zero and the feed rate stays put. With $1.0$, the method jumps from $0$ to
   $8$, exactly as far past the minimum as it was before it. There, the slope
   is $+8$, and it jumps back to $0$. For this parabola, the method would
   oscillate endlessly between $0$ and $8$ and never converge.
````

````{admonition} Exercise 8.2 (✩)
:class: tip
A classmate typed up gradient descent for the order quantity from
Chapter 8.1. Their code is:

```python
def total_cost(quantity):
    """Annual cost C(Q) in € for the order quantity Q = quantity."""
    return 12000 / quantity * 50 + quantity / 2 * 1.2

quantity = 500
for k in range(3):
    slope = central(total_cost, quantity, 1e-6)
    quantity = quantity + 200 * slope
    cost = total_cost(quantity)
    print(f'Order quantity {quantity:8.1f} units, cost €{cost:.1f}')
```

Write down your guess in a Markdown cell before you run the code.

1. Find the error.
2. The slope at 500 units is $-1.8$ €/unit. Where does the first step land?
   Does the cost go up or down?
3. After the second step, the order quantity is negative, and so is the cost.
   Why does `total_cost()` return a value at all, and why is it meaningless?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def total_cost(quantity):
    """Annual cost C(Q) in € for the order quantity Q = quantity."""
    return 12000 / quantity * 50 + quantity / 2 * 1.2

quantity = 500
for k in range(3):
    slope = central(total_cost, quantity, 1e-6)
    quantity = quantity + 200 * slope
    cost = total_cost(quantity)
    print(f'Order quantity {quantity:8.1f} units, cost €{cost:.1f}')
```
Output:

```text
Order quantity    140.0 units, cost €4369.7
Order quantity  -5862.5 units, cost €-3619.8
Order quantity  -5745.9 units, cost €-3552.0
```

1. The rule contains a plus instead of a minus. The correct line is
   `quantity = quantity - 200 * slope`. With the plus, the method moves in the
   direction of the slope, i.e. uphill.
2. The first step leads to $500 + 200 \cdot (-1.8) = 140$ units. There, the
   cost of €4,369.70 is almost three times as high as before.
3. At 140 units, the curve is very steep, and the slope is about $-30$
   €/unit. The next step therefore goes about $6000$ units to the left, far
   into negative numbers. Python evaluates the formula for negative numbers,
   too. The model, however, only applies to positive order quantities, and a
   negative order quantity and a negative cost have no meaning. A method that
   produces nonsense often does not stop anyway. That is why we always have to
   check the results for plausibility.
````

````{admonition} Exercise 8.3 (✩)
:class: tip
A **snap-action switch** has two stable positions. The stored energy in mJ
depends on the deflection $x$ in mm: $E(x) = x^4 - 4x^2 + x$. The curve has
two valleys, at about $x = -1.47\,\text{mm}$ and $x = 1.35\,\text{mm}$, with a
hump at about $x = 0.13\,\text{mm}$ in between. The switch stays in the valley
it rolls into when released. The following code is given:

```python
def energy(x):
    """Stored energy in mJ at the deflection x in mm."""
    return x**4 - 4 * x**2 + x

for start in [0.5, -0.5, 0.1]:
    history = gradient_descent(energy, start, 0.02, 1e-4, 500)
    x_end = history[-1]
    e_end = energy(x_end)
    print(f'Start {start:5.2f} mm: end at {x_end:6.3f} mm, {e_end:6.3f} mJ')
```

Write down your guess in a Markdown cell before you run the code.

1. In which valley does the method end for each of the three starting values?
   Explain the starting value $0.1\,\text{mm}$ in particular.
2. Each valley is a **local minimum**. The deepest valley is also called the
   **global minimum**. Which valley is the global minimum? Estimate it using
   the formula.
3. How can we find the global minimum of a function with several valleys if we
   only have gradient descent at our disposal?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
def energy(x):
    """Stored energy in mJ at the deflection x in mm."""
    return x**4 - 4 * x**2 + x

for start in [0.5, -0.5, 0.1]:
    history = gradient_descent(energy, start, 0.02, 1e-4, 500)
    x_end = history[-1]
    e_end = energy(x_end)
    print(f'Start {start:5.2f} mm: end at {x_end:6.3f} mm, {e_end:6.3f} mJ')
```
Output:

```text
Start  0.50 mm: end at  1.347 mm, -2.619 mJ
Start -0.50 mm: end at -1.473 mm, -5.444 mJ
Start  0.10 mm: end at -1.473 mm, -5.444 mJ
```

1. With the small learning rate $0.02$, the method walks downhill in short
   steps and stays in the valley on whose slope it starts. From
   $0.5\,\text{mm}$, it goes into the right valley, and from $-0.5\,\text{mm}$
   into the left one. The starting value $0.1\,\text{mm}$ lies just to the
   left of the hump at $0.13\,\text{mm}$. There, the curve slopes down to the
   left, and the method rolls into the left valley, even though the starting
   value is closer to the right valley.
2. Without the term $+x$, both valleys would be equally deep. The term makes
   the energy smaller for negative $x$ and larger for positive $x$. So the left
   valley with $-5.444\,\text{mJ}$ is the global minimum, and the right one
   with $-2.619\,\text{mJ}$ is only a local minimum.
3. With a small learning rate, gradient descent usually only finds the valley
   on whose slope it starts. So we start it from several starting values
   spread over the whole range and take the result with the smallest function
   value. This does not guarantee the global minimum, but the chances increase
   with the number of starting values.
````

````{admonition} Exercise 8.4 (✩)
:class: tip
A spring is deflected by $1$, $2$ and $3\,\text{cm}$, and the measured forces
are $2.3$, $4.1$ and $6.2\,\text{N}$. The model is $F = c \cdot s$ with the
spring stiffness $c$ in N/cm. The following code is given:

```python
deflection = np.array([1.0, 2.0, 3.0])
force = np.array([2.3, 4.1, 6.2])

for c in [2.0, 2.1]:
    deviation = force - c * deflection
    mse = np.mean(deviation**2)
    print(c, np.round(deviation, 2), round(mse, 4))
```

Write down your guess in a Markdown cell before you run the code.

1. For both values of $c$, compute the three deviations and the mean squared
   error by hand.
2. Which spring stiffness fits better? What is the unit of the mean squared
   error?
3. For $c = 2.0$, all deviations are positive. What does this mean for the
   model line compared with the measurement points?
4. Run the code and check your predictions.
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
```python
deflection = np.array([1.0, 2.0, 3.0])
force = np.array([2.3, 4.1, 6.2])

for c in [2.0, 2.1]:
    deviation = force - c * deflection
    mse = np.mean(deviation**2)
    print(c, np.round(deviation, 2), round(mse, 4))
```
Output:

```text
2.0 [0.3 0.1 0.2] 0.0467
2.1 [ 0.2 -0.1 -0.1] 0.02
```

1. For $c = 2.0$, the deviations are $0.3$, $0.1$ and $0.2\,\text{N}$. Their
   squares $0.09$, $0.01$ and $0.04$ give a mean of
   $0.14 / 3 \approx 0.0467$. For $c = 2.1$, the deviations are $0.2$, $-0.1$
   and $-0.1\,\text{N}$, and the squares $0.04$, $0.01$ and $0.01$ give a mean
   of $0.06 / 3 = 0.02$.
2. $c = 2.1\,\text{N/cm}$ fits better, because the mean squared error is less
   than half as large. Its unit is $\text{N}^2$, because we square forces.
3. The deviation is the measured value minus the model. If all deviations are
   positive, all measurement points lie above the model line. The line is too
   flat, so $c$ should be larger.
````

````{admonition} Exercise 8.5 (✩✩)
:class: tip
A truck drives $400\,\text{km}$ on the autobahn. The faster it drives, the
shorter the trip and the lower the wage costs for the driver. The fuel
consumption, however, increases with the speed. At the speed $v$ in km/h, the
truck uses $20 + 0.0015 \cdot v^2$ liters per $100\,\text{km}$. The driver
costs €30 per hour, and a liter of diesel costs €1.70. So the trip costs

$$C(v) = \frac{400}{v} \cdot 30 + \frac{400}{100} \cdot (20 + 0.0015 \cdot v^2) \cdot 1.70.$$

1. Write a function `trip_cost(v)` and plot the cost for speeds from $50$ to
   $100\,\text{km/h}$.
2. Determine the cheapest speed with `gradient_descent()`. Start at
   $60\,\text{km/h}$ with the learning rate $10$, the tolerance $10^{-3}$ and
   at most 500 iterations. What happens with the learning rate $50$?
3. In Germany, trucks over $7.5\,\text{t}$ may drive at most
   $80\,\text{km/h}$ on the autobahn. How much more expensive is a trip at
   $80\,\text{km/h}$ than one at the cheapest speed?
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
1. The function follows the formula directly:

   ```python
   # task 1: cost of the trip against speed
   def trip_cost(v):
       """Cost in € for 400 km at the speed v in km/h."""
       wages = 400 / v * 30
       diesel = 400 / 100 * (20 + 0.0015 * v**2) * 1.70
       return wages + diesel

   v_values = np.linspace(50, 100, 200)
   fig, ax = plt.subplots(figsize=(7, 4))
   ax.plot(v_values, trip_cost(v_values))
   ax.set_xlabel('Speed in km/h')
   ax.set_ylabel('Cost of the trip in €')
   ax.set_title('Wages and diesel for 400 km')
   ax.grid(True)
   plt.show()
   ```

   The curve has a flat minimum between $80$ and $90\,\text{km/h}$.
2. We start at $60\,\text{km/h}$:

   ```python
   # task 2: cheapest speed
   for learning_rate in [10, 50]:
       history = gradient_descent(trip_cost, 60.0, learning_rate, 1e-3, 500)
       n_iterations = len(history) - 1
       v_end = history[-1]
       print(f'Learning rate {learning_rate}: {n_iterations} iterations, '
             f'v = {v_end:.2f} km/h')
   ```

   Output:

   ```text
   Learning rate 10: 7 iterations, v = 83.78 km/h
   Learning rate 50: 500 iterations, v = 147.10 km/h
   ```

   With the learning rate $10$, the method finds $83.78\,\text{km/h}$ after
   seven iterations. With $50$, it jumps back and forth, does not meet the
   stopping criterion and ends at a nonsensical speed.
3. We compare the cost at both speeds:

   ```python
   # task 3: extra cost at 80 km/h
   history = gradient_descent(trip_cost, 60.0, 10, 1e-3, 500)
   cost_best = trip_cost(history[-1])
   cost_80 = trip_cost(80)
   extra_cost = cost_80 - cost_best
   print(f'At the cheapest speed: €{cost_best:.2f}')
   print(f'At 80 km/h:            €{cost_80:.2f}')
   print(f'Extra cost:            €{extra_cost:.2f}')
   ```

   Output:

   ```text
   At the cheapest speed: €350.83
   At 80 km/h:            €351.28
   Extra cost:            €0.45
   ```

   At $80\,\text{km/h}$, the trip costs only €0.45 more. Because the minimum
   is so flat, the trucking company loses practically nothing because of the
   speed limit. Since the cost keeps falling up to the minimum at
   $83.8\,\text{km/h}$, $80\,\text{km/h}$ is the cheapest permitted speed
   here.
````

````{admonition} Exercise 8.6 (✩✩)
:class: tip
In Chapter 8.3, we claimed that the weighted center of gravity minimizes the
sum of the squared distances. We now check this with gradient descent. The
plants and loads from Chapter 8.3 are:

```python
plants = np.array([[6.0, 24.0], [16.0, 30.0], [20.0, 12.0],
                   [8.0, 6.0], [44.0, 10.0]])
loads = np.array([12, 10, 10, 8, 6])
```

1. Write a function `effort_squared(location)` that computes
   $\sum n_i \cdot d_i^2$.
2. Start `gradient_descent_2d()` at $(40, 30)$ with the learning rate $0.2$
   from Chapter 8.3, the tolerance $0.01$ and at most 200 iterations. What
   happens? Then try the learning rates $0.02$, $0.01$ and $0.005$.
3. Compare the result with the weighted center of gravity. Why does this cost
   function need a much smaller learning rate than `effort()` in Chapter 8.3?
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
1. Instead of the square root, we add up the squares directly:

   ```python
   # task 1: sum of the weighted squared distances
   plants = np.array([[6.0, 24.0], [16.0, 30.0], [20.0, 12.0],
                      [8.0, 6.0], [44.0, 10.0]])
   loads = np.array([12, 10, 10, 8, 6])

   def effort_squared(location):
       """Sum of loads times squared distance in km²."""
       difference = plants - location
       squares = difference[:, 0]**2 + difference[:, 1]**2
       return np.sum(loads * squares)
   ```

2. We try out all four learning rates:

   ```python
   # task 2: different learning rates
   start = np.array([40.0, 30.0])
   for learning_rate in [0.2, 0.02, 0.01, 0.005]:
       history = gradient_descent_2d(effort_squared, start, learning_rate,
                                     0.01, 200)
       n_iterations = len(history) - 1
       print(f'Learning rate {learning_rate}: {n_iterations} iterations, '
             f'end at {np.round(history[-1], 3)}')
   ```

   Output (the very large numbers may differ slightly depending on the
   computer):

   ```text
   Learning rate 0.2: 8 iterations, end at [3.03756161e+11 9.90524457e+10]
   Learning rate 0.02: 72 iterations, end at [16.522 17.739]
   Learning rate 0.01: 5 iterations, end at [16.522 17.739]
   Learning rate 0.005: 21 iterations, end at [16.522 17.739]
   ```

   With $0.2$, the method blows up. The fact that it stops after eight
   iterations does not mean that it has found a minimum. The coordinates are
   so large that the difference quotient becomes zero because of rounding
   errors. With $0.02$, it jumps back and forth for a long time, and with
   $0.01$, it reaches the goal after only five iterations.
3. We compute the center of gravity as in Chapter 8.3:

   ```python
   # task 3: weighted center of gravity for comparison
   center_x = np.sum(loads * plants[:, 0]) / np.sum(loads)
   center_y = np.sum(loads * plants[:, 1]) / np.sum(loads)
   print('Center of gravity:', np.round([center_x, center_y], 3))
   ```

   Output:

   ```text
   Center of gravity: [16.522 17.739]
   ```

   Gradient descent ends up at the center of gravity within the tolerance.
   This confirms the claim from Chapter 8.3 for our plants, but it is not a
   general proof.

   The gradient of `effort_squared()` is exactly $2 \cdot 46 = 92$ times as
   large as the distance from the center of gravity, because all plants
   together need 46 loads. A step with the learning rate $\alpha$ is therefore
   $92 \cdot \alpha$ times as long as the distance. With
   $\alpha = 1/92 \approx 0.011$, the very first step lands exactly at the
   center of gravity, and with $0.01$ almost, as with the learning rate $0.5$
   in Exercise 8.1. At exactly $\alpha = 2/92 \approx 0.022$, each step jumps
   exactly as far past the goal as it was before it, and the method oscillates
   with a constant distance. If $\alpha$ is larger, the distance grows with
   every step, and the method blows up. With $0.02$, we are just below the
   limit and oscillate for a long time. For `effort()` in Chapter 8.3, on the
   other hand, the gradient does not grow with the distance, and its length is
   never larger than 46. There, the steps stay limited even far away from the
   goal, and for the starting value in Chapter 8.3, the learning rate $0.2$
   worked well.
````

````{admonition} Exercise 8.7 (✩✩✩) Mini-project: Positioning the placement robot more precisely
:class: tip
In Chapter 5.4, we determined the joint angles of the SCARA robot for the
placement site $P_1 = (0.30, 0.35)$ with a grid search in $1°$ steps. After
$27\,331$ positions, the gripper with $\alpha = 9°$ and $\beta = 99°$ was still
$3.2\,\text{mm}$ away from the site. Now we will do better. For this exercise,
you only need the following formula from Chapter 5.4 for the position of the
gripper with the arm lengths $l_1 = 0.4\,\text{m}$ and $l_2 = 0.3\,\text{m}$:

$$x = l_1 \cos\alpha + l_2 \cos(\alpha + \beta), \qquad
y = l_1 \sin\alpha + l_2 \sin(\alpha + \beta).$$

Joint 2 may only bend between $0°$ and $150°$.

**Part 1:** Write a function `gripper(angles)` that returns the position of the
gripper as an array for `angles = [alpha, beta]` in degrees. `np.deg2rad()`
converts degrees to radians. Check: in the home position $(0°, 0°)$, the
gripper is at $(0.7, 0)$. Then write a cost function `cost(angles)` that
computes the square of the distance between the gripper and $P_1$ in
$\text{mm}^2$. Use it to check the result of the grid search.

**Part 2:** Start `gradient_descent_2d()` at the result of the grid search with
the learning rate $0.01$, the tolerance $10^{-3}$ and at most 500 iterations.
Which angles do you find, and how far is the gripper from $P_1$ now? How often
was `cost()` called, compared with the grid search?

**Part 3:** Now start the method in the position $(90°, 0°)$, in which the arm
points straight up, and store the result in `angles_up`. Which angles does it
find? The following code draws both solutions as a polyline from the origin
via joint 2 to the gripper. It expects the solution from Part 2 in
`angles_best`, the target $P_1$ in `target` and the length of arm 1 in `l_1`.

```python
# both positions of the robot arm
fig, ax = plt.subplots(figsize=(6, 6))
for angles, name in [(angles_best, 'solution from Part 2'),
                     (angles_up, 'solution from Part 3')]:
    alpha = np.deg2rad(angles[0])
    joint_2 = l_1 * np.array([np.cos(alpha), np.sin(alpha)])
    tip = gripper(angles)
    ax.plot([0, joint_2[0], tip[0]], [0, joint_2[1], tip[1]],
            marker='o', linewidth=3, label=name)
ax.scatter(target[0], target[1], marker='x', s=100, color='black', label='P1')
ax.set_aspect('equal')
ax.set_xlabel('x in m')
ax.set_ylabel('y in m')
ax.set_title('Two positions for the same placement site')
ax.legend()
ax.grid(True)
plt.show()
```

**Closing question:** Is the robot allowed to move to the solution from
Part 3? What does this mean for using gradient descent, and how can grid
search and gradient descent be combined sensibly?
````

```{code-cell} python
# code cell
```

````{admonition} Solution
:class: tip
:class: dropdown
**Part 1:** The function follows the formula, and the cost function converts
the distance to millimeters and squares it:

```python
# Part 1: position of the gripper and cost function
l_1 = 0.4
l_2 = 0.3
target = np.array([0.30, 0.35])

def gripper(angles):
    """Position of the gripper in m for angles = [alpha, beta] in degrees."""
    alpha = np.deg2rad(angles[0])
    beta = np.deg2rad(angles[1])
    x = l_1 * np.cos(alpha) + l_2 * np.cos(alpha + beta)
    y = l_1 * np.sin(alpha) + l_2 * np.sin(alpha + beta)
    return np.array([x, y])

def cost(angles):
    """Square of the distance between gripper and target in mm²."""
    difference = (gripper(angles) - target) * 1000
    return difference[0]**2 + difference[1]**2

print('Home position:', gripper(np.array([0.0, 0.0])))
remaining_grid = np.sqrt(cost(np.array([9.0, 99.0])))
print(f'Grid search: {remaining_grid:.1f} mm away from P1')
```

Output:

```text
Home position: [0.7 0. ]
Grid search: 3.2 mm away from P1
```

The functions confirm the home position and the remaining distance of
$3.2\,\text{mm}$ from Chapter 5.4.

**Part 2:** We start at the result of the grid search:

```python
# Part 2: gradient descent starting from the result of the grid search
start = np.array([9.0, 99.0])
history = gradient_descent_2d(cost, start, 0.01, 1e-3, 500)
angles_best = history[-1]
remaining = np.sqrt(cost(angles_best))
n_iterations = len(history) - 1
calls = 4 * (n_iterations + 1)
print(f'{n_iterations} iterations, {calls} calls of cost()')
print('Angles in degrees:', np.round(angles_best, 3))
print(f'Remaining distance: {remaining:.6f} mm')
```

Output:

```text
21 iterations, 88 calls of cost()
Angles in degrees: [ 9.398 98.989]
Remaining distance: 0.000090 mm
```

After 21 iterations, the gripper in the model is less than $0.1\,\mu\text{m}$
away from $P_1$. This is a computational accuracy. How accurately the real
robot positions depends on its mechanics. For the gradient, each iteration
evaluates `cost()` four times, and including the last check of the stopping
criterion, that makes 88 calls. On top of that comes the grid search that
provided the starting value. The solution of the closing question shows how
many calls can be saved in total.

**Part 3:** We start in the position stretched straight up and draw both
solutions. Joint 2 is at $l_1 (\cos\alpha, \sin\alpha)$:

```python
# Part 3: different starting value
history_up = gradient_descent_2d(cost, np.array([90.0, 0.0]),
                                 0.01, 1e-3, 500)
angles_up = history_up[-1]
print('Angles in degrees:', np.round(angles_up, 3))

fig, ax = plt.subplots(figsize=(6, 6))
for angles, name in [(angles_best, 'solution from Part 2'),
                     (angles_up, 'solution from Part 3')]:
    alpha = np.deg2rad(angles[0])
    joint_2 = l_1 * np.array([np.cos(alpha), np.sin(alpha)])
    tip = gripper(angles)
    ax.plot([0, joint_2[0], tip[0]], [0, joint_2[1], tip[1]],
            marker='o', linewidth=3, label=name)
ax.scatter(target[0], target[1], marker='x', s=100, color='black', label='P1')
ax.set_aspect('equal')
ax.set_xlabel('x in m')
ax.set_ylabel('y in m')
ax.set_title('Two positions for the same placement site')
ax.legend()
ax.grid(True)
plt.show()
```

Output:

```text
Angles in degrees: [ 89.399 -98.989]
```

From the stretched position, the method finds $\alpha = 89.4°$ and
$\beta = -99.0°$. There, too, the gripper in the model is practically exactly
at $P_1$. The two positions are mirror images about the line from the origin
to $P_1$: in one, arm 2 bends to the left, and in the other, to the right.

**Closing question:** No. With $\beta = -99°$, joint 2 would have to bend
clockwise, but only $0°$ to $150°$ is allowed. Gradient descent does not know
this limit. It walks downhill into the valley near which it starts. For
$P_1$, there are two arm positions that put the gripper exactly on the site.
With this small learning rate, the starting value decides which one the method
finds. That is why we have to check every result against the joint limits.

Grid search and gradient descent complement each other well. A coarse grid
search that only tries out allowed angles provides a starting value close to
the allowed arm position here, but only an inaccurate solution. Gradient
descent refines it with a few calls. A grid with $10°$ steps would already
have been enough. With $\alpha$ from $0°$ to $180°$ and $\beta$ from $0°$ to
$150°$, it tries out 19 times 16, i.e. 304 positions, and finds
$(10°, 100°)$, $8.8\,\text{mm}$ away from $P_1$. From there, gradient descent
needs 100 calls to reach the solution from Part 2. Together, that makes a
little over 400 calls instead of $27\,331$. We also have to check the refined
result against the joint limits again. In addition, if a cost function has
very narrow valleys, a coarse grid can miss the right valley.
````
