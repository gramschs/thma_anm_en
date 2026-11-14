---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Preparation

In Chapters 7.1 and 7.2 we compute derivatives from measured values and from
formulas. For this you need some math, Python and physics that you know from
earlier semesters and chapters. Before the lecture, take the quiz on this page
to check whether you are up to speed. It takes about ten minutes. For every
topic where you make mistakes, you will find material to review below the
quiz.

## What you should already know

From **math** you should be able to:

* compute the slope of a straight line through two points
* understand the derivative as a limit: the secant becomes the tangent
* differentiate power functions with the power rule
* work with powers of ten

In **Python** you should be able to:

* write a `for` loop with `range()` and the index `k`, accessing
  `values[k + 1]`
* create an array with `np.zeros()` and fill it in a loop
* write functions with parameters and `return`, and use the index `-1` and
  `len()`
* find the index of the smallest or largest value with `np.argmin()` and
  `np.argmax()`
* draw several plots one above the other with `plt.subplots()`

From **physics** you should know the following and be able to use it:

* distance, velocity and acceleration with their units
* When a vehicle drives straight ahead in one direction, its velocity is the
  derivative of the distance with respect to time, and its acceleration is
  the derivative of the velocity.
* uniformly accelerated motion from rest
* converting between m/s and km/h

Our application example, the AGV, is familiar from Chapter 6. You do not need
to know anything else about automated guided vehicles.

## Prerequisite check

The quiz asks ten questions on the three topics. At the end, you see how many
questions you answered correctly for each topic. Your progress is saved in
your browser. The next time you take the quiz, the questions you got wrong
come first. Click the image to start the quiz, and click the cross in the
upper right corner to close it.

<!-- markdownlint-disable -->
<details class="applet-overlay">
<summary>
<img src="pics/chap07_sec00_quiz_preview.png"
  alt="Preview of the prerequisite check. Click to start the quiz.">
</summary>
<div class="applet-container">
<iframe
  src="https://gramschs.github.io/thma_anm_assets/interactive/chapter07/chap07_sec00_quiz.html?lang=en"
  width="100%"
  frameborder="0"
  scrolling="auto">
</iframe>
</div>
</details>
<!-- markdownlint-enable -->

## What to review

### Math

```{admonition} Math refresher: difference quotient, derivative, powers of ten
:class: note
The slope of the secant through the points $(x_1, y_1)$ and $(x_2, y_2)$ is the
**difference quotient**

$$m = \frac{y_2 - y_1}{x_2 - x_1}.$$

If the second point moves closer and closer to the first, the secant becomes
the tangent. Its slope is the **derivative**:

$$f'(x) = \lim_{\Delta x \to 0} \frac{f(x + \Delta x) - f(x)}{\Delta x}.$$

By the power rule, the derivative of $x^n$ is $n\,x^{n-1}$. For example, the
derivative of $0.2\,t^2$ is $0.4\,t$. You can find the derivatives of other
functions in the
[table of derivatives](https://en.wikipedia.org/wiki/Derivative#Rules_for_basic_functions).

For powers of ten, $10^a \cdot 10^b = 10^{a+b}$ and $10^a / 10^b = 10^{a-b}$.
The notation `2.1e-03` in Python means $2.1 \cdot 10^{-3} = 0.0021$.
```

The following applet shows how the secant turns into the tangent for the
parabola $f(x) = x^2 - 2x + 3$ at the point $x_0 = 2$. Use the slider to
decrease $\Delta x$ and watch the secant approach the tangent.

<!-- markdownlint-disable -->
<div class="applet-container applet-750">
<iframe
  src="https://gramschs.github.io/thma_anm_assets/interactive/chapter04/sekante-tangente.html?lang=en"
  width="100%"
  frameborder="0"
  scrolling="no">
</iframe>
</div>
<!-- markdownlint-enable -->

### Python

All the tools you need came up in earlier chapters. Go back to whatever gave
you trouble in the quiz:

* loops with `for` and `range()`: [Chapter 1.1](../chapter01/chapter01_sec01.md)
* functions with `return`, the index `-1` and `len()`:
  [Chapter 1.3](../chapter01/chapter01_sec03.md)
* everything at a glance: [Python Cheat Sheet](../chapter01/chapter01_sec06.md)
* `np.zeros()` and other arrays: [Chapter 2.1](../chapter02/chapter02_sec01.md)
* several plots with `plt.subplots()`:
  [Chapter 2.3](../chapter02/chapter02_sec03.md)
* `np.argmax()`: [Chapter 2.4](../chapter02/chapter02_sec04.md)
* creating an array with `np.zeros()` and filling it in a loop, exactly as in
  Chapter 7.1: section "How does the AGV turn along the path?" in
  [Chapter 6.3](../chapter06/chapter06_sec03.md)

### Physics

```{admonition} Physics refresher: distance, velocity, acceleration
:class: note
When a vehicle drives straight ahead in one direction, its **velocity** $v$ is
the derivative of the distance $s$ traveled with respect to time, and its
**acceleration** $a$ is the derivative of the velocity:

$$v(t) = s'(t), \qquad a(t) = v'(t) = s''(t).$$

We measure distances in m, velocities in m/s and accelerations in
$\text{m/s}^2$. For the conversion, $1\,\text{m/s} = 3.6\,\text{km/h}$.

If a vehicle accelerates uniformly from rest at $a$, then after the time $t$

$$v = a\,t, \qquad s = \frac{a}{2}\,t^2.$$

An AGV that accelerates from rest at $0.4\,\text{m/s}^2$ for $2\,\text{s}$ is
then moving at $0.8\,\text{m/s}$ and has covered $0.8\,\text{m}$.
```
