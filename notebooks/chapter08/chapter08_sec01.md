---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 8.1 Cost Function and Gradient Descent

A company assembles gearboxes and uses 12,000 ball bearings of the same type
per year. Until now, the purchasing department has ordered 500 bearings every
two weeks. Each order costs €50 for processing, shipping and incoming
inspection, no matter how many bearings are delivered. Each bearing in stock
costs €1.20 per year for storage space, insurance and the capital tied up in
it. *Should the company order less often and buy more each time?*

A problem in which we seek the optimal value of a variable is called an
**optimization problem**. In Chapter 7.2, we computed the derivative of a
Python function with the central difference quotient. In this chapter, the
derivative guides us to the smallest value of a function. The method is called
**gradient descent**. It is at the heart of many optimization tools in design
and manufacturing, and it is the workhorse for training neural networks.

## Which order quantity is the cheapest?

The number of bearings the company orders at a time is called the **order
quantity** $Q$. The annual cost consists of two parts.

* With an annual demand of $D$ units, the company places $D / Q$ orders per
  year. At $C_O$ per order, this adds up to the **ordering costs**
  $D / Q \cdot C_O$.
* Right after each delivery, there are $Q$ bearings in stock. Until the next
  delivery, the stock decreases steadily to zero, so on average $Q / 2$ units
  are in stock. With a holding cost rate of $c_H$ per unit per year, this
  gives the **holding costs** $Q / 2 \cdot c_H$.

Adding both parts gives the total annual cost:

$$C(Q) = \frac{D}{Q} \cdot C_O + \frac{Q}{2} \cdot c_H.$$

| Symbol | Meaning | Value | Name in code |
| --- | --- | --- | --- |
| $Q$ | order quantity | unknown, currently 500 units | `quantity` |
| $D$ | annual demand | 12,000 units | `demand` |
| $C_O$ | cost per order | €50 | `cost_per_order` |
| $c_H$ | holding cost rate | €1.20 per unit per year | `holding_rate` |
| $C(Q)$ | total annual cost | in € | `total_cost()` |

An uppercase $C$ denotes an amount of money in €, and a lowercase $c$ denotes
a rate per unit per year.

First, we define the known quantities. In the code, we use descriptive names
instead of the symbols. The last column of the table shows which name goes
with which symbol.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt

# annual demand D in units
demand = 12000
# cost C_O per order in €
cost_per_order = 50
# holding cost rate c_H in € per unit per year
holding_rate = 1.2
```

We write the total cost as a function of the order quantity.

```{code-cell} python
def total_cost(quantity):
    """Annual cost C(Q) in € for the order quantity Q = quantity."""
    # TODO: ???   compute the ordering costs from the annual demand, the order quantity and the cost per order, and store them in ordering_cost
    # TODO: ???   compute the holding costs from the average stock and the holding cost rate, and store them in holding_cost
    return ordering_cost + holding_cost
```

We compare the current order quantity of 500 units with half, twice and four
times that amount.

```{code-cell} python
# total cost for a few order quantities
for quantity in [250, 500, 1000, 2000]:
    cost = total_cost(quantity)
    print(f'Order quantity {quantity:4d} units: €{cost:7.2f} per year')
```

Currently, the company pays €1,500 per year. With 1000 units per order, it
would pay only €1,200, but with 2000 units it would be back at €1,500. So the
minimum lies somewhere in between. *But where exactly?* To find out, we
evaluate the function for 400 order quantities between 100 and 4000 units.
`total_cost()` contains only basic arithmetic, which NumPy performs
element-wise. So if we pass in an array of order quantities, we get an array
of costs back.

```{code-cell} python
# 400 order quantities from 100 to 4000 units
quantity_values = np.linspace(100, 4000, 400)
cost_values = total_cost(quantity_values)
```

The plot shows the total cost against the order quantity, with the current
order quantity highlighted.

```{code-cell} python
# plot: total cost against order quantity
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(quantity_values, cost_values)
ax.plot(500, total_cost(500), marker='o', color='red', label='current')
ax.set_xlabel('Order quantity in units')
ax.set_ylabel('Total cost in € per year')
ax.set_title('Ordering and holding costs')
ax.set_ylim(0, 4000)
ax.legend()
ax.grid(True)
plt.show()
```

On the left, the curve drops steeply, and on the right, it rises slowly. In
between lies a flat valley with the minimum at about 1000 units and €1,200.
For small order quantities, the frequent orders drive up the cost. For large
ones, the high inventory levels do.

## What is a cost function?

In optimization, a function whose smallest value gives the best solution is
called a **cost function**. The point at which it reaches its minimum is called
the **minimizer**. Here the cost function actually measures euros, but that
does not have to be the case. Any function we want to minimize is called a
cost function, for example the deviation between a model and measured data
(Chapter 8.2) or the transport effort in truck-kilometers per week
(Chapter 8.3). In machine learning, the cost function is also called the
**loss function**. In economics, the term is used more narrowly for cost as a
function of production volume.

## Which way is downhill?

For the plot, we evaluated the function 400 times, and we still know the
minimum only approximately. If the cost depends on several quantities, the
number of evaluations grows very quickly. With two quantities and 400 values
each, that is already 160,000 evaluations, and with three quantities, 64
million. So let us imagine that we only know the cost at the current order
quantity and want to walk downhill from there, like a hiker in fog.

The slope, i.e. the derivative $C'(Q)$, tells us which way to go. If it is
negative, the cost decreases as the order quantity increases, and we should
order more. If it is positive, we should order less. **Gradient descent**
turns this into an update rule:

$$Q_\text{new} = Q - \alpha \cdot C'(Q).$$

The minus sign makes sure that we move against the slope, i.e. downhill. The
number $\alpha > 0$ is called the **learning rate**. It determines how far we
move relative to the slope. Where the curve is steep, we take large steps.
Close to the minimum, the slope is almost zero, and the steps automatically
become small. Each repetition of this calculation is called an **iteration**.
The name "gradient" comes from Chapter 8.3, where the cost depends on two
quantities. For a single quantity, the gradient is simply the derivative.

We compute the derivative with the central difference quotient from
Chapter 7.2. Instead of the time `t`, the variable is now called `point`,
because it can stand for any quantity. As announced in Chapter 7.2, we use a
step size of $10^{-6}$.

```{code-cell} python
def central(function, point, dx):
    """Central difference quotient of function at the given point."""
    return (function(point + dx) - function(point - dx)) / (2 * dx)
```

At the current order quantity of 500 units, we get the following slope.

```{code-cell} python
# slope of the cost function at the current order quantity
# TODO: ???   compute the slope of the total cost at 500 units with step size 1e-6 and store it in slope
print(f'Slope at 500 units: {slope:.4f} €/unit')
```

The slope is negative. If the company orders one more bearing at a time, the
annual cost drops by about €1.80. So we should move to the right. The rule of
thumb for the step size from Chapter 7.2 applies to quantities around 1. The
order quantity is around 1000, so the best step size would be larger. With
$10^{-6}$, however, the error stays below $10^{-7}$ €/unit, which is
negligible.

We take one step with a learning rate of 200.

```{code-cell} python
# one step of gradient descent
learning_rate = 200
quantity = 500
# TODO: ???   take one step of gradient descent from quantity and store the new order quantity in quantity_new

# cost before and after the step
cost_old = total_cost(quantity)
cost_new = total_cost(quantity_new)
print(f'New order quantity: {quantity_new:.1f} units')
print(f'Cost before: €{cost_old:.2f}, after: €{cost_new:.2f}')
```

A single step takes us from 500 to 860 units and lowers the cost from €1,500
to €1,213.67. A learning rate of 200 seems large, but it is not. The product
$\alpha \cdot C'(Q)$ has to be a number of units, but the slope is measured in
€/unit. So the right size for the learning rate depends on the units of the
problem.

Now we repeat the step ten times in a loop. We use `append()` to add each new
order quantity to the list `history`.

```{code-cell} python
# ten iterations of gradient descent, starting at 500 units
quantity = 500
history = [quantity]
for k in range(10):
    slope = central(total_cost, quantity, 1e-6)
    quantity = quantity - learning_rate * slope
    history.append(quantity)

print('Order quantities:', np.round(history, 1))
```

The order quantity grows with every iteration, but more and more slowly:
first by 360 units, then by 42, and in the end by only 3. The reason is not
the learning rate, which stays at 200, but the slope, which gets smaller the
closer we get to the minimum. After ten iterations, we are at 991 units, just
short of the minimum.

## When have we reached the minimum?

So far, we have set a fixed number of iterations. It is better to stop as soon
as we have reached the minimum, where the slope is zero. In practice, however,
the slope never becomes exactly zero, so we set a small **tolerance**. Once
the absolute value of the slope is smaller than the tolerance, we stop. Such a
condition is called a **stopping criterion**. The slope is measured in €/unit,
and we choose a tolerance of $10^{-4}$ €/unit.

`abs()` computes the absolute value. The statement `break` exits a `for` loop
immediately, even if it has not completed all its iterations. We still cap the
number of iterations with `max_iterations`, so that the calculation ends even
if the stopping criterion is never met. We wrap the whole method in a function.

```{code-cell} python
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
        # TODO: ???   end the loop if the absolute value of the slope is smaller than the tolerance
        point = point - learning_rate * slope
        history.append(point)
    return np.array(history)
```

Again, we start at 500 units with a learning rate of 200. The number of
iterations is one less than the length of the history, because the first entry
is the starting value.

```{code-cell} python
# gradient descent with stopping criterion
history = gradient_descent(total_cost, 500, 200, 1e-4, 100)

# result: number of iterations, order quantity and cost at the end
n_iterations = len(history) - 1
quantity_best = history[-1]
cost_best = total_cost(quantity_best)
print(f'{n_iterations} iterations')
print(f'Order quantity: {quantity_best:.2f} units')
print(f'Total cost: €{cost_best:.2f} per year')
```

After 28 iterations, the slope is smaller than the tolerance. The method finds
an order quantity of 999.94 units, or 1000 units after rounding, at a cost of
€1,200 per year. If the company switches to ordering 1000 bearings once a month
instead of 500 every two weeks, it saves €300 a year.

## From operations management: the EOQ formula

For this simple model, the minimizer can also be computed exactly. The
**economic order quantity (EOQ) formula** is
$Q^* = \sqrt{2 \cdot D \cdot C_O / c_H}$. With our numbers, it gives
$\sqrt{2 \cdot 12000 \cdot 50 / 1.2} = 1000$ units. Once the model becomes
more realistic, for example with quantity discounts or limited storage space,
there is usually no such formula. Gradient descent, on the other hand, only
needs the cost function as a Python function.

*Which learning rate is the right one?* We compare four learning rates and
plot the order quantity against the iteration. Such a plot shows whether, and
how quickly, the method approaches the minimum. This behavior is called
**convergence**. `ax.axhline()` draws the horizontal line at 1000 units.

```{code-cell} python
# plot: order quantity against iteration for four learning rates
fig, ax = plt.subplots(figsize=(7, 4))
for learning_rate in [50, 200, 800, 2000]:
    history = gradient_descent(total_cost, 500, learning_rate, 1e-4, 100)
    ax.plot(history, marker='.', label=f'learning rate {learning_rate}')
ax.axhline(1000, color='gray', linestyle='--')
ax.set_xlim(0, 30)
ax.set_xlabel('Iteration')
ax.set_ylabel('Order quantity in units')
ax.set_title('Convergence of gradient descent')
ax.legend()
ax.grid(True)
plt.show()
```

The four learning rates show typical behavior.

* With a learning rate of 50, the order quantity creeps toward the minimum.
  After 100 iterations, the stopping criterion is still not met.
* With 200, the order quantity approaches the minimum steadily from below.
* With 800, the first step overshoots the minimum by a wide margin and lands
  at 1940 units. Because the curve is flat on the right, the method still
  comes back quickly and converges after only seven iterations.
* With 2000, every step jumps across the valley, and in the end the order
  quantity oscillates endlessly between 815 and 1421 units. The method **does
  not converge**.

No learning rate works for every problem. If it is too small, the method needs
many iterations. If it is too large, the method starts to oscillate. In
practice, we try out a few learning rates and look at the convergence plot.

## Summary and outlook

A cost function assigns each value of a quantity a number that we want to
make as small as possible, here the annual cost of ordering and holding.
Gradient descent searches for its minimum without evaluating the function
everywhere. Starting from an initial value, it moves step by step against the
slope, following the update rule $Q_\text{new} = Q - \alpha \cdot C'(Q)$. We
compute the slope with the central difference quotient from Chapter 7.2. The
learning rate $\alpha$ determines whether the method converges slowly,
quickly or not at all. A stopping criterion ends the calculation as soon as
the slope is almost zero.

In Chapter 8.2, you will set up a cost function yourself that measures how
well a model fits measured data. You will then use `gradient_descent()` to
find the parameter for which the model and the measurements agree best. In
Chapter 8.3, the cost depends on two quantities at once: we will look for the
best location for a central warehouse. The derivative then becomes the
gradient.

## Mini-exercises

### Mini-exercise 1

1. Answer without code: why does the cost rise so steeply for very small order
   quantities, but only slowly for large ones?
2. For an order quantity of 1000 units, compute the ordering costs and the
   holding costs separately. What do you notice?
3. Answer without code: the holding cost rate rises to €2.40 per unit per
   year. Is the cheapest order quantity then above or below 1000 units?

```{code-cell} python
# code cell
```

### Mini-exercise 2

1. First answer without code: we start at 2000 units. What is the sign of the
   slope there, and in which direction does the first step go? Check your
   answer by repeating the ten iterations, starting at 2000 units.
2. For this simple model, we know the derivative as a formula:
   $C'(Q) = -D \cdot C_O / Q^2 + c_H / 2$. Evaluate it at 500 units and
   compare the result with `central()`.
3. Answer without code: why can gradient descent overshoot the minimum, even
   though the steps get small close to the minimum?

```{code-cell} python
# code cell
```

### Mini-exercise 3

1. Answer without code: where does the first step land with a learning rate of
   2000 if we start at 500 units? You already know the slope there.
2. Call `gradient_descent()` with learning rates of 400 and 1600, starting at
   500 units. How many iterations does the method need in each case?
3. Answer without code: with a learning rate of 2000, `gradient_descent()`
   still returns an order quantity. How can you tell from the return value
   that the result is useless?

```{code-cell} python
# code cell
```
