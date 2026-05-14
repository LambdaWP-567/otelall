from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import yaml
import os
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

CONFIG_PATH = "/etc/otelcol-config/config.yaml"

# Supported components (for multi-select)
AVAILABLE_RECEIVERS = ["otlp", "hostmetrics", "prometheus", "jaeger", "kafka"]
AVAILABLE_PROCESSORS = ["batch", "transform", "memory_limiter", "resource", "attributes"]
AVAILABLE_EXPORTERS = ["influxdb", "logging", "otlp", "otlphttp", "prometheusremotewrite"]
AVAILABLE_SCRAPERS = ["cpu", "memory", "disk", "network", "load", "filesystem", "processes"]

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    config = load_config()

    # Parse OTLP endpoint
    otlp_endpoint = config.get("receivers", {}).get("otlp", {}).get("protocols", {}).get("grpc", {}).get("endpoint", "0.0.0.0:4317")
    ip, port = otlp_endpoint.split(":") if ":" in otlp_endpoint else ("0.0.0.0", "4317")

    # Active components in pipelines
    metrics_pipeline = config.get("service", {}).get("pipelines", {}).get("metrics", {})
    active_receivers = metrics_pipeline.get("receivers", [])
    active_processors = metrics_pipeline.get("processors", [])
    active_exporters = metrics_pipeline.get("exporters", [])

    # Active scrapers
    active_scrapers = list(config.get("receivers", {}).get("hostmetrics", {}).get("scrapers", {}).keys())

    # Transform statements
    transform_statements = config.get("processors", {}).get("transform", {}).get("metric_statements", [])
    # Simplify for UI: extract value > X logic
    simple_transforms = []
    for entry in transform_statements:
        for stmt in entry.get("statements", []):
            match = re.search(r"where (value_double|value_int) > (\d+)", stmt)
            if match:
                simple_transforms.append({"threshold": match.group(2)})

    return templates.TemplateResponse(request=request, name="index.html", context={
        "config": config,
        "otlp_ip": ip,
        "otlp_port": port,
        "available_receivers": AVAILABLE_RECEIVERS,
        "active_receivers": active_receivers,
        "available_processors": AVAILABLE_PROCESSORS,
        "active_processors": active_processors,
        "available_exporters": AVAILABLE_EXPORTERS,
        "active_exporters": active_exporters,
        "available_scrapers": AVAILABLE_SCRAPERS,
        "active_scrapers": active_scrapers,
        "simple_transforms": simple_transforms
    })

@app.post("/save")
async def handle_save(
    request: Request,
    otlp_ip: str = Form(...),
    otlp_port: str = Form(...),
    receivers: list = Form([]),
    processors: list = Form([]),
    exporters: list = Form([]),
    scrapers: list = Form([]),
    transform_threshold: str = Form(None)
):
    config = load_config()

    # Update OTLP endpoint
    if "receivers" not in config: config["receivers"] = {}
    if "otlp" not in config["receivers"]: config["receivers"]["otlp"] = {"protocols": {"grpc": {}, "http": {}}}
    config["receivers"]["otlp"]["protocols"]["grpc"]["endpoint"] = f"{otlp_ip}:{otlp_port}"
    config["receivers"]["otlp"]["protocols"]["http"]["endpoint"] = f"{otlp_ip}:{int(otlp_port)+1}"

    # Update Scrapers
    if "hostmetrics" not in config["receivers"]: config["receivers"]["hostmetrics"] = {"scrapers": {}}
    config["receivers"]["hostmetrics"]["scrapers"] = {s: {} for s in scrapers}
    config["receivers"]["hostmetrics"]["root_path"] = "/hostfs"
    config["receivers"]["hostmetrics"]["collection_interval"] = "10s"

    # Update Pipeline
    if "service" not in config: config["service"] = {"pipelines": {"metrics": {}}}
    config["service"]["pipelines"]["metrics"]["receivers"] = receivers
    config["service"]["pipelines"]["metrics"]["processors"] = processors
    config["service"]["pipelines"]["metrics"]["exporters"] = exporters

    # Update Transform Processor
    if transform_threshold:
        if "processors" not in config: config["processors"] = {}
        config["processors"]["transform"] = {
            "metric_statements": [{
                "context": "datapoint",
                "statements": [
                    f"set(value_double, value_double * -1) where value_double > {transform_threshold}",
                    f"set(value_int, value_int * -1) where value_int > {transform_threshold}"
                ]
            }]
        }

    save_config(config)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
