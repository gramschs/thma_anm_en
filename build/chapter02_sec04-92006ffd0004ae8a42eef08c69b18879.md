---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.4 Prüfstandsbericht für einen Elektromotor

In den Kapiteln 2.1 bis 2.3 haben wir NumPy-Arrays berechnet, statistisch
ausgewertet und mit Matplotlib dargestellt. In diesem Kapitel wenden wir diese
Werkzeuge gemeinsam an und werten einen kompletten Prüfstandslauf des
Elektromotors aus Kapitel 2.3 aus. Bearbeiten Sie die Teilaufgaben möglichst zu
zweit und der Reihe nach, denn jeder Teil baut auf den Ergebnissen des
vorherigen auf.

```{admonition} Projekt: Prüfstandsbericht für den Elektromotor (✩✩)
:class: tip
Am Prüfstand wurde die Drehzahl des Motors in zwölf Stufen von 250 auf
3000 1/min erhöht. An jeder Stufe wurden das Drehmoment an der Welle und die
elektrisch aufgenommene Leistung gemessen. Die Messwerte sind in der ersten
Code-Zelle bereits als Arrays hinterlegt. Aus ihnen erstellen wir die
Abbildungen und Kennzahlen für den Prüfstandsbericht.
```

```{admonition} Teil 1: Messdaten einlesen und Kenngrößen berechnen
:class: tip
In der Code-Zelle sind die Messwerte bereits als Arrays `drehzahl`,
`drehmoment` und `aufgenommene_leistung` hinterlegt.

1. Prüfen Sie mit `.shape`, dass alle drei Arrays gleich lang sind.
2. Berechnen Sie die Winkelgeschwindigkeit `omega = 2 * np.pi * drehzahl / 60`
   in rad/s.
3. Berechnen Sie die mechanische Leistung `p_mech = drehmoment * omega` in
   Watt.
4. Berechnen Sie den Wirkungsgrad
   `wirkungsgrad = p_mech / aufgenommene_leistung` und geben Sie das Array aus.
```

```{code-cell} python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('seaborn-v0_8')

drehzahl = np.array([250, 500, 750, 1000, 1250, 1500,
                     1750, 2000, 2250, 2500, 2750, 3000])          # 1/min
drehmoment = np.array([7.4, 6.7, 6.1, 5.4, 4.7, 4.1,
                       3.4, 2.9, 2.3, 1.7, 1.1, 0.5])              # Nm
aufgenommene_leistung = np.array([1350, 1660, 1720, 1520, 1230, 980,
                                  800, 720, 660, 600, 560, 470])   # W

# Ergänzen Sie: Formen prüfen, omega, p_mech und wirkungsgrad berechnen
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
print(drehzahl.shape, drehmoment.shape, aufgenommene_leistung.shape)

omega = 2 * np.pi * drehzahl / 60
p_mech = drehmoment * omega
wirkungsgrad = p_mech / aufgenommene_leistung

print(wirkungsgrad)
```
Alle drei Arrays haben die Form `(12,)`. Die drei Rechnungen sind
Vektoroperationen und wirken auf das ganze Array. Der Wirkungsgrad liegt
zwischen rund 0.14 und 0.84 und ist damit überall kleiner als 1, wie es für
einen realen Motor sein muss. Er steigt zunächst mit der Drehzahl an, erreicht
ein Maximum und fällt danach wieder ab.
````

```{admonition} Teil 2: Kennlinienfeld als Subplots
:class: tip
Erstellen Sie eine Figure mit drei Subplots untereinander (`nrows=3`). Zeigen
Sie oben das Drehmoment, in der Mitte die mechanische Leistung und unten den
Wirkungsgrad, jeweils über der Drehzahl. Beschriften Sie jeden Subplot mit
seiner y-Achse und geben Sie dem Wirkungsgrad-Subplot mit `set_ylim(0, 1)` die
volle Skala. Die x-Achsenbeschriftung und das Gitter setzen Sie über eine
`for`-Schleife über `ax`. Der oberste Subplot bekommt einen Titel. Richten Sie
die Figure mit `plt.tight_layout()` aus.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(7, 8))

ax[0].plot(drehzahl, drehmoment)
ax[0].set_ylabel('Drehmoment in Nm')

ax[1].plot(drehzahl, p_mech)
ax[1].set_ylabel('Mechanische Leistung in W')

ax[2].plot(drehzahl, wirkungsgrad)
ax[2].set_ylabel('Wirkungsgrad')
ax[2].set_ylim(0, 1)

for einzelachse in ax:
    einzelachse.set_xlabel('Drehzahl in 1/min')
    einzelachse.grid(True)

ax[0].set_title('Kennlinienfeld aus dem Prüfstandslauf')

plt.tight_layout()
plt.show()
```
So sehen wir die drei gemessenen Größen erstmals im Zusammenhang. Wir behandeln
die Messpunkte als Kennlinie und verbinden sie mit einer Linie, um den Verlauf
zu zeigen. Das Drehmoment fällt annähernd linear, die mechanische Leistung hat
ihr Maximum in der Mitte des Drehzahlbereichs, und der Wirkungsgrad wird erst
bei hoher Drehzahl gut.
````

```{admonition} Teil 3: Betriebspunkte bestimmen
:class: tip
Die Funktion `np.argmax(array)` gibt den Index des größten Werts im Array
zurück. Mit `drehzahl[np.argmax(p_mech)]` finden Sie also die Drehzahl, bei der
die mechanische Leistung am größten ist.

1. Bestimmen Sie die Drehzahl, bei der die mechanische Leistung maximal ist.
2. Bestimmen Sie die Drehzahl, bei der der Wirkungsgrad maximal ist.
3. Berechnen Sie Mittelwert, Standardabweichung und Maximum der mechanischen
   Leistung über den gesamten Lauf.
4. Geben Sie die Ergebnisse als kurzen Textbericht mit f-Strings aus.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
drehzahl_max_leistung = drehzahl[np.argmax(p_mech)]
drehzahl_max_wirkungsgrad = drehzahl[np.argmax(wirkungsgrad)]

mittlere_leistung = np.mean(p_mech)
streuung_leistung = np.std(p_mech)
maximale_leistung = np.max(p_mech)

print(f"Größte mechanische Leistung bei {drehzahl_max_leistung} 1/min")
print(f"Bester Wirkungsgrad bei {drehzahl_max_wirkungsgrad} 1/min")
print(f"Mechanische Leistung: Mittelwert {mittlere_leistung:.0f} W, "
      f"Streuung {streuung_leistung:.0f} W, Maximum {maximale_leistung:.0f} W")
```
Die mechanische Leistung ist mit rund 644 W bei 1500 1/min am größten, der
Wirkungsgrad mit 0.84 erst bei 2000 1/min. Der Motor gibt seine höchste
Leistung also nicht bei der Drehzahl ab, bei der er die geringsten Verluste
hat.
````

````{admonition} Teil 4: Wirkungsgrad mit Messunsicherheit
:class: tip
Jeder Wirkungsgrad-Wert ist der Mittelwert aus drei Wiederholungsmessungen. Die
Standardabweichung dieser Wiederholungen ist gegeben:

```python
wirkungsgrad_std = np.array([0.015, 0.018, 0.020, 0.022, 0.025, 0.024,
                             0.022, 0.020, 0.019, 0.018, 0.028, 0.030])
```

1. Stellen Sie den Wirkungsgrad über der Drehzahl mit `ax.errorbar()` und
   Fehlerbalken in y-Richtung dar (`fmt='o'`, `capsize=4`).
2. Heben Sie den Betriebspunkt mit dem besten Wirkungsgrad hervor, indem Sie
   ihn mit einem zweiten `ax.scatter()`-Aufruf als großen Stern einzeichnen
   (`marker='*'`, `s=200`).
3. Beschriften Sie Achsen und Titel und zeigen Sie eine Legende an.
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 4
:class: tip
:class: dropdown
```python
wirkungsgrad_std = np.array([0.015, 0.018, 0.020, 0.022, 0.025, 0.024,
                             0.022, 0.020, 0.019, 0.018, 0.028, 0.030])

i_best = np.argmax(wirkungsgrad)

fig, ax = plt.subplots(figsize=(7, 4))

ax.errorbar(drehzahl, wirkungsgrad, yerr=wirkungsgrad_std,
            fmt='o', capsize=4, label='Messung')
ax.scatter(drehzahl[i_best], wirkungsgrad[i_best],
           marker='*', s=200, color='red', zorder=5, label='Bester Betriebspunkt')

ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Wirkungsgrad mit Messunsicherheit')
ax.legend()
ax.grid(True)

plt.show()
```
Die Fehlerbalken sind bei niedriger Drehzahl im Verhältnis zum Messwert am
größten, weil der Wirkungsgrad dort selbst klein ist. Der beste Betriebspunkt
bei 2000 1/min ist dagegen sehr genau bestimmt. Das `zorder=5` sorgt dafür,
dass der Stern über den Fehlerbalken liegt.
````

```{admonition} Abschlussfrage
:class: tip
Beantworten Sie in eigenen Worten, ohne weiteren Code:

1. Der Motor gibt seine größte mechanische Leistung bei 1500 1/min ab, arbeitet
   aber bei 2000 1/min am effizientesten. Für welche Drehzahl würden Sie den
   Motor im Dauerbetrieb auslegen? Begründen Sie.
2. An welchen Messpunkten ist die relative Messunsicherheit des Wirkungsgrads
   am größten? Was folgt daraus für die Planung weiterer Messungen?
```

````{admonition} Lösung Abschlussfrage
:class: tip
:class: dropdown
1. Für den Dauerbetrieb wählt man in der Regel eine Drehzahl nahe dem besten
   Wirkungsgrad, also rund 2000 1/min. Dort geht am wenigsten Energie als Wärme
   verloren, der Motor läuft kühler und die Betriebskosten sind niedriger. Die
   maximale Leistung bei 1500 1/min ist eher für kurzzeitige Lastspitzen
   interessant. Braucht die Anwendung dauerhaft die höchste Leistung, muss man
   den geringeren Wirkungsgrad bewusst in Kauf nehmen.
2. Die relative Unsicherheit ist der Quotient aus `wirkungsgrad_std` und
   `wirkungsgrad`. Sie ist bei den niedrigen Drehzahlen am größten, weil der
   Wirkungsgrad dort selbst klein ist, während die absolute Streuung ähnlich
   bleibt. Bei 250 1/min liegt sie über zehn Prozent. Für weitere Messungen
   lohnt es sich, im unteren Drehzahlbereich mehr Wiederholungen aufzunehmen
   oder ein genaueres Messverfahren einzusetzen. Der gut vermessene Bereich um
   2000 1/min braucht dagegen weniger Aufwand.
````

````{admonition} Zusatzaufgabe: Zweiter Prüfstandslauf mit warmem Motor (✩✩✩)
:class: tip
Nach einer Stunde Dauerlauf ist der Motor warm. Ein zweiter Prüfstandslauf bei
denselben Drehzahlen und demselben Drehmoment liefert eine höhere aufgenommene
Leistung, weil die Wicklungswiderstände mit der Temperatur steigen:

```python
aufgenommene_leistung_warm = np.array([1420, 1780, 1880, 1680, 1370, 1100,
                                       910, 830, 770, 710, 660, 560])   # W
```

1. Berechnen Sie den Wirkungsgrad `wirkungsgrad_warm` für den warmen Lauf. Das
   Drehmoment und damit `p_mech` bleiben unverändert.
2. Stellen Sie beide Wirkungsgrad-Kurven, kalt und warm, in einem gemeinsamen
   Diagramm dar, mit Legende.
3. Vergleichen Sie: Wie stark sinkt der Spitzenwirkungsgrad? Verschiebt sich
   die Drehzahl des besten Betriebspunkts?
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Zusatzaufgabe
:class: tip
:class: dropdown
```python
aufgenommene_leistung_warm = np.array([1420, 1780, 1880, 1680, 1370, 1100,
                                       910, 830, 770, 710, 660, 560])

wirkungsgrad_warm = p_mech / aufgenommene_leistung_warm

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(drehzahl, wirkungsgrad,      marker='o', label='Kalter Motor')
ax.plot(drehzahl, wirkungsgrad_warm, marker='o', label='Warmer Motor')
ax.set_xlabel('Drehzahl in 1/min')
ax.set_ylabel('Wirkungsgrad')
ax.set_title('Wirkungsgrad bei kaltem und warmem Motor')
ax.set_ylim(0, 1)
ax.legend()
ax.grid(True)
plt.show()

print(f"Spitzenwirkungsgrad kalt: {np.max(wirkungsgrad):.2f} "
      f"bei {drehzahl[np.argmax(wirkungsgrad)]} 1/min")
print(f"Spitzenwirkungsgrad warm: {np.max(wirkungsgrad_warm):.2f} "
      f"bei {drehzahl[np.argmax(wirkungsgrad_warm)]} 1/min")
```
Der Spitzenwirkungsgrad sinkt von rund 0.84 auf rund 0.73, also um mehr als
zehn Prozentpunkte. Die Drehzahl des besten Betriebspunkts bleibt bei
2000 1/min. Die Motortemperatur verschlechtert den Wirkungsgrad also deutlich,
ohne die Lage des Optimums zu verschieben. Für einen belastbaren Bericht sollte
immer angegeben werden, bei welcher Betriebstemperatur gemessen wurde.
````
