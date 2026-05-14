# Erweiterung des Collectors

Um den Collector um weitere Komponenten (Receiver, Processors, Exporters) zu erweitern, müssen Sie das `Dockerfile` im Verzeichnis `otel-collector` anpassen.

## Schritte zur Erweiterung

1.  **Builder-Config anpassen:** Öffnen Sie das `Dockerfile` und suchen Sie den Abschnitt `COPY <<EOF builder-config.yaml`.
2.  **Komponente hinzufügen:** Fügen Sie die gewünschte Komponente unter dem entsprechenden Schlüssel hinzu. Beispiel für den `logging` exporter:
    ```yaml
    exporters:
      - gomod: go.opentelemetry.io/collector/exporter/loggingexporter v0.92.0
    ```
3.  **Neu bauen:** Führen Sie `docker-compose build otel-collector` aus.
4.  **Konfigurieren:** Aktivieren Sie die neue Komponente in der `config.yaml` (entweder direkt oder über die Config UI).

Eine vollständige Liste verfügbarer Komponenten finden Sie im [opentelemetry-collector-contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) Repository.
