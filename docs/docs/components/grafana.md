# Grafana

Grafana dient zur Visualisierung der in InfluxDB gespeicherten Metriken.

## Automatische Einrichtung

Grafana ist so vorkonfiguriert, dass es beim Start automatisch:
1.  Die InfluxDB-Datenquelle verbindet.
2.  Das "OTel Dashboard" importiert.

## Dashboards

Das bereitgestellte Dashboard enthält Panels für:
*   **Simulierte Ressourcen:** Kombinierte Ansicht von CPU-, Speicher- und Disk-Simulationen.
*   **Konstante & Inkrementelle Werte:** Visualisierung der Test-Metriken 42 und 0-999.
*   **Host-Metriken:** Beispielhafte Darstellung von System-Last und Speicherverbrauch des Hosts.
