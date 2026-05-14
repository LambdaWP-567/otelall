# Simulator

Der Simulator ist eine Python-Anwendung, die künstliche Last erzeugt, um die Pipeline zu testen.

## Erzeugte Metriken

1.  **CPU Simulation:** Zufallswerte zwischen 0 und 100 %.
2.  **Speichersimulation:** Zufallswerte zwischen 2048 und 8192 MB.
3.  **Disk Write Simulation:** Zufallswerte für Schreibvorgänge (0-500 MB/s).
4.  **Konstante 42:** Schreibt jede Sekunde den Wert 42.
5.  **Inkrementeller Zähler:** Erhöht einen Wert von 0 bis 999 und beginnt dann von vorn.

## Übertragung

Die Metriken werden via **OTLP/gRPC** an den Collector gesendet.
