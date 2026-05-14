# Config UI

Die Config UI ist eine Python-basierte Webanwendung (FastAPI), die eine einfache Schnittstelle zur Verwaltung der OTel-Collector-Konfiguration bietet.

## Funktionen

*   **Live-Editor:** Bearbeiten der `config.yaml` direkt im Browser.
*   **Automatischer Neustart:** Beim Speichern wird die Datei im Shared Volume aktualisiert. Der Collector erkennt dies und startet seinen internen Prozess neu.
*   **Sicherheit:** Läuft ohne privilegierte Rechte durch Nutzung von Shared Volumes statt Docker-Socket-Zugriff.
