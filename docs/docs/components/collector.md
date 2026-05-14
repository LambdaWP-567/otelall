# Custom OTel Collector

Der Collector wurde speziell für dieses Projekt mit dem `ocb` (OpenTelemetry Collector Builder) erstellt.

## Besonderheiten

*   **Minimalistisches Design:** Enthält nur die notwendigen Komponenten (`otlp`, `hostmetrics`, `influxdb`).
*   **Watcher-Dienst:** Ein in Go geschriebener Wrapper (`watcher`) überwacht die `config.yaml`. Bei Änderungen wird der Collector-Prozess automatisch neu gestartet, ohne dass der Container beendet werden muss.
*   **Host-Monitoring:** Durch Mounten von `/proc`, `/sys` und dem Root-Dateisystem kann der Collector Metriken des zugrunde liegenden Host-Systems erfassen.

## Konfiguration

Die Konfiguration befindet sich unter `otel-collector/config/config.yaml` und wird über ein Shared Volume auch der Config UI zugänglich gemacht.
