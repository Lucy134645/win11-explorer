# Windows 11 File Explorer für Arch Linux

Ein 1:1 Nachbau des modernen **Windows 11 File Explorers** (Fluent Design / Mica) für Arch Linux (und arch-basierte Distributionen wie CachyOS, EndeavourOS, Manjaro) auf Basis von **PyQt6** und modernem Vektor-Rendering.

![Windows 11 Explorer Preview](win11_explorer_preview.png)

## Highlights & Features

- **Windows 11 Fluent Design & Mica Styling**:
  - Abgerundete Ecken, authentische Farbpaletten (Dark & Light Mode).
  - Modernste Segoe UI / System-Typografie.
  - Vektorbasierte Fluent-Icons (Gelbe Win11-Ordner, Downloads-Pfeil, Desktop-Monitor, Laufwerke mit Speicherbalken, Papierkorb etc.).
- **Tabs wie in Windows 11**:
  - Beliebig viele Tabs nebeneinander.
  - Tab hinzufügen mit dem `+` Button oder `Strg + T`.
  - Tab schließen mit `✕` oder `Strg + W`.
  - Jeder Tab merkt sich seinen eigenen Pfad, Vor-/Zurück-Verlauf und Ansichtsmodus.
- **Interaktive Breadcrumb-Adressleiste**:
  - Klickbare Pfadsegmente (`Home > Documents > Projects`).
  - Dropdown-Chevrons (`>`) neben jedem Ordner zur schnellen Auswahl von Unterordnern.
  - Klick in den leeren Bereich schaltet nahtlos in ein bearbeitbares Textfeld um (`/home/apex/...`) mit Enter-Navigation.
  - Integrierter Aktualisieren-Button (`F5`).
- **Windows 11 Suchleiste**:
  - Dynamischer Platzhalter ("Downloads durchsuchen").
  - Live-Filterung während des Tippens oder Suchbereinigung mit `✕`.
- **Command Bar (Ribbon)**:
  - `+ Neu` Dropdown (Ordner, Textdokument, Terminal).
  - Schnellaktions-Icons: Ausschneiden (`Strg+X`), Kopieren (`Strg+C`), Einfügen (`Strg+V`), Umbenennen (`F2`), Freigeben, Löschen (in den Papierkorb `Entf`).
  - `Sortieren` Dropdown (Name, Änderungsdatum, Typ, Größe; Aufsteigend / Absteigend).
  - `Ansicht` Dropdown (Große Symbole, Mittelgroße Symbole, Kleine Symbole, Liste, Details, Kacheln, Ausgeblendete Elemente anzeigen).
  - `...` (Mehr) Menü: Im Terminal öffnen, Pfad kopieren, Alles auswählen, Design umschalten (Dark / Light), Eigenschaften (`Alt+Enter`).
- **Navigationsbereich (Sidebar)**:
  - **Startseite / Schnellzugriff**: Desktop, Downloads, Dokumente, Bilder, Musik, Videos, Persönlicher Ordner.
  - **Dieser PC**: Linux-Root-Laufwerk (`/`), Home-Partition (`/home`) und Wechsellaufwerke mit Speicherkapazitätsbalken.
  - **Papierkorb** (Recycle Bin).
- **Dateiansichten**:
  - **Details**: Windows 11 Tabellenansicht mit Name, Änderungsdatum, Typ, formatierter Dateigröße und sortierbaren Spaltenköpfen.
  - **Große Symbole / Rasteransicht**: Fluent-Icon-Karten mit automatischer Zeilenumbruch-Beschriftung.
  - **Liste & Kacheln**.
- **Modernes Windows 11 Kontextmenü**:
  - Horizontale Schnellaktionsleiste oben (Ausschneiden, Kopieren, Umbenennen, Freigeben, Löschen).
  - Öffnen, Im Terminal öffnen, Als Pfad kopieren, Eigenschaften.
- **Windows 11 Eigenschaften-Dialog**:
  - Detailtreuer Dateieigenschaften-Dialog (Allgemein & Sicherheit/Rechte) mit Dateityp, Öffnen mit, Speicherort, Größe, Größe auf Datenträger, Zeitstempeln und Attributen.
- **Tastatur-Kurzbefehle**:
  - `Strg + T`: Neuer Tab
  - `Strg + W`: Aktuellen Tab schließen
  - `Strg + N`: Neues Fenster
  - `Strg + Shift + N`: Neuer Ordner
  - `Strg + C` / `Strg + X` / `Strg + V`: Kopieren, Ausschneiden, Einfügen
  - `Entf`: In den Papierkorb verschieben
  - `F2`: Umbenennen
  - `F5`: Aktualisieren
  - `Alt + Pfeil nach oben`: Übergeordneter Ordner
  - `Alt + Pfeil nach links / rechts`: Zurück / Vorwärts
  - `Strg + L` oder `Alt + D`: Adressleiste fokussieren
  - `Strg + F`: Suchleiste fokussieren
  - `Strg + H`: Ausgeblendete Dateien ein-/ausblenden
  - `Strg + A`: Alles auswählen
  - `Alt + Enter`: Eigenschaften anzeigen

## Starten

### Option 1: Direkt über das Skript
```bash
./run.sh
```

Oder einen beliebigen Pfad öffnen:
```bash
./run.sh ~/Downloads
```

### Option 2: Systemweit über das Terminal
```bash
win11-explorer
```

### Option 3: Über das Anwendungsmenü (KDE Plasma, GNOME, Rofi, etc.)
Drücke die `Super` / `Windows`-Taste und tippe:
```
Windows 11 Explorer
```
