---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.1 NumPy-Grundlagen

In der Messtechnik fallen schnell tausende von Messwerten an. Ein
Beschleunigungssensor, der eine vibrierende Maschine überwacht, liefert
beispielsweise 10.000 Messwerte pro Sekunde. Wollen wir diese Daten mit
Python-Listen verarbeiten, brauchen wir Schleifen über tausende von Elementen:
mühsam zu schreiben und langsam in der Ausführung. In diesem Kapitel lernen wir
NumPy kennen, eine Bibliothek, die genau für solche Aufgaben gebaut wurde. Ihr
zentraler Datentyp, das **Array**, erlaubt es, mathematische Operationen und
statistische Kenngrößen direkt auf ganze Zahlenreihen anzuwenden, ohne eine
einzige Schleife zu schreiben.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie wissen, was ein **NumPy-Array** ist und wie es sich von einer
  Python-Liste unterscheidet.
* [ ] Sie können ein Array mit `np.array()`, `np.linspace()` und `np.zeros()`
  erzeugen.
* [ ] Sie können **Vektoroperationen** (elementweise Addition, Multiplikation,
  Skalierung) auf Arrays anwenden.
* [ ] Sie können mathematische Funktionen wie `np.sin()` und `np.exp()` auf
  Arrays anwenden.
* [ ] Sie können mit `np.mean()`, `np.std()`, `np.min()` und `np.max()`
  statistische Kenngrößen eines Arrays berechnen.
```

## Was ist ein NumPy-Array?

NumPy (kurz für *Numerical Python*) ist eine Bibliothek, also eine Sammlung
fertiger Funktionen, die wir in eigenem Code nutzen können, ohne sie selbst
zu schreiben. Bevor wir eine Bibliothek verwenden können, müssen wir sie mit
`import` laden. Für NumPy hat sich eine feste Abkürzung etabliert, unter der
wir die Bibliothek im restlichen Code ansprechen:

```{code-cell} python
import numpy as np
```

Diese Zeile lädt die Bibliothek `numpy` und macht sie im Code über den Namen
`np` verfügbar. Ab jetzt rufen wir alle Funktionen aus NumPy mit diesem
Kürzel auf, zum Beispiel `np.array()`. Die Abkürzung `np` ist reine
Konvention, ein anderer Name würde technisch genauso funktionieren, aber
`np` ist in der Python-Welt so verbreitet, dass praktisch jeder NumPy-Code
sie verwendet.

Der zentrale Datentyp von NumPy ist das **Array**. Es erlaubt uns,
mathematische Operationen direkt auf ganze Zahlenreihen anzuwenden, ohne
eine einzige Schleife zu schreiben, wie wir im Folgenden sehen.

Den Unterschied zwischen Liste und Array sehen wir am schnellsten an einem
Beispiel. Ein Sensor liefert fünf Beschleunigungswerte in m/s^2:

```{code-cell} python
# Beschleunigungen in m/s^2 als Python-Liste
messwerte_liste = [0.3, 1.2, 2.5, 1.8, 0.7]

# Beschleunigungen in m/s^2 als NumPy-Array
messwerte_array = np.array([0.3, 1.2, 2.5, 1.8, 0.7])

print(messwerte_liste)
print(messwerte_array)
```

Auf den ersten Blick sehen Liste und Array ähnlich aus. Ein NumPy-Array ist
jedoch speziell für numerische Daten und mathematische Berechnungen ausgelegt.
Dadurch können wir Rechenoperationen direkt auf ganze Messreihen anwenden.
Zunächst sehen wir uns jedoch weitere Möglichkeiten an, ein NumPy-Array zu
erzeugen.

Neben `np.array()`, das eine bestehende Liste in ein Array umwandelt, stellt
NumPy zwei weitere Funktionen bereit, mit denen wir Arrays direkt erzeugen, ohne
die Werte einzeln aufzuschreiben.

`np.linspace(start, stop, anzahl)` erzeugt `anzahl` gleichmäßig verteilte Werte
zwischen `start` und `stop`. Der Endwert `stop` ist dabei standardmäßig
enthalten. Das eignet sich beispielsweise für Zeitachsen:

```{code-cell} python
t = np.linspace(0, 2, 5)    # 5 Werte zwischen 0 und 2 Sekunden
print(t)
```

In der Ausgabe steht hinter jeder ganzen Zahl ein Punkt, also `0.` statt `0`.
`np.linspace()` erzeugt die Werte immer als Fließkommazahlen, auch wenn wir
ganzzahlige Grenzen angeben. Das ist beabsichtigt, denn die gleichmäßig
verteilten Zwischenwerte einer Achse sind im Allgemeinen keine ganzen Zahlen.

`np.zeros(anzahl)` erzeugt ein Array aus lauter Nullen. Das ist nützlich, um
ein Array als Platzhalter anzulegen, das später mit Werten gefüllt wird:

```{code-cell} python
platzhalter = np.zeros(5)   # Platzhalter mit 5 Nullen 
print(platzhalter)
```

Mit diesen drei Funktionen, `np.array()`, `np.linspace()` und `np.zeros()`,
decken wir bereits die meisten Fälle ab, in denen wir ein Array neu anlegen
müssen: aus vorhandenen Werten, als gleichmäßig verteilte Achse oder als
Platzhalter.

Bevor wir mit den erzeugten Arrays weiterrechnen, prüfen wir ihre grundlegenden
Eigenschaften: Größe und Datentyp.

```{code-cell} python
print(messwerte_array.shape)   # Anzahl der Elemente je Dimension
print(messwerte_array.dtype)   # Datentyp der gespeicherten Werte
```

`.shape` gibt die Abmessungen des Arrays als Tupel zurück. `(5,)` bedeutet: eine
Dimension mit fünf Elementen. `.dtype` gibt den gemeinsamen Datentyp aller
Elemente zurück, hier typischerweise `float64` für Fließkommazahlen. Diese
beiden Attribute sind der schnellste Weg, ein unbekanntes Array zu prüfen.

```{admonition} Mini-Übung (✩)
:class: tip
Ein Temperatursensor liefert vier Messwerte in °C: `18.5`, `19.2`, `18.9`,
`20.1`.

1. Legen Sie die Werte in einem Array namens `temperaturen` ab.
2. Geben Sie Form und Datentyp von `temperaturen` aus.
3. Legen Sie eine Zeitachse `zeit` mit vier gleichmäßig verteilten Werten
   zwischen 0 und 3 Sekunden an, ohne die Werte einzeln aufzuschreiben.
4. Legen Sie ein Array `kalibrierwerte` mit vier Nullen an, das später als
   Platzhalter für Kalibrierfaktoren dienen soll.
5. Beantworten Sie ohne Ausführen: Welchen Datentyp gibt `zeit.dtype` zurück,
   obwohl Sie in `np.linspace()` nur die ganzen Zahlen 0 und 3 als Grenzen
   angegeben haben? Begründen Sie Ihre Antwort.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

temperaturen = np.array([18.5, 19.2, 18.9, 20.1])
print(temperaturen.shape)   # (4,)
print(temperaturen.dtype)   # float64

zeit = np.linspace(0, 3, 4)
print(zeit)                 # [0. 1. 2. 3.]

kalibrierwerte = np.zeros(4)
print(kalibrierwerte)       # [0. 0. 0. 0.]
```
`zeit.dtype` gibt `float64` zurück. `np.linspace()` erzeugt seine Werte
grundsätzlich als Fließkommazahlen, weil die berechneten Zwischenwerte einer
Achse im Allgemeinen nicht ganzzahlig sind. Deshalb speichert NumPy auch die
zufällig ganzzahligen Werte 0, 1, 2 und 3 als Floats, erkennbar am Punkt in der
Ausgabe `[0. 1. 2. 3.]`.
````

## Vektoroperationen und mathematische Funktionen

Im letzten Abschnitt haben wir Arrays erzeugt und uns ihre Struktur mit
`.shape` und `.dtype` angesehen. Jetzt sehen wir, was Arrays wirklich
nützlich macht: Rechenoperationen, die auf ganze Zahlenreihen wirken, ohne
eine einzige Schleife zu schreiben.

Angenommen, wir wollen aus den Beschleunigungswerten die wirkende Kraft
berechnen. Es gilt $F = m \cdot a$, wobei die Masse $m = 5\,\mathrm{kg}$
beträgt. Mit einer Python-Liste brauchen wir dafür eine Schleife:

```{code-cell} python
# Mit der Liste: manuelle Schleife notwendig
kraefte_liste = []
for a in messwerte_liste:
    kraefte_liste.append(5.0 * a)

print(kraefte_liste)
```

Mit dem NumPy-Array genügt eine einzige Zeile:

```{code-cell} python
kraefte_array = 5.0 * messwerte_array
print(kraefte_array)
```

Die Multiplikation mit dem Skalar `5.0` wird automatisch auf **jedes Element**
von `messwerte_array` angewendet. Solche Operationen auf ganzen Zahlenreihen
nennen wir **Vektoroperationen**. Sie vermeiden explizite Schleifen und sind
daher bei großen Messreihen in der Regel deutlich effizienter.

*Ist dieser Unterschied bei fünf Messwerten überhaupt spürbar?* Bei fünf Werten
nicht. Sobald ein Sensor aber mehrere tausend Werte pro Sekunde liefert,
entscheidet die Vektoroperation darüber, ob eine Auswertung Sekundenbruchteile
oder mehrere Minuten dauert.

Dasselbe Prinzip gilt für die Grundrechenarten `+`, `-`, `*`, `/` und `**`.
Addieren wir zwei eindimensionale Arrays gleicher Länge, werden ihre Elemente
paarweise addiert:

```{code-cell} python
sensor_a = np.array([0.3, 1.2, 2.5, 1.8, 0.7])
sensor_b = np.array([0.1, 0.2, 0.3, 0.1, 0.2])

summe = sensor_a + sensor_b
print(summe)
```

Das erste Element von `sensor_a` wird dabei mit dem ersten Element von
`sensor_b` addiert, das zweite mit dem zweiten und so weiter. Da beide Arrays
fünf Elemente enthalten, ist diese Zuordnung von Partnern eindeutig.

Für eindimensionale Arrays ist eine paarweise Operation normalerweise nur
möglich, wenn beide Arrays dieselbe Länge besitzen. Bei mehrdimensionalen
Arrays müssen die Formen (`.shape`) der Arrays zueinander passen. NumPy kann
unter bestimmten Bedingungen auch unterschiedlich geformte Arrays kombinieren;
diese Regeln heißen **Broadcasting** und werden später behandelt.

Neben den Grundrechenarten stellt NumPy auch mathematische Funktionen
bereit, die elementweise auf Arrays wirken. Zwei davon brauchen wir häufig:
`np.sin()` für trigonometrische Berechnungen und `np.exp()` für
Exponentialfunktionen.

```{code-cell} python
winkel = np.linspace(0, 2 * np.pi, 5)
print(np.sin(winkel))
```

`np.sin()` wendet den Sinus auf jedes Element von `winkel` einzeln an und
gibt ein neues Array derselben Länge zurück. In der Ausgabe fällt auf, dass bei
den Winkeln $\pi$ und $2\pi$ nicht exakt `0` steht, sondern ein winziger Wert in
der Größenordnung `1e-16`. Der exakte Sinus wäre an diesen Stellen null. Diese
kleine Abweichung ist ein **Rundungsfehler** der Fließkomma-Arithmetik, mit dem
wir bei numerischen Rechnungen grundsätzlich rechnen müssen.

`np.exp()` funktioniert nach demselben Prinzip:

```{code-cell} python
werte = np.array([0.0, 1.0, 2.0, 3.0])
print(np.exp(werte))
```

Python bringt mit dem Modul `math` bereits `math.sin()` und `math.exp()` mit,
diese akzeptieren aber nur einzelne Zahlen, keine Arrays. Um sie auf mehrere
Werte anzuwenden, bräuchten wir wieder eine Schleife. Die NumPy-Varianten
`np.sin()` und `np.exp()` sind für Arrays gebaut und damit in dieser Vorlesung
die richtige Wahl.

````{admonition} Mini-Übung (✩)
:class: tip
An einem Kran ziehen zwei Seile mit folgenden Kräften in kN, gemessen an
vier Zeitpunkten:

```python
seil_1 = np.array([120.0, 135.0, 128.0, 140.0])
seil_2 = np.array([80.0, 75.0, 82.0, 78.0])
```

1. Berechnen Sie die Summe der Beträge beider Seilzugkräfte an jedem Zeitpunkt
   und speichern Sie sie in `summe_seilkraefte_kn`.
2. Rechnen Sie `summe_seilkraefte_kn` in Newton um und speichern Sie das Ergebnis
   in `summe_seilkraefte_newton` (1 kN = 1000 N).
3. Seil 1 ist gegenüber der Horizontalen geneigt. Der Winkel beträgt an den
   vier Zeitpunkten in rad:

```python
   winkel = np.array([0.50, 0.55, 0.52, 0.58])
```

   Berechnen Sie die vertikale Komponente der Kraft in Seil 1 und speichern
   Sie sie in `seil_1_vertikal`.
4. Beantworten Sie ohne Ausführen: Wie viele Elemente hat `seil_1 * np.sin(winkel)`,
   und welcher Winkel gehört zum dritten Element von `seil_1`? Ist die vertikale
   Komponente an jedem Zeitpunkt größer oder kleiner als die Gesamtkraft im Seil?
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

seil_1 = np.array([120.0, 135.0, 128.0, 140.0])
seil_2 = np.array([80.0, 75.0, 82.0, 78.0])

summe_seilkraefte_kn = seil_1 + seil_2
print(summe_seilkraefte_kn)

summe_seilkraefte_newton = summe_seilkraefte_kn * 1000.0
print(summe_seilkraefte_newton)

winkel = np.array([0.50, 0.55, 0.52, 0.58])
seil_1_vertikal = seil_1 * np.sin(winkel)
print(seil_1_vertikal)
```
`seil_1 * np.sin(winkel)` hat wieder vier Elemente, da NumPy die beiden Arrays
elementweise multipliziert. Das dritte Element von `seil_1` (128.0 kN) gehört
zum dritten Winkel (0.52 rad). Die vertikale Komponente ist an jedem Zeitpunkt
kleiner als die Gesamtkraft im Seil, weil der Sinus für Winkel zwischen 0 und
$\pi/2$ Werte zwischen 0 und 1 liefert.
````

## Statistische Kenngrößen

Bisher haben wir einzelne Werte eines Arrays betrachtet oder das ganze Array
auf einmal transformiert. Oft interessiert uns aber nicht jeder einzelne
Wert, sondern eine zusammenfassende Kennzahl: Wie groß ist ein Messwert im
Mittel? Wie stark schwanken die Werte? NumPy stellt dafür Funktionen
bereit, die aus einem Array eine einzelne Zahl berechnen.

Als Datengrundlage nehmen wir eine Messreihe: die Spitzenbeschleunigung, die
ein Sensor bei zwölf aufeinanderfolgenden Testläufen derselben Maschine
aufgezeichnet hat.

```{code-cell} python
spitzenwerte = np.array([4.8, 5.1, 4.6, 5.3, 4.9, 5.0,
                         4.7, 5.2, 4.9, 5.4, 4.8, 5.0])
print(spitzenwerte)
```

Mit den NumPy-Funktionen `np.mean()`, `np.min()` und `np.max()` berechnen wir
Mittelwert, Minimum und Maximum. `np.mean()` addiert alle Werte und teilt durch
die Anzahl der Elemente, genau wie eine Mittelwertberechnung von Hand, nur ohne
Schleife. `np.min()` und `np.max()` liefern den kleinsten beziehungsweise
größten Wert im Array.

```{code-cell} python
print(f"Mittelwert: {np.mean(spitzenwerte):.2f} m/s^2")
print(f"Minimum:    {np.min(spitzenwerte):.2f} m/s^2")
print(f"Maximum:    {np.max(spitzenwerte):.2f} m/s^2")
```

Die Standardabweichung beschreibt, wie stark die einzelnen Werte im Mittel vom
Mittelwert abweichen. Eine kleine Standardabweichung bedeutet, dass die
Testläufe sehr ähnliche Spitzenwerte lieferten. Eine große Standardabweichung
zeigt, dass die Maschine von Lauf zu Lauf deutlich unterschiedlich reagiert.
Berechnet wird die Standardabweichung mit `np.std()`.

```{code-cell} python
print(f"Standardabweichung: {np.std(spitzenwerte):.3f} m/s^2")
```

`np.mean()`, `np.std()`, `np.min()` und `np.max()` lassen sich auch direkt
als Methode des Arrays aufrufen: `spitzenwerte.mean()` liefert dasselbe
Ergebnis wie `np.mean(spitzenwerte)`. Beide Schreibweisen sind gebräuchlich.
In diesem Skript verwenden wir durchgehend die Funktionsschreibweise
`np.funktion(array)`, weil sie unabhängig davon funktioniert, ob wir mit
einem Array oder einer gewöhnlichen Liste arbeiten.

Mit diesen vier Funktionen lässt sich jede Messreihe auf einen Blick
charakterisieren: ein typischer Wert durch den Mittelwert, die Streuung durch
die Standardabweichung und die Extremwerte durch Minimum und Maximum. Das sind
die ersten Werkzeuge, um aus reinen Zahlenreihen belastbare Aussagen über ein
gemessenes System abzuleiten.

````{admonition} Mini-Übung (✩)
:class: tip
Bei einer Qualitätsprüfung wird das Anzugsmoment von zehn Schrauben
gemessen, in Nm:

```python
momente = np.array([45.2, 44.8, 46.1, 45.5, 44.9,
                     45.8, 46.3, 44.6, 45.1, 45.9])
```

1. Bestimmen Sie das mittlere Anzugsmoment und speichern Sie es in
   `mittleres_moment`.
2. Bestimmen Sie, wie stark die Werte im Mittel um diesen Mittelwert
   streuen, und speichern Sie das Ergebnis in `streuung`.
3. Bestimmen Sie das kleinste und das größte gemessene Moment und speichern
   Sie sie in `min_moment` und `max_moment`.
4. Berechnen Sie aus `min_moment` und `max_moment` die Spannweite der
   Messung (Differenz zwischen größtem und kleinstem Wert) und speichern
   Sie sie in `spannweite`.
5. Schätzen Sie vor dem Ausführen: Liegt `streuung` eher bei 0.6 Nm oder eher
   bei 6 Nm? Begründen Sie mit einem Blick auf die zehn Messwerte.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np

momente = np.array([45.2, 44.8, 46.1, 45.5, 44.9,
                     45.8, 46.3, 44.6, 45.1, 45.9])

mittleres_moment = np.mean(momente)
print(f"Mittelwert: {mittleres_moment:.2f} Nm")

streuung = np.std(momente)
print(f"Streuung:   {streuung:.3f} Nm")

min_moment = np.min(momente)
max_moment = np.max(momente)
print(f"Minimum:    {min_moment:.2f} Nm")
print(f"Maximum:    {max_moment:.2f} Nm")

spannweite = max_moment - min_moment
print(f"Spannweite: {spannweite:.2f} Nm")
```
Alle Messwerte liegen dicht zwischen 44.6 Nm und 46.3 Nm, also in einem Band von
nur rund 1.7 Nm Breite. Die Standardabweichung misst die mittlere Abweichung vom
Mittelwert und ist daher deutlich kleiner als diese Bandbreite, hier rund
0.6 Nm. Ein Wert von 6 Nm wäre unmöglich, da keine einzelne Abweichung so groß
ist.
````

## Zusammenfassung und Ausblick

Wir haben NumPy-Arrays als Alternative zu Python-Listen kennengelernt, mit
`np.array()`, `np.linspace()` und `np.zeros()` erzeugt und mit `.shape` und
`.dtype` untersucht. Vektoroperationen und Funktionen wie `np.sin()` und
`np.exp()` wenden wir direkt auf ganze Arrays an, ohne Schleifen zu
schreiben. Mit `np.mean()`, `np.std()`, `np.min()` und `np.max()` fassen wir
eine Messreihe in wenigen Kennzahlen zusammen.

Im nächsten Kapitel wenden wir diese Werkzeuge in einem zusammenhängenden
Projekt an und werten den Prüfstandslauf einer Windkraftanlage aus. Danach
lernen wir Matplotlib kennen, um ganze Messreihen grafisch darzustellen.
Zweidimensionale Arrays und lineare Gleichungssysteme folgen in Kapitel 3.
