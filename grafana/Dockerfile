FROM grafana/grafana:10.2.0

USER root
RUN apk add --no-cache curl
USER grafana

COPY provisioning /etc/grafana/provisioning
