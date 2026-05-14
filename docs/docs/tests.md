# Test Cases

Das Projekt umfasst verschiedene Testebenen, um die Stabilität und Korrektheit zu gewährleisten.

## 1. Container Start Tests
Es wird für alle Container geprüft, ob sie korrekt starten und ihre Ports binden.

## 2. E2E Test (Container 6)
Der E2E-Test führt folgende Schritte aus:
*   **Warten auf InfluxDB:** Prüft die `/health` API von InfluxDB.
*   **Verifikation der Simulator-Daten:**
    *   `cpu_sim`: Vorhandensein von CPU-Simulationsdaten prüfen.
    *   `mem_sim`: Vorhandensein von Speicher-Simulationsdaten prüfen.
    *   `disk_sim`: Vorhandensein von Disk-Simulationsdaten prüfen.
    *   `const_42`: Prüfen, ob der konstante Wert 42 ankommt.
    *   `inc_999`: Prüfen, ob der inkrementierende Zähler Daten liefert.
*   **Verifikation der Host-Daten:**
    *   Prüft auf `system.cpu.load_average.1m` und `system.memory.usage`.

## 3. Manueller Dashboard Test
Nach dem Start kann in Grafana unter dem "OTel Dashboard" visuell geprüft werden, ob die Graphen live aktualisiert werden.
