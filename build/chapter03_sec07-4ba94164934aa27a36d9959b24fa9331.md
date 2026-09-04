---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Exkurs: Rechenzeit und Skalierung

Dieses Kapitel ist ein optionaler Exkurs. Bisher haben wir `np.linalg.solve`
für Systeme mit 3 oder 6 Unbekannten benutzt. In der Ingenieurpraxis entstehen
bei einer Finite-Elemente-Simulation Systeme mit Tausenden bis Millionen von
Unbekannten. *Wie schnell wächst die Rechenzeit mit der Systemgröße, und wo
stößt `np.linalg.solve` an seine Grenzen?*

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können mit `np.random` ein zufälliges, eindeutig lösbares
  Gleichungssystem beliebiger Größe erzeugen.
* [ ] Sie können mit `time.perf_counter()` die Rechenzeit einer Operation
  messen.
* [ ] Sie können die Rechenzeit über der Systemgröße in einem log-log-Diagramm
  darstellen und den Skalierungsexponenten mit `np.polyfit` schätzen.
* [ ] Sie können die beobachtete $O(n^3)$-Skalierung erklären und ihre
  Konsequenzen für große Systeme abschätzen.
```

## Zufällige Testsysteme erzeugen

Für die Zeitmessung brauchen wir Testprobleme: Matrizen und rechte Seiten
beliebiger Größe, die ein eindeutig lösbares System bilden. Eine zufällige
Matrix ist fast immer lösbar. Wir sichern das ab, indem wir die Diagonale
verstärken.

```{code-cell} python
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

def erzeuge_lgs(n, seed=0):
    """Erzeugt ein zufälliges, eindeutig lösbares n x n-Gleichungssystem.

    n:    Größe des Systems
    seed: Zufallsseed für reproduzierbare Ergebnisse
    Rückgabe: Matrix A und rechte Seite b
    """
    zufall = np.random.default_rng(seed)
    A = zufall.standard_normal((n, n))
    A = A + n * np.eye(n)          # Diagonale verstärken -> immer lösbar
    b = zufall.standard_normal(n)
    return A, b

A, b = erzeuge_lgs(5)
print('Form von A:  ', A.shape)
print('Determinante:', round(float(np.linalg.det(A)), 1))
```

Wir addieren $n$ mal die Einheitsmatrix, damit jedes Diagonalelement um $n$
wächst. Der Faktor $n$ ist wichtig: Die typische Zeilensumme einer
$n \times n$-Zufallsmatrix wächst mit $\sqrt{n}$, ein fester Zuwachs würde bei
großen $n$ nicht mehr ausreichen, um die Diagonale dominieren zu lassen.

```{admonition} Mini-Übung (✩)
:class: tip
1. Rufen Sie `erzeuge_lgs(5, seed=0)` zweimal auf und prüfen Sie mit
   `np.allclose`, ob beide Aufrufe dieselbe Matrix liefern.
2. Beantworten Sie ohne Code: Warum ist es beim Messen von Rechenzeiten
   sinnvoll, immer denselben `seed` zu verwenden?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
A1, _ = erzeuge_lgs(5, seed=0)
A2, _ = erzeuge_lgs(5, seed=0)
print('gleiche Matrix:', np.allclose(A1, A2))
```
Beide Aufrufe liefern dieselbe Matrix, weil der `seed` den Startzustand des
Zufallsgenerators festlegt. Für einen fairen Vergleich der Rechenzeiten
verschiedener Systemgrößen sollen sich die Testmatrizen nur in der Größe
unterscheiden, nicht in zufälligen Eigenschaften. Ein fester `seed` macht die
Messung außerdem wiederholbar.
````

## Rechenzeit messen und darstellen

`time.perf_counter()` gibt eine Uhrzeit in Sekunden zurück. Die Differenz
zweier Aufrufe ist die vergangene Zeit. Wir messen, wie lange `np.linalg.solve`
für verschiedene Systemgrößen braucht.

```{code-cell} python
def messe_rechenzeit(n):
    """Erzeugt ein n x n-System, löst es und gibt die Rechenzeit in s zurück."""
    A, b = erzeuge_lgs(n)
    start = time.perf_counter()
    np.linalg.solve(A, b)
    return time.perf_counter() - start

n_werte = np.array([100, 200, 400, 700, 1000, 1500, 2000])
t_werte = np.zeros(len(n_werte))

for i, n in enumerate(n_werte):
    t_werte[i] = messe_rechenzeit(n)
    print(f'n = {n:5d}:  {t_werte[i] * 1000:7.2f} ms')
```

Die absoluten Zeiten hängen von der Hardware ab und schwanken bei jedem
Durchlauf etwas. Für die Frage nach der Skalierung stellen wir die Zeiten über
der Systemgröße dar, und zwar mit `ax.loglog`: Beide Achsen sind logarithmisch.
Ein Potenzgesetz $t \propto n^\alpha$ erscheint dann als Gerade, deren Steigung
der Exponent $\alpha$ ist.

```{code-cell} python
# Referenzlinie für O(n^3), an den ersten Messpunkt angepasst
t_referenz = t_werte[0] * (n_werte / n_werte[0])**3

fig, ax = plt.subplots(figsize=(7, 4))
ax.loglog(n_werte, t_werte, marker='o', label='gemessen')
ax.loglog(n_werte, t_referenz, linestyle='dashed', label='Steigung 3 (O(n³))')
ax.set_xlabel('Systemgröße n')
ax.set_ylabel('Rechenzeit in s')
ax.set_title('Rechenzeit von np.linalg.solve')
ax.legend()
ax.grid(True, which='both')
plt.show()
```

```{admonition} Mini-Übung (✩)
:class: tip
1. Stellen Sie dieselben Daten zusätzlich mit `ax.plot` statt `ax.loglog` dar.
2. Beantworten Sie ohne Code: In welcher der beiden Darstellungen kann man den
   Skalierungsexponenten leichter ablesen, und warum?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(n_werte, t_werte, marker='o')
ax.set_xlabel('Systemgröße n')
ax.set_ylabel('Rechenzeit in s')
ax.set_title('Rechenzeit, lineare Achsen')
ax.grid(True)
plt.show()
```
In der linearen Darstellung dominiert der steile Anstieg bei großen $n$ das
ganze Bild, kleine $n$ sind zusammengedrückt und nicht unterscheidbar. In der
log-log-Darstellung erscheint ein Potenzgesetz als Gerade, deren Steigung man
direkt als Exponenten ablesen kann. Für die Skalierungsanalyse ist die
log-log-Darstellung daher besser geeignet.
````

## Den Skalierungsexponenten bestimmen

Im log-log-Raum gilt $\log t = \alpha \cdot \log n + \text{const}$. Der
Exponent $\alpha$ ist also die Steigung einer Geraden durch die Punkte
$(\log n,\ \log t)$. Diese Steigung liefert `np.polyfit`.

```{code-cell} python
log_n = np.log(n_werte)
log_t = np.log(t_werte)

# np.polyfit(x, y, 1) legt eine Gerade durch die Punkte und gibt
# [Steigung, Achsenabschnitt] zurück. Wir nehmen nur die obere Hälfte
# der Messpunkte, da bei kleinen n der feste Aufwand die Messung verfälscht.
mitte = len(n_werte) // 2
steigung = np.polyfit(log_n[mitte:], log_t[mitte:], 1)[0]

print(f'geschätzter Exponent: {steigung:.2f}')
print('theoretischer Wert:   3.00')
```

Der gemessene Exponent liegt in der Nähe von 3, die genaue Zahl schwankt von
Messung zu Messung. Das bestätigt die theoretische $O(n^3)$-Komplexität:
`np.linalg.solve` zerlegt die Matrix intern in ein
Produkt zweier Dreiecksmatrizen (LU-Zerlegung), und dieser Schritt kostet in
der Größenordnung $n^3$ Rechenoperationen. Verdoppelt man die Systemgröße,
steigt die Rechenzeit um den Faktor $2^3 = 8$.

```{admonition} Mini-Übung (✩)
:class: tip
1. Schätzen Sie mit $t(n) \approx t(n_0) \cdot (n / n_0)^3$ die Rechenzeit für
   $n = 20\,000$, wobei $n_0$ und $t(n_0)$ der größte gemessene Punkt sind
   (`n_werte[-1]` und `t_werte[-1]`).
2. Beantworten Sie ohne Code: Eine Finite-Elemente-Simulation hat oft
   $n = 10^6$ Unbekannte. Ist `np.linalg.solve` dafür geeignet? Recherchieren
   Sie die Stichwörter *dünnbesetzte Matrix* und *iterativer Löser*.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
n0 = n_werte[-1]
t0 = t_werte[-1]
n_neu = 20000
t_neu = t0 * (n_neu / n0)**3
print(f'geschätzte Rechenzeit für n = {n_neu}: {t_neu:.1f} s ({t_neu / 60:.1f} min)')
```
Für $n = 20\,000$ ergeben sich je nach Rechner einige Sekunden bis Minuten.
Für $n = 10^6$ wäre die Rechenzeit mit `np.linalg.solve` nicht mehr praktikabel
und der Speicherbedarf einer vollen $10^6 \times 10^6$-Matrix gigantisch. In
der Praxis sind die Matrizen großer Ingenieurprobleme **dünnbesetzt**, das
heißt fast alle Einträge sind null. Dafür gibt es spezielle iterative Löser
(zum Beispiel in `scipy.sparse.linalg`), die nur die von null verschiedenen
Einträge speichern und deutlich weniger Rechenoperationen brauchen.
````

## Zusammenfassung

Die Rechenzeit von `np.linalg.solve` wächst mit der dritten Potenz der
Systemgröße, $O(n^3)$, weil intern eine LU-Zerlegung durchgeführt wird. Für
kleine und mittlere Systeme bis einige Tausend Unbekannte ist das kein Problem.
Für die großen, dünnbesetzten Systeme der Ingenieurpraxis braucht man
spezialisierte iterative Löser.

Damit endet Part 3. In Part 4 lösen wir mit demselben Werkzeug ein größeres
Maschinenbau-Problem: die Verformung eines Fachwerks.
