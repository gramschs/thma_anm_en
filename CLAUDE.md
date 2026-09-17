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

## Granularität

- Richtwert: **5-8 Lücken pro Notebook** für eine 45-minütige Live-Session.
- Feine Granularität (pro Zeile/Schritt) nur beim zentralen Lernkonzept der
  Einheit (z.B. Koeffizientenmatrix zeilenweise ablesen).
- Alles andere grob bzw. einzeilig lassen (z.B. ein `# TODO: ???` für einen
  ganzen `np.linalg.solve(...)`-Aufruf).
- Rein mechanische Schritte (gegebene Werte, Prints, Unpacking von Ergebnissen)
  bleiben ausgefüllt — keine Lücken, das kostet nur Tipparbeit ohne
  Lerneffekt.
