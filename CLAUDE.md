# Code-Along-Notebooks

Ziel: aus den fertigen Notebooks in `notebooks/chapterNN/` Code-Along-Fassungen
machen, die in der Vorlesung live gemeinsam ausgefüllt werden (ca. 45 Min. pro
Notebook).

## Workflow

1. `./build_notebooks.sh chapterNN` kopiert `chapterNN/*.md` (Master-Quelle,
   wird für GitHub Pages gerendert — **nie direkt bearbeiten**) nach
   `notebooks/chapterNN/*.md` und bereinigt sie mit
   `convert_myst_to_notebook.py`.
2. Lücken werden **nur** in dieser bereinigten `.md` in `notebooks/chapterNN/`
   eingefügt, nicht im Master und nicht direkt im `.ipynb` (das wird beim
   nächsten Build-Lauf überschrieben).
3. Danach manuell (nicht mehr Teil von `build_notebooks.sh`):

   ```code
   jupytext --to ipynb notebooks/chapterNN/*.md
   jupytext --set-formats ipynb notebooks/chapterNN/*.ipynb
   ```

4. Achtung: ein erneuter Lauf von `build_notebooks.sh chapterNN` kopiert die
   `.md` wieder frisch aus dem Master und macht damit bereits eingefügte
   Lücken rückgängig.

## Applets im Notebook

Ein Applet (iframe aus `thma_anm_assets/interactive/...`, eingerahmt von
`<!-- markdownlint-disable -->` und `<!-- markdownlint-enable -->`) ersetzt
der Konverter durch das Standbild `pics/<applet>.png` und darunter einen Link
"Interactive version: open the applet in the browser" mit der URL des iframes
(samt `?lang=en`). `<applet>` ist der Dateiname des Applets ohne `.html`. Der
Alternativtext kommt aus dem `title`-Attribut des iframes, sonst aus dem
Dateinamen. Gibt es kein Standbild, bleibt nur der Link (Hinweis "note" in
der Ausgabe des Konverters). Das Standbild entsteht per
Puppeteer aus dem Applet mit `?standbild=1&lang=en` (Endzustand ohne
Bedienelemente), Beispiel `chapter07/pics/chap07_sec01_ftf_meldungen.png`.

## Lücken-Markierung

Kommentar `# TODO: ???` an der Stelle, an der Code entfernt wurde. Bei
mehrzeiligen Blöcken (z.B. Matrixzeilen) pro Zeile ein `# TODO: ???` mit
kurzem Hinweis, welche Gleichung/welcher Schritt gemeint ist.

## Wo Lücken hin

- **Nur im Hauptteil** (Präsentation/Live-Coding-Teil) jedes Notebooks.
- **Nicht** in den Mini-Exercises am Ende — die haben bereits eigene
  `# code cell`-Platzhalter fürs Selbststudium (für Studierende, die die
  Vorlesung verpasst haben) und bleiben unverändert.

## Welche Notebooks bekommen Lücken

Pro Lehrveranstaltungstermin gibt es typischerweise mehrere Notebooks mit
unterschiedlicher Rolle — nur das "Input"-Notebook (erste 45 Min, Vorlesung
im Code-Along-Stil) bekommt Lücken:

- **Input** (z.B. `chapter01_sec01`, `chapter01_sec03`): Lücken einfügen.
- **Geführte Übung direkt danach** (z.B. `chapter01_sec02`, `chapter01_sec04`):
  keine Lücken — ist bereits komplett als Übungsblatt mit `# code cell`
  aufgebaut, teils mit eigener `___`-Lückenkonvention in vorgegebenen
  Codebeispielen.
- **Hausaufgaben** (z.B. `chapter01_sec05`): keine Lücken.
- **Reine Referenz/wie-benutze-ich-Jupyter-Seiten** (z.B. `chapter01_sec00`,
  Cheat-Sheet `chapter01_sec06`): keine Lücken, teils nicht mal
  `{code-cell}`-Zellen.

Diese Rolle steht nicht immer im Dateinamen — bei Kapiteln ohne die
Python-Grundlagen (z.B. Kapitel 3) ist meist jede Section ein eigenständiges
Input-Notebook zu einem Thema, ohne begleitendes Übungsblatt in derselben
Nummerierung. Vor dem Einfügen von Lücken den Inhalt kurz sichten.

## Übungsblätter fürs Selbststudium (sec05)

✩-Aufgaben (Code vorhersagen) enthalten nach dem vorgegebenen Code immer den
Satz "Write down your guess in a Markdown cell before you run the code." und
enden mit "Run the code and check your predictions."

Ab Kapitel 7 wird das Übungskapitel (H1 "N.M Exercises", in Kapitel 7 die
`chapter07_sec03`) nicht als Notebook, sondern als PDF ohne Lösungen
ausgegeben. Damit üben die Studierenden das Format von CA 3: Aufgaben auf
Papier, gelöst lokal am PC ohne Internet. `build_notebooks.sh` erkennt das
Kapitel an der Überschrift und ruft statt des Notebook-Konverters

```code
python3 convert_myst_to_latex.py --pdf chapterNN/chapterNN_secMM.md notebooks/chapterNN/chapterNN_secMM.tex
```

auf. Das geht auch einzeln, ohne die Lücken der Code-Along-Notebooks zu
überschreiben. Satz wie in CA 2 (`../internal/exams/exam_2026ws/ca02`):
Präambel `latex/exercises_preamble.tex`, Code in `code`-Boxen. Jede Aufgabe
steht in einer `aufgabe`-Box mit Richtzeit rechts statt Punkten, gestaltet
wie die Admonition `tip` im Buch (grüner Rand links, hellgrüne Kopfzeile mit
Stift, weißer Inhalt). Eine Aufgabe wird nicht über zwei Seiten geteilt,
außer sie hat mehr als 60 Zeilen im Master (dann `aufgabelang`, mit
Hinweis "note"). Der Konverter setzt vorne den Abschnitt "How to
Practice" mit drei Hinweisen zum Arbeiten ohne Internet ein. Nicht
unterstützte Blöcke (Abbildungen, Tabellen, `hide-input`-Zellen) meldet er
als "note". Langen vorgegebenen Code vermeiden, denn er muss abgetippt
werden.

## Granularität

- Richtwert: **5-6 Lücken pro Notebook** für eine 45-minütige Live-Session.
- Feine Granularität (pro Zeile/Schritt) nur beim zentralen Lernkonzept der
  Einheit (z.B. Koeffizientenmatrix zeilenweise ablesen).
- Alles andere grob bzw. einzeilig lassen (z.B. ein `# TODO: ???` für einen
  ganzen `np.linalg.solve(...)`-Aufruf).
- Rein mechanische Schritte (gegebene Werte, Prints, Unpacking von Ergebnissen)
  bleiben ausgefüllt — keine Lücken, das kostet nur Tipparbeit ohne
  Lerneffekt.
