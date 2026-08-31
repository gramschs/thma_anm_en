---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.5 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 1.1 bis 1.4. Rechnen Sie mit rund zwei Stunden Bearbeitungszeit.

Der Schwierigkeitsgrad steht im Titel jeder Aufgabe:

* ✩ Verständnis: Code und Ausgaben vorhersagen und erklären (ca. 5 min)
* ✩✩ Anwendung: eigenen Code schreiben und Ergebnisse interpretieren (ca. 10 min)
* ✩✩✩ Mini-Projekt: mehrere Konzepte des Parts kombinieren (ca. 30 min)

```{admonition} Aufgabe 1.1 (✩)
:class: tip
Welcher Datentyp liegt vor? Schreiben Sie Ihre Vermutung hinter den Pfeil,
bevor Sie den Code ausführen.

* `7` -->
* `-7` -->
* `'Stahl'` -->
* `7.0` -->
* `7,0` -->
* `7**2` -->
* `7**(1/2)` -->
* `7 == 7.0` -->

Überprüfen Sie anschließend jede Zeile mit `type()` in einer Code-Zelle.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
print(type(7))
print(type(-7))
print(type('Stahl'))
print(type(7.0))

komma_zahl = 7,0
print(type(komma_zahl))

print(type(7**2))
print(type(7**(1/2)))
print(type(7 == 7.0))
```
`7` und `-7` sind Integer, `'Stahl'` ist ein String, `7.0` ist ein Float.
`7**2` bleibt ein Integer (`49`), `7**(1/2)` ist ein Float
(`2.6457513110645907`). `7 == 7.0` ist ein `bool` mit dem Wert `True`, da
Python beim Vergleich den Zahlenwert betrachtet, nicht den Datentyp.

Der interessanteste Fall ist `7,0`: Das Komma erzeugt in Python keine
Dezimalzahl, sondern bündelt die beiden Werte `7` und `0` zu einem Paar. Es
kommt dabei zu keiner Fehlermeldung, was diesen Tippfehler besonders tückisch
macht. Verwenden Sie für Dezimalzahlen daher immer einen Punkt statt eines
Kommas.
````

```{admonition} Aufgabe 1.2 (✩✩)
:class: tip
Eine Feder gehorcht dem Federgesetz `kraft = federkonstante * auslenkung`.
Berechnen Sie die Federkraft für eine Federkonstante von 250 N/m und eine
Auslenkung von 0.12 m. Geben Sie das Ergebnis mit einem f-String und der
Einheit Newton aus, gerundet auf zwei Nachkommastellen.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
federkonstante = 250    # N/m
auslenkung = 0.12       # m

kraft = federkonstante * auslenkung
print(f'Federkraft: {kraft:.2f} N')
```
Die Federkraft beträgt 30.00 N. Da `federkonstante` ein Integer und
`auslenkung` ein Float ist, wandelt Python das Ergebnis der Multiplikation
automatisch in einen Float um.
````

```{admonition} Aufgabe 1.3 (✩)
:class: tip
Was geben die folgenden Ausdrücke zurück? Notieren Sie `True` oder `False`,
bevor Sie den Code ausführen.

* `5 > 3` -->
* `5 >= 5` -->
* `'Stahl' == 'stahl'` -->
* `not (5 > 3)` -->
* `(5 > 3) and (2 > 4)` -->
* `(5 > 3) or (2 > 4)` -->
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
print(5 > 3)
print(5 >= 5)
print('Stahl' == 'stahl')
print(not (5 > 3))
print((5 > 3) and (2 > 4))
print((5 > 3) or (2 > 4))
```
`5 > 3` und `5 >= 5` sind `True`. `'Stahl' == 'stahl'` ist `False`, da
Python beim Vergleich von Strings Groß- und Kleinschreibung unterscheidet.
`not (5 > 3)` kehrt `True` zu `False` um. Bei `and` müssen beide Seiten
wahr sein, daher ist das Ergebnis `False`. Bei `or` reicht eine wahre Seite,
daher ist das Ergebnis `True`.
````

```{admonition} Aufgabe 1.4 (✩✩)
:class: tip
Ein Werkstoff hat eine gemessene Zugfestigkeit von
`zugfestigkeit_mpa = 420`. Schreiben Sie eine `if`/`elif`/`else`-
Verzweigung, die folgende Kategorien ausgibt:

* unter 300 MPa: `'niedrigfest'`
* von 300 bis 600 MPa (jeweils einschließlich): `'mittelfest'`
* über 600 MPa: `'hochfest'`
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
zugfestigkeit_mpa = 420

if zugfestigkeit_mpa < 300:
    kategorie = 'niedrigfest'
elif zugfestigkeit_mpa <= 600:
    kategorie = 'mittelfest'
else:
    kategorie = 'hochfest'

print(f'Kategorie: {kategorie}')
```
Bei 420 MPa liegt der Werkstoff im Bereich von 300 bis 600 MPa und wird
daher als `'mittelfest'` eingestuft.
````

```{admonition} Aufgabe 1.5 (✩✩)
:class: tip
Schreiben Sie eine for-Schleife, die für die Temperaturen 0, 20, 40, 60, 80
und 100 Grad Celsius jeweils den Wert in Fahrenheit ausgibt. Verwenden Sie
dafür die Formel `fahrenheit = celsius * 9/5 + 32`.

Hinweis: `range(start, stop, step)` erzeugt Zahlen mit einer Schrittweite
ungleich 1. Der Wert `stop` selbst gehört nicht mehr zum Bereich, wählen Sie
ihn daher passend größer.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
for celsius in range(0, 101, 20):
    fahrenheit = celsius * 9/5 + 32
    print(f'{celsius} Grad Celsius entsprechen {fahrenheit:.1f} Grad Fahrenheit')
```
`range(0, 101, 20)` erzeugt die Werte 0, 20, 40, 60, 80 und 100. Da der Wert
101 selbst nicht mehr im Bereich enthalten ist, deckt diese Wahl alle sechs
gewünschten Temperaturen ab.
````

```{admonition} Aufgabe 1.6 (✩✩)
:class: tip
Ein Bauteil kühlt sich ausgehend von 180 Grad Celsius in jedem Zeitschritt um
12 Grad ab. Schreiben Sie eine for-Schleife mit `range(15)`, die für jeden
Zeitschritt die Temperatur berechnet und ausgibt. Ergänzen Sie im
Schleifenkörper eine `if`-Abfrage, die zusätzlich `unter 20 Grad` ausgibt,
sobald die Temperatur die Marke von 20 Grad Celsius unterschreitet.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
for zeitschritt in range(15):
    temperatur = 180 - zeitschritt * 12
    print(f'Zeitschritt {zeitschritt}: {temperatur} Grad Celsius')
    if temperatur < 20:
        print('unter 20 Grad')
```
Die Temperatur sinkt in gleichmäßigen Schritten von 180 auf 12 Grad Celsius.
Ab Zeitschritt 14 liegt sie mit 12 Grad Celsius erstmals unter der Marke von
20 Grad, dort erscheint die Zusatzmeldung. Mit `range(15)` decken wir alle
Zeitschritte bis zum Unterschreiten der Marke ab.
````

```{admonition} Aufgabe 1.7 (✩)
:class: tip
Gegeben ist die Liste `liste = [15, 8, 23, 4, 16, 42]`. Notieren Sie zunächst
Ihre Vermutung, bevor Sie den Code ausführen.

* `liste[0]` -->
* `liste[2]` -->
* `liste[-1]` -->
* `liste[-3]` -->
* `len(liste)` -->
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
liste = [15, 8, 23, 4, 16, 42]
print(liste[0])
print(liste[2])
print(liste[-1])
print(liste[-3])
print(len(liste))
```
`liste[0]` ist `15`, das erste Element, `liste[2]` ist `23`, das Element an
Index 2. `liste[-1]` ist `42`, das letzte Element. `liste[-3]` ist `4`, denn
von hinten gezählt liegen `42` bei -1, `16` bei -2 und `4` bei -3.
`len(liste)` ergibt `6`, die Anzahl der Elemente.
````

```{admonition} Aufgabe 1.8 (✩✩)
:class: tip
Gegeben ist die Liste `messreihe = [15.2, 8.7, 23.1, 4.4, 16.9, 42.0]` mit
Kraftmesswerten in Newton. Bestimmen Sie mit einer for-Schleife den
kleinsten und größten Wert der Liste, ohne die eingebauten Funktionen
`min()` und `max()` zu verwenden.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
messreihe = [15.2, 8.7, 23.1, 4.4, 16.9, 42.0]

minimum = messreihe[0]
maximum = messreihe[0]

for wert in messreihe:
    if wert < minimum:
        minimum = wert
    if wert > maximum:
        maximum = wert

print(f'Minimum: {minimum} N, Maximum: {maximum} N')
```
Wir starten `minimum` und `maximum` mit dem ersten Listenelement und
vergleichen anschließend jedes weitere Element. Das Minimum der Messreihe
ist 4.4 N, das Maximum ist 42.0 N.
````

```{admonition} Aufgabe 1.9 (✩✩)
:class: tip
Erstellen Sie ein Dictionary `bauteil` für eine Welle mit folgenden
Informationen:

* bezeichnung: `'Welle_A1'`
* durchmesser_mm: 25.0
* werkstoff: `'42CrMo4'`
* max_drehmoment_nm: 180

Geben Sie dann aus: "Welle_A1 aus 42CrMo4 (Durchmesser 25.0 mm) hält
maximal 180 Nm."
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
bauteil = {
    'bezeichnung': 'Welle_A1',
    'durchmesser_mm': 25.0,
    'werkstoff': '42CrMo4',
    'max_drehmoment_nm': 180
}

print(f'{bauteil["bezeichnung"]} aus {bauteil["werkstoff"]} '
      f'(Durchmesser {bauteil["durchmesser_mm"]} mm) hält maximal '
      f'{bauteil["max_drehmoment_nm"]} Nm.')
```
Der Zugriff auf jeden Wert erfolgt über den passenden Schlüssel. Ein
Dictionary macht hier sofort sichtbar, welcher Wert wofür steht, im
Gegensatz zu einer Liste mit denselben vier Werten.
````

```{admonition} Aufgabe 1.10 (✩✩)
:class: tip
Schreiben Sie eine Funktion `spannung(kraft_n, querschnitt_mm2=100)`, die
die mechanische Spannung `sigma = kraft_n / querschnitt_mm2` in N/mm² (MPa)
berechnet und zurückgibt. Versehen Sie die Funktion mit einem Docstring.
Rufen Sie die Funktion einmal mit `kraft_n = 5000` und dem Default-
Querschnitt sowie einmal mit `kraft_n = 5000` und
`querschnitt_mm2 = 50` auf. Vergleichen Sie die beiden Ergebnisse in einem
Satz.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
def spannung(kraft_n, querschnitt_mm2=100):
    """Berechnet die mechanische Spannung in MPa (N/mm²)."""
    return kraft_n / querschnitt_mm2

print(f'{spannung(5000):.1f} MPa')
print(f'{spannung(5000, querschnitt_mm2=50):.1f} MPa')
```
Mit dem Default-Querschnitt von 100 mm² ergibt sich eine Spannung von 50.0
MPa, mit dem kleineren Querschnitt von 50 mm² verdoppelt sich die Spannung
auf 100.0 MPa. Dieselbe Kraft verteilt sich bei kleinerem Querschnitt auf
weniger Fläche, wodurch die Spannung steigt.
````

```{admonition} Aufgabe 1.11 (✩✩✩, Mini-Projekt)
:class: tip
Bei einem Zugversuch wird eine Probe mit dem konstanten Querschnitt
`querschnitt_mm2 = 19.6` schrittweise belastet. Die gemessenen Kräfte sind
`kraefte_n = [1200, 3400, 5800, 7200, 8100, 6500]`. Setzen Sie folgende
Schritte um.

**Teil 1:** Schreiben Sie eine Funktion `spannung(kraft_n, querschnitt_mm2)`,
die die Spannung in MPa zurückgibt.

**Teil 2:** Erstellen Sie ein Dictionary `versuch` mit den Schlüsseln
`werkstoff` (`'S235JR'`), `querschnitt_mm2` (19.6) und `streckgrenze_mpa`
(235.0).

**Teil 3:** Durchlaufen Sie `kraefte_n` mit einer for-Schleife. Berechnen
Sie für jeden Wert die Spannung mit Ihrer Funktion und geben Sie pro
Messwert aus, ob die Streckgrenze aus dem Dictionary überschritten wird
(`'Im elastischen Bereich'` oder `'Streckgrenze überschritten'`). Merken
Sie sich zusätzlich, bei welcher Kraft die Streckgrenze zum ersten Mal
überschritten wird.

**Teil 4:** Bestimmen Sie die maximale Spannung der gesamten Messreihe ohne
`max()` und geben Sie diese am Ende aus.

**Abschlussfrage:** Bei welcher Kraft aus der Liste wird die Streckgrenze
erstmals überschritten, und was bedeutet das physikalisch für die
Werkstoffprobe?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
def spannung(kraft_n, querschnitt_mm2):
    """Berechnet die mechanische Spannung in MPa (N/mm²)."""
    return kraft_n / querschnitt_mm2

versuch = {
    'werkstoff': 'S235JR',
    'querschnitt_mm2': 19.6,
    'streckgrenze_mpa': 235.0
}

kraefte_n = [1200, 3400, 5800, 7200, 8100, 6500]

maximale_spannung = 0
erste_ueberschreitung_kraft = 0
ueberschreitung_gefunden = False

for kraft in kraefte_n:
    sigma = spannung(kraft, versuch['querschnitt_mm2'])

    if sigma > versuch['streckgrenze_mpa']:
        status = 'Streckgrenze überschritten'
        if not ueberschreitung_gefunden:
            erste_ueberschreitung_kraft = kraft
            ueberschreitung_gefunden = True
    else:
        status = 'Im elastischen Bereich'

    print(f'{kraft} N -> {sigma:.1f} MPa: {status}')

    if sigma > maximale_spannung:
        maximale_spannung = sigma

print(f'Maximale Spannung: {maximale_spannung:.1f} MPa')
print(f'Erste Überschreitung bei {erste_ueberschreitung_kraft} N')
```
Die Streckgrenze von 235.0 MPa wird erstmals bei 5800 N überschritten, dort
beträgt die Spannung rund 295.9 MPa. Die maximale Spannung der gesamten
Messreihe tritt bei der größten Kraft von 8100 N auf und beträgt rund
413.3 MPa, denn die Spannung wächst bei konstantem Querschnitt proportional
zur Kraft.

Physikalisch bedeutet das Überschreiten der Streckgrenze, dass sich die
Werkstoffprobe ab diesem Belastungspunkt nicht mehr rein elastisch, sondern
plastisch verformt. Die Probe nimmt also eine bleibende Verformung an, die
auch nach einer vollständigen Entlastung nicht mehr verschwindet.
````
