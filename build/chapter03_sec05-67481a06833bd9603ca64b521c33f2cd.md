---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 3.5 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 3.1 bis 3.4. Rechnen Sie mit gut eineinhalb Stunden
Bearbeitungszeit.

Der Schwierigkeitsgrad steht im Titel jeder Aufgabe:

* ✩ Verständnis: Code und Ausgaben vorhersagen und erklären (ca. 5 min)
* ✩✩ Anwendung: eigenen Code schreiben und Ergebnisse interpretieren (ca. 10 min)
* ✩✩✩ Mini-Projekt: mehrere Konzepte des Parts kombinieren (ca. 30 min)

````{admonition} Aufgabe 3.1 (✩)
:class: tip
Gegeben ist folgender Code:

```python
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)
b = np.array([1.0, 2.0, 3.0])
```

Notieren Sie Ihre Vermutung, bevor Sie den Code ausführen.

1. Was gibt `A.shape` zurück?
2. Was gibt `A[2, 0]` zurück?
3. Was gibt `A[1, 2]` zurück?
4. Schauen Sie sich die drei Zeilen von `A` genau an. Wird `np.linalg.det(A)`
   nahe bei null liegen? Begründen Sie.
5. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)

print(A.shape)
print(A[2, 0])
print(A[1, 2])
print(np.linalg.det(A))
```
Ausgabe:
```
(3, 3)
7.0
6.0
-9.51619735392994e-16
```
`A.shape` ist `(3, 3)`, also drei Zeilen und drei Spalten. `A[2, 0]` ist der
Wert in Zeile 2, Spalte 0, also `7.0`. `A[1, 2]` steht in Zeile 1, Spalte 2 und
ist `6.0`. Die Determinante ist im Rechner eine winzige Zahl nahe null, weil
die dritte Zeile eine Kombination der ersten beiden ist:
$[7,8,9] = 2 \cdot [4,5,6] - [1,2,3]$. Das System hat keine eindeutige Lösung.
````

````{admonition} Aufgabe 3.2 (✩)
:class: tip
Gegeben ist folgender Code:

```python
import numpy as np

A = np.array([[2, 1], [5, 3]], dtype=float)
b = np.array([8.0, 19.0])
```

Notieren Sie Ihre Vermutung, bevor Sie den Code ausführen.

1. Berechnen Sie die Determinante im Kopf: $\det = 2 \cdot 3 - 1 \cdot 5$. Hat
   das System eine eindeutige Lösung?
2. Was gibt `np.linalg.solve(A, b)` zurück?
3. Setzen Sie Ihre Lösung von Hand in beide Gleichungen ein und prüfen Sie,
   dass sie stimmt.
4. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([[2, 1], [5, 3]], dtype=float)
b = np.array([8.0, 19.0])

print(np.linalg.det(A))
x = np.linalg.solve(A, b)
print(x)
print('Probe:', np.allclose(A @ x, b))
```
Ausgabe:
```
1.0000000000000002
[ 5. -2.]
Probe: True
```
Die Determinante ist $2 \cdot 3 - 1 \cdot 5 = 1$, also ungleich null: genau eine
Lösung. `np.linalg.solve` gibt $x = (5,\ -2)$ zurück. Die Probe von Hand:
$2 \cdot 5 + 1 \cdot (-2) = 8$ und $5 \cdot 5 + 3 \cdot (-2) = 19$, beide
Gleichungen stimmen.
````

````{admonition} Aufgabe 3.3 (✩)
:class: tip
Gegeben ist folgender Code:

```python
import numpy as np

A = np.array([[2, 4], [1, 2]], dtype=float)
b = np.array([10.0, 3.0])

try:
    x = np.linalg.solve(A, b)
    print('Lösung:', x)
except np.linalg.LinAlgError:
    print('Matrix ist singulär.')
```

Notieren Sie Ihre Vermutung, bevor Sie den Code ausführen.

1. Berechnen Sie `np.linalg.det(A)` im Kopf. Was fällt an den beiden Zeilen
   von `A` auf?
2. Wird der `try`-Zweig oder der `except`-Zweig ausgeführt? Was wird
   ausgegeben?
3. Führen Sie den Code aus und überprüfen Sie Ihre Vorhersagen.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

A = np.array([[2, 4], [1, 2]], dtype=float)
b = np.array([10.0, 3.0])

print('Determinante:', np.linalg.det(A))

try:
    x = np.linalg.solve(A, b)
    print('Lösung:', x)
except np.linalg.LinAlgError:
    print('Matrix ist singulär.')
```
Ausgabe:
```
Determinante: 0.0
Matrix ist singulär.
```
Die zweite Zeile ist genau die Hälfte der ersten ($[1, 2] = 0.5 \cdot [2, 4]$),
sie enthält also keine neue Information. Die Determinante ist null,
`np.linalg.solve` wirft einen `LinAlgError`, und der `except`-Zweig gibt
`Matrix ist singulär.` aus.
````

```{admonition} Aufgabe 3.4 (✩✩)
:class: tip
Drei Personen teilen sich die Kosten für einen Haushalt. In drei Monaten
zahlen sie unterschiedliche Anteile für Miete (M), Strom (S) und Internet (I),
und der Gesamtbetrag ist bekannt:

| Monat | Anteil M | Anteil S | Anteil I | Gesamt in Euro |
| --- | --- | --- | --- | --- |
| Januar | 0.50 | 0.30 | 0.20 | 980.00 |
| Februar | 0.40 | 0.35 | 0.25 | 960.00 |
| März | 0.45 | 0.25 | 0.30 | 970.00 |

Gesucht sind die monatlichen Gesamtkosten $M$, $S$, $I$ der drei Posten.

1. Schreiben Sie das Gleichungssystem als $\mathbf{A} \cdot \vec{x} = \vec{b}$
   mit $\vec{x} = (M,\ S,\ I)^\top$.
2. Prüfen Sie mit der Determinante die Lösbarkeit.
3. Lösen Sie das System mit `np.linalg.solve` und geben Sie die drei Kosten
   aus.
4. Führen Sie eine Probe durch.

Strukturieren Sie Ihren Code mit EVA-Kommentaren.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

# Eingabe
A = np.array([
    [0.50, 0.30, 0.20],
    [0.40, 0.35, 0.25],
    [0.45, 0.25, 0.30],
])
b = np.array([980.00, 960.00, 970.00])

# Verarbeitung
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

# Ausgabe
print(f'Determinante: {det_A:.5f}')
print(f'Miete:    {x[0]:.2f} Euro')
print(f'Strom:    {x[1]:.2f} Euro')
print(f'Internet: {x[2]:.2f} Euro')
print('Probe bestanden:', np.allclose(A @ x, b))
```
Ausgabe:
```
Determinante: 0.00750
Miete:    1080.00 Euro
Strom:    880.00 Euro
Internet: 880.00 Euro
Probe bestanden: True
```
Die Determinante ist mit 0.0075 klein, aber nicht null: Das System hat genau
eine Lösung. Miete kostet 1080 Euro im Monat, Strom und Internet je 880 Euro.
````

```{admonition} Aufgabe 3.5 (✩✩)
:class: tip
Ein waagerechter Träger der Länge $L = 6\,\text{m}$ ist links in A durch ein
Festlager, rechts in B durch ein Loslager gelagert. Das Festlager nimmt $A_x$
(waagerecht) und $A_y$ (senkrecht) auf, das Loslager nur $B_y$. Auf den Träger
wirken:

* eine waagerechte Kraft $H = 3\,\text{kN}$ nach rechts auf Höhe der
  Trägerachse,
* eine Last $F_1 = 6\,\text{kN}$ senkrecht nach unten im Abstand $2\,\text{m}$
  von A,
* eine Last $F_2 = 3\,\text{kN}$ senkrecht nach unten im Abstand $4\,\text{m}$
  von A.

1. Stellen Sie die drei Gleichgewichtsbedingungen auf ($\sum F_x = 0$,
   $\sum F_y = 0$, $\sum M_A = 0$; Kräfte nach rechts und oben positiv, Momente
   gegen den Uhrzeigersinn positiv).
2. Schreiben Sie sie als $\mathbf{A} \cdot \vec{x} = \vec{b}$ mit
   $\vec{x} = (A_x,\ A_y,\ B_y)^\top$, prüfen Sie die Determinante und lösen
   Sie das System.
3. Geben Sie die drei Auflagerkräfte aus und deuten Sie das Vorzeichen von
   $A_x$.

Strukturieren Sie Ihren Code mit EVA-Kommentaren.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

# Eingabe
# Summe Fx:  A_x + 3 = 0
# Summe Fy:  A_y + B_y - 6 - 3 = 0   ->   A_y + B_y = 9
# Summe M_A: 6*B_y - 6*2 - 3*4 = 0   ->   6*B_y = 24
A = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 1.0],
    [0.0, 0.0, 6.0],
])
b = np.array([-3.0, 9.0, 24.0])

# Verarbeitung
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

# Ausgabe
print(f'Determinante: {det_A:.1f}')
print(f'A_x = {x[0]:.1f} kN')
print(f'A_y = {x[1]:.1f} kN')
print(f'B_y = {x[2]:.1f} kN')
print('Probe bestanden:', np.allclose(A @ x, b))
```
Ausgabe:
```
Determinante: 6.0
A_x = -3.0 kN
A_y = 5.0 kN
B_y = 4.0 kN
Probe bestanden: True
```
Die Determinante ist 6.0, das System ist eindeutig lösbar. Das negative
Vorzeichen von $A_x$ bedeutet, dass die waagerechte Auflagerkraft mit
$3\,\text{kN}$ nach links zeigt, entgegen der angesetzten Richtung. Sie hält
der waagerechten Kraft $H$ das Gleichgewicht.
````

```{admonition} Aufgabe 3.6 (✩✩)
:class: tip
Ein Menüplan wird aus drei Zutaten zusammengestellt: Reis (R), Hähnchen (H)
und Brokkoli (B). Die Tabelle zeigt den Gehalt an Kalorien, Protein und
Kohlenhydraten pro 100 g sowie die Zielwerte pro Mahlzeit:

| Nährstoff | Reis | Hähnchen | Brokkoli | Ziel |
| --- | --- | --- | --- | --- |
| Kalorien | 130 | 165 | 34 | 600 |
| Protein in g | 2.7 | 31.0 | 2.8 | 55 |
| Kohlenhydrate in g | 28.0 | 0.0 | 7.0 | 80 |

Gesucht ist die Menge jeder Zutat (in 100-g-Einheiten), die genau diese
Nährwerte liefert.

1. Schreiben Sie das Gleichungssystem als $\mathbf{A} \cdot \vec{x} = \vec{b}$.
2. Prüfen Sie die Determinante, lösen Sie das System und geben Sie die Mengen
   in Gramm aus.
3. Führen Sie eine Probe durch.

Strukturieren Sie Ihren Code mit EVA-Kommentaren.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

# Eingabe
# Zeile = Nährstoff, Spalte = Zutat [Reis, Hähnchen, Brokkoli]
A = np.array([
    [130.0, 165.0, 34.0],
    [  2.7,  31.0,  2.8],
    [ 28.0,   0.0,  7.0],
])
b = np.array([600.0, 55.0, 80.0])

# Verarbeitung
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

# Ausgabe
print(f'Determinante: {det_A:.1f}')
print(f'Reis:     {x[0] * 100:.0f} g')
print(f'Hähnchen: {x[1] * 100:.0f} g')
print(f'Brokkoli: {x[2] * 100:.0f} g')
print('Probe bestanden:', np.allclose(A @ x, b))
```
Ausgabe:
```
Determinante: 8515.5
Reis:     227 g
Hähnchen: 136 g
Brokkoli: 236 g
Probe bestanden: True
```
Die Determinante ist deutlich ungleich null. Der Menüplan besteht aus rund
227 g Reis, 136 g Hähnchen und 236 g Brokkoli. Die Probe bestätigt, dass diese
Mengen genau die drei Zielwerte treffen.
````

````{admonition} Aufgabe 3.7 (✩✩✩) Mini-Projekt: Stromtarife
:class: tip
Ein Haushalt bezieht Strom zu drei Tarifen: Hochtarif (HT), Niedertarif (NT)
und Sondertarif (ST). In drei Monaten wurden die Verbräuche gemessen und die
Rechnungsbeträge gestellt:

| Monat | HT in kWh | NT in kWh | ST in kWh | Betrag in Euro |
| --- | --- | --- | --- | --- |
| Januar | 210 | 180 | 40 | 105.00 |
| Februar | 190 | 160 | 35 | 94.25 |
| März | 230 | 200 | 50 | 116.50 |

**Teil 1:** Stellen Sie das Gleichungssystem auf, prüfen Sie die Determinante
und berechnen Sie die Preise für HT, NT und ST in Cent pro kWh.

**Teil 2:** Im April werden 250 kWh HT, 220 kWh NT und 60 kWh ST verbraucht.
Berechnen Sie den erwarteten Rechnungsbetrag mit der Lösung aus Teil 1.
Hinweis: Der Betrag ist das Skalarprodukt aus Verbrauchsvektor und Preisvektor,
also `verbrauch_april @ x`.

**Teil 3:** Der HT-Preis steigt um 10 Prozent. Legen Sie einen neuen
Preisvektor an (die anderen beiden Preise bleiben gleich) und berechnen Sie den
neuen April-Betrag sowie die absolute und die prozentuale Änderung.

**Abschlussfrage:** Der HT-Preis steigt um 10 Prozent, der Rechnungsbetrag aber
nur um rund 6 Prozent. Woran liegt das?

Strukturieren Sie Ihren Code mit EVA-Kommentaren.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

# Eingabe
A = np.array([
    [210.0, 180.0, 40.0],
    [190.0, 160.0, 35.0],
    [230.0, 200.0, 50.0],
])
b = np.array([105.00, 94.25, 116.50])

# Verarbeitung Teil 1: Tarifpreise
det_A = np.linalg.det(A)
x = np.linalg.solve(A, b)

print(f'Determinante: {det_A:.1f}')
print(f'HT-Preis: {x[0] * 100:.2f} ct/kWh')
print(f'NT-Preis: {x[1] * 100:.2f} ct/kWh')
print(f'ST-Preis: {x[2] * 100:.2f} ct/kWh')
print('Probe bestanden:', np.allclose(A @ x, b))

# Verarbeitung Teil 2: Vorhersage April
verbrauch_april = np.array([250.0, 220.0, 60.0])
betrag_april = verbrauch_april @ x
print(f'April-Rechnung: {betrag_april:.2f} Euro')

# Verarbeitung Teil 3: HT-Preis plus 10 Prozent
x_neu = np.array([x[0] * 1.10, x[1], x[2]])
betrag_neu = verbrauch_april @ x_neu
aenderung_abs = betrag_neu - betrag_april
aenderung_proz = aenderung_abs / betrag_april * 100

print(f'April-Rechnung nach HT-Erhöhung: {betrag_neu:.2f} Euro')
print(f'Absolute Änderung:   {aenderung_abs:.2f} Euro')
print(f'Prozentuale Änderung: {aenderung_proz:.2f} %')
```
Ausgabe:
```
Determinante: -3000.0
HT-Preis: 30.00 ct/kWh
NT-Preis: 20.00 ct/kWh
ST-Preis: 15.00 ct/kWh
Probe bestanden: True
April-Rechnung: 128.00 Euro
April-Rechnung nach HT-Erhöhung: 135.50 Euro
Absolute Änderung:   7.50 Euro
Prozentuale Änderung: 5.86 %
```
Die drei Tarifpreise betragen 30, 20 und 15 ct/kWh. Die April-Rechnung steigt
von 128.00 auf 135.50 Euro.

**Abschlussfrage:** Der HT-Preis steigt zwar um 10 Prozent, aber der Hochtarif
macht nur einen Teil der Rechnung aus. Von den 128 Euro entfallen $250 \cdot
0.30 = 75$ Euro auf HT, der Rest auf NT und ST, deren Preise unverändert
bleiben. 10 Prozent von 75 Euro sind 7.50 Euro, und bezogen auf die gesamten
128 Euro sind das eben nur rund 6 Prozent.
````
