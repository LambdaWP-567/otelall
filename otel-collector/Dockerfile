# BUILDER STAGE for the watcher
FROM golang:1.24-alpine AS watcher-builder
WORKDIR /app
COPY go.mod go.sum main.go ./
RUN go build -o watcher main.go

# BUILDER STAGE for the custom collector
FROM golang:1.24-alpine AS collector-builder
RUN apk add --no-cache git build-base
RUN go install go.opentelemetry.io/collector/cmd/builder@v0.92.0
WORKDIR /app
COPY <<EOF builder-config.yaml
dist:
  name: otelcol
  description: Custom OTel Collector
  output_path: ./dist
  otelcol_version: 0.92.0

exporters:
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/exporter/influxdbexporter v0.92.0
receivers:
  - gomod: go.opentelemetry.io/collector/receiver/otlpreceiver v0.92.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/receiver/hostmetricsreceiver v0.92.0
processors:
  - gomod: go.opentelemetry.io/collector/processor/batchprocessor v0.92.0
  - gomod: github.com/open-telemetry/opentelemetry-collector-contrib/processor/transformprocessor v0.92.0
EOF

RUN builder --config builder-config.yaml

# FINAL STAGE
FROM alpine:latest
RUN apk add --no-cache ca-certificates
COPY --from=collector-builder /app/dist/otelcol /usr/local/bin/otelcol
COPY --from=watcher-builder /app/watcher /usr/local/bin/watcher

# Standard config location
COPY config/config.yaml /etc/otelcol-config/config.yaml

ENTRYPOINT ["/usr/local/bin/watcher"]
