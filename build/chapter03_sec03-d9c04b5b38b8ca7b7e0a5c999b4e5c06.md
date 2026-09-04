---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.3 Wärmeübertragung in einer Mehrschichtwand

In Kapitel 3.1 haben wir lineare Gleichungssysteme mit NumPy gelöst, in
Kapitel 3.2 die Auflagerkräfte eines Trägers berechnet. Beide Male haben wir
die Gleichungen von Hand aufgestellt. Jetzt wenden wir dasselbe Werkzeug auf
ein klassisches Maschinenbau-Problem an: eine Außenwand aus drei Schichten mit
unterschiedlichen Wärmedurchgangswiderständen. *Wie hoch ist die Temperatur an
den Grenzflächen, und wie groß ist der Wärmestrom?*

Wir werden sehen, dass der Weg von den physikalischen Gleichungen zur Matrix
immer gleich ist: alle Unbekannten auf die linke Seite, alle bekannten Größen
auf die rechte.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können physikalische Bilanzgleichungen so umformen, dass alle
  Unbekannten auf der linken Seite stehen.
* [ ] Sie können die Koeffizientenmatrix $\mathbf{A}$ und den Vektor $\vec{b}$
  aus den umgeformten Gleichungen ablesen.
* [ ] Sie können das LGS mit `np.linalg.solve` lösen und das Ergebnis
  physikalisch deuten, auch ein negatives Vorzeichen.
```

## Das physikalische Modell

Wir betrachten eine Wand aus drei Schichten A, B, C mit den thermischen
Widerständen $R_A$, $R_B$, $R_C$ in K/W. Links herrscht die Temperatur
$T_{LA}$, rechts $T_{CR}$.

```{figure} pics/waermeuebertragung_mehrschichtwand.svg
:alt: Querschnitt einer dreischichtigen Wand mit Temperaturprofil und Wärmestrom
:align: center
:label: fig_waermeuebertragung_mehrschichtwand

Temperaturprofil einer Mehrschichtwand im stationären Zustand (schematische
Darstellung bei gleicher geometrischer Schichtdicke). Da der Wärmestrom durch
alle Schichten gleich ist, ist die Steigung des Temperaturprofils proportional
zum thermischen Widerstand der jeweiligen Schicht, in Schicht C am steilsten, in
Schicht B am flachsten. (Quelle: eigene Abbildung; Lizenz [CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0))
```

Im **stationären Zustand** ist der Wärmestrom $Q$ durch alle Schichten gleich
groß. Das **Wärmeübertragungsgesetz**, analog zum Ohmschen Gesetz, lautet für
jede Schicht

$$Q = \frac{\Delta T_i}{R_i},$$

wobei $\Delta T_i$ die Temperaturdifferenz über die Schicht ist. Mit den beiden
unbekannten Grenzflächentemperaturen $T_{AB}$, $T_{BC}$ und dem unbekannten
Wärmestrom $Q$ liefert das drei Gleichungen:

$$\frac{T_{LA} - T_{AB}}{R_A} = Q \qquad (1)$$

$$\frac{T_{AB} - T_{BC}}{R_B} = Q \qquad (2)$$

$$\frac{T_{BC} - T_{CR}}{R_C} = Q \qquad (3)$$

```{admonition} Mini-Übung (✩)
:class: tip
1. Beantworten Sie ohne Code: Warum ist der Wärmestrom $Q$ im stationären
   Zustand in allen drei Schichten gleich groß? Was würde es bedeuten, wenn
   $Q$ in Schicht B größer wäre als in Schicht A?
2. Für eine einzelne Wand ohne Zwischenschichten gilt
   $Q = (T_{LA} - T_{CR}) / R_\text{gesamt}$ mit
   $R_\text{gesamt} = R_A + R_B + R_C$. Berechnen Sie diesen Wert für
   $R_A = 0.5$, $R_B = 0.3$, $R_C = 0.7$ (alle in K/W), $T_{LA} = 293$ K und
   $T_{CR} = 273$ K.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
R_gesamt = 0.5 + 0.3 + 0.7
Q = (293 - 273) / R_gesamt
print(f'Gesamtwiderstand: {R_gesamt} K/W')
print(f'Wärmestrom Q:     {Q:.4f} W')
```
Der Wärmestrom ist überall gleich, weil sich im stationären Zustand nirgends
Wärme ansammelt oder verschwindet: Was in eine Schicht hineinfließt, muss auch
wieder herausfließen. Wäre $Q$ in Schicht B größer als in Schicht A, würde an
der Grenzfläche A-B laufend Wärme verschwinden, die Temperatur dort würde
sinken, und der Zustand wäre nicht stationär. Der Gesamtwiderstand ist
1.5 K/W, der Wärmestrom rund 13.33 W. Dasselbe Ergebnis liefert gleich auch
das Gleichungssystem.
````

## Von den Gleichungen zur Matrixform

Die drei Gleichungen enthalten die Unbekannten in Brüchen. Wir bringen alle
Unbekannten auf die linke Seite, indem wir jede Gleichung mit $R_i$
multiplizieren und umordnen:

$$T_{AB} + R_A \cdot Q = T_{LA} \qquad (1')$$

$$-T_{AB} + T_{BC} + R_B \cdot Q = 0 \qquad (2')$$

$$-T_{BC} + R_C \cdot Q = -T_{CR} \qquad (3')$$

Jetzt lesen wir die Koeffizientenmatrix zeilenweise ab. Der Lösungsvektor ist
$\vec{x} = (T_{AB},\ T_{BC},\ Q)^\top$:

$$\begin{pmatrix}
+1 &  0 & R_A \\
-1 & +1 & R_B \\
 0 & -1 & R_C
\end{pmatrix}
\cdot
\begin{pmatrix} T_{AB} \\ T_{BC} \\ Q \end{pmatrix}
=
\begin{pmatrix} T_{LA} \\ 0 \\ -T_{CR} \end{pmatrix}$$

Jede umgeformte Gleichung liefert eine Zeile von $\mathbf{A}$ und einen Eintrag
in $\vec{b}$. Der Koeffizient der $j$-ten Unbekannten in der $i$-ten Gleichung
steht in $A_{ij}$. Unbekannte, die in einer Gleichung nicht vorkommen, erhalten
den Koeffizienten 0.

```{admonition} Mini-Übung (✩)
:class: tip
Beantworten Sie ohne Code:

1. In der Koeffizientenmatrix steht in Zeile 2, Spalte 1 der Wert $-1$. Aus
   welcher Gleichung stammt dieser Eintrag, und warum ist er negativ?
2. Warum ist der zweite Eintrag der rechten Seite, $b[1]$, gleich null? Was
   bedeutet das physikalisch?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
1. Der Eintrag $A_{21} = -1$ stammt aus Gleichung (2'), die durch Umformen aus
   $(T_{AB} - T_{BC}) / R_B = Q$ entsteht. Die Temperaturdifferenz über
   Schicht B ist $T_{AB} - T_{BC}$, dort steht $T_{AB}$ mit positivem
   Vorzeichen. Nach dem Multiplizieren mit $R_B$ und dem Sortieren aller
   Unbekannten nach links bleibt $-T_{AB}$ stehen, der Koeffizient ist also
   $-1$.
2. $b[1] = 0$, weil in Gleichung (2') keine bekannte Temperatur auftaucht. Die
   mittlere Schicht grenzt nur an die beiden Grenzflächen, deren Temperaturen
   selbst unbekannt sind. Es gibt für diese Gleichung keine von außen
   vorgegebene Randbedingung.
````

## Implementierung und Lösung

```{code-cell} python
import numpy as np

# gegebene Größen
R_A = 0.5    # thermischer Widerstand Schicht A in K/W
R_B = 0.3    # thermischer Widerstand Schicht B in K/W
R_C = 0.7    # thermischer Widerstand Schicht C in K/W
T_LA = 293.0    # Temperatur linke Seite (innen) in K
T_CR = 273.0    # Temperatur rechte Seite (außen) in K

# Koeffizientenmatrix, Unbekannte x = [T_AB, T_BC, Q]
A = np.array([
    [+1.0,  0.0, R_A],   # Gleichung (1'):  T_AB + R_A*Q = T_LA
    [-1.0, +1.0, R_B],   # Gleichung (2'): -T_AB + T_BC + R_B*Q = 0
    [ 0.0, -1.0, R_C],   # Gleichung (3'): -T_BC + R_C*Q = -T_CR
])
b = np.array([T_LA, 0.0, -T_CR])

# Lösbarkeit prüfen
det_A = np.linalg.det(A)
print(f'Determinante: {det_A:.4f}')

# Lösen
x = np.linalg.solve(A, b)
T_AB, T_BC, Q = x   # Ergebnis in drei Variablen entpacken

print(f'T_AB = {T_AB:.2f} K   (Grenzfläche A-B)')
print(f'T_BC = {T_BC:.2f} K   (Grenzfläche B-C)')
print(f'Q    = {Q:.4f} W   (Wärmestrom)')

print('Probe bestanden:', np.allclose(A @ x, b))
```

Der Wärmestrom $Q$ ist positiv. Das passt zu unserem Ansatz: Die positive
Richtung zeigt von links nach rechts, und die Wärme fließt von der wärmeren
linken Seite ($T_{LA} = 293$ K) zur kälteren rechten Seite ($T_{CR} = 273$ K).
Ein negativer Wert würde bedeuten, dass die Wärme in die andere Richtung
fließt.

Zur Kontrolle berechnen wir die Temperaturdifferenz über jede Schicht. Schicht
C hat den größten Widerstand und sollte daher den größten Temperatursprung
liefern, genauso wie der größte Widerstand in einem Stromkreis den größten
Spannungsabfall erzeugt.

```{code-cell} python
delta_A = T_AB - T_LA
delta_B = T_BC - T_AB
delta_C = T_CR - T_BC

print(f'Temperaturdifferenz Schicht A (R = {R_A} K/W): {delta_A:.2f} K')
print(f'Temperaturdifferenz Schicht B (R = {R_B} K/W): {delta_B:.2f} K')
print(f'Temperaturdifferenz Schicht C (R = {R_C} K/W): {delta_C:.2f} K')
print(f'Summe: {delta_A + delta_B + delta_C:.2f} K '
      f'(muss T_CR - T_LA = {T_CR - T_LA:.1f} K ergeben)')
```

```{admonition} Mini-Übung (✩)
:class: tip
Eine Kühlhauswand hält innen $T_\text{innen} = 268$ K (−5 °C), während außen
$T_\text{außen} = 293$ K (20 °C) herrschen. Die linke Seite ist innen
($T_{LA} = T_\text{innen}$), die rechte außen ($T_{CR} = T_\text{außen}$).

| Schicht | Material | $R$ in K/W |
| --- | --- | --- |
| A | Beton | 0.2 |
| B | Polyurethan-Schaum | 1.8 |
| C | Stahlblech | 0.05 |

1. Beantworten Sie ohne Code: Welche Schicht wird den größten Temperaturabfall
   haben?
2. Legen Sie `A` und `b` mit den neuen Werten an, lösen Sie das System und
   geben Sie $T_{AB}$, $T_{BC}$ und $Q$ aus.
3. Der Wärmestrom kommt negativ heraus. Warum?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

R_A = 0.2
R_B = 1.8
R_C = 0.05
T_LA = 268.0    # innen (kalt)
T_CR = 293.0    # außen (warm)

A = np.array([
    [+1.0,  0.0, R_A],
    [-1.0, +1.0, R_B],
    [ 0.0, -1.0, R_C],
])
b = np.array([T_LA, 0.0, -T_CR])

x = np.linalg.solve(A, b)
T_AB, T_BC, Q = x

print(f'T_AB = {T_AB:.2f} K  ({T_AB - 273.15:.1f} °C)')
print(f'T_BC = {T_BC:.2f} K  ({T_BC - 273.15:.1f} °C)')
print(f'Q    = {Q:.4f} W')
print('Probe bestanden:', np.allclose(A @ x, b))

print(f'Temperaturabfall Schicht A (Beton):  {abs(T_AB - T_LA):.2f} K')
print(f'Temperaturabfall Schicht B (Schaum): {abs(T_BC - T_AB):.2f} K')
print(f'Temperaturabfall Schicht C (Stahl):  {abs(T_CR - T_BC):.2f} K')
```
Den größten Temperaturabfall hat Schicht B, der Polyurethan-Schaum, mit rund
22 K. Ihr thermischer Widerstand ist mit $R_B = 1.8$ K/W bei weitem am
größten. Genau das ist der Sinn einer Wärmedämmung: Sie übernimmt fast die
gesamte Temperaturdifferenz zwischen innen und außen.

Der Wärmestrom ist negativ (rund −12.2 W), weil wir die positive Richtung von
links (innen) nach rechts (außen) gewählt haben, die Wärme aber von der warmen
Außenseite in das kalte Kühlhaus fließt. Betrag und Vorzeichen sind zusammen
korrekt.
````

## Zusammenfassung und Ausblick

Der Weg ist immer derselbe: physikalische Bilanzgleichungen umformen, alle
Unbekannten nach links, alle bekannten Größen nach rechts, dann $\mathbf{A}$
und $\vec{b}$ zeilenweise ablesen. `np.linalg.solve` liefert die Lösung,
`np.allclose` sichert sie ab, und das Vorzeichen des Ergebnisses deuten wir
über die gewählte Richtungskonvention.

Im nächsten Kapitel vertiefen wir dieses Beispiel: Wir erweitern die Wand um
eine vierte Schicht und untersuchen mit einer Parameterstudie, wie stark eine
zusätzliche Dämmung den Wärmestrom senkt.
