---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.4 Vertiefung (Teil 2)

Die folgenden Aufgaben bauen auf dem Code-Along aus Kapitel 1.3 auf. Aufgaben
mit einem Stern (✩) und zwei Sternen (✩✩) sind Pflichtaufgaben. Die Aufgabe mit
drei Sternen (✩✩✩) ist eine Zusatzaufgabe für alle, die schneller fertig sind.
Arbeiten Sie nach Möglichkeit zu zweit. Wenn Sie einen Begriff nachschlagen
wollen, hilft der Spickzettel am Ende von Part 1.

```{admonition} Aufwärmaufgabe (✩)
:class: tip
Ein Beschleunigungstest liefert die Geschwindigkeiten `72`, `88` und `95`
km/h. Legen Sie sie als Liste `geschwindigkeiten_kmh` an. Geben Sie das erste
und das letzte Element sowie mit `len()` die Anzahl der Elemente aus.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeiten_kmh = [72, 88, 95]

print(geschwindigkeiten_kmh[0])
print(geschwindigkeiten_kmh[-1])
print(len(geschwindigkeiten_kmh))
```
`geschwindigkeiten_kmh[0]` ist `72`, das erste Element, `geschwindigkeiten_kmh[-1]`
ist `95`, das letzte. `len(...)` ist `3`, die Anzahl der Elemente.
````

```{admonition} Aufgabe A (✩)
:class: tip
Gegeben ist die Liste `geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]`.
Notieren Sie zunächst Ihre Vermutung, bevor Sie den Code ausführen.

* `geschwindigkeiten_kmh[0]` -->
* `geschwindigkeiten_kmh[2]` -->
* `geschwindigkeiten_kmh[-1]` -->
* `len(geschwindigkeiten_kmh)` -->

Überprüfen Sie anschließend jede Zeile in einer Code-Zelle.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]
print(geschwindigkeiten_kmh[0])
print(geschwindigkeiten_kmh[2])
print(geschwindigkeiten_kmh[-1])
print(len(geschwindigkeiten_kmh))
```
`geschwindigkeiten_kmh[0]` ist `72`, das erste Element. `geschwindigkeiten_kmh[2]`
ist `95`, das Element an Index 2. `geschwindigkeiten_kmh[-1]` ist `130`, das
letzte Element. `len(...)` ist `6`, die Anzahl der Elemente.
````

````{admonition} Aufgabe B (✩)
:class: tip
Gegeben ist folgender Code. Notieren Sie, welche Zeilen er ausgibt und welchen
Wert `anzahl` am Ende hat, bevor Sie ihn ausführen.

```python
geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]
anzahl = 0

for geschwindigkeit in geschwindigkeiten_kmh:
    if geschwindigkeit > 90:
        print(f'{geschwindigkeit} km/h: schnell')
        anzahl = anzahl + 1

print(f'Anzahl schneller Messungen: {anzahl}')
```
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]
anzahl = 0

for geschwindigkeit in geschwindigkeiten_kmh:
    if geschwindigkeit > 90:
        print(f'{geschwindigkeit} km/h: schnell')
        anzahl = anzahl + 1

print(f'Anzahl schneller Messungen: {anzahl}')
```
Die `if`-Abfrage ist nur für die Werte 95, 110 und 130 wahr, daher werden
genau diese drei Zeilen mit `schnell` ausgegeben. Die Variable `anzahl` wird
in genau diesen drei Durchgängen um 1 erhöht und hat am Ende den Wert `3`.
````

````{admonition} Aufgabe C (✩✩)
:class: tip
Vervollständigen Sie den Code an den `___`-Stellen. Erstellen Sie ein
Dictionary `fahrzeug` mit den Angaben zum Prüffahrzeug und geben Sie den Satz
aus. Die Masse beträgt 1200 kg.

```python
fahrzeug = {
    'name': 'Testwagen_3',
    'masse_kg': ___,
    'baujahr': 2021,
}

print(f'{fahrzeug[___]} (Baujahr {fahrzeug["baujahr"]}) wiegt '
      f'{fahrzeug["masse_kg"]} kg.')
```
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fahrzeug = {
    'name': 'Testwagen_3',
    'masse_kg': 1200,
    'baujahr': 2021,
}

print(f'{fahrzeug["name"]} (Baujahr {fahrzeug["baujahr"]}) wiegt '
      f'{fahrzeug["masse_kg"]} kg.')
```
An der ersten Lücke steht der Wert `1200`, an der zweiten der Schlüssel
`"name"` in Anführungszeichen. Die Ausgabe lautet
`Testwagen_3 (Baujahr 2021) wiegt 1200 kg.` Ein f-String darf über mehrere
Zeilen verteilt werden, solange jede Teilzeichenkette mit einem `f` beginnt.
````

````{admonition} Aufgabe D (✩✩)
:class: tip
Ergänzen Sie die Funktion und den Aufruf an den `___`-Stellen. Die Funktion
`kmh_zu_ms` soll eine Geschwindigkeit von km/h in m/s umrechnen, indem sie
durch 3.6 teilt. Danach wird sie in einer Schleife für jede Messung
aufgerufen.

```python
def kmh_zu_ms(geschwindigkeit_kmh):
    return geschwindigkeit_kmh ___ 3.6

geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]

for geschwindigkeit_kmh in geschwindigkeiten_kmh:
    geschwindigkeit_ms = ___(geschwindigkeit_kmh)
    print(f'{geschwindigkeit_kmh} km/h entsprechen {geschwindigkeit_ms:.1f} m/s')
```
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
def kmh_zu_ms(geschwindigkeit_kmh):
    return geschwindigkeit_kmh / 3.6

geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]

for geschwindigkeit_kmh in geschwindigkeiten_kmh:
    geschwindigkeit_ms = kmh_zu_ms(geschwindigkeit_kmh)
    print(f'{geschwindigkeit_kmh} km/h entsprechen {geschwindigkeit_ms:.1f} m/s')
```
An der ersten Lücke steht der Divisionsoperator `/`, an der zweiten der
Funktionsname `kmh_zu_ms`. Da die Funktion einmal definiert wird, können wir
sie beliebig oft mit unterschiedlichen Argumenten aufrufen, ohne die
Umrechnungsformel jedes Mal neu hinzuschreiben.
````

```{admonition} Aufgabe E (✩✩✩, Mini-Projekt)
:class: tip
Ein Beschleunigungstest liefert die Messreihe
`geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]` in km/h. Setzen Sie
folgende Schritte um.

**Teil 1:** Schreiben Sie eine Funktion
`kinetische_energie(geschwindigkeit_kmh, masse=1200)`, die zunächst intern in
m/s umrechnet und anschließend die kinetische Energie in Joule zurückgibt.

**Teil 2:** Durchlaufen Sie `geschwindigkeiten_kmh` mit einer for-Schleife.
Berechnen Sie für jeden Messwert die kinetische Energie und merken Sie sich in
einer Variable `maximale_energie` den bisher größten berechneten Wert
(Hinweis: Starten Sie mit `maximale_energie = 0` vor der Schleife und
vergleichen Sie in jedem Durchgang mit einer `if`-Abfrage).

**Teil 3:** Geben Sie nach der Schleife den größten gefundenen Energiewert
aus.

**Abschlussfrage:** Bei welcher Geschwindigkeit aus der Messreihe tritt dieser
Maximalwert auf, und warum lässt sich das ohne Ausführen des Codes bereits
vermuten?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
def kinetische_energie(geschwindigkeit_kmh, masse=1200):
    geschwindigkeit_ms = geschwindigkeit_kmh / 3.6
    return 0.5 * masse * geschwindigkeit_ms**2

geschwindigkeiten_kmh = [72, 88, 95, 60, 110, 130]

maximale_energie = 0
for geschwindigkeit_kmh in geschwindigkeiten_kmh:
    energie = kinetische_energie(geschwindigkeit_kmh)
    if energie > maximale_energie:
        maximale_energie = energie

print(f'Maximale kinetische Energie: {maximale_energie:.1f} Joule')
```
Der Maximalwert tritt bei 130 km/h auf, dem größten Wert der Messreihe. Da die
kinetische Energie mit dem Quadrat der Geschwindigkeit wächst und die Masse
über die gesamte Messreihe konstant bleibt, liegt das Maximum der Energie
immer bei der höchsten gemessenen Geschwindigkeit. Diese Vermutung lässt sich
also bereits aus der Formel ableiten, ohne den Code auszuführen.
````
