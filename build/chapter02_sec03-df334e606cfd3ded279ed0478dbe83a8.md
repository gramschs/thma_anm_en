---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.3 Diagramme mit Matplotlib

In den Kapiteln 2.1 und 2.2 haben wir Messreihen als NumPy-Arrays berechnet und
mit `print()` ausgegeben. Eine Spalte aus zweihundert Zahlen sagt uns aber
wenig darüber, wie sich eine Größe verhält. Am Prüfstand eines Elektromotors
wollen wir zum Beispiel auf einen Blick sehen, wie Drehmoment, Leistung und
Wirkungsgrad von der Drehzahl abhängen. In diesem Kapitel lernen wir
**Matplotlib** kennen, die Standardbibliothek für Diagramme in Python, und
verwandeln unser Zahlenmaterial in aussagekräftige Grafiken.

Als durchgehendes Beispiel begleiten wir einen Prüfstandslauf, bei dem die
Drehzahl eines Elektromotors langsam von null auf die Leerlaufdrehzahl
hochgefahren wird. Aus der Drehzahl berechnen wir die übrigen Kenngrößen und
stellen sie Schritt für Schritt dar.

## Lernziele

```{admonition} Lernziele
:class: attention
* [ ] Sie kennen den Zusammenhang von **Figure** und **Axes** und erzeugen
  beide mit `plt.subplots()`.
* [ ] Sie erstellen **Linienplots** mit `ax.plot()`, zeichnen mehrere Kurven in
  ein Diagramm und ergänzen Achsenbeschriftung, Titel, Legende und Gitter.
* [ ] Sie speichern ein Diagramm mit `fig.savefig()`.
* [ ] Sie legen mit `plt.subplots(nrows, ncols)` mehrere Zeichenbereiche an,
  sprechen sie über `ax[i]` an und richten sie mit `plt.tight_layout()` aus.
* [ ] Sie stellen Messpunkte mit `ax.scatter()` dar und ergänzen
  Messunsicherheiten mit `ax.errorbar()`.
```

## Einen Kennlinienverlauf als Linienplot zeichnen

Wir starten direkt mit einem Beispiel. Aus der Drehzahl berechnen wir das
Drehmoment des Motors. Ein einfaches Modell nimmt an, dass das Drehmoment
linear mit der Drehzahl abnimmt: Bei Stillstand ist es am größten, bei
Leerlaufdrehzahl fällt es auf null.

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

drehzahl = np.linspace(0, 3000, 200)     # 1/min
leerlaufdrehzahl = 3000.0
drehmoment_still = 8.0                    # Nm bei Stillstand

drehmoment = drehmoment_still * (1 - drehzahl / leerlaufdrehzahl)

fig, ax = plt.subplots()
ax.plot(drehzahl, drehmoment)
plt.show()
```

Die Zeilen mit `import` laden NumPy und Matplotlib. `import matplotlib.pyplot as
plt` ist die feste Konvention für den Zugriff auf Matplotlib, so wie `np` für
NumPy. Die beiden Zeilen mit `style` sind optional und sorgen nur dafür, dass
die Diagramme etwas ansprechender aussehen.

`plt.subplots()` erzeugt zwei Objekte. Die **Figure** ist die gesamte
Abbildung, also das Fenster oder die Bilddatei. Die **Axes** ist der
Zeichenbereich darin, mit x-Achse, y-Achse und allen Kurven. Das Muster
`fig, ax = plt.subplots()` steht am Anfang jedes Diagramms in diesem Skript.

`ax.plot(drehzahl, drehmoment)` zeichnet eine Linie durch die Punkte
`(drehzahl[0], drehmoment[0])`, `(drehzahl[1], drehmoment[1])` und so weiter.
Das erste Argument ist immer die x-Achse, das zweite die y-Achse. `plt.show()`
zeigt das fertige Diagramm an.

Ein Diagramm ohne beschriftete Achsen ist in der Ingenieurpraxis wertlos. Wir
ergänzen daher Achsenbeschriftungen mit Einheiten, einen Titel und ein Gitter.

```{code-cell} python
fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(drehzahl, drehmoment)

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Drehmoment in Nm')
ax.set_title('Drehmoment-Kennlinie des Elektromotors')
ax.grid(True)

plt.show()
```

`figsize=(7, 4)` legt Breite und Höhe der Figure in Zoll fest. `set_xlabel()`
und `set_ylabel()` beschriften die Achsen, `set_title()` setzt einen Titel und
`grid(True)` legt ein Gitter über den Zeichenbereich.

Oft wollen wir mehrere Kurven vergleichen. Dazu rufen wir `ax.plot()` einfach
mehrfach auf. Wir vergleichen unseren Motor mit einer schwächeren Variante, die
bei Stillstand nur 6 Nm liefert. Jede Kurve bekommt ein `label`, das
anschließend in der Legende erscheint.

```{code-cell} python
drehmoment_schwach = 6.0 * (1 - drehzahl / leerlaufdrehzahl)

fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(drehzahl, drehmoment, label='Standardmotor (8 Nm)')
ax.plot(drehzahl, drehmoment_schwach, linestyle='dashed',
        label='Schwache Variante (6 Nm)')

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Drehmoment in Nm')
ax.set_title('Zwei Motorvarianten im Vergleich')
ax.legend()
ax.grid(True)

plt.show()
```

Matplotlib gibt jeder Kurve automatisch eine eigene Farbe. Mit `linestyle`
ändern wir den Linienstil, mögliche Werte sind `'solid'`, `'dashed'`,
`'dotted'` und `'dashdot'`. Der Aufruf `ax.legend()` ohne Argumente sammelt
alle `label`-Einträge ein und zeigt sie als Legende an. Das ist sauberer, als
eine Liste von Texten an `ax.legend()` zu übergeben, weil die Beschriftung
direkt beim jeweiligen `ax.plot()`-Aufruf steht.

In der Praxis wollen wir ein Diagramm nicht nur ansehen, sondern auch in einen
Bericht einfügen. `fig.savefig()` speichert die Figure als Datei. Wir rufen es
in derselben Code-Zelle auf, in der wir das Diagramm erzeugen, direkt vor
`plt.show()`.

```{code-cell} python
fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(drehzahl, drehmoment, label='Standardmotor (8 Nm)')
ax.plot(drehzahl, drehmoment_schwach, linestyle='dashed',
        label='Schwache Variante (6 Nm)')
ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Drehmoment in Nm')
ax.set_title('Zwei Motorvarianten im Vergleich')
ax.legend()
ax.grid(True)

fig.savefig('drehmoment_kennlinie.png', dpi=150, bbox_inches='tight')
plt.show()
```

`dpi=150` legt die Auflösung fest, für Berichte sind 150 bis 300 dpi üblich.
`bbox_inches='tight'` verhindert, dass Beschriftungen am Rand abgeschnitten
werden. Das Dateiformat erkennt Matplotlib an der Endung, `.png` für
Rastergrafiken, `.pdf` oder `.svg` für Vektorgrafiken.

```{admonition} Mini-Übung (✩)
:class: tip
Zeichnen Sie die **Winkelgeschwindigkeit** des Motors über der Drehzahl. Es
gilt `winkelgeschwindigkeit = 2 * np.pi * drehzahl / 60` in rad/s.

1. Erstellen Sie einen Linienplot mit der Drehzahl auf der x-Achse und der
   Winkelgeschwindigkeit auf der y-Achse.
2. Beschriften Sie beide Achsen mit Einheiten und vergeben Sie einen Titel.
3. Fügen Sie ein Gitter hinzu.
4. Beantworten Sie ohne Code: Sie rufen `ax.plot()` einmal auf und danach
   `ax.legend()`, ohne beim `plot()`-Aufruf ein `label` gesetzt zu haben. Was
   zeigt die Legende dann an?
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
winkelgeschwindigkeit = 2 * np.pi * drehzahl / 60

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(drehzahl, winkelgeschwindigkeit)
ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Winkelgeschwindigkeit in rad/s')
ax.set_title('Winkelgeschwindigkeit des Elektromotors')
ax.grid(True)
plt.show()
```
Die Winkelgeschwindigkeit steigt linear mit der Drehzahl, bei 3000 1/min
erreicht sie rund 314 rad/s. Rufen wir `ax.legend()` auf, ohne ein `label`
gesetzt zu haben, bleibt die Legende leer und Matplotlib gibt zusätzlich eine
Warnung aus. Eine Legende ist nur sinnvoll, wenn mindestens eine Kurve ein
`label` besitzt.
````

## Drehmoment, Leistung und Wirkungsgrad zusammen zeigen

Aus Drehmoment und Winkelgeschwindigkeit berechnen wir die abgegebene Leistung,
und für den Wirkungsgrad verwenden wir ein Modell, das sein Maximum in der Nähe
der Nenndrehzahl hat.

```{code-cell} python
winkelgeschwindigkeit = 2 * np.pi * drehzahl / 60
leistung = drehmoment * winkelgeschwindigkeit
wirkungsgrad = 0.9 * np.exp(-((drehzahl - 2200) / 900)**2)
```

*Warum zeichnen wir diese drei Größen nicht einfach in ein einziges Diagramm?*
Weil sie völlig verschiedene Wertebereiche und Einheiten haben: das Drehmoment
liegt zwischen 0 und 8 Nm, die Leistung bei einigen hundert Watt und der
Wirkungsgrad zwischen 0 und 1. In einem gemeinsamen Achsensystem wären
Drehmoment und Wirkungsgrad als flache Linien am unteren Rand nicht mehr
erkennbar. Die Lösung sind **Subplots**: mehrere Zeichenbereiche in einer
gemeinsamen Figure.

```{code-cell} python
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 8))

ax[0].plot(drehzahl, drehmoment)
ax[0].set_ylabel('Drehmoment in Nm')

ax[1].plot(drehzahl, leistung)
ax[1].set_ylabel('Leistung in W')

ax[2].plot(drehzahl, wirkungsgrad)
ax[2].set_ylabel('Wirkungsgrad')

for einzelachse in ax:
    einzelachse.set_xlabel('Drehzahl in 1/min')
    einzelachse.grid(True)

ax[0].set_title('Kennlinienfeld des Elektromotors')

plt.tight_layout()
plt.show()
```

`plt.subplots(nrows=3, ncols=1)` erzeugt drei Zeichenbereiche untereinander und
gibt sie als Array `ax` zurück. Wir sprechen den obersten mit `ax[0]` an, den
mittleren mit `ax[1]` und den untersten mit `ax[2]`, genau wie bei einem
NumPy-Array.

Für die x-Achsenbeschriftung und das Gitter schreiben wir eine `for`-Schleife
über `ax`, denn diese beiden Einstellungen sind für alle drei Subplots gleich.
Die Schleifenvariable `einzelachse` ist bei jedem Durchlauf einer der drei
Zeichenbereiche. Alles, was sich zwischen den Subplots unterscheidet, also die
y-Beschriftung und der Titel, setzen wir einzeln über `ax[0]`, `ax[1]` und
`ax[2]`.

`plt.tight_layout()` vergrößert die Abstände zwischen den Subplots so, dass sich
Beschriftungen nicht überlappen. Wir rufen es immer direkt vor `plt.show()`
auf.

Manchmal wollen wir den sichtbaren Bereich einer Achse festlegen, statt ihn
Matplotlib zu überlassen. Für den Wirkungsgrad ist der natürliche Bereich 0 bis
1, das machen wir mit `set_ylim()` sichtbar.

```{code-cell} python
fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(drehzahl, wirkungsgrad)
ax.set_ylim(0, 1)
ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Wirkungsgrad mit fester y-Achse von 0 bis 1')
ax.grid(True)

plt.show()
```

Ohne `set_ylim()` skaliert Matplotlib die y-Achse automatisch auf den
tatsächlichen Wertebereich der Daten, hier etwa 0 bis 0.9. Mit `set_ylim(0, 1)`
erzwingen wir die volle Skala und sehen sofort, wie viel Abstand noch zum
idealen Wirkungsgrad von 1 bleibt.

```{admonition} Mini-Übung (✩)
:class: tip
Erzeugen Sie zwei Subplots nebeneinander (`nrows=1, ncols=2`).

1. Links: Leistung über der Drehzahl.
2. Rechts: Wirkungsgrad über der Drehzahl, mit `set_ylim(0, 1)`.
3. Beschriften Sie beide Subplots mit Achsen und Titel, fügen Sie ein Gitter
   hinzu und richten Sie die Figure mit `plt.tight_layout()` aus.
4. Beantworten Sie ohne weiteren Code: Bei welcher Drehzahl ist die Leistung
   maximal? Ist das dieselbe Drehzahl, bei der der Wirkungsgrad maximal ist?
   Begründen Sie mit Blick auf die beiden Kurven.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 4))

ax[0].plot(drehzahl, leistung)
ax[0].set_xlabel('Drehzahl in 1/min')
ax[0].set_ylabel('Leistung in W')
ax[0].set_title('Leistung')
ax[0].grid(True)

ax[1].plot(drehzahl, wirkungsgrad)
ax[1].set_ylim(0, 1)
ax[1].set_xlabel('Drehzahl in 1/min')
ax[1].set_ylabel('Wirkungsgrad')
ax[1].set_title('Wirkungsgrad')
ax[1].grid(True)

plt.tight_layout()
plt.show()
```
Die Leistung ist bei rund 1500 1/min maximal, also bei der halben
Leerlaufdrehzahl. Dort ist das Produkt aus dem noch recht hohen Drehmoment und
der schon recht hohen Winkelgeschwindigkeit am größten. Der Wirkungsgrad
erreicht sein Maximum erst bei rund 2200 1/min. Ein Motor gibt seine höchste
Leistung also nicht bei der Drehzahl ab, bei der er am effizientesten arbeitet.
````

## Messpunkte mit Streuung und Unsicherheit

Bisher haben wir berechnete Kurven gezeichnet. Am realen Prüfstand messen wir
den Wirkungsgrad nur an einzelnen Drehzahlen, und jede Messung streut. Solche
Einzelmesswerte verbinden wir nicht mit einer Linie, sondern stellen sie als
einzelne Punkte dar. Das nennt man ein **Streudiagramm**, erzeugt mit
`ax.scatter()`.

```{code-cell} python
messdrehzahl = np.array([300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700])
messwirkungsgrad = np.array([0.02, 0.05, 0.10, 0.28, 0.47, 0.75, 0.87, 0.88, 0.55])

fig, ax = plt.subplots(figsize=(7, 4))

ax.scatter(messdrehzahl, messwirkungsgrad)

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Gemessener Wirkungsgrad an neun Drehzahlen')
ax.grid(True)

plt.show()
```

`ax.scatter()` erwartet wie `ax.plot()` zuerst die x-Werte, dann die y-Werte,
zeichnet aber nur Punkte ohne Verbindungslinie. Das ist genau richtig, wenn
zwischen den Messpunkten kein durchgehender Verlauf gemessen wurde.

Jeder Messpunkt ist der Mittelwert aus mehreren Wiederholungsmessungen und hat
eine Unsicherheit. Diese stellen wir mit **Fehlerbalken** dar. Die passende
Funktion ist `ax.errorbar()`.

```{code-cell} python
messunsicherheit = np.array([0.02, 0.02, 0.03, 0.03, 0.04, 0.03, 0.02, 0.03, 0.05])

fig, ax = plt.subplots(figsize=(7, 4))

ax.errorbar(messdrehzahl, messwirkungsgrad, yerr=messunsicherheit,
            fmt='o', capsize=4)

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Gemessener Wirkungsgrad mit Messunsicherheit')
ax.grid(True)

plt.show()
```

`yerr` übergibt die Unsicherheit in y-Richtung als Array. `fmt='o'` zeichnet die
Messpunkte als Kreise, `capsize=4` gibt den Querstrichen an den Enden der
Fehlerbalken eine Breite von 4 Punkten, damit sie besser ablesbar sind.

Zum Schluss vergleichen wir die Messung mit unserem Modell aus dem letzten
Abschnitt. Wir zeichnen die Messpunkte mit Fehlerbalken und die Modellkurve in
dasselbe Diagramm.

```{code-cell} python
fig, ax = plt.subplots(figsize=(7, 4))

ax.errorbar(messdrehzahl, messwirkungsgrad, yerr=messunsicherheit,
            fmt='o', capsize=4, label='Messung')
ax.plot(drehzahl, wirkungsgrad, label='Modell')

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Messung und Modell im Vergleich')
ax.legend()
ax.grid(True)

plt.show()
```

Messpunkte als Symbole, Modell oder Regression als durchgezogene Linie: Dieses
Muster begegnet uns in fast jedem quantitativen Ingenieurbericht. Die
Modellkurve verläuft durch fast alle Fehlerbalken, das Modell beschreibt die
Messung also gut. Nur der Punkt bei 2700 1/min liegt deutlich unter der Kurve,
dort lohnt sich eine genauere Betrachtung.

````{admonition} Mini-Übung (✩)
:class: tip
Am selben Prüfstand wird das Drehmoment an fünf Drehzahlen gemessen:

```python
messdrehzahl_m = np.array([500, 1000, 1500, 2000, 2500])
messdrehmoment = np.array([6.5, 5.6, 3.9, 2.8, 1.5])
messunsicherheit_m = np.array([0.3, 0.4, 0.3, 0.5, 0.4])
```

1. Stellen Sie die Messpunkte mit `ax.errorbar()` und Fehlerbalken in
   y-Richtung dar.
2. Zeichnen Sie die Modellkurve `drehmoment` über `drehzahl` in dasselbe
   Diagramm.
3. Beschriften Sie die Achsen, vergeben Sie einen Titel und eine Legende.
4. Beantworten Sie ohne Code: Warum stellen wir die fünf Messpunkte mit
   `ax.errorbar()` statt mit `ax.plot()` dar?
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung
:class: tip
:class: dropdown
```python
messdrehzahl_m = np.array([500, 1000, 1500, 2000, 2500])
messdrehmoment = np.array([6.5, 5.6, 3.9, 2.8, 1.5])
messunsicherheit_m = np.array([0.3, 0.4, 0.3, 0.5, 0.4])

fig, ax = plt.subplots(figsize=(7, 4))

ax.errorbar(messdrehzahl_m, messdrehmoment, yerr=messunsicherheit_m,
            fmt='o', capsize=4, label='Messung')
ax.plot(drehzahl, drehmoment, label='Modell')

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Drehmoment in Nm')
ax.set_title('Gemessenes und modelliertes Drehmoment')
ax.legend()
ax.grid(True)

plt.show()
```
Die Modellgerade läuft durch alle Fehlerbalken, die lineare Annahme für das
Drehmoment passt also zur Messung. Wir verwenden `ax.errorbar()` statt
`ax.plot()`, weil zwischen den fünf Drehzahlen nichts gemessen wurde. Eine
Verbindungslinie würde einen durchgehenden Messverlauf vortäuschen, den es
nicht gibt. Die Modellkurve dagegen ist tatsächlich für jede Drehzahl
berechnet und darf als Linie gezeichnet werden.
````

## Zusammenfassung und Ausblick

Wir haben Matplotlib als Werkzeug zum Visualisieren von Messdaten
kennengelernt. Das Muster `fig, ax = plt.subplots()` steht am Anfang jedes
Diagramms. Mit `ax.plot()` zeichnen wir Linien, mit `set_xlabel()`,
`set_ylabel()`, `set_title()`, `legend()` und `grid()` beschriften und
gestalten wir das Diagramm, mit `fig.savefig()` speichern wir es. Mehrere
Zeichenbereiche legen wir mit `plt.subplots(nrows, ncols)` an und sprechen sie
über `ax[i]` an, `plt.tight_layout()` richtet sie sauber aus. Einzelne
Messpunkte stellen wir mit `ax.scatter()` dar, ihre Unsicherheit mit
`ax.errorbar()`.

Im nächsten Kapitel wenden wir NumPy und Matplotlib gemeinsam in einem
zusammenhängenden Projekt an und werten die Messdaten eines kompletten
Prüfstandslaufs aus.
