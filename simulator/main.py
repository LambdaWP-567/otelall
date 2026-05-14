import time
import random
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

# Resource information
resource = Resource(attributes={
    "service.name": "simulator"
})

# OTLP Exporter
exporter = OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=1000)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter("simulator-meter")

# Define metrics
cpu_sim = meter.create_gauge("cpu_sim", description="Simulated CPU usage")
mem_sim = meter.create_gauge("mem_sim", description="Simulated Memory usage")
disk_sim = meter.create_gauge("disk_sim", description="Simulated Disk write operations")
const_42 = meter.create_gauge("const_42", description="Constant value 42")
inc_999 = meter.create_gauge("inc_999", description="Incrementing value up to 999")

counter_val = 0

print("Simulator started, sending metrics to otel-collector:4317...")

try:
    while True:
        # 1. CPU Simulation (Random 0-100)
        cpu_sim.set(random.uniform(0, 100))

        # 2. Memory Simulation (Random 2048-8192 MB)
        mem_sim.set(random.uniform(2048, 8192))

        # 3. Disk Write Simulation (Random 0-500 MB/s)
        disk_sim.set(random.uniform(0, 500))

        # 4. Constant 42
        const_42.set(42)

        # 5. Incrementing 0-999
        inc_999.set(counter_val)
        counter_val += 1
        if counter_val > 999:
            counter_val = 0

        time.sleep(1)
except KeyboardInterrupt:
    print("Simulator stopped.")
