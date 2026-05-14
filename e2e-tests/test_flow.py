import os
import time
import requests
import sys

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "myorg")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "metrics")
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://grafana:3000")

def query_influxdb(query):
    url = f"{INFLUXDB_URL}/api/v2/query?org={INFLUXDB_ORG}"
    headers = {
        "Authorization": f"Token {INFLUXDB_TOKEN}",
        "Content-Type": "application/vnd.flux",
        "Accept": "application/csv"
    }
    response = requests.post(url, headers=headers, data=query)
    response.raise_for_status()
    return response.text

def check_metric(measurement):
    query = f'from(bucket: "{INFLUXDB_BUCKET}") |> range(start: -1m) |> filter(fn: (r) => r["_measurement"] == "{measurement}")'
    result = query_influxdb(query)
    return len(result.strip().split("\n")) > 1

def wait_for_service(name, url, expected_status=200):
    print(f"Waiting for {name} at {url}...")
    for _ in range(30):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == expected_status:
                print(f"{name} is up!")
                return True
        except:
            pass
        time.sleep(2)
    return False

def main():
    if not wait_for_service("InfluxDB", f"{INFLUXDB_URL}/health"):
        print("InfluxDB did not become healthy in time.")
        sys.exit(1)

    if not wait_for_service("Grafana", f"{GRAFANA_URL}/api/health"):
        print("Grafana did not become healthy in time.")
        sys.exit(1)

    # Give some time for metrics to flow
    print("Waiting 15 seconds for metrics to flow...")
    time.sleep(15)

    metrics_to_check = ["cpu_sim", "mem_sim", "disk_sim", "const_42", "inc_999"]

    # Also check for some host metrics
    metrics_to_check.extend(["system.cpu.load_average.1m", "system.memory.usage"])

    all_passed = True
    for metric in metrics_to_check:
        print(f"Checking for metric: {metric}...", end=" ")
        if check_metric(metric):
            print("FOUND")
        else:
            print("NOT FOUND")
            all_passed = False

    if all_passed:
        print("\nAll E2E tests PASSED!")
        sys.exit(0)
    else:
        print("\nSome E2E tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
