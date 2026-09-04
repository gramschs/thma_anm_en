---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Exkurs: Modellierung einer Messbrücke

Dieses Kapitel ist ein optionaler Exkurs. Es zeigt an einer elektrischen
Schaltung, dass der Weg von den physikalischen Gleichungen zur Matrix immer
derselbe ist, und es führt mit dem **Rang** das allgemeine Kriterium für die
Lösbarkeit eines Gleichungssystems ein.

In Kapitel 3.3 haben wir ein Gleichungssystem aus Energiebilanzen aufgestellt.
Für elektrische Schaltungen nutzen wir stattdessen die **Kirchhoffschen
Regeln**. Als Beispiel modellieren wir eine **Wheatstone-Brücke**: Drei
Widerstände sind bekannte Referenzwiderstände, der vierte, $R_4$, ist ein
Messwiderstand, dessen Wert sich durch eine physikalische Einwirkung ändert,
zum Beispiel durch Dehnung bei einem Dehnungsmessstreifen. Stehen alle vier
Widerstände in einem bestimmten Verhältnis, ist der Querstrom $I$ durch den
Brückenwiderstand $R_B$ null, die Brücke ist **abgeglichen**. Jede Abweichung
erzeugt einen messbaren Strom.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können die Kirchhoffsche Knoten- und Maschenregel in ein LGS
  $\mathbf{A} \cdot \vec{x} = \vec{b}$ überführen.
* [ ] Sie können mit `np.linalg.matrix_rank` den Rang einer Matrix bestimmen
  und daraus ablesen, ob ein LGS genau eine, keine oder unendlich viele
  Lösungen hat.
* [ ] Sie können eine Parameterstudie über einen Widerstand durchführen und
  den Abgleichpunkt der Brücke bestimmen.
```

## Von den Kirchhoffschen Regeln zum Gleichungssystem

```{figure} pics/wheatstone_bruecke.svg
:alt: Wheatstone-Brückenschaltung mit eingezeichneten Stromrichtungen
:align: center
:width: 75%

Wheatstone-Brücke mit den vier Widerständen $R_1, R_2, R_3, R_4$, dem
Brückenwiderstand $R_B$ und der Spannungsquelle $U_0$. Die Pfeile geben die
angenommenen Zählrichtungen der sechs Ströme an.
(Quelle: eigene Abbildung; Lizenz [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0))
```

Die Brücke hat sechs unbekannte Ströme:
$\vec{x} = (I_0,\ I_1,\ I_2,\ I_3,\ I_4,\ I)^\top$. Wir brauchen also sechs
Gleichungen.

Die **Knotenregel** (Ladungserhaltung) sagt: An jedem Knoten ist die Summe der
zufließenden gleich der Summe der abfließenden Ströme. Die drei Knoten liefern:

$$I_0 - I_1 - I_3 = 0 \qquad
I_1 - I_2 - I = 0 \qquad
I_3 + I - I_4 = 0$$

Die **Maschenregel** (Energieerhaltung) sagt: Entlang einer geschlossenen
Masche ist die Summe der Spannungsabfälle $R \cdot I$ gleich der
Quellenspannung. Die zwei äußeren Maschen und die Quermasche liefern:

$$R_1 I_1 + R_2 I_2 = U_0 \qquad
R_3 I_3 + R_4 I_4 = U_0 \qquad
R_1 I_1 - R_3 I_3 - R_B I = 0$$

Diese sechs Gleichungen setzen wir in eine Matrix um. Wir verpacken das gleich
in eine Funktion, damit wir $R_4$ später leicht variieren können.

```{code-cell} python
import numpy as np

R1 = 100.0   # Ohm
R2 = 100.0   # Ohm
R3 = 100.0   # Ohm
RB = 10.0    # Ohm (Brückenwiderstand)
U0 = 10.0    # V

def loese_bruecke(R4):
    """Löst das 6x6-Gleichungssystem der Wheatstone-Brücke.

    R4: Messwiderstand in Ohm
    Rückgabe: Lösungsvektor [I0, I1, I2, I3, I4, I] in Ampere
    """
    A = np.array([
        [+1.0, -1.0,  0.0, -1.0,  0.0,  0.0],   # Knoten 1
        [ 0.0, +1.0, -1.0,  0.0,  0.0, -1.0],   # Knoten 2
        [ 0.0,  0.0,  0.0, +1.0, -1.0, +1.0],   # Knoten 3
        [ 0.0,   R1,   R2,  0.0,  0.0,  0.0],   # Masche 1
        [ 0.0,  0.0,  0.0,   R3,   R4,  0.0],   # Masche 2
        [ 0.0,   R1,  0.0,  -R3,  0.0,  -RB],   # Quermasche
    ])
    b = np.array([0.0, 0.0, 0.0, U0, U0, 0.0])
    return np.linalg.solve(A, b)

x = loese_bruecke(R4=200.0)
I0, I1, I2, I3, I4, I = x

print(f'Gesamtstrom I0 = {I0 * 1000:.2f} mA')
print(f'Querstrom   I  = {I * 1000:.4f} mA')
```

Bei $R_4 = 200\,\Omega$ fließt ein Querstrom von rund −15.6 mA. Das negative
Vorzeichen sagt, dass der Strom entgegen der angenommenen Zählpfeilrichtung
fließt.

```{admonition} Mini-Übung (✩)
:class: tip
1. Rufen Sie `loese_bruecke(R4=50.0)` auf und geben Sie den Querstrom aus.
2. Beantworten Sie ohne weiteren Code: Bei $R_4 = 200\,\Omega$ ist der
   Querstrom negativ, bei $R_4 = 50\,\Omega$ positiv. Was passiert
   offenbar bei einem Wert dazwischen, und was bedeutet das für die
   Brücke?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
x = loese_bruecke(R4=50.0)
print(f'Querstrom I = {x[5] * 1000:.4f} mA')
```
Bei $R_4 = 50\,\Omega$ ist der Querstrom mit rund +22.7 mA positiv, bei
$R_4 = 200\,\Omega$ war er negativ. Irgendwo dazwischen wechselt er das
Vorzeichen und ist dabei null. An diesem Wert von $R_4$ ist die Brücke
abgeglichen. Diesen Punkt bestimmen wir weiter unten genau.
````

## Wann hat ein LGS keine eindeutige Lösung? Der Rang

Für die sechs unbekannten Ströme haben wir genau sechs Gleichungen genommen:
drei Knoten und drei Maschen. *Was wäre passiert, wenn wir eine weitere
Maschengleichung dazugenommen hätten?* Sie wäre keine neue Information gewesen,
sondern eine Kombination der vorhandenen. Das Gleichungssystem hätte dann mehr
Zeilen als Unbekannte gehabt, ohne besser bestimmt zu sein.

Wie viele Gleichungen wirklich unabhängige Information tragen, misst der
**Rang** einer Matrix. In Kapitel 3.1 haben wir die Lösbarkeit über die
Determinante geprüft. Der Rang ist das allgemeinere Kriterium: Er ist auch für
nicht-quadratische Matrizen definiert und sagt zusätzlich, ob ein nicht
eindeutig lösbares System *keine* oder *unendlich viele* Lösungen hat.

Dafür brauchen wir neben $\mathbf{A}$ auch die **erweiterte
Koeffizientenmatrix** $[\mathbf{A} \mid \vec{b}]$: die Matrix $\mathbf{A}$ mit
$\vec{b}$ als zusätzlicher Spalte. In NumPy hängt `np.column_stack` sie an.

```{code-cell} python
# Ein eindeutig lösbares System
A = np.array([
    [2.0, 1.0, 1.0],
    [1.0, 3.0, 1.0],
    [1.0, 1.0, 4.0],
])
b = np.array([1.0, 2.0, 3.0])

Ab = np.column_stack((A, b))

n = A.shape[1]   # Anzahl Unbekannte
print('Rang von A:      ', np.linalg.matrix_rank(A))
print('Rang von [A | b]:', np.linalg.matrix_rank(Ab))
print('Anzahl Unbekannte:', n)
```

Für ein System mit $n$ Unbekannten gelten die drei Fälle:

| $\text{rang}(\mathbf{A})$ | $\text{rang}([\mathbf{A} \mid \vec{b}])$ | Lösbarkeit |
| :---: | :---: | :--- |
| $= n$ | $= n$ | genau eine Lösung |
| $< n$ | $= \text{rang}(\mathbf{A})$ | unendlich viele Lösungen |
| $< n$ | $> \text{rang}(\mathbf{A})$ | keine Lösung |

Wir sehen uns die beiden nicht eindeutigen Fälle an einer Matrix an, deren
zweite Zeile das Doppelte der ersten ist:

```{code-cell} python
A = np.array([
    [1.0, 2.0, 1.0],
    [2.0, 4.0, 2.0],   # = 2 * Zeile 1, keine neue Information
    [0.0, 1.0, 1.0],
])

b_widerspruch = np.array([3.0, 7.0, 2.0])   # b[1] müsste 2*b[0] = 6 sein, ist aber 7
b_vertraeglich = np.array([3.0, 6.0, 2.0])  # b[1] = 6 = 2*b[0], passt zu Zeile 2 = 2*Zeile 1

print('rang A:', np.linalg.matrix_rank(A))
print('mit b_widerspruch:  rang [A|b] =',
      np.linalg.matrix_rank(np.column_stack((A, b_widerspruch))))
print('mit b_vertraeglich: rang [A|b] =',
      np.linalg.matrix_rank(np.column_stack((A, b_vertraeglich))))
```

Bei `b_widerspruch` steigt der Rang der erweiterten Matrix auf 3, während
$\text{rang}(\mathbf{A}) = 2$ bleibt: Das System hat **keine Lösung**, die
Gleichungen widersprechen sich. Bei `b_vertraeglich` bleibt der Rang bei 2: Das
System hat **unendlich viele Lösungen**, eine Unbekannte bleibt frei wählbar.
Denselben Widerspruchsfall haben wir in der Zusatzaufgabe von Kapitel 3.2
gesehen: ein Träger ohne waagerechte Fesselung.

```{admonition} Mini-Übung (✩)
:class: tip
Gegeben ist

$$\mathbf{A} = \begin{pmatrix} 1 & 1 & 2 \\ 3 & 3 & 6 \\ 1 & 0 & 1 \end{pmatrix},
\qquad \vec{b} = \begin{pmatrix} 4 \\ 12 \\ 1 \end{pmatrix}.$$

1. Beantworten Sie ohne Code: Welche zwei Zeilen von $\mathbf{A}$ sind
   voneinander abhängig?
2. Bestimmen Sie $\text{rang}(\mathbf{A})$ und
   $\text{rang}([\mathbf{A} \mid \vec{b}])$ mit `np.linalg.matrix_rank`. Welcher
   der drei Fälle liegt vor?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([
    [1.0, 1.0, 2.0],
    [3.0, 3.0, 6.0],
    [1.0, 0.0, 1.0],
])
b = np.array([4.0, 12.0, 1.0])

n = A.shape[1]
rang_A = np.linalg.matrix_rank(A)
rang_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))

print(f'rang A = {rang_A}, rang [A|b] = {rang_Ab}, n = {n}')
```
Ausgabe: `rang A = 2, rang [A|b] = 2, n = 3`.

Die zweite Zeile von $\mathbf{A}$ ist das Dreifache der ersten. Da auch
$b[1] = 3 \cdot b[0]$ gilt, widerspricht sich nichts:
$\text{rang}(\mathbf{A}) = \text{rang}([\mathbf{A} \mid \vec{b}]) = 2 < 3$. Das
System hat unendlich viele Lösungen.
````

## Parameterstudie: den Abgleichpunkt finden

Jetzt variieren wir $R_4$ systematisch und suchen den Wert, bei dem der
Querstrom null wird. Für jeden $R_4$-Wert lösen wir ein eigenes
Gleichungssystem.

```{code-cell} python
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

r4_werte = np.linspace(10.0, 300.0, 500)
i_werte = np.zeros(500)
p_werte = np.zeros(500)

for k, r4 in enumerate(r4_werte):
    strom = loese_bruecke(r4)[5]
    i_werte[k] = strom
    p_werte[k] = RB * strom**2   # Verlustleistung P = R_B * I^2

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(7, 7), sharex=True)

ax[0].plot(r4_werte, i_werte * 1000)
ax[0].axhline(0, color='gray', linestyle='dashed', linewidth=1)
ax[0].set_ylabel('Querstrom in mA')
ax[0].set_title('Wheatstone-Brücke: Querstrom und Verlustleistung')
ax[0].grid(True)

ax[1].plot(r4_werte, p_werte * 1000)
ax[1].set_xlabel('Messwiderstand R4 in Ohm')
ax[1].set_ylabel('Verlustleistung in mW')
ax[1].grid(True)

plt.tight_layout()
plt.show()
```

Der Querstrom kreuzt die Nulllinie, die Verlustleistung berührt dort die
x-Achse. Den Nulldurchgang finden wir mit `np.argmin` über den Betrag und
vergleichen ihn mit der bekannten Abgleichbedingung
$R_4^\ast = R_2 \cdot R_3 / R_1$.

```{code-cell} python
k_null = np.argmin(np.abs(i_werte))
r4_abgleich = r4_werte[k_null]

r4_analytisch = R2 * R3 / R1

print(f'numerisch:   R4* = {r4_abgleich:.1f} Ohm')
print(f'analytisch:  R4* = {r4_analytisch:.1f} Ohm')
```

Der numerische Wert weicht leicht vom analytischen ab, weil `np.linspace` die
Nullstelle nicht exakt trifft. Ein feineres Gitter verkleinert die Abweichung.

```{admonition} Mini-Übung (✩)
:class: tip
1. Erhöhen Sie in der Parameterstudie die Anzahl der Stützstellen von 500 auf
   2000. Wie ändert sich der numerisch gefundene Abgleichwert $R_4^\ast$?
2. Beantworten Sie ohne Code: Warum berührt die Verlustleistung an der
   Nullstelle die x-Achse, statt sie zu kreuzen?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
r4_fein = np.linspace(10.0, 300.0, 2000)
i_fein = np.array([loese_bruecke(r4)[5] for r4 in r4_fein])
print(f'R4* mit 2000 Stützstellen: {r4_fein[np.argmin(np.abs(i_fein))]:.2f} Ohm')
```
Mit mehr Stützstellen liegt der gefundene Wert näher an den analytischen
100 Ohm. Die Verlustleistung $P = R_B \cdot I^2$ enthält den Strom im Quadrat.
Ein Quadrat ist nie negativ, daher kann $P$ die x-Achse nicht kreuzen. An der
Nullstelle des Stroms wird $P$ genau null und berührt die Achse.
````

## Zusammenfassung

Das Modell der Wheatstone-Brücke besteht aus sechs Kirchhoff-Gleichungen für
sechs unbekannte Ströme. Der **Rang** von $\mathbf{A}$ und der erweiterten
Matrix $[\mathbf{A} \mid \vec{b}]$ sagt, ob ein Gleichungssystem genau eine,
keine oder unendlich viele Lösungen hat, und ist damit allgemeiner als der
Determinanten-Test. Mit einer Parameterstudie über $R_4$ und `np.argmin` haben
wir den Abgleichpunkt der Brücke bestimmt und mit der analytischen Formel
bestätigt.

Der zweite Exkurs in Kapitel 3.7 wechselt die Perspektive: Dort untersuchen
wir, wie die Rechenzeit von `np.linalg.solve` mit der Größe des
Gleichungssystems wächst.
