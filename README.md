# OTel All-in-One Monitoring Stack

Dieses Projekt bietet eine schlüsselfertige Monitoring-Lösung basierend auf **OpenTelemetry**, **InfluxDB v2** und **Grafana**. Es umfasst eine vollständige Pipeline von der Metrikerzeugung über die Verarbeitung bis hin zur Visualisierung.

## 🚀 Schnellstart

Stellen Sie sicher, dass Docker und Docker Compose installiert sind.

```bash
docker compose up --build
```

Nach dem Start sind folgende Oberflächen erreichbar:

| Dienst | URL | Anmeldedaten |
| :--- | :--- | :--- |
| **Grafana** | [http://localhost:3000](http://localhost:3000) | `admin` / `admin` |
| **InfluxDB UI** | [http://localhost:8086](http://localhost:8086) | `admin` / `password123` |
| **Config UI** | [http://localhost:8000](http://localhost:8000) | - |

## 🏗 Architektur

Das System besteht aus 6 Docker-Containern:

1.  **InfluxDB v2:** Zeitreihendatenbank zur Speicherung der Metriken.
2.  **Grafana:** Visualisierung der Daten mittels vorkonfigurierter Dashboards.
3.  **Custom OTel Collector:** Ein spezialisierter Collector, der Metriken verarbeitet (inkl. Transformationen) und weiterleitet.
4.  **Config UI:** Eine Web-Oberfläche (FastAPI), um die Collector-Konfiguration live anzupassen.
5.  **Simulator:** Ein Python-Dienst, der kontinuierlich Testmetriken erzeugt.
6.  **E2E-Tests:** Validiert automatisch die gesamte Pipeline beim Start.

## 🛠 Besonderheiten

*   **Custom Collector Build:** Der Collector wird mittels `ocb` minimal gebaut und enthält einen Go-basierten Watcher für Konfigurationsänderungen.
*   **Datenverarbeitung:** Beinhaltet ein Beispiel für den `transformprocessor`, der Werte über 90 mit -1 multipliziert.
*   **Sicherheit:** Die UI benötigt keinen Zugriff auf den Docker-Socket, sondern nutzt Shared Volumes.
*   **CI/CD:** Automatisierte Builds und Tests via GitHub Actions sowie Deployment der Dokumentation auf GitHub Pages.

## 📚 Dokumentation

Die ausführliche Dokumentation finden Sie im Ordner `docs/` oder (nach Deployment) auf den GitHub Pages dieses Repositories.
