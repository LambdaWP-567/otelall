#!/bin/bash
set -e

# Start InfluxDB in the background
/usr/local/bin/docker-entrypoint.sh influxd &

# Wait for InfluxDB to start and then run the provisioning script
python3 /usr/local/bin/provision_dashboard.py &

# Wait for the background influxd process
wait -n
