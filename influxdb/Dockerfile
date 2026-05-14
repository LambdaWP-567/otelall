FROM influxdb:2.7-alpine

RUN apk add --no-cache python3 py3-requests

COPY provision_dashboard.py /usr/local/bin/provision_dashboard.py

# We can't run it during build because influx isn't running.
# We will use a custom entrypoint or just run it in the background on startup.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["influxd"]
