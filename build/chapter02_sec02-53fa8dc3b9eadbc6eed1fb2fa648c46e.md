---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# 2.2 Prüfstand für eine Windkraftanlage

In Kapitel 2.1 haben wir NumPy-Arrays erzeugt, mit Vektoroperationen und
Funktionen wie `np.exp()` bearbeitet und mit `np.mean()` und `np.std()` zu
Kennzahlen zusammengefasst. In diesem Kapitel wenden wir diese Werkzeuge auf
einen zusammenhängenden Fall an: die Auswertung eines Prüfstandslaufs für eine
Windkraftanlage. Bearbeiten Sie die Teilaufgaben möglichst zu zweit und der
Reihe nach, denn jeder Teil baut auf den Ergebnissen des vorherigen auf.

````{admonition} Projekt: Prüfstandslauf einer Windkraftanlage (✩✩)
:class: tip
Ein Testlauf misst die Windgeschwindigkeit an acht Zeitpunkten während einer
70 Sekunden langen Anlaufphase (in m/s):

```text
3.2, 5.1, 6.8, 7.5, 6.2, 4.9, 5.5, 6.0
```

Aus diesen Messwerten bestimmen wir Schritt für Schritt die elektrische
Leistung, die der Generator abgibt, und charakterisieren den Testlauf
anschließend statistisch.
````

```{admonition} Teil 1: Daten und Zeitachse anlegen
:class: tip
Legen Sie die Windgeschwindigkeiten als Array `windgeschwindigkeit` an. Legen
Sie außerdem eine Zeitachse `zeit` mit acht gleichmäßig verteilten Werten
zwischen 0 und 70 s an, ohne die Werte einzeln aufzuschreiben. Geben Sie Form
und Datentyp beider Arrays aus.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 1
:class: tip
:class: dropdown
```python
import numpy as np

windgeschwindigkeit = np.array([3.2, 5.1, 6.8, 7.5, 6.2, 4.9, 5.5, 6.0])
zeit = np.linspace(0, 70, 8)

print(windgeschwindigkeit.shape, windgeschwindigkeit.dtype)
print(zeit.shape, zeit.dtype)
```
Beide Arrays haben die Form `(8,)` und den Datentyp `float64`.
`np.linspace(0, 70, 8)` erzeugt die Zeitpunkte 0, 10, 20 bis 70 s, der Abstand
zwischen zwei Messungen beträgt also 10 s.
````

```{admonition} Teil 2: Rotorleistung berechnen
:class: tip
Die Rotorleistung lässt sich vereinfacht mit $P = k \cdot v^3$ berechnen, mit
$k = 1.2$. Berechnen Sie `rotorleistung` in Watt aus `windgeschwindigkeit`.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 2
:class: tip
:class: dropdown
```python
k = 1.2
rotorleistung = k * windgeschwindigkeit**3
print(rotorleistung)
```
Die Potenz `**3` und die Multiplikation mit `k` wirken elementweise auf das
ganze Array. Weil die Leistung mit der dritten Potenz der Windgeschwindigkeit
wächst, liefert der schnellste Messwert (7.5 m/s) mit rund 506 W schon etwa das
Dreizehnfache des langsamsten (3.2 m/s, rund 39 W).
````

```{admonition} Teil 3: Wirkungsgrad des Generators
:class: tip
Der Generator braucht eine Anlaufzeit, um seinen vollen Wirkungsgrad zu
erreichen. Der Wirkungsgrad zum Zeitpunkt $t$ folgt näherungsweise

$$\eta(t) = \eta_{max} \cdot \left(1 - e^{-t/\tau}\right)$$

mit $\eta_{max} = 0.95$ und $\tau = 20\,\text{s}$. Berechnen Sie `wirkungsgrad`
für die Zeitpunkte aus `zeit`.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 3
:class: tip
:class: dropdown
```python
eta_max = 0.95
tau = 20.0
wirkungsgrad = eta_max * (1 - np.exp(-zeit / tau))
print(wirkungsgrad)
```
`np.exp()` wirkt elementweise auf `-zeit / tau`. Zum Zeitpunkt 0 s ist der
Wirkungsgrad 0, danach nähert er sich dem Grenzwert 0.95. Nach 70 s, also
dreieinhalb Zeitkonstanten, sind rund 97 Prozent dieses Grenzwerts erreicht.
````

```{admonition} Teil 4: Elektrische Leistung
:class: tip
Berechnen Sie die tatsächlich abgegebene elektrische Leistung
`elektrische_leistung` aus `rotorleistung` und `wirkungsgrad`.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 4
:class: tip
:class: dropdown
```python
elektrische_leistung = rotorleistung * wirkungsgrad
print(elektrische_leistung)
```
Beide Arrays haben acht Elemente, daher multipliziert NumPy sie paarweise: Zu
jedem Zeitpunkt wird die Rotorleistung mit dem zugehörigen Wirkungsgrad
gewichtet. Am ersten Zeitpunkt ist das Ergebnis 0 W, weil der Generator noch
nicht angelaufen ist.
````

```{admonition} Teil 5: Testlauf charakterisieren
:class: tip
Bestimmen Sie die mittlere, minimale und maximale abgegebene Leistung sowie die
Streuung der Leistung um den Mittelwert.
```

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Teil 5
:class: tip
:class: dropdown
```python
mittlere_leistung = np.mean(elektrische_leistung)
min_leistung = np.min(elektrische_leistung)
max_leistung = np.max(elektrische_leistung)
streuung = np.std(elektrische_leistung)

print(f"Mittelwert: {mittlere_leistung:.1f} W")
print(f"Minimum:    {min_leistung:.1f} W")
print(f"Maximum:    {max_leistung:.1f} W")
print(f"Streuung:   {streuung:.1f} W")
```
Das Minimum von 0 W stammt vom ersten Zeitpunkt, an dem der Generator noch
stillsteht. Die Streuung liegt in derselben Größenordnung wie der Mittelwert,
der Testlauf liefert also eine sehr ungleichmäßige Leistung. Das liegt sowohl an
der Anlaufphase des Generators als auch an der schwankenden Windgeschwindigkeit.
````

```{admonition} Abschlussfrage
:class: tip
Beantworten Sie in eigenen Worten, ohne weiteren Code:

1. Die Windgeschwindigkeit schwankt im Testlauf nur zwischen etwa 3 und 8 m/s.
   Warum schwankt die Rotorleistung trotzdem so viel stärker?
2. Was bedeutet die große Streuung der elektrischen Leistung für den Betrieb der
   Anlage? Nennen Sie eine praktische Konsequenz.
```

````{admonition} Lösung Abschlussfrage
:class: tip
:class: dropdown
1. Die Rotorleistung wächst mit der dritten Potenz der Windgeschwindigkeit
   ($P = k \cdot v^3$). Aus dem Verhältnis von rund 8 zu 3 der beiden
   Windgeschwindigkeiten wird durch die dritte Potenz ein Verhältnis von etwa
   19 zu 1 in der Rotorleistung. Schon moderate Änderungen der
   Windgeschwindigkeit schlagen daher überproportional auf die Leistung durch.
2. Eine stark schwankende elektrische Leistung belastet das Stromnetz und die
   Leistungselektronik der Anlage. In der Praxis muss die Anlage die
   Schwankungen abfedern, zum Beispiel durch Regelung der Rotorblätter, durch
   Zwischenspeicher oder durch eine Netzeinspeisung erst ab einer
   Mindestwindgeschwindigkeit.
````

````{admonition} Zusatzaufgabe: Zweiter Standort (✩✩✩)
:class: tip
Ein zweiter Testlauf an einem windreicheren Standort liefert an denselben acht
Zeitpunkten folgende Windgeschwindigkeiten (m/s):

```text
7.5, 8.1, 6.9, 9.2, 8.8, 7.6, 8.4, 9.0
```

Führen Sie die Berechnung aus Teil 1 bis Teil 5 für diesen zweiten Standort
durch. Die Zeitachse und der Wirkungsgradverlauf hängen nur von der Anlaufzeit
ab, nicht vom Standort, und bleiben daher unverändert. Welcher Standort liefert
im Mittel mehr Leistung? Welcher liefert die im Verhältnis zum Mittelwert
gleichmäßigere Leistung?
````

```{code-cell} python
# Code-Zelle
```

````{admonition} Lösung Zusatzaufgabe
:class: tip
:class: dropdown
```python
windgeschwindigkeit_2 = np.array([7.5, 8.1, 6.9, 9.2, 8.8, 7.6, 8.4, 9.0])

# k und wirkungsgrad stammen aus Teil 2 und Teil 3 und gelten unverändert.
rotorleistung_2 = k * windgeschwindigkeit_2**3
elektrische_leistung_2 = rotorleistung_2 * wirkungsgrad

mittlere_leistung_2 = np.mean(elektrische_leistung_2)
streuung_2 = np.std(elektrische_leistung_2)

print(f"Standort 1: {mittlere_leistung:.1f} W (Streuung {streuung:.1f} W)")
print(f"Standort 2: {mittlere_leistung_2:.1f} W (Streuung {streuung_2:.1f} W)")

print(f"Streuung/Mittelwert Standort 1: {streuung / mittlere_leistung:.2f}")
print(f"Streuung/Mittelwert Standort 2: {streuung_2 / mittlere_leistung_2:.2f}")
```
Standort 2 liefert eine deutlich höhere mittlere Leistung, weil die
Windgeschwindigkeiten durchweg höher liegen und die Leistung mit der dritten
Potenz wächst. Die absolute Streuung ist an Standort 2 ebenfalls größer.
Aussagekräftiger ist das Verhältnis von Streuung zu Mittelwert: Dieser Wert ist
an Standort 2 kleiner, die Leistung ist dort also im Verhältnis gleichmäßiger.
````
