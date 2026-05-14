# InfluxDB

Dieses Projekt verwendet InfluxDB v2.7 als zentrale Zeitreihendatenbank.

## Konfiguration

Die Datenbank wird automatisch über Umgebungsvariablen in der `docker-compose.yml` initialisiert:
*   **Organisation:** `myorg`
*   **Bucket:** `metrics`
*   **Token:** `mysecrettoken` (Voreingestellt für Demo-Zwecke)

## Persistenz

Die Daten werden im Docker-Volume `influxdb_data` gespeichert, um Neustarts zu überstehen.
