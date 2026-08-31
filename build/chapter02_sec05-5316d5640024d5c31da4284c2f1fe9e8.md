---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.5 Übungen

Diese Aufgaben sind für das Selbststudium zuhause gedacht und wiederholen den
Stoff der Kapitel 2.1 bis 2.4. Rechnen Sie mit rund 90 Minuten Bearbeitungszeit.

Der Schwierigkeitsgrad steht im Titel jeder Aufgabe:

* ✩ Verständnis: Code und Ausgaben vorhersagen und erklären (ca. 5 min)
* ✩✩ Anwendung: eigenen Code schreiben und Ergebnisse interpretieren (ca. 10 min)
* ✩✩✩ Mini-Projekt: mehrere Konzepte des Parts kombinieren (ca. 30 min)

````{admonition} Aufgabe 2.1 (✩)
:class: tip
Gegeben ist folgender Code:

```python
import numpy as np

t = np.linspace(0, 10, 5)
platzhalter = np.zeros(3)
zaehler = np.array([2, 4, 6])
messung = np.array([2, 4, 6.0])
```

Notieren Sie Ihre Vermutung, bevor Sie den Code ausführen.

1. Welche Werte enthält `t` und was gibt `t.shape` zurück?
2. Was gibt `platzhalter.dtype` zurück?
3. Was gibt `zaehler.dtype` zurück und was `messung.dtype`? Warum
   unterscheiden sich die beiden, obwohl nur eine Zahl anders geschrieben ist?
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

t = np.linspace(0, 10, 5)
platzhalter = np.zeros(3)
zaehler = np.array([2, 4, 6])
messung = np.array([2, 4, 6.0])

print(t)
print(t.shape)
print(platzhalter.dtype)
print(zaehler.dtype)
print(messung.dtype)
```
Ausgabe:
```
[ 0.   2.5  5.   7.5 10. ]
(5,)
float64
int64
float64
```
`t` enthält fünf gleichmäßig verteilte Werte von 0 bis 10, `t.shape` ist
`(5,)`, also eine Dimension mit fünf Elementen. `np.zeros()` und
`np.linspace()` erzeugen immer Fließkommazahlen. Bei `zaehler` stehen nur
ganze Zahlen, daher wählt NumPy `int64`. Bei `messung` erzwingt die eine
Kommazahl `6.0`, dass alle Werte als `float64` gespeichert werden, denn ein
Array hat genau einen Datentyp.
````

````{admonition} Aufgabe 2.2 (✩)
:class: tip
Gegeben sind zwei Messreihen:

```python
import numpy as np

messwerte_1 = np.array([2.0, 4.0, 6.0, 8.0])
messwerte_2 = np.array([1.0, 2.0, 3.0, 4.0])
winkel = np.array([0.0, np.pi / 2, np.pi])
```

Notieren Sie Ihre Vermutung, bevor Sie den Code ausführen.

1. Was geben `messwerte_1 + messwerte_2`, `messwerte_1 * messwerte_2` und
   `messwerte_1 / messwerte_2` zurück?
2. Was gibt `messwerte_2 ** 2` zurück?
3. Was gibt `np.sin(winkel)` zurück? Warum steht an der Stelle von $\pi$ nicht
   exakt `0`?
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

messwerte_1 = np.array([2.0, 4.0, 6.0, 8.0])
messwerte_2 = np.array([1.0, 2.0, 3.0, 4.0])
winkel = np.array([0.0, np.pi / 2, np.pi])

print(messwerte_1 + messwerte_2)
print(messwerte_1 * messwerte_2)
print(messwerte_1 / messwerte_2)
print(messwerte_2 ** 2)
print(np.sin(winkel))
```
Ausgabe:
```
[ 3.  6.  9. 12.]
[ 2.  8. 18. 32.]
[2. 2. 2. 2.]
[ 1.  4.  9. 16.]
[0.0000000e+00 1.0000000e+00 1.2246468e-16]
```
Alle Grundrechenarten wirken elementweise, jedes Element wird mit dem Element
an derselben Position verrechnet. `np.sin(np.pi)` liefert nicht exakt `0`,
sondern einen winzigen Wert in der Größenordnung `1e-16`. Das ist ein
Rundungsfehler der Fließkomma-Arithmetik, denn $\pi$ lässt sich im Rechner
nicht exakt speichern.
````

````{admonition} Aufgabe 2.3 (✩)
:class: tip
An einem Hydraulikprüfstand wird der Systemdruck achtmal gemessen, in bar:

```python
import numpy as np

druck = np.array([4.9, 5.1, 5.0, 4.8, 5.2, 5.0, 4.95, 5.05])
```

Beantworten Sie zunächst ohne Code:

1. Liegt `np.mean(druck)` näher bei 5.0 oder bei 5.5?
2. Liegt `np.std(druck)` näher bei 0.1 oder bei 1.0? Begründen Sie mit einem
   Blick auf die Messwerte.
3. Was berechnet `np.max(druck) - np.min(druck)` inhaltlich?
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

druck = np.array([4.9, 5.1, 5.0, 4.8, 5.2, 5.0, 4.95, 5.05])

print(np.mean(druck))
print(np.std(druck))
print(np.max(druck) - np.min(druck))
```
Ausgabe:
```
5.0
0.11456439237389597
0.40000000000000036
```
Der Mittelwert ist genau 5.0 bar. Die Standardabweichung liegt bei rund 0.11
bar und damit nahe bei 0.1, denn alle Messwerte liegen dicht um den
Mittelwert, im Band zwischen 4.8 und 5.2 bar. `np.max(druck) - np.min(druck)`
ist die Spannweite, also der Abstand zwischen größtem und kleinstem Messwert,
hier 0.4 bar.
````

````{admonition} Aufgabe 2.4 (✩)
:class: tip
Gegeben ist folgender Code:

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

t = np.linspace(0, 1, 500)

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
ax[0].plot(t, np.sin(2 * np.pi * 3 * t), linestyle='dashed', label='3 Hz')
ax[1].plot(t, np.exp(-2 * t))
plt.tight_layout()
plt.show()
```

Notieren Sie Ihre Vermutung, bevor Sie den Code ausführen.

1. Welchen Linienstil hat die obere Kurve und wie viele volle Schwingungen
   zeigt sie im dargestellten Bereich?
2. Der obere `plot`-Aufruf hat `label='3 Hz'`, aber es gibt keinen Aufruf von
   `ax[0].legend()`. Was ist dadurch im Diagramm zu sehen?
3. Wie viele Subplots erzeugt `plt.subplots(nrows=2, ncols=1)` und wie sprechen
   Sie den unteren an?
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
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

t = np.linspace(0, 1, 500)

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))
ax[0].plot(t, np.sin(2 * np.pi * 3 * t), linestyle='dashed', label='3 Hz')
ax[1].plot(t, np.exp(-2 * t))
plt.tight_layout()
plt.show()
```
1. Die obere Kurve ist gestrichelt (`linestyle='dashed'`) und zeigt drei volle
   Schwingungen, da die Frequenz 3 Hz beträgt und der Bereich eine Sekunde
   lang ist.
2. Nichts. `label='3 Hz'` speichert die Beschriftung nur intern. Erst
   `ax[0].legend()` würde daraus eine sichtbare Legende erzeugen.
3. `plt.subplots(nrows=2, ncols=1)` erzeugt zwei Subplots untereinander. Der
   untere wird mit `ax[1]` angesprochen, der obere mit `ax[0]`.
````

````{admonition} Aufgabe 2.5 (✩✩)
:class: tip
An einem Prüfstand wird die Haltekraft einer Schraubverbindung achtmal
gemessen, in Newton:

```python
kraft_n = np.array([812, 798, 825, 803, 819, 807, 830, 815])
```

1. Berechnen Sie Mittelwert, Standardabweichung, Minimum und Maximum und geben
   Sie die Ergebnisse formatiert aus.
2. Die Verbindung gilt als in Ordnung, wenn alle Messwerte zwischen 780 N und
   840 N liegen. Prüfen Sie das mit einer `if`-Abfrage über `np.min(kraft_n)`
   und `np.max(kraft_n)` und geben Sie eine passende Meldung aus.
3. Rechnen Sie die Messreihe in Kilonewton um (1 kN = 1000 N) und geben Sie das
   Array `kraft_kn` aus.

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
kraft_n = np.array([812, 798, 825, 803, 819, 807, 830, 815])
untere_grenze = 780
obere_grenze = 840

# Verarbeitung
mittelwert = np.mean(kraft_n)
streuung = np.std(kraft_n)
kraft_min = np.min(kraft_n)
kraft_max = np.max(kraft_n)
kraft_kn = kraft_n / 1000

# Ausgabe
print(f"Mittelwert:         {mittelwert:.1f} N")
print(f"Standardabweichung: {streuung:.1f} N")
print(f"Minimum:            {kraft_min} N")
print(f"Maximum:            {kraft_max} N")

if kraft_min >= untere_grenze and kraft_max <= obere_grenze:
    print("Alle Messwerte im Toleranzbereich.")
else:
    print("Toleranzbereich verlassen!")

print(f"Messreihe in kN: {kraft_kn}")
```
Ausgabe:
```
Mittelwert:         813.6 N
Standardabweichung: 10.2 N
Minimum:            798 N
Maximum:            830 N
Alle Messwerte im Toleranzbereich.
Messreihe in kN: [0.812 0.798 0.825 0.803 0.819 0.807 0.83  0.815]
```
Der kleinste Wert ist 798 N, der größte 830 N. Beide liegen innerhalb der
Grenzen von 780 N und 840 N, die Verbindung ist also in Ordnung. Die Division
durch 1000 wirkt als Vektoroperation auf jedes Element.
````

````{admonition} Aufgabe 2.6 (✩✩)
:class: tip
Ein heißes Bauteil kühlt in ruhender Luft ab. Die Temperatur folgt dem
Abklinggesetz

$$T(t) = T_\text{Umgebung} + (T_\text{Start} - T_\text{Umgebung}) \cdot e^{-t / \tau}$$

1. Schreiben Sie eine Funktion
   `bauteiltemperatur(zeit, t_umgebung, t_start, tau)`, die die Temperatur als
   NumPy-Array zurückgibt. Versehen Sie die Funktion mit einem Docstring.
2. Rufen Sie die Funktion für eine Zeitachse von 0 bis 600 s mit 100 Punkten
   auf, mit `t_umgebung = 20`, `t_start = 200` und `tau = 150`.
3. Stellen Sie den Temperaturverlauf als Linienplot dar, mit
   Achsenbeschriftung, Titel und Gitter.

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
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Eingabe
def bauteiltemperatur(zeit, t_umgebung, t_start, tau):
    """Berechnet den Abkühlverlauf eines Bauteils in ruhender Luft.

    zeit:       Zeitachse als NumPy-Array in s
    t_umgebung: Umgebungstemperatur in Grad Celsius
    t_start:    Anfangstemperatur des Bauteils in Grad Celsius
    tau:        Zeitkonstante der Abkühlung in s
    Rückgabe:   Temperatur als NumPy-Array in Grad Celsius
    """
    return t_umgebung + (t_start - t_umgebung) * np.exp(-zeit / tau)

zeit = np.linspace(0, 600, 100)

# Verarbeitung
temperatur = bauteiltemperatur(zeit, 20, 200, 150)

# Ausgabe
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(zeit, temperatur)
ax.set_xlabel('Zeit in s')
ax.set_ylabel('Temperatur in Grad Celsius')
ax.set_title('Abkühlung eines Bauteils in ruhender Luft')
ax.grid(True)
plt.show()
```
Nach 600 s ist die Temperatur auf rund 23 Grad Celsius gefallen und damit fast
auf Umgebungsniveau. Die Kurve fällt am Anfang steil und wird mit
abnehmendem Temperaturunterschied immer flacher.
````

````{admonition} Aufgabe 2.7 (✩✩)
:class: tip
Dasselbe Bauteil wird einmal in ruhender Luft (`tau = 200`) und einmal mit
einem Gebläse (`tau = 80`) abgekühlt. In beiden Fällen ist die
Umgebungstemperatur 20 Grad Celsius und die Anfangstemperatur 200 Grad
Celsius.

1. Berechnen Sie beide Temperaturverläufe für eine Zeitachse von 0 bis 600 s
   mit 100 Punkten. Verwenden Sie die Formel aus Aufgabe 2.6.
2. Stellen Sie beide Verläufe in einem gemeinsamen Diagramm dar, mit Legende,
   Achsenbeschriftung, Titel und Gitter.

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
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Eingabe
zeit = np.linspace(0, 600, 100)
t_umgebung = 20
t_start = 200

# Verarbeitung
temperatur_ruhend = t_umgebung + (t_start - t_umgebung) * np.exp(-zeit / 200)
temperatur_geblaese = t_umgebung + (t_start - t_umgebung) * np.exp(-zeit / 80)

# Ausgabe
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(zeit, temperatur_ruhend, label='Ruhende Luft')
ax.plot(zeit, temperatur_geblaese, label='Mit Gebläse')
ax.set_xlabel('Zeit in s')
ax.set_ylabel('Temperatur in Grad Celsius')
ax.set_title('Abkühlung mit und ohne Gebläse')
ax.legend()
ax.grid(True)
plt.show()
```
Mit Gebläse ist die Zeitkonstante kleiner, das Bauteil kühlt deutlich
schneller ab. Nach 240 s liegt es mit Gebläse schon fast auf
Umgebungstemperatur, während es in ruhender Luft noch über 70 Grad Celsius
heiß ist.
````

````{admonition} Aufgabe 2.8 (✩✩)
:class: tip
Der Wirkungsgrad eines Getriebes wird bei sechs Drehzahlen gemessen, jeder
Wert als Mittelwert aus mehreren Wiederholungen mit Standardabweichung:

```python
drehzahl = np.array([500, 1000, 1500, 2000, 2500, 3000])
wirkungsgrad = np.array([0.89, 0.93, 0.95, 0.96, 0.94, 0.91])
wirkungsgrad_std = np.array([0.010, 0.008, 0.006, 0.006, 0.009, 0.012])
```

1. Stellen Sie den Wirkungsgrad über der Drehzahl mit `ax.errorbar()` und
   Fehlerbalken in y-Richtung dar (`fmt='o'`, `capsize=4`).
2. Bestimmen Sie mit `np.argmax()` den Punkt mit dem besten Wirkungsgrad und
   zeichnen Sie ihn mit einem zweiten `ax.scatter()`-Aufruf als großen Stern
   ein (`marker='*'`, `s=200`).
3. Beschriften Sie Achsen und Titel und zeigen Sie eine Legende an.

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
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Eingabe
drehzahl = np.array([500, 1000, 1500, 2000, 2500, 3000])
wirkungsgrad = np.array([0.89, 0.93, 0.95, 0.96, 0.94, 0.91])
wirkungsgrad_std = np.array([0.010, 0.008, 0.006, 0.006, 0.009, 0.012])

# Verarbeitung
i_best = np.argmax(wirkungsgrad)

# Ausgabe
fig, ax = plt.subplots(figsize=(7, 4))
ax.errorbar(drehzahl, wirkungsgrad, yerr=wirkungsgrad_std,
            fmt='o', capsize=4, label='Messung')
ax.scatter(drehzahl[i_best], wirkungsgrad[i_best],
           marker='*', s=200, color='red', zorder=5, label='Bester Wirkungsgrad')
ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Getriebewirkungsgrad mit Messunsicherheit')
ax.legend()
ax.grid(True)
plt.show()
```
Der beste Wirkungsgrad liegt bei 2000 1/min mit 0.96. Zwischen 1500 und
2500 1/min ist die Kurve nahezu flach, das Getriebe arbeitet also in einem
breiten Drehzahlbereich mit gutem Wirkungsgrad.
````

`````{admonition} Aufgabe 2.9 (✩✩✩) Mini-Projekt: Kennlinie einer Kreiselpumpe
:class: tip
An einem Pumpenprüfstand wird der Volumenstrom in acht Stufen erhöht. An jeder
Stufe werden die Förderhöhe und die elektrisch aufgenommene Leistung gemessen:

```python
volumenstrom = np.array([2, 4, 6, 8, 10, 12, 14, 16])                 # l/s
foerderhoehe = np.array([48, 47, 45, 42, 38, 33, 26, 18])             # m
aufgenommene_leistung = np.array([2700, 3550, 4080, 4520,
                                  4970, 5400, 5760, 6280])            # W
```

**Teil 1:** Legen Sie die drei Messreihen als Arrays an und prüfen Sie mit
`.shape`, dass alle gleich lang sind. Stellen Sie die Förderhöhe über dem
Volumenstrom als Streudiagramm dar.

**Teil 2:** Berechnen Sie die hydraulische Leistung
`p_hydraulisch = 1000 * 9.81 * volumenstrom_m3s * foerderhoehe`, wobei
`volumenstrom_m3s = volumenstrom / 1000` der Volumenstrom in m³/s ist.
Berechnen Sie den Wirkungsgrad
`wirkungsgrad = p_hydraulisch / aufgenommene_leistung`.

**Teil 3:** Erstellen Sie eine Figure mit drei Subplots untereinander:
Förderhöhe, hydraulische Leistung und Wirkungsgrad, jeweils über dem
Volumenstrom. Geben Sie dem Wirkungsgrad-Subplot mit `set_ylim(0, 1)` die
volle Skala. x-Achsenbeschriftung und Gitter setzen Sie über eine
`for`-Schleife.

**Teil 4:** Bestimmen Sie mit `np.argmax()` den Volumenstrom mit dem besten
Wirkungsgrad. Berechnen Sie außerdem Mittelwert, Standardabweichung und
Maximum der hydraulischen Leistung. Geben Sie die Ergebnisse als kurzen
Textbericht mit f-Strings aus.

**Abschlussfrage:** Der beste Wirkungsgrad und die größte hydraulische
Leistung treten bei unterschiedlichen Volumenströmen auf. Für welchen
Volumenstrom sollte die Pumpe im Dauerbetrieb ausgelegt werden, und was
bedeutet die fallende Förderhöhe für den Betrieb, wenn plötzlich mehr
Durchfluss verlangt wird?

Strukturieren Sie Ihren Code mit EVA-Kommentaren.
`````

```{code-cell} python
# Code-Zelle
```

`````{admonition} Lösung
:class: tip
:class: dropdown
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

# Eingabe
volumenstrom = np.array([2, 4, 6, 8, 10, 12, 14, 16])
foerderhoehe = np.array([48, 47, 45, 42, 38, 33, 26, 18])
aufgenommene_leistung = np.array([2700, 3550, 4080, 4520,
                                  4970, 5400, 5760, 6280])

print(volumenstrom.shape, foerderhoehe.shape, aufgenommene_leistung.shape)

# Verarbeitung
volumenstrom_m3s = volumenstrom / 1000
p_hydraulisch = 1000 * 9.81 * volumenstrom_m3s * foerderhoehe
wirkungsgrad = p_hydraulisch / aufgenommene_leistung

volumenstrom_bester_wirkungsgrad = volumenstrom[np.argmax(wirkungsgrad)]
mittlere_leistung = np.mean(p_hydraulisch)
streuung_leistung = np.std(p_hydraulisch)
maximale_leistung = np.max(p_hydraulisch)

# Ausgabe: Streudiagramm
fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(volumenstrom, foerderhoehe)
ax.set_xlabel('Volumenstrom in l/s')
ax.set_ylabel('Förderhöhe in m')
ax.set_title('Gemessene Förderhöhe über dem Volumenstrom')
ax.grid(True)
plt.show()

# Ausgabe: Kennlinienfeld
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 8))

ax[0].plot(volumenstrom, foerderhoehe)
ax[0].set_ylabel('Förderhöhe in m')

ax[1].plot(volumenstrom, p_hydraulisch)
ax[1].set_ylabel('Hydraulische Leistung in W')

ax[2].plot(volumenstrom, wirkungsgrad)
ax[2].set_ylabel('Wirkungsgrad')
ax[2].set_ylim(0, 1)

for einzelachse in ax:
    einzelachse.set_xlabel('Volumenstrom in l/s')
    einzelachse.grid(True)

ax[0].set_title('Kennlinienfeld der Kreiselpumpe')
plt.tight_layout()
plt.show()

# Ausgabe: Textbericht
print(f"Bester Wirkungsgrad bei {volumenstrom_bester_wirkungsgrad} l/s")
print(f"Hydraulische Leistung: Mittelwert {mittlere_leistung:.0f} W, "
      f"Streuung {streuung_leistung:.0f} W, Maximum {maximale_leistung:.0f} W")
```
Ausgabe:
```
(8,) (8,) (8,)
Bester Wirkungsgrad bei 10 l/s
Hydraulische Leistung: Mittelwert 2842 W, Streuung 952 W, Maximum 3885 W
```
Der beste Wirkungsgrad von rund 0.75 liegt bei 10 l/s, die größte hydraulische
Leistung von rund 3885 W erst bei 12 l/s.

**Abschlussfrage:** Für den Dauerbetrieb legt man die Pumpe auf den
Volumenstrom mit dem besten Wirkungsgrad aus, also rund 10 l/s. Dort geht am
wenigsten Antriebsleistung als Verlust verloren. Die fallende Förderhöhe
bedeutet, dass die Pumpe bei mehr Durchfluss immer weniger Druck aufbauen
kann. Verlangt die Anlage plötzlich mehr Volumenstrom, sinkt die Förderhöhe,
und ab einem gewissen Punkt reicht der Druck nicht mehr aus, um die Anlage
gegen ihren Widerstand zu versorgen.
`````
