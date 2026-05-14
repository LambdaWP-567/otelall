import os
import json
import requests
import time

def create_dashboard():
    # Use the service name from docker-compose
    host = "http://influxdb:8086"
    url = f"{host}/api/v2/dashboards"
    token = os.getenv("DOCKER_INFLUXDB_INIT_ADMIN_TOKEN")
    org_name = os.getenv("DOCKER_INFLUXDB_INIT_ORG")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }

    print(f"Connecting to InfluxDB at {host}...")

    # Wait for API to be ready
    for _ in range(10):
        try:
            resp = requests.get(f"{host}/health", timeout=5)
            if resp.status_code == 200:
                break
        except:
            pass
        time.sleep(2)

    # 1. Get Org ID
    orgs_resp = requests.get(f"{host}/api/v2/orgs?org={org_name}", headers=headers)
    if orgs_resp.status_code == 200:
        orgs = orgs_resp.json().get("orgs", [])
        if not orgs:
            print(f"Org {org_name} not found")
            return
        org_id = orgs[0]["id"]
    else:
        print(f"Failed to get org ID: {orgs_resp.text}")
        return

    dashboard = {
        "orgID": org_id,
        "name": "OTel Monitoring Dashboard",
        "description": "Dashboard for simulated and host metrics",
        "cells": [
            {
                "name": "Simulated Metrics",
                "x": 0, "y": 0, "w": 12, "h": 4,
                "view": {
                    "properties": {
                        "shape": "chronograf-v2",
                        "type": "xy",
                        "queries": [
                            {
                                "text": "from(bucket: \"metrics\")\n  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)\n  |> filter(fn: (r) => r[\"_measurement\"] == \"cpu_sim\" or r[\"_measurement\"] == \"mem_sim\" or r[\"_measurement\"] == \"disk_sim\")\n  |> filter(fn: (r) => r[\"_field\"] == \"gauge\")\n  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)\n  |> yield(name: \"mean\")",
                                "editMode": "advanced",
                                "name": "mean"
                            }
                        ],
                        "axes": {
                            "x": {"label": "", "show": True},
                            "y": {"label": "Value", "show": True}
                        }
                    }
                }
            }
        ]
    }

    resp = requests.post(url, headers=headers, json=dashboard)
    if resp.status_code == 201:
        print("InfluxDB Dashboard created successfully")
    else:
        print(f"Failed to create InfluxDB dashboard: {resp.text}")

if __name__ == "__main__":
    create_dashboard()
