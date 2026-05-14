# Config UI v2 (Smart Configurator)

Die Smart Config UI bietet eine strukturierte Möglichkeit, den OTel-Collector zu verwalten, ohne YAML-Kenntnisse vorauszusetzen.

## Funktionen

*   **Endpoint Management:** IP und Port des OTLP-Receivers können getrennt bearbeitet werden.
*   **Scraper Auswahl:** Ein Multi-Selektor für Host-Metrik-Scraper (CPU, Mem, Disk, etc.).
*   **Pipeline Builder:** Grafische Auswahl von Receivern, Processoren und Exportern.
*   **Transform Logic:** Ein vereinfachtes Interface für Schwellenwert-Operationen.

## Sicherheit und Validierung

Die UI liest die bestehende `config.yaml` ein und stellt sicher, dass beim Speichern ein valides YAML-Format beibehalten wird. Durch die Nutzung von Dropdown-Menüs und Checkboxen wird verhindert, dass ungültige Komponentennamen eingegeben werden.
