---
kernelspec:
  name: python3
  display_name: 'Python 3'
---

# Spickzettel Python

Diese Seite fasst die Python-Bausteine aus Part 1 auf einen Blick zusammen. Sie
ist als Nachschlagehilfe für die Übungen und die Klausur gedacht.

## Variablen und Datentypen

```python
geschwindigkeit = 27.8        # Float (Kommazahl, Dezimalpunkt)
anzahl = 50                   # Integer (ganze Zahl)
name = 'Sensor_A'             # String (Text in Anführungszeichen)

type(geschwindigkeit)         # zeigt den Datentyp an: <class 'float'>
```

Eine **Zuweisung** mit `=` berechnet zuerst die rechte Seite und speichert das
Ergebnis in der Variable links. `anzahl = anzahl + 1` erhöht `anzahl` um 1.

## Ausgabe mit print() und f-Strings

```python
print(geschwindigkeit)                      # einfache Ausgabe
print(f'Wert: {geschwindigkeit} km/h')      # f-String: Variable in { }
print(f'Wert: {geschwindigkeit:.2f} km/h')  # auf 2 Nachkommastellen gerundet
```

## Operatoren

| Art | Operatoren |
| --- | --- |
| Arithmetik | `+`  `-`  `*`  `/`  `**` (Potenz) |
| Vergleich | `>`  `<`  `>=`  `<=`  `==` (gleich)  `!=` (ungleich) |
| Logik | `and`  `or`  `not` |

Ein Vergleich liefert immer `True` oder `False`. `=` ist die Zuweisung, `==`
ist der Vergleich.

## Verzweigung: if / elif / else

```python
if geschwindigkeit > 33.3:
    print('zu schnell')
elif geschwindigkeit == 33.3:
    print('genau am Limit')
else:
    print('im Limit')
```

Die Kopfzeile endet mit `:`, der zugehörige Block ist eingerückt.

## Wiederholung: for-Schleife

```python
for zeitschritt in range(5):          # 0, 1, 2, 3, 4
    print(zeitschritt)

for wert in messreihe:                # direkt über eine Liste
    print(wert)
```

`range(5)` erzeugt 0 bis 4. `range(0, 101, 20)` erzeugt 0, 20, 40, 60, 80, 100.

## Liste

```python
messreihe = [80, 95, 120, 60, 110]

messreihe[0]          # erstes Element: 80
messreihe[-1]         # letztes Element: 110
len(messreihe)        # Anzahl der Elemente: 5
messreihe.append(75)  # Wert am Ende anhängen
```

## Dictionary

```python
sensor = {
    'name': 'Sensor_A',
    'messbereich_max': 200.0,
}

sensor['name']                 # Zugriff über den Schlüssel: 'Sensor_A'
sensor['messbereich_max'] = 250.0   # Wert ändern
sensor['kalibriert'] = True         # neues Schlüssel-Wert-Paar
```

## Funktion

```python
def kmh_zu_ms(geschwindigkeit_kmh):
    """Rechnet km/h in m/s um."""     # Docstring: kurze Beschreibung
    return geschwindigkeit_kmh / 3.6

kmh_zu_ms(95)                          # Aufruf mit einem Argument

def kinetische_energie(v, masse=1200):    # masse hat einen Default-Wert
    return 0.5 * masse * v ** 2

kinetische_energie(27.8)                   # masse = 1200
kinetische_energie(27.8, masse=1500)       # masse überschrieben
```

`def` definiert die Funktion, `return` gibt einen Wert zurück. Ohne `return`
liefert die Funktion `None`.
