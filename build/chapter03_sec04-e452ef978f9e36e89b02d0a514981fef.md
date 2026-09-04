---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.4 Wie viel bringt eine dickere Dämmung?

In Kapitel 3.3 haben wir die Temperaturen und den Wärmestrom in einer
dreischichtigen Wand berechnet. In diesem Kapitel erweitern wir die Wand um
eine Dämmschicht und untersuchen mit einer Parameterstudie, wie stark der
Wärmestrom sinkt, wenn wir die Dämmung verstärken. Bearbeiten Sie die
Teilaufgaben möglichst zu zweit und der Reihe nach.

````{admonition} Projekt: Parameterstudie zur Dämmstärke (✩✩)
:class: tip
Eine Außenwand besteht aus vier Schichten. Innen herrscht
$T_{LA} = 293\,\text{K}$ (20 °C), außen $T_{DR} = 263\,\text{K}$ (−10 °C).

| Schicht | Bauteil | $R$ in K/W |
| --- | --- | --- |
| A | Innenputz | 0.04 |
| B | Mauerwerk | 0.5 |
| C | Dämmung | $R_C$ (variabel) |
| D | Außenputz | 0.04 |

Die Unbekannten sind die drei Grenzflächentemperaturen $T_{AB}$, $T_{BC}$,
$T_{CD}$ und der Wärmestrom $Q$. Wie in Kapitel 3.3 gilt für jede Schicht
$Q = \Delta T_i / R_i$.
````

```{admonition} Teil 1: Das Gleichungssystem aufstellen
:class: tip
Formen Sie die vier Schichtgleichungen so um, dass alle Unbekannten links
stehen (multiplizieren Sie jede mit ihrem $R_i$). Schreiben Sie das Ergebnis
als Matrixgleichung $\mathbf{A} \cdot \vec{x} = \vec{b}$ mit
$\vec{x} = (T_{AB},\ T_{BC},\ T_{CD},\ Q)^\top$. Die Matrix hat dieselbe
Struktur wie in Kapitel 3.3, nur mit einer Zeile und einer Spalte mehr.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
Die umgeformten Gleichungen lauten:

$$T_{AB} + R_A Q = T_{LA}$$
$$-T_{AB} + T_{BC} + R_B Q = 0$$
$$-T_{BC} + T_{CD} + R_C Q = 0$$
$$-T_{CD} + R_D Q = -T_{DR}$$

Daraus die Matrixform:

$$\begin{pmatrix}
+1 &  0 &  0 & R_A \\
-1 & +1 &  0 & R_B \\
 0 & -1 & +1 & R_C \\
 0 &  0 & -1 & R_D
\end{pmatrix}
\cdot
\begin{pmatrix} T_{AB} \\ T_{BC} \\ T_{CD} \\ Q \end{pmatrix}
=
\begin{pmatrix} T_{LA} \\ 0 \\ 0 \\ -T_{DR} \end{pmatrix}$$
````

```{admonition} Teil 2: Für eine feste Dämmung lösen
:class: tip
Legen Sie `A` und `b` für $R_C = 1.0\,\text{K/W}$ als NumPy-Arrays an. Prüfen
Sie die Determinante, lösen Sie mit `np.linalg.solve` und geben Sie die drei
Grenzflächentemperaturen (in °C) und den Wärmestrom aus. Sichern Sie das
Ergebnis mit einer Probe ab.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
import numpy as np

R_A = 0.04
R_B = 0.5
R_C = 1.0
R_D = 0.04
T_LA = 293.0
T_DR = 263.0

A = np.array([
    [+1.0,  0.0,  0.0, R_A],
    [-1.0, +1.0,  0.0, R_B],
    [ 0.0, -1.0, +1.0, R_C],
    [ 0.0,  0.0, -1.0, R_D],
])
b = np.array([T_LA, 0.0, 0.0, -T_DR])

print(f'Determinante: {np.linalg.det(A):.4f}')

x = np.linalg.solve(A, b)
T_AB, T_BC, T_CD, Q = x

print(f'T_AB = {T_AB - 273.15:.1f} °C')
print(f'T_BC = {T_BC - 273.15:.1f} °C')
print(f'T_CD = {T_CD - 273.15:.1f} °C')
print(f'Q    = {Q:.2f} W')
print('Probe bestanden:', np.allclose(A @ x, b))
```
Mit $R_C = 1.0$ K/W ergibt sich ein Wärmestrom von rund 19.0 W. Die Temperatur
fällt von 20 °C innen über den Innenputz kaum merklich auf 19.1 °C, dann über
das Mauerwerk auf 9.6 °C und schließlich innerhalb der Dämmung steil auf
−9.4 °C. Fast die gesamte Temperaturdifferenz liegt über der Dämmschicht.
````

````{admonition} Teil 3: Parameterstudie und Diagramm
:class: tip
Untersuchen Sie, wie der Wärmestrom von der Dämmstärke abhängt. Variieren Sie
$R_C$ mit

```python
r_c_werte = np.linspace(0.0, 3.0, 31)
```

Lösen Sie für jeden Wert das Gleichungssystem, speichern Sie den Wärmestrom in
einem Array `q_werte` und stellen Sie `q_werte` über `r_c_werte` als Linienplot
dar (Achsenbeschriftung, Titel, Gitter).
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

R_A, R_B, R_D = 0.04, 0.5, 0.04
T_LA, T_DR = 293.0, 263.0

r_c_werte = np.linspace(0.0, 3.0, 31)
q_werte = np.zeros(31)

for i, r_c in enumerate(r_c_werte):
    A = np.array([
        [+1.0,  0.0,  0.0, R_A],
        [-1.0, +1.0,  0.0, R_B],
        [ 0.0, -1.0, +1.0, r_c],
        [ 0.0,  0.0, -1.0, R_D],
    ])
    b = np.array([T_LA, 0.0, 0.0, -T_DR])
    x = np.linalg.solve(A, b)
    q_werte[i] = x[3]

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(r_c_werte, q_werte)
ax.set_xlabel('Wärmewiderstand der Dämmung in K/W')
ax.set_ylabel('Wärmestrom in W')
ax.set_title('Wärmestrom in Abhängigkeit von der Dämmstärke')
ax.grid(True)
plt.show()
```
Für jeden Wert von $R_C$ lösen wir ein eigenes Gleichungssystem. Nur der eine
Matrixeintrag in Zeile 3, Spalte 4 ändert sich, alles andere bleibt gleich.
````

```{admonition} Teil 4: Das Diagramm auswerten
:class: tip
Beantworten Sie in eigenen Worten:

1. Wie verändert sich der Wärmestrom, wenn $R_C$ von 0 auf 0.5 K/W steigt, und
   wie, wenn es von 2.5 auf 3.0 K/W steigt?
2. Was bedeutet die Form der Kurve für die Frage, ob sich eine immer dickere
   Dämmung lohnt?
```

````{admonition} Lösung Teil 4
:class: tip
:class: dropdown
1. Am Anfang bringt zusätzliche Dämmung viel: Von $R_C = 0$ bis $R_C = 0.5$
   K/W fällt der Wärmestrom von rund 52 W auf rund 28 W. Am Ende bringt sie
   wenig: Von $R_C = 2.5$ bis $R_C = 3.0$ K/W sinkt er nur noch von etwa
   9.7 W auf 8.4 W.
2. Die Kurve fällt zuerst steil und wird dann immer flacher. Der Nutzen jeder
   weiteren Dämmschicht nimmt ab. Ab einem gewissen Punkt steht der zusätzliche
   Materialaufwand in keinem Verhältnis mehr zur eingesparten Wärme. Das nennt
   man den **abnehmenden Grenznutzen** der Dämmung.
````

````{admonition} Zusatzaufgabe: Halbierung des Wärmestroms (✩✩✩)
:class: tip
Bestimmen Sie aus der Parameterstudie, bei welchem $R_C$ der Wärmestrom auf die
Hälfte des Wertes ohne Dämmung ($R_C = 0$) gesunken ist.

1. Der Wert ohne Dämmung steht in `q_werte[0]`. Bilden Sie das Ziel
   `q_ziel = q_werte[0] / 2`.
2. Finden Sie den Index des `q_werte`-Eintrags, der `q_ziel` am nächsten liegt,
   mit `np.argmin(np.abs(q_werte - q_ziel))`.
3. Geben Sie das zugehörige $R_C$ aus und markieren Sie den Punkt im Diagramm
   aus Teil 3 mit einem zweiten `ax.scatter()`-Aufruf.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Zusatzaufgabe
:class: tip
:class: dropdown
```python
q_ziel = q_werte[0] / 2
i_halb = np.argmin(np.abs(q_werte - q_ziel))
r_c_halb = r_c_werte[i_halb]

print(f'Wärmestrom ohne Dämmung: {q_werte[0]:.1f} W')
print(f'Halber Wärmestrom:       {q_ziel:.1f} W')
print(f'erreicht bei R_C = {r_c_halb:.2f} K/W')

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(r_c_werte, q_werte, label='Wärmestrom')
ax.scatter(r_c_halb, q_werte[i_halb], color='red', zorder=5,
           label='halber Wärmestrom')
ax.set_xlabel('Wärmewiderstand der Dämmung in K/W')
ax.set_ylabel('Wärmestrom in W')
ax.set_title('Halbierung des Wärmestroms')
ax.legend()
ax.grid(True)
plt.show()
```
Der Wärmestrom ohne Dämmung beträgt rund 52 W. Die Hälfte davon, rund 26 W,
wird schon bei einer Dämmung mit $R_C \approx 0.6$ K/W erreicht. Um ihn noch
einmal zu halbieren, bräuchte man deutlich mehr als das Doppelte an
Dämmwiderstand, was wieder den abnehmenden Grenznutzen zeigt.
````
