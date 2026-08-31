---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.3 Listen, Dictionaries und Funktionen

In Kapitel 1.1 haben wir einzelne Messwerte in Variablen gespeichert und mit
einer Verzweigung geprüft, ob ein Tempolimit eingehalten wird. Ein Prüffahrzeug
liefert während eines Beschleunigungstests aber nicht nur einen einzelnen
Messwert, sondern eine ganze Messreihe. Eine einzelne Variable reicht dafür
nicht mehr aus. In diesem Kapitel lernen wir daher die Datenstrukturen
**Liste** und **Dictionary** kennen, mit denen wir mehrere Werte gemeinsam
verwalten. Anschließend kapseln wir wiederkehrende Berechnungen wie die
Umrechnung von km/h in m/s in eigenen **Funktionen**.

Wie in Kapitel 1.1 sind zur Vorbereitung wieder kurze Videos am Ende der
Abschnitte eingebettet.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie können **Listen** erzeugen, mit `append()` erweitern und über den
  **Index** auf Elemente zugreifen.
* [ ] Sie können **Dictionaries** mit Schlüssel-Wert-Paaren erstellen,
  lesen und verändern.
* [ ] Sie können eigene **Funktionen** mit `def` schreiben, Parameter
  verwenden und mit `return` einen Wert zurückgeben.
* [ ] Sie wissen, was ein **Default-Wert** und ein **Docstring** sind.
```

## Wie sammeln wir mehrere Messwerte in einer Liste?

Stellen wir uns einen Beschleunigungstest vor, bei dem ein Sensor die
Geschwindigkeit zu mehreren Zeitpunkten erfasst. Wir sammeln diese Werte in
einer **Liste**, erkennbar an den eckigen Klammern.

```{code-cell} python
geschwindigkeiten_kmh = [80, 95, 120, 60, 110]
print(geschwindigkeiten_kmh)
```

Eine Liste kann beliebig viele Elemente enthalten. Mit `len()` lassen wir
uns die Anzahl der Elemente anzeigen.

```{code-cell} python
anzahl_messungen = len(geschwindigkeiten_kmh)
print(f'Anzahl Messungen: {anzahl_messungen}')
```

Auf einzelne Elemente greifen wir über den **Index** zu. Python beginnt die
Zählung bei 0. Mit dem Index `-1` greifen wir bequem auf das letzte Element
zu.

```{code-cell} python
erste_messung = geschwindigkeiten_kmh[0]
letzte_messung = geschwindigkeiten_kmh[-1]
print(f'Erste Messung: {erste_messung} km/h')
print(f'Letzte Messung: {letzte_messung} km/h')
```

Um eine neue Messung am Ende der Liste zu ergänzen, verwenden wir die
Methode `append()`.

```{code-cell} python
geschwindigkeiten_kmh.append(75)
print(geschwindigkeiten_kmh)
```

Wenn wir jeden Messwert einer Liste verarbeiten wollen, durchlaufen wir die
Liste direkt mit einer for-Schleife, ohne den Umweg über `range()` und den
Index zu gehen.

```{code-cell} python
for geschwindigkeit in geschwindigkeiten_kmh:
    print(f'Messwert: {geschwindigkeit} km/h')
```

```{admonition} Mini-Übung (✩)
:class: tip
Erstellen Sie eine Liste `temperaturen` mit fünf Temperaturmesswerten Ihrer
Wahl. Hängen Sie einen weiteren Messwert mit `append()` an und geben Sie
anschließend die Anzahl der Elemente mit `len()` aus.

Beantworten Sie zusätzlich, ohne den Code auszuführen: Was gibt
`temperaturen[-2]` zurück, nachdem Sie den sechsten Wert angehängt haben?
Begründen Sie Ihre Antwort.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
temperaturen = [18.5, 19.2, 21.0, 22.4, 20.1]
temperaturen.append(23.7)
anzahl = len(temperaturen)
print(f'Anzahl Messwerte: {anzahl}')
```
`temperaturen[-2]` gibt das vorletzte Element der Liste zurück, also den
Wert `22.4`. Der Index `-1` zeigt auf das letzte Element (`23.7`, der gerade
angehängte Wert), `-2` zeigt auf das Element direkt davor.
````

```{dropdown} Video "Listen in Python - Einführung" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/ihF8bZoauBs" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video "Zugriff auf Listen" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/_XzWPXvya2w?si=50tgXK-UUqOpQS8E"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "for-Schleife mit Listen" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/_XzWPXvya2w?si=50tgXK-UUqOpQS8E"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Wie strukturieren wir Daten mit Schlüsseln?

Eine Liste wie `[200.0, 'Pruefstand_1', 'Sensor_A']` speichert mehrere Werte,
aber *wie behalten wir bei einer längeren Liste den Überblick, welcher Wert
wofür steht?* Bei Index 0 müssten wir uns merken, dass dort der Messbereich
steht, bei Index 1 der Standort und bei Index 2 der Name. Für solche Fälle
eignet sich das **Dictionary** besser, da wir über aussagekräftige Schlüssel
statt über einen numerischen Index zugreifen.

```{code-cell} python
sensor = {
    'name': 'Sensor_A',
    'standort': 'Pruefstand_1',
    'messbereich_max': 200.0
}
print(sensor)
```

Der Zugriff auf einen Wert erfolgt über den zugehörigen Schlüssel in eckigen
Klammern.

```{code-cell} python
print(f'Sensor: {sensor["name"]}')
print(f'Standort: {sensor["standort"]}')
```

Wir können bestehende Werte ändern oder neue Schlüssel-Wert-Paare ergänzen.

```{code-cell} python
sensor['messbereich_max'] = 250.0
sensor['kalibrierdatum'] = '2026-01-15'
print(sensor)
```

```{admonition} Mini-Übung (✩)
:class: tip
Erstellen Sie ein Dictionary `messung` für einen Temperaturmesswert mit den
Schlüsseln `temperatur` (23.5), `ort` (`'Pruefstand_2'`) und `zeitstempel`
(`'14:32'`). Geben Sie Temperatur und Ort mit passenden Beschriftungen aus.

Beantworten Sie zusätzlich: Warum wäre eine Liste `[23.5, 'Pruefstand_2',
'14:32']` für diese Daten weniger geeignet als ein Dictionary? Formulieren
Sie Ihre Antwort in eigenen Worten.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
messung = {
    'temperatur': 23.5,
    'ort': 'Pruefstand_2',
    'zeitstempel': '14:32'
}
print(f'Temperatur: {messung["temperatur"]} Grad Celsius')
print(f'Ort: {messung["ort"]}')
```
Bei der Liste müssten wir uns merken, dass Index 0 die Temperatur, Index 1
den Ort und Index 2 den Zeitstempel enthält. Diese Zuordnung ist für
Außenstehende nicht erkennbar und fehleranfällig, sobald sich die
Reihenfolge ändert. Das Dictionary macht die Bedeutung jedes Werts über den
Schlüssel sofort sichtbar.
````

```{dropdown} Video "Dictionaries" von Pitrium
<iframe width="560" height="315"
src="https://www.youtube.com/embed/fQGQ4MIBKBY?si=w4hfWIM4n_PyuF5i"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Wie kapseln wir Berechnungen in Funktionen?

In Kapitel 1.1 haben wir die Formel `geschwindigkeit_kmh / 3.6` zur
Umrechnung in m/s mehrfach von Hand hingeschrieben. Mit einer eigenen
**Funktion** kapseln wir diese Berechnung, sodass wir sie nur einmal
definieren und beliebig oft wiederverwenden können.

```{code-cell} python
def kmh_zu_ms(geschwindigkeit_kmh):
    geschwindigkeit_ms = geschwindigkeit_kmh / 3.6
    return geschwindigkeit_ms

geschwindigkeit_ms = kmh_zu_ms(95)
print(geschwindigkeit_ms)
```

Eine Funktion beginnt mit dem Schlüsselwort `def`, gefolgt vom Funktionsnamen
und den **Parametern** in runden Klammern. Auch hier schließt die Kopfzeile
mit einem Doppelpunkt `:` ab und der Funktionskörper ist eingerückt. Das
Schlüsselwort `return` legt fest, welcher Wert an die aufrufende Stelle
zurückgegeben wird. Sobald die Funktion definiert ist, rufen wir sie beliebig
oft mit unterschiedlichen Argumenten auf, zum Beispiel für jeden Messwert
unserer Liste.

```{code-cell} python
for geschwindigkeit in geschwindigkeiten_kmh:
    print(f'{geschwindigkeit} km/h entsprechen {kmh_zu_ms(geschwindigkeit):.1f} m/s')
```

Eine Funktion kann mehrere Parameter besitzen. Schreiben wir hinter einen
Parameter ein `=` mit einem Wert, ist das ein **Default-Wert**: Rufen wir die
Funktion ohne dieses Argument auf, verwendet Python automatisch den
Default-Wert.

```{code-cell} python
def kinetische_energie(geschwindigkeit_ms, masse=1200):
    return 0.5 * masse * geschwindigkeit_ms**2

print(f'{kinetische_energie(27.8):.1f} Joule')            # masse = 1200
print(f'{kinetische_energie(27.8, masse=1500):.1f} Joule')
```

Direkt unter der Kopfzeile einer Funktion können wir in dreifachen
Anführungszeichen einen **Docstring** notieren, einen kurzen Satz, der
beschreibt, was die Funktion tut.

```{code-cell} python
def kmh_zu_ms(geschwindigkeit_kmh):
    """Rechnet eine Geschwindigkeit von km/h in m/s um."""
    return geschwindigkeit_kmh / 3.6
```

```{dropdown} Video "Funktionen selbst definieren" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/LQCfN5HS9xI" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

```{dropdown} Video "Funktionen mit Parametern" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/af9ORp1Pty0" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video "Funktionen mit Rückgabewert" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/ehSP-sYoKCY" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{admonition} Mini-Übung (✩)
:class: tip
Schreiben Sie eine Funktion `bremsweg(geschwindigkeit_kmh)`, die den
Bremsweg nach der Faustformel `(geschwindigkeit_kmh / 10) ** 2 / 2`
zurückgibt. Rufen Sie die Funktion für `geschwindigkeit_kmh = 100` auf und
geben Sie das Ergebnis aus.

Beantworten Sie zusätzlich, ohne den Code auszuführen: Was gibt der
Funktionsaufruf zurück, wenn Sie in der Funktion das Schlüsselwort `return`
vergessen? Begründen Sie Ihre Antwort.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
def bremsweg(geschwindigkeit_kmh):
    return (geschwindigkeit_kmh / 10) ** 2 / 2

print(f'Bremsweg: {bremsweg(100):.1f} m')
```
Ohne `return` gibt die Funktion automatisch den Wert `None` zurück. Die
Berechnung innerhalb der Funktion würde zwar durchgeführt, das Ergebnis
ginge aber verloren, da es nicht an die aufrufende Stelle zurückgegeben
wird.
````

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir gelernt, wie wir mehrere Messwerte in einer
**Liste** sammeln, mit aussagekräftigen Schlüsseln in einem **Dictionary**
strukturieren und wiederkehrende Berechnungen in eigenen **Funktionen** mit
Parametern und Rückgabewerten kapseln. Damit besitzen wir nun das
Handwerkszeug, um die Messreihen aus unseren Beschleunigungstests zu
verarbeiten.

Einige Python-Themen haben wir bewusst ausgespart und holen sie später nach,
wenn wir sie brauchen, zum Beispiel die Fehlerbehandlung mit `try` und
`except` bei den numerischen Verfahren. In Kapitel 2 verwenden wir **NumPy**
und **Matplotlib**, um ganze Messreihen wie `geschwindigkeiten_kmh` ohne
eigene Schleife auf einmal zu verarbeiten und grafisch darzustellen.
