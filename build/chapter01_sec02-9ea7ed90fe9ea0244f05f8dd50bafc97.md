---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.2 Vertiefung (Teil 1)

Die folgenden Aufgaben bauen auf dem Code-Along aus Kapitel 1.1 auf. Aufgaben
mit einem Stern (✩) und zwei Sternen (✩✩) sind Pflichtaufgaben. Die Aufgabe mit
drei Sternen (✩✩✩) ist eine Zusatzaufgabe für alle, die schneller fertig sind.
Arbeiten Sie nach Möglichkeit zu zweit, das hilft besonders, wenn Python für
Sie noch neu ist. Wenn Sie einen Begriff nachschlagen wollen, hilft der
Spickzettel am Ende von Part 1.

```{admonition} Aufwärmaufgabe (✩)
:class: tip
Ein Prüffahrzeug fährt mit 27.8 m/s. Legen Sie eine Variable
`geschwindigkeit_ms` mit diesem Wert an und eine Variable `fahrzeug` mit dem
Wert `'Testwagen_3'`. Geben Sie beide mit `print()` aus und lassen Sie sich
mit `type()` den Datentyp von `geschwindigkeit_ms` anzeigen.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeit_ms = 27.8
fahrzeug = 'Testwagen_3'

print(geschwindigkeit_ms)
print(fahrzeug)
print(type(geschwindigkeit_ms))
```
`geschwindigkeit_ms` ist ein Float, da `27.8` einen Dezimalpunkt enthält.
````

```{admonition} Aufgabe A (✩)
:class: tip
Ein Prüffahrzeug liefert verschiedene Messwerte. Welcher Datentyp liegt jeweils
vor? Schreiben Sie Ihre Vermutung zunächst auf, bevor Sie den Code ausführen.

* `120` (Anzahl der Messungen) -->
* `27.8` (Geschwindigkeit in m/s) -->
* `'Testwagen_3'` (Fahrzeugname) -->
* `120 / 4` -->
* `2 ** 8` -->
* `27.8 > 33.3` -->

Überprüfen Sie anschließend jede Zeile mit `type()` in einer Code-Zelle.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
print(type(120))
print(type(27.8))
print(type('Testwagen_3'))
print(type(120 / 4))
print(type(2 ** 8))
print(type(27.8 > 33.3))
```
`120` ist ein Integer, `27.8` ein Float und `'Testwagen_3'` ein String.
`120 / 4` ergibt mit dem `/`-Operator immer einen Float, auch wenn das Ergebnis
ganzzahlig ist. `2 ** 8` bleibt ein Integer, da beide Operanden Integer sind.
Der Vergleich `27.8 > 33.3` liefert den Datentyp `bool`, da Vergleiche immer
einen Wahrheitswert zurückgeben.
````

````{admonition} Aufgabe B (✩)
:class: tip
Gegeben ist folgender Code. Notieren Sie, was er ausgibt, bevor Sie ihn
ausführen.

```python
geschwindigkeit_ms = 30.0
tempolimit_ms = 33.3

if geschwindigkeit_ms > tempolimit_ms:
    print('zu schnell')
elif geschwindigkeit_ms == tempolimit_ms:
    print('genau am Limit')
else:
    print('im Limit')
```

Was ändert sich an der Ausgabe, wenn in der ersten Zeile
`geschwindigkeit_ms = 33.3` steht?
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeit_ms = 30.0
tempolimit_ms = 33.3

if geschwindigkeit_ms > tempolimit_ms:
    print('zu schnell')
elif geschwindigkeit_ms == tempolimit_ms:
    print('genau am Limit')
else:
    print('im Limit')
```
Mit `geschwindigkeit_ms = 30.0` ist die erste Bedingung falsch und die zweite
ebenfalls, daher greift der `else`-Zweig und die Ausgabe lautet `im Limit`.
Mit `geschwindigkeit_ms = 33.3` ist die erste Bedingung weiterhin falsch, die
zweite (`==`) aber wahr, daher lautet die Ausgabe dann `genau am Limit`.
````

````{admonition} Aufgabe C (✩✩)
:class: tip
Vervollständigen Sie den Code an den mit `___` markierten Stellen. Ein
Prüffahrzeug fährt mit `geschwindigkeit_kmh = 95`. Der Code soll die
Geschwindigkeit in m/s umrechnen und ausgeben, ob das Tempolimit von 33.3 m/s
überschritten wird.

```python
geschwindigkeit_kmh = 95
tempolimit_ms = 33.3

geschwindigkeit_ms = geschwindigkeit_kmh / ___

if geschwindigkeit_ms ___ tempolimit_ms:
    print(f'{geschwindigkeit_ms:.1f} m/s: Tempolimit überschritten')
else:
    print(f'{geschwindigkeit_ms:.1f} m/s: im erlaubten Bereich')
```
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeit_kmh = 95
tempolimit_ms = 33.3

geschwindigkeit_ms = geschwindigkeit_kmh / 3.6

if geschwindigkeit_ms > tempolimit_ms:
    print(f'{geschwindigkeit_ms:.1f} m/s: Tempolimit überschritten')
else:
    print(f'{geschwindigkeit_ms:.1f} m/s: im erlaubten Bereich')
```
An der ersten Lücke steht `3.6`, denn 1 m/s entspricht 3.6 km/h. An der zweiten
Lücke steht der Vergleichsoperator `>`. 95 km/h entsprechen rund 26.4 m/s und
liegen unter dem Tempolimit, die Ausgabe lautet daher
`26.4 m/s: im erlaubten Bereich`.
````

````{admonition} Aufgabe D (✩✩)
:class: tip
Ergänzen Sie die for-Schleife an den `___`-Stellen. Ein Beschleunigungstest
läuft über sieben Zeitschritte. In jedem Zeitschritt steigt die Geschwindigkeit
um 7 m/s. Der Code soll für jeden Zeitschritt die Geschwindigkeit ausgeben und
zusätzlich `zu schnell`, sobald sie über dem Tempolimit von 33.3 m/s liegt.

```python
tempolimit_ms = 33.3

for zeitschritt in range(7):
    geschwindigkeit_ms = zeitschritt * ___
    print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_ms:.1f} m/s')
    if ___:
        print('zu schnell')
```
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
tempolimit_ms = 33.3

for zeitschritt in range(7):
    geschwindigkeit_ms = zeitschritt * 7.0
    print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_ms:.1f} m/s')
    if geschwindigkeit_ms > tempolimit_ms:
        print('zu schnell')
```
An der ersten Lücke steht `7.0` (Zunahme pro Zeitschritt), an der zweiten die
Bedingung `geschwindigkeit_ms > tempolimit_ms`. Die Geschwindigkeit nimmt die
Werte 0, 7, 14, 21, 28, 35 und 42 m/s an. `zu schnell` erscheint in den
Zeitschritten 5 und 6.
````

```{admonition} Aufgabe E (✩✩✩, Mini-Projekt)
:class: tip
Ein Prüfstand simuliert einen Beschleunigungstest über zehn Zeitschritte.
Setzen Sie folgende Schritte um.

**Teil 1:** Schreiben Sie eine for-Schleife mit `range(10)` für die
Zeitschritte 0 bis 9. In jedem Zeitschritt beträgt die Geschwindigkeit
`geschwindigkeit_ms = zeitschritt * 5.0`. Geben Sie Zeitschritt und
Geschwindigkeit mit einem f-String aus.

**Teil 2:** Ergänzen Sie im Schleifenkörper eine `if`/`else`-Abfrage, die zu
jedem Zeitschritt ausgibt, ob das Tempolimit `tempolimit_ms = 33.3`
eingehalten oder überschritten wird.

**Teil 3:** Zählen Sie mit, in wie vielen Zeitschritten das Tempolimit
überschritten wird. Legen Sie dazu vor der Schleife eine Variable
`anzahl_zu_schnell = 0` an und erhöhen Sie sie im passenden Fall um 1. Geben
Sie die Zahl nach der Schleife aus.

**Abschlussfrage:** Ab welchem Zeitschritt wird das Tempolimit überschritten,
und wie hängt das mit der gewählten Beschleunigung von 5.0 m/s pro Zeitschritt
zusammen?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
tempolimit_ms = 33.3
anzahl_zu_schnell = 0

for zeitschritt in range(10):
    geschwindigkeit_ms = zeitschritt * 5.0
    if geschwindigkeit_ms > tempolimit_ms:
        print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_ms:.1f} m/s, zu schnell')
        anzahl_zu_schnell = anzahl_zu_schnell + 1
    else:
        print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_ms:.1f} m/s, im Limit')

print(f'Zu schnell in {anzahl_zu_schnell} Zeitschritten.')
```
Die Geschwindigkeit nimmt die Werte 0, 5, 10, ... bis 45 m/s an. Das Tempolimit
wird ab `zeitschritt = 7` überschritten, denn dort beträgt die Geschwindigkeit
`7 * 5.0 = 35.0` m/s und liegt erstmals über 33.3 m/s. Insgesamt ist das
Fahrzeug in den Zeitschritten 7, 8 und 9 zu schnell, also in drei
Zeitschritten. Die Variable `anzahl_zu_schnell` wirkt dabei als Zähler, den wir
in jedem passenden Durchlauf um 1 erhöhen. Bei einer größeren Beschleunigung
pro Zeitschritt wäre das Limit früher überschritten.
````
