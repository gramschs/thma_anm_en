---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Preparation

In Chapters 7.1 and 7.2 we compute derivatives from measured values and from
formulas. For this you need some mathematics, Python and physics that you
already know from earlier semesters and chapters. Before the lecture, use the
quiz on this page to check whether everything is in place. It takes about ten
minutes. For every topic where you make mistakes, you will find below the quiz
what you can review.

## What you should bring along

From **mathematics** you should be able to:

* compute the slope of a straight line through two points
* understand the derivative as a limit: the secant becomes the tangent
* differentiate power functions with the power rule
* calculate with powers of ten

In **Python** you should be able to:

* write a `for` loop with `range` and the index `k`, accessing
  `values[k + 1]`
* create an array with `np.zeros` and fill it in a loop
* write functions with parameters and `return`, use the index `-1` and `len`
* find the index of the smallest or largest value with `np.argmin` and
  `np.argmax`
* draw several plots below each other with `plt.subplots`

From **physics** you should know and be able to:

* distance, velocity and acceleration with their units
* The velocity is the derivative of the distance with respect to time, the
  acceleration is the derivative of the velocity.
* uniformly accelerated motion from rest
* convert between m/s and km/h

You know the AGV as an application example from Chapter 6. You do not need any
further knowledge about automated guided vehicles.

## Prerequisite check

The quiz asks ten questions on the three topics. At the end you see how many
questions per topic you answered correctly. Your progress is stored in your
browser. In the next round, the questions you got wrong come first. Click the
image to start the quiz, and click the cross at the top right to close it.

<!-- markdownlint-disable MD033 -->
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
<!-- markdownlint-enable MD033 -->

## What you can review

### Mathematics

```{admonition} Math refresher: difference quotient, derivative, powers of ten
:class: note
The slope of the secant through the points $(x_1, y_1)$ and $(x_2, y_2)$ is the
**difference quotient**

$$m = \frac{y_2 - y_1}{x_2 - x_1}.$$

If the second point moves closer and closer to the first, the secant becomes
the tangent. Its slope is the **derivative**:

$$f'(x) = \lim_{\Delta x \to 0} \frac{f(x + \Delta x) - f(x)}{\Delta x}.$$

By the power rule, the derivative of $x^n$ is $n\,x^{n-1}$. For example, the
derivative of $0.2\,t^2$ is $0.4\,t$. You can find derivatives of further
functions in the
[table of derivatives](https://en.wikipedia.org/wiki/Derivative#Rules_for_basic_functions).

For powers of ten, $10^a \cdot 10^b = 10^{a+b}$ and $10^a / 10^b = 10^{a-b}$.
The notation `2.1e-03` in Python means $2.1 \cdot 10^{-3} = 0.0021$.
```

### Python

All the tools you need appeared in earlier chapters. Review there whatever did
not work in the quiz:

* loops with `for` and `range`: [Chapter 1.1](../chapter01/chapter01_sec01.md)
* functions with `return`, the index `-1` and `len`:
  [Chapter 1.3](../chapter01/chapter01_sec03.md)
* everything at a glance: [Python Cheat Sheet](../chapter01/chapter01_sec06.md)
* `np.zeros` and other arrays: [Chapter 2.1](../chapter02/chapter02_sec01.md)
* several plots with `plt.subplots`:
  [Chapter 2.3](../chapter02/chapter02_sec03.md)
* `np.argmax`: [Chapter 2.4](../chapter02/chapter02_sec04.md)
* creating an array with `np.zeros` and filling it in a loop, exactly as in
  Chapter 7.1: section "How does the AGV turn along the path?" in
  [Chapter 6.3](../chapter06/chapter06_sec03.md)

### Physics

```{admonition} Physics refresher: distance, velocity, acceleration
:class: note
The **velocity** $v$ is the derivative of the distance $s$ with respect to
time, the **acceleration** $a$ is the derivative of the velocity:

$$v(t) = s'(t), \qquad a(t) = v'(t) = s''(t).$$

We measure distances in m, velocities in m/s and accelerations in
$\text{m/s}^2$. For the conversion, $1\,\text{m/s} = 3.6\,\text{km/h}$.

If a vehicle accelerates uniformly from rest with $a$, then after the time $t$

$$v = a\,t, \qquad s = \frac{a}{2}\,t^2.$$

An AGV that accelerates at $0.4\,\text{m/s}^2$ for $2\,\text{s}$ then moves at
$0.8\,\text{m/s}$ and has covered $0.8\,\text{m}$.
```
