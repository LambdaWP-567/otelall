# OTel All-in-One Monitoring Stack

Dieses Projekt bietet eine schlüsselfertige Monitoring-Lösung basierend auf **OpenTelemetry**, **InfluxDB v2** und **Grafana**.

## 🚀 Schnellstart

Stellen Sie sicher, dass Docker und Docker Compose installiert sind.

```bash
docker compose up --build
```

Nach dem Start sind folgende Oberflächen erreichbar:

| Dienst | URL | Beschreibung |
| :--- | :--- | :--- |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | Visualisierung (Admin / admin) |
| **InfluxDB UI** | [http://localhost:8086](http://localhost:8086) | Datenbank-Management |
| **Smart Configurator** | [http://localhost:8001](http://localhost:8001) | **Neue strukturierte UI** |
| **Expert Configurator** | [http://localhost:8000](http://localhost:8000) | YAML Editor (Backup) |

## 🏗 Architektur

Das System besteht aus 7 Docker-Containern:
- **InfluxDB v2 & Grafana:** Mit automatischer Dashboard-Provisionierung.
- **Custom OTel Collector:** Mit Go-Watcher für Konfigurationsänderungen.
- **Smart Config UI (Neu):** Strukturierte Oberfläche zur Konfiguration von Endpunkten, Scrapern und Pipelines.
- **Simulator:** Kontinuierliche Erzeugung von Testmetriken.
- **E2E-Tests:** Automatische Validierung.

## 🛠 Besonderheiten
- **Transformations-Logik:** Werte > 90 werden mit -1 multipliziert (Beispiel-Prozessor).
- **Integritätsprüfung:** Die Smart UI validiert die Konfiguration, bevor sie gespeichert wird.
