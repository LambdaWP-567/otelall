# Custom OTel Collector

Der Collector wurde speziell für dieses Projekt mit dem `ocb` (OpenTelemetry Collector Builder) erstellt.

## Besonderheiten

*   **Minimalistisches Design:** Enthält nur die notwendigen Komponenten (`otlp`, `hostmetrics`, `influxdb`, `transform`).
*   **Watcher-Dienst:** Ein in Go geschriebener Wrapper (`watcher`) überwacht die `config.yaml`. Bei Änderungen wird der Collector-Prozess automatisch neu gestartet.
*   **Host-Monitoring:** Erfasst Metriken des zugrunde liegenden Host-Systems.

## Datenverarbeitung (Transform Processor)

Der Collector enthält ein Beispiel für die Datenverarbeitung zur Laufzeit. In der `config.yaml` ist folgende Regel konfiguriert:

```yaml
processors:
  transform:
    metric_statements:
      - context: datapoint
        statements:
          - set(value_double, value_double * -1) where value_double > 90
          - set(value_int, value_int * -1) where value_int > 90
```

Diese Regel stellt sicher, dass alle Messwerte über 90 (z.B. hohe CPU-Spitzen in der Simulation) als negative Werte gespeichert werden, um sie in Grafana hervorzuheben.
