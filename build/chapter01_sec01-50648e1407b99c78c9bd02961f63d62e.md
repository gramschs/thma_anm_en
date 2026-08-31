---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 1.1 Variablen, Operatoren und Kontrollstrukturen

In der Fahrzeugentwicklung liefern Sensoren laufend Messwerte: die
Geschwindigkeit eines Prüffahrzeugs, die Kraft an einem Prüfstand oder die
Temperatur eines Bauteils. Bevor wir solche Messreihen in den folgenden
Kapiteln mit numerischen Verfahren auswerten, brauchen wir das Handwerkszeug
der Programmiersprache Python. In diesem Kapitel lernen wir, wie wir
einzelne Messwerte in Variablen speichern, mit ihnen rechnen und den Ablauf
unseres Programms mit Verzweigungen und Schleifen steuern.

Wir arbeiten dabei mit Jupyter Notebooks. Ein Notebook besteht aus einzelnen
Code-Zellen, die wir nacheinander ausführen. Das Ergebnis einer Zelle
erscheint direkt darunter, sodass wir unseren Code Schritt für Schritt
aufbauen und testen können. Probieren wir das gleich anhand eines ersten
Beispiels aus.

Wer noch nie programmiert hat, kann sich zur Vorbereitung die kurzen Videos
ansehen, die in diesem Kapitel jeweils am Ende eines Abschnitts eingebettet
sind.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie kennen die Datentypen **Integer**, **Float** und **String** und
  können sie mit `type()` unterscheiden.
* [ ] Sie können Variablen erzeugen, mit der **print()**-Funktion ausgeben
  und mit **f-Strings** formatieren.
* [ ] Sie kennen arithmetische, Vergleichs- und logische **Operatoren** und
  den Unterschied zwischen Zuweisung `=` und Vergleich `==`.
* [ ] Sie können Programmabläufe mit **if/elif/else** verzweigen.
* [ ] Sie können eine **for-Schleife** mit `range()` schreiben.
```

## Wie speichern wir Messwerte in Variablen?

Stellen wir uns vor, ein Sensor an einem Prüffahrzeug misst die aktuelle
Geschwindigkeit. Wir wollen diesen Wert sowie weitere Informationen zur
Messung in unserem Programm speichern.

```{code-cell} python
geschwindigkeit = 27.8
anzahl_messungen = 50
sensorname = 'Sensor_A'
```

Wir nennen `geschwindigkeit`, `anzahl_messungen` und `sensorname`
**Variablen**. Eine Variable ist wie eine beschriftete Schublade: Wir geben
ihr einen Namen und legen einen Wert hinein. Das Hineinlegen nennen wir
**Zuweisung** und verwenden dafür das Gleichheitszeichen `=`. Technisch
gesehen ist die Schublade ein kleiner Bereich im Arbeitsspeicher des
Computers.

Als nächstes geben wir den Inhalt der Variablen auf dem Monitor oder Display
aus. Dazu benutzen wir die in Python eingebaute Funktion `print()`.

```{code-cell} python
print(geschwindigkeit)
print(anzahl_messungen)
print(sensorname)
```

Funktionen erkennen wir an den runden Klammern nach dem Funktionsnamen. Dort
hinein kommt das sogenannte **Argument**. Ein Argument ist sozusagen der Input,
der an die Funktion übergeben wird, damit Python weiß, welcher Wert auf dem
Bildschirm angezeigt werden soll.

Python unterscheidet die Werte in einer Variable nach ihrem **Datentyp**. In
diesem Abschnitt lernen wir drei einfache Datentypen kennen:

* **Integer**: eine ganze Zahl, zum Beispiel die Anzahl der Messungen.
* **Float**: eine Kommazahl, zum Beispiel eine Geschwindigkeit in km/h. Das
  Dezimaltrennzeichen ist in Python immer ein Punkt, kein Komma.
* **String**: eine Zeichenkette, zum Beispiel der Name eines Sensors. Strings
  stehen in einfachen oder doppelten Anführungszeichen.

Mit der Funktion `type()` lassen wir uns den Datentyp einer Variable
anzeigen.

```{code-cell} python
print(type(geschwindigkeit))
print(type(anzahl_messungen))
print(type(sensorname))
```

Variablen lassen sich auch nachträglich verändern. Häufig schreiben wir Code
wie im folgenden Beispiel, um eine Variable um einen Wert zu erhöhen.

```{code-cell} python
anzahl_messungen = anzahl_messungen + 1
print(anzahl_messungen)
```

*Ist das nicht ein Widerspruch zur Mathematik?* In der Mathematik dürften
wir auf beiden Seiten der Gleichung `anzahl_messungen` subtrahieren und
kämen auf `0 = 1`, was offensichtlich falsch ist. Das Gleichheitszeichen `=`
ist in Python jedoch keine mathematische Gleichung, sondern eine
**Zuweisung**. Python berechnet zuerst den Wert auf der rechten Seite und
speichert das Ergebnis anschließend in der Variable auf der linken Seite.

Um Werte gemeinsam mit Text auszugeben, verwenden wir **f-Strings**. Dazu
setzen wir ein `f` direkt vor das Anführungszeichen und schreiben den
Variablennamen in geschweifte Klammern.

```{code-cell} python
print(f'Der Sensor {sensorname} misst eine Geschwindigkeit von {geschwindigkeit} km/h.')
```

Bei Floats können wir zusätzlich die Anzahl der Nachkommastellen festlegen.
Dazu schreiben wir hinter den Variablennamen einen Doppelpunkt, gefolgt von
der gewünschten Anzahl Nachkommastellen und einem `f`.

```{code-cell} python
pi = 3.141592653589793
print(f'Pi auf zwei Nachkommastellen: {pi:.2f}')
```

```{admonition} Mini-Übung (✩)
:class: tip
Legen Sie für eine Werkstoffprobe drei Variablen an: `masse` (Float, in kg),
`anzahl_pruefungen` (Integer) und `werkstoff` (String, zum Beispiel
`'Stahl'`). Geben Sie alle drei Werte mit `print()` aus und lassen Sie sich
anschließend den Datentyp von `masse` mit `type()` anzeigen.

Beantworten Sie zusätzlich, ohne den Code auszuführen: Welchen Datentyp
würde `type()` zurückgeben, wenn Sie stattdessen `masse = 5` ohne
Dezimalpunkt schreiben? Begründen Sie Ihre Antwort.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
masse = 4.85
anzahl_pruefungen = 3
werkstoff = 'Stahl'

print(masse)
print(anzahl_pruefungen)
print(werkstoff)
print(type(masse))
```
Bei `masse = 5` ohne Dezimalpunkt würde `type()` den Datentyp `int`
zurückgeben, da Python eine Zahl ohne Punkt als ganze Zahl interpretiert.
Erst der Dezimalpunkt macht aus einer Zahl einen Float.
````

```{dropdown} Video "Zahlen in Python" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/VtiDkRDPA_c?si=YvJ89BBqE0Eak8yG"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "Strings" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/sTEf4_mrLvw?si=fG01zUB72QxlgWYV"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "Variablen" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/jfOLXKPGXJ0" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

```{dropdown} Video "Datentypen" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/1WqFJ5wsA4o" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

## Wie rechnen und vergleichen wir in Python?

Aus der Physik-Grundvorlesung kennen wir bereits die SI-Einheit m/s für die
Geschwindigkeit. Sensordaten liegen aber häufig in km/h vor, daher rechnen
wir zunächst um.

```{code-cell} python
geschwindigkeit_kmh = 100
geschwindigkeit_ms = geschwindigkeit_kmh / 3.6
print(geschwindigkeit_ms)
```

Python kennt die üblichen arithmetischen Operatoren: `+` für die Addition,
`-` für die Subtraktion, `*` für die Multiplikation, `/` für die Division
und `**` für das Potenzieren. Mit diesen Operatoren berechnen wir
beispielsweise die kinetische Energie eines Fahrzeugs.

```{code-cell} python
masse = 1200                # kg
geschwindigkeit_ms = 27.8   # m/s

kinetische_energie = 0.5 * masse * geschwindigkeit_ms**2
print(f'Kinetische Energie: {kinetische_energie:.1f} Joule')
```

Neben dem Rechnen mit Zahlen müssen wir Werte oft auch vergleichen, zum
Beispiel um zu prüfen, ob ein Tempolimit eingehalten wird. Dafür stehen uns
**Vergleichsoperatoren** zur Verfügung: `>`, `<`, `>=`, `<=`, `==` für "ist
gleich" und `!=` für "ist ungleich". Das Ergebnis eines Vergleichs ist immer
ein **Wahrheitswert**, also entweder `True` oder `False`.

```{code-cell} python
tempolimit_ms = 33.3   # entspricht 120 km/h

print(geschwindigkeit_ms > tempolimit_ms)
print(geschwindigkeit_ms == tempolimit_ms)
```

```{admonition} Achtung: = ist nicht gleich ==
:class: warning
Das einfache Gleichheitszeichen `=` ist der Zuweisungsoperator und legt
einen Wert in einer Variable ab. Das doppelte Gleichheitszeichen `==`
vergleicht zwei Werte und gibt `True` oder `False` zurück. Diese
Verwechslung gehört zu den häufigsten Anfängerfehlern in Python.
```

Mehrere Bedingungen verknüpfen wir mit den **logischen Operatoren** `and` und
`or`. Bei `and` müssen beide Bedingungen wahr sein, bei `or` genügt eine.

```{code-cell} python
ist_schnell = geschwindigkeit_ms > 25
ist_im_limit = geschwindigkeit_ms <= tempolimit_ms

print(ist_schnell and ist_im_limit)
```

Mit dem Operator `not` kehren wir einen Wahrheitswert um, aus `True` wird
`False` und umgekehrt.

```{admonition} Mini-Übung (✩)
:class: tip
Berechnen Sie den Bremsweg eines Fahrzeugs nach der Faustformel
`bremsweg = (geschwindigkeit_kmh / 10) ** 2 / 2`. Verwenden Sie
`geschwindigkeit_kmh = 80` und geben Sie das Ergebnis mit einem f-String und
einer Nachkommastelle aus.

Beantworten Sie zusätzlich ohne Ausführen des Codes: Was gibt der Ausdruck
`5 == 5.0` zurück, obwohl ein Integer und ein Float verglichen werden?
Begründen Sie Ihre Antwort.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
geschwindigkeit_kmh = 80
bremsweg = (geschwindigkeit_kmh / 10) ** 2 / 2
print(f'Bremsweg: {bremsweg:.1f} m')
```
`5 == 5.0` gibt `True` zurück. Python vergleicht beim `==`-Operator den
Zahlenwert, nicht den Datentyp. Da 5 und 5.0 denselben Zahlenwert besitzen,
ist der Vergleich wahr, obwohl `type(5)` und `type(5.0)` unterschiedliche
Datentypen liefern.
````

```{dropdown} Video "Zuweisungsoperator" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/XKFQ2_et5k8?si=d0qZ9ENucDPQRMi6"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "Vergleiche" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/ucsv_Nhhxmk?si=9VdPcN0JR2Rubn4d"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "Logische Operatoren" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/075l6R42tkQ?si=mgnUloDE3AhdfIDX"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

## Wie steuert unser Programm den Ablauf?

Bisher wurde jede Zeile unseres Programms genau einmal ausgeführt. Häufig
wollen wir aber abhängig von einer Bedingung unterschiedlichen Code
ausführen, zum Beispiel je nachdem, ob ein Tempolimit eingehalten wird.

```{code-cell} python
geschwindigkeit_ms = 35.0
tempolimit_ms = 33.3

if geschwindigkeit_ms > tempolimit_ms:
    print('Geschwindigkeit zu hoch!')
elif geschwindigkeit_ms == tempolimit_ms:
    print('Geschwindigkeit genau am Limit.')
else:
    print('Geschwindigkeit im erlaubten Bereich.')
```

Diese Struktur nennen wir **Verzweigung**. Die Zeile mit `if` heißt
**Kopfzeile** und wird mit einem Doppelpunkt `:` abgeschlossen. Alle
Anweisungen, die zu dieser Bedingung gehören, rücken wir um die gleiche
Anzahl von Leerzeichen ein. Diese **Einrückung** zeigt Python, welcher Code
zusammengehört. Mit `elif` (kurz für "else if") prüfen wir eine weitere
Bedingung, mit `else` fangen wir alle übrigen Fälle ab.

Oft müssen wir eine Anweisung mehrfach wiederholen, zum Beispiel um mehrere
Zeitschritte einer Messung zu simulieren. Dafür verwenden wir die
**for-Schleife** zusammen mit der Funktion `range()`.

```{code-cell} python
for zeitschritt in range(5):
    print(f'Zeitschritt {zeitschritt}: Messung wird durchgeführt.')
```

Die Kopfzeile besteht aus den festen Schlüsselwörtern `for` und `in`. Dazwischen
steht `zeitschritt`, die **Schleifenvariable**. Sie nimmt bei jedem Durchlauf
den nächsten Wert aus `range(5)` an, also nacheinander 0, 1, 2, 3 und 4, denn
`range(5)` erzeugt fünf Zahlen, beginnend bei 0. Die eingerückten Zeilen
darunter bilden den **Schleifenkörper** und werden bei jedem Durchlauf
ausgeführt.

Innerhalb des Schleifenkörpers dürfen wir auch eine Verzweigung verwenden,
zum Beispiel um für jeden Zeitschritt zu prüfen, ob ein Grenzwert
überschritten ist.

```{code-cell} python
for zeitschritt in range(5):
    geschwindigkeit_ms = zeitschritt * 12.0
    if geschwindigkeit_ms > tempolimit_ms:
        print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_ms:.1f} m/s, zu schnell!')
    else:
        print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_ms:.1f} m/s, im Limit.')
```

Die Schleife durchläuft alle fünf Zeitschritte. In jedem Durchlauf berechnen
wir die aktuelle Geschwindigkeit und entscheiden mit der `if`-Abfrage, welche
Meldung ausgegeben wird.

```{admonition} Mini-Übung (✩)
:class: tip
Schreiben Sie eine for-Schleife mit `range(5)`, die ausgehend von 0 km/h die
Geschwindigkeit in jedem Schleifendurchgang um 30 km/h erhöht und den
jeweiligen Wert ausgibt.

Ergänzen Sie im Schleifenkörper eine `if`-Abfrage, die zusätzlich
`zu schnell` ausgibt, sobald die Geschwindigkeit über 80 km/h liegt.
Beantworten Sie vor dem Ausführen: In welchen Durchgängen erscheint
`zu schnell`? Begründen Sie Ihre Antwort.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
for zeitschritt in range(5):
    geschwindigkeit_kmh = zeitschritt * 30
    print(f'Zeitschritt {zeitschritt}: {geschwindigkeit_kmh} km/h')
    if geschwindigkeit_kmh > 80:
        print('zu schnell')
```
Die Schleifenvariable `zeitschritt` läuft durch die Werte 0 bis 4, die
Geschwindigkeit nimmt die Werte 0, 30, 60, 90 und 120 km/h an. `zu schnell`
erscheint in den Durchgängen 3 und 4, denn dort liegt die Geschwindigkeit mit
90 beziehungsweise 120 km/h über der Grenze von 80 km/h.
````

```{dropdown} Video "if-Anweisung" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/b6KzYbM-Hvg?si=nv1PyfW57Y6wO-_g"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "if, elif, else" von Programmieren Starten
<iframe width="560" height="315"
src="https://www.youtube.com/embed/f3YdEdYSNdk?si=qazZv5vzNL7PQTlt"
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay;
clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

```{dropdown} Video "for-Schleife in Python: Zählerschleife" von Programmieren Starten
<iframe width="560" height="315" src="https://www.youtube.com/embed/pQh5Idw2sKM" 
title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>
```

## Zusammenfassung und Ausblick

In diesem Kapitel haben wir die Grundbausteine von Python kennengelernt:
Variablen zum Speichern von Messwerten, die Datentypen Integer, Float und
String, arithmetische, Vergleichs- und logische Operatoren sowie die
Verzweigung mit `if`/`elif`/`else` und die `for`-Schleife zur Wiederholung.
Damit können wir bereits einzelne Werte verarbeiten und wiederkehrende
Berechnungen automatisieren.

Was uns aber noch fehlt, ist eine Möglichkeit, mehrere Messwerte gemeinsam
zu verwalten. Im nächsten Kapitel 1.2 vertiefen wir das Gelernte an
Prüfstandsaufgaben. In Kapitel 1.3 lernen wir dann die Datenstrukturen
**Liste** und **Dictionary** kennen und schreiben eigene **Funktionen**, um
wiederkehrende Berechnungen wie die Umrechnung von km/h in m/s zu kapseln. In
Kapitel 2 verwenden wir schließlich **NumPy** und **Matplotlib**, um ganze
Messreihen ohne Schleifen zu verarbeiten und grafisch darzustellen.
