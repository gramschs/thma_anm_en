---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Preparation

In Chapters 8.1 to 8.4 we use gradient descent to find the smallest value of a
cost function. For this, you need some math, Python and physics from earlier
semesters and chapters. Before the lecture, take the quiz on this page to check
whether you are up to speed. It takes about ten minutes. Below the quiz, you
will find review material for any topics you had trouble with.

## What you should already know

From **math** you should be able to:

* tell from the sign of the derivative whether a function is decreasing or
  increasing, and know that the derivative is zero at a minimum in the
  interior of the domain if the function is differentiable there
* differentiate power functions with a negative exponent, for example $1/x$
* use the natural logarithm to solve an exponential equation for the exponent
* compute the distance between two points in the plane with the Pythagorean
  theorem

In **Python** you should be able to:

* pass a function as an argument to another function, as with `central()`
  from Chapter 7.2
* do element-wise arithmetic with arrays and summarize the result with
  `np.mean()` or `np.sum()`
* select an entire column of a two-dimensional array with `plants[:, 0]`
* generate values with `np.linspace()`, and create an array with `np.zeros()`
  and fill it in a loop
* plot measurements as points with `ax.scatter()` and a model as a line
  with `ax.plot()`

From **physics** you should know the following and be able to use it:

* solve a linear characteristic curve $U = m \cdot F + b$ for the force $F$
* explain why a hot object cools faster the more its temperature differs from
  the ambient temperature

The applications in Chapter 8 (order quantity, cooling, warehouse location and
load cell) are explained where they come up. You do not need any further
background in logistics or measurement technology.

## Prerequisite check

The quiz asks ten questions on the three topics. At the end, you see how many
questions you answered correctly for each topic. Your progress is saved in
your browser. The next time you take the quiz, the questions you got wrong
come first. Click the image to start the quiz, and click the cross in the
upper right corner to close it.

<!-- markdownlint-disable -->
<details class="applet-overlay">
<summary>
<img src="pics/chap08_sec00_quiz_preview.png"
  alt="Preview of the prerequisite check. Click to start the quiz.">
</summary>
<div class="applet-container">
<iframe
  title="Prerequisite check for Chapter 8"
  src="https://gramschs.github.io/thma_anm_assets/interactive/chapter08/chap08_sec00_quiz.html?lang=en"
  width="100%"
  frameborder="0"
  scrolling="auto">
</iframe>
</div>
</details>
<!-- markdownlint-enable -->

## What to review

### Math

```{admonition} Math refresher: minimum, power rule, logarithm, distance
:class: note
If the derivative $f'$ is negative on an interval, $f$ is decreasing there. If
it is positive, $f$ is increasing. If the derivative changes from negative to
positive at a point $x_0$ where $f$ is differentiable, $f$ has a local
**minimum** there, and $f'(x_0) = 0$. At a sharp corner where $f$ is not
differentiable, a minimum can also occur without $f'(x_0) = 0$. We will run
into this in Chapter 8.3.

The power rule also holds for negative exponents. We write $1/x = x^{-1}$ and
get the derivative $-1 \cdot x^{-2} = -1/x^2$. You can find the derivatives of
other functions in the
[table of derivatives](https://en.wikipedia.org/wiki/Derivative#Rules_for_basic_functions).

The natural logarithm $\ln$ is the inverse function of the exponential
function, so $\ln(e^a) = a$. This lets us solve an equation such as
$e^{-0.05\,t} = 0.25$ for $t$. Taking the logarithm of both sides gives
$-0.05\,t = \ln 0.25$. Since $\ln 0.25 = -\ln 4 \approx -1.386$, we get

$$t = \frac{-1.386}{-0.05} \approx 27.7.$$

In Python, `np.exp()` computes the exponential function and `np.log()` the
natural logarithm.

The distance between the points $(x_1, y_1)$ and $(x_2, y_2)$ follows from the
Pythagorean theorem:

$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}.$$
```

### Python

All the tools you need came up in earlier chapters. Go back to whatever gave
you trouble in the quiz:

* passing a function as an argument, `central()`: section "How accurate is the
  difference quotient?" in [Chapter 7.2](../chapter07/chapter07_sec02.md)
* computing element-wise, `np.mean()` and `np.linspace()`:
  [Chapter 2.1](../chapter02/chapter02_sec01.md)
* matrices and two-dimensional arrays: section "How do we write a system of
  equations as a matrix?" in [Chapter 3.1](../chapter03/chapter03_sec01.md)
* filling and selecting an entire column with `[:, 0]`: section "Where is the
  obstacle in the warehouse?" in [Chapter 6.1](../chapter06/chapter06_sec01.md)
* creating an array with `np.zeros()` and filling it in a loop:
  [Chapter 7.1](../chapter07/chapter07_sec01.md)
* measured points and a model curve in one plot: section "Measured points
  with scatter and uncertainty" in [Chapter 2.3](../chapter02/chapter02_sec03.md)
* everything at a glance: [Python Cheat Sheet](../chapter01/chapter01_sec06.md)

### Physics

```{admonition} Physics refresher: characteristic curve and cooling
:class: note
Many sensors have a linear **characteristic curve** $U = m \cdot F + b$. The
slope $m$ is called the sensitivity, and the intercept $b$ the zero offset.
To get the force from a measured voltage, we solve for $F$:

$$F = \frac{U - b}{m}.$$

The larger the temperature difference, the more heat a hot part gives off to
its surroundings. That is why its temperature drops quickly at first and then
more and more slowly. If the ambient temperature is constant and there is no
additional cooling, the part's temperature approaches the ambient temperature
but never drops below it. You will learn the law behind this in Chapter 8.2.
```
