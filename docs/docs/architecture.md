# Architektur

Die Systemarchitektur basiert auf einer containerisierten Microservice-Struktur.

```mermaid
graph TD
    Host[Host System] -->|Metriken| Collector
    Sim[Simulator] -->|OTLP/gRPC| Collector
    UI[Config UI] -->|Schreibt config.yaml| Vol[(Shared Volume)]
    Vol -->|Liest config.yaml| Collector
    Collector -->|Write| InfluxDB[(InfluxDB v2)]
    InfluxDB -->|Query/Flux| Grafana[Grafana Dashboards]
    E2E[E2E Tests] -->|Prüft Daten| InfluxDB
```

## Datenfluss

1.  Der **Simulator** erzeugt sekündlich künstliche Metriken.
2.  Der **Hostmetrics Receiver** im Collector liest Systemdaten des Hosts.
3.  Der **Custom OTel Collector** verarbeitet diese Daten (Batching) und sendet sie an **InfluxDB**.
4.  **Grafana** visualisiert die Daten mittels vordefinierter Dashboards.
5.  Die **Config UI** ermöglicht es, die Pipeline des Collectors zur Laufzeit anzupassen.
