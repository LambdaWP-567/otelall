# OTel All-in-One Projekt

Dieses Projekt bietet eine vollständige Pipeline zur Erfassung, Verarbeitung und Visualisierung von Metriken mittels OpenTelemetry, InfluxDB und Grafana.

## Schnellstart

Um das gesamte System zu starten, führen Sie den folgenden Befehl im Wurzelverzeichnis aus:

```bash
docker-compose up --build
```

Nach dem Start sind folgende Dienste verfügbar:

*   **Grafana:** [http://localhost:3000](http://localhost:3000) (Admin / admin)
*   **InfluxDB:** [http://localhost:8086](http://localhost:8086)
*   **Config UI:** [http://localhost:8000](http://localhost:8000)

## Enthaltene Container

1.  **InfluxDB v2:** Zeitreihendatenbank zur Speicherung der Metriken.
2.  **Grafana:** Dashboard zur Visualisierung der Daten.
3.  **Custom OTel Collector:** Selbstgebauter Collector, der Metriken empfängt und weiterleitet.
4.  **Config UI:** Web-Oberfläche zur Live-Konfiguration des Collectors.
5.  **Simulator:** Erzeugt Test-Metriken (CPU, RAM, Disk, etc.).
6.  **E2E-Tests:** Automatische Validierung der gesamten Datenkette.
