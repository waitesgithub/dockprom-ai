# Observability 3.0: AI-Powered APM = AI Stack + Observability Stack

## Docker Monitoring with AI Observability

A comprehensive monitoring solution for Docker hosts and containers with [Prometheus](https://prometheus.io/), [Grafana](http://grafana.org/), [cAdvisor](https://github.com/google/cadvisor), [NodeExporter](https://github.com/prometheus/node_exporter), [AlertManager](https://github.com/prometheus/alertmanager), [Loki](https://grafana.com/oss/loki/), [Tempo](https://grafana.com/oss/tempo/), and [OpenTelemetry](https://opentelemetry.io/) - enhanced with AI-powered monitoring capabilities.

<img width="4877" height="3408" alt="image" src="https://github.com/user-attachments/assets/2f026eaf-bd8c-44b2-969a-eae52f3188ff" />

In today's cloud-based world, observability is no longer just about collecting logs, metrics, and traces. We can take observability to the next level with AI-powered APM (Application Performance Monitoring). Tools like Claude (cloud-based AI) and Ollama (self-hosted AI), combined with Prometheus, Grafana, Loki, Tempo, and OpenTelemetry, enable us to create an intelligent observability ecosystem. In this hands-on guide, I'll show you step-by-step how to integrate AI with observability platforms. We'll run with various LLM models and compare their results. The integration of AI and observability systems will enable real-time anomaly detection and faster root cause analysis for your systems.

## 📗 Medium Articles

- [📝Observability 3.0 AI-Powered APM = Claude (cloud-based) / Ollama (self-hosted) + MCP Server + n8n + Prometheus, Grafana, Loki, Tempo, OpenTelemetry, PostgreSQL Exporter, Node Exporter, cAdvisor, Promtail, Alert Manager — A Comprehensive Hands-On Guide for Live Monitoring with LLMs (Large Language Models)](https://cmakkaya.medium.com/observability-3-0-ai-powered-apm-claude-cloud-based-ollama-self-hosted-mcp-server-n8n-monitor-6ea436e271fe?postPublishedType=repub)

- [📝Introduction Observability 3.0: AI-Powered APM = AI Stack + Observability Stack— A Hands-On Guide (Part-2)](https://cmakkaya.medium.com/introduction-observability-3-0-ai-powered-apm-ai-stack-observability-stack-part-2-33b1d6a262d7?postPublishedType=repub)

- [📝Observability 3.0: AI-Powered APM = Claude (cloud-based) + MCP Server + Observability Stack — A Comprehensive Hands-On Guide for Live Monitoring with LLMs (Part-3)](https://cmakkaya.medium.com/observability-3-0-5d3ccd6d42de?postPublishedType=repub)

- [📝Observability 3.0: AI-Powered APM = Ollama (self-hosted) + GrafanaToolServer + Observability Stack — A Comprehensive Hands-On Guide for Live Monitoring with LLMs (Part-4)]() `soon.`

## Install

Clone this repository on your Docker host, cd into dockprom-ai directory and run compose up:

```bash
git clone https://github.com/waitesgithub/dockprom-ai
cd dockprom-ai

ADMIN_USER='admin' ADMIN_PASSWORD='admin' ADMIN_PASSWORD_HASH='$2a$14$1l.IozJx7xQRVmlkEQ32OeEEfP5mRxTpbDTCTcXRqn19gXD8YK1pO' docker-compose up -d
```

**Caddy v2 does not accept plaintext passwords. It MUST be provided as a hash value. The above password hash corresponds to ADMIN_PASSWORD 'admin'. To know how to generate hash password, refer [Updating Caddy to v2](#updating-caddy-to-v2)**

Prerequisites:

* Docker Engine >= 1.13
* Docker Compose >= 1.11

## Containers

* Prometheus (metrics database) `http://<host-ip>:9090`
* Prometheus-Pushgateway (push acceptor for ephemeral and batch jobs) `http://<host-ip>:9091`
* AlertManager (alerts management) `http://<host-ip>:9093`
* Grafana (visualize metrics) `http://<host-ip>:3000`
* Loki (logs database) `http://<host-ip>:3100`
* Tempo (traces database) `http://<host-ip>:3200`
* OpenTelemetry Collector (OTLP ingest) `http://<host-ip>:4318` and `<host-ip>:4317`
* Ollama Gateway (HTTP proxy + tracing/metrics) `http://<host-ip>:11435`
* NodeExporter (host metrics collector)
* cAdvisor (containers metrics collector)
* Alloy (Docker logs collector → Loki)
* Caddy (reverse proxy and basic auth provider for prometheus/alertmanager/loki/tempo)

## AI Observability (Ollama + OTEL + Loki + Tempo)

This repo extends traditional monitoring with a **drop-in observability bundle** for AI/LLM apps:

- **Traces**: Apps (or the Ollama gateway) send OTLP traces to `otel-collector` → stored in **Tempo** → viewed in **Grafana**
- **Logs**: Docker container logs are collected by **Alloy** → stored in **Loki** → viewed in **Grafana**
- **Metrics**: OTLP metrics can be sent to `otel-collector` and are exposed for **Prometheus** scraping
- **Ollama gateway**: an Envoy proxy that forwards to your host Ollama and emits **request-level tracing + Prometheus metrics** automatically

### 1) Make host Ollama reachable from containers

The gateway runs in Docker and forwards to `host.docker.internal:11434`. On Linux, that resolves to the host gateway IP, but **Ollama must listen on a non-loopback interface**.

For example:

```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

### 2) Call Ollama through the gateway (no-code option)

Point users/apps at:

- **Gateway**: `http://<host-ip>:11435`

This gives you:

- **Tempo traces** for each request
- **Prometheus metrics** for RPS/latency/errors (Envoy)
- **Loki logs** for gateway/access logs (via Docker log collection)

### 3) OTEL setup for apps (host + Docker)

If you *also* instrument your app (recommended), set OTEL exporter endpoint to the collector.

**Apps running on the host:**

```bash
export OTEL_SERVICE_NAME="my-app"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://127.0.0.1:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
```

**Apps running in Docker on the same `monitor-net` network:**

```bash
OTEL_SERVICE_NAME=my-app
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

Notes:
- The gateway gives you **transport-level observability** (latency/errors/throughput). Token/cost/quality metrics typically require **app-level instrumentation**.

## Setup Grafana

Navigate to `http://<host-ip>:3000` and login with user ***admin*** password ***admin***. You can change the credentials in the compose file or by supplying the `ADMIN_USER` and `ADMIN_PASSWORD` environment variables on compose up. The config file can be added directly in grafana part like this

```yaml
grafana:
  image: grafana/grafana:12.0.2
  env_file:
    - config
```

and the config file format should have this content

```yaml
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=changeme
GF_USERS_ALLOW_SIGN_UP=false
```

If you want to change the password, you have to remove this entry, otherwise the change will not take effect

```yaml
- grafana_data:/var/lib/grafana
```

Grafana is preconfigured with dashboards and Prometheus as the default data source:

* Name: Prometheus
* Type: Prometheus
* Url: [http://prometheus:9090](http://prometheus:9090)
* Access: proxy

***Docker Host Dashboard***

![Host](screens/Grafana_Docker_Host.png)

The Docker Host Dashboard shows key metrics for monitoring the resource usage of your server:

* Server uptime, CPU idle percent, number of CPU cores, available memory, swap and storage
* System load average graph, running and blocked by IO processes graph, interrupts graph
* CPU usage graph by mode (guest, idle, iowait, irq, nice, softirq, steal, system, user)
* Memory usage graph by distribution (used, free, buffers, cached)
* IO usage graph (read Bps, read Bps and IO time)
* Network usage graph by device (inbound Bps, Outbound Bps)
* Swap usage and activity graphs

For storage and particularly Free Storage graph, you have to specify the fstype in grafana graph request.
You can find it in `grafana/provisioning/dashboards/docker_host.json`, at line 480 :

```yaml
"expr": "sum(node_filesystem_free_bytes{fstype=\"btrfs\"})",
```

I work on BTRFS, so i need to change `aufs` to `btrfs`.

You can find right value for your system in Prometheus `http://<host-ip>:9090` launching this request :

```yaml
node_filesystem_free_bytes
```

***Docker Containers Dashboard***

![Containers](screens/Grafana_Docker_Containers.png)

The Docker Containers Dashboard shows key metrics for monitoring running containers:

* Total containers CPU load, memory and storage usage
* Running containers graph, system load graph, IO usage graph
* Container CPU usage graph
* Container memory usage graph
* Container cached memory usage graph
* Container network inbound usage graph
* Container network outbound usage graph

Note that this dashboard doesn't show the containers that are part of the monitoring stack.

For storage and particularly Storage Load graph, you have to specify the fstype in grafana graph request.
You can find it in `grafana/provisioning/dashboards/docker_containers.json`, at line 406 :

```yaml
"expr": "(node_filesystem_size_bytes{fstype=\"btrfs\"} - node_filesystem_free_bytes{fstype=\"btrfs\"}) / node_filesystem_size_bytes{fstype=\"btrfs\"}  * 100"，
```

I work on BTRFS, so i need to change `aufs` to `btrfs`.

You can find right value for your system in Prometheus `http://<host-ip>:9090` launching this request :

```yaml
node_filesystem_size_bytes
node_filesystem_free_bytes
```

***Monitor Services Dashboard***

![Monitor Services](screens/Grafana_Prometheus.png)

The Monitor Services Dashboard shows key metrics for monitoring the containers that make up the monitoring stack:

* Prometheus container uptime, monitoring stack total memory usage, Prometheus local storage memory chunks and series
* Container CPU usage graph
* Container memory usage graph
* Prometheus chunks to persist and persistence urgency graphs
* Prometheus chunks ops and checkpoint duration graphs
* Prometheus samples ingested rate, target scrapes and scrape duration graphs
* Prometheus HTTP requests graph
* Prometheus alerts graph

## Define alerts

Three alert groups have been setup within the [alert.rules](prometheus/alert.rules) configuration file:

* Monitoring services alerts [targets](prometheus/alert.rules#L2-L11)
* Docker Host alerts [host](prometheus/alert.rules#L13-L40)
* Docker Containers alerts [containers](prometheus/alert.rules#L42-L69)

You can modify the alert rules and reload them by making a HTTP POST call to Prometheus:

```bash
curl -X POST http://admin:admin@<host-ip>:9090/-/reload
```

***Monitoring services alerts***

Trigger an alert if any of the monitoring targets (node-exporter and cAdvisor) are down for more than 30 seconds:

```yaml
- alert: monitor_service_down
    expr: up == 0
    for: 30s
    labels:
      severity: critical
    annotations:
      summary: "Monitor service non-operational"
      description: "Service {{ $labels.instance }} is down."
```

***Docker Host alerts***

Trigger an alert if the Docker host CPU is under high load for more than 30 seconds:

```yaml
- alert: high_cpu_load
    expr: node_load1 > 1.5
    for: 30s
    labels:
      severity: warning
    annotations:
      summary: "Server under high load"
      description: "Docker host is under high load, the avg load 1m is at {{ $value}}. Reported by instance {{ $labels.instance }} of job {{ $labels.job }}."
```

Modify the load threshold based on your CPU cores.

Trigger an alert if the Docker host memory is almost full:

```yaml
- alert: high_memory_load
    expr: (sum(node_memory_MemTotal_bytes) - sum(node_memory_MemFree_bytes + node_memory_Buffers_bytes + node_memory_Cached_bytes) ) / sum(node_memory_MemTotal_bytes) * 100 > 85
    for: 30s
    labels:
      severity: warning
    annotations:
      summary: "Server memory is almost full"
      description: "Docker host memory usage is {{ humanize $value}}%. Reported by instance {{ $labels.instance }} of job {{ $labels.job }}."
```

Trigger an alert if the Docker host storage is almost full:

```yaml
- alert: high_storage_load
    expr: (node_filesystem_size_bytes{fstype="aufs"} - node_filesystem_free_bytes{fstype="aufs"}) / node_filesystem_size_bytes{fstype="aufs"}  * 100 > 85
    for: 30s
    labels:
      severity: warning
    annotations:
      summary: "Server storage is almost full"
      description: "Docker host storage usage is {{ humanize $value}}%. Reported by instance {{ $labels.instance }} of job {{ $labels.job }}."
```

***Docker Containers alerts***

Trigger an alert if a container is down for more than 30 seconds:

```yaml
- alert: jenkins_down
    expr: absent(container_memory_usage_bytes{name="jenkins"})
    for: 30s
    labels:
      severity: critical
    annotations:
      summary: "Jenkins down"
      description: "Jenkins container is down for more than 30 seconds."
```

Trigger an alert if a container is using more than 10% of total CPU cores for more than 30 seconds:

```yaml
- alert: jenkins_high_cpu
    expr: sum(rate(container_cpu_usage_seconds_total{name="jenkins"}[1m])) / count(node_cpu_seconds_total{mode="system"}) * 100 > 10
    for: 30s
    labels:
      severity: warning
    annotations:
      summary: "Jenkins high CPU usage"
      description: "Jenkins CPU usage is {{ humanize $value}}%."
```

Trigger an alert if a container is using more than 1.2GB of RAM for more than 30 seconds:

```yaml
- alert: jenkins_high_memory
    expr: sum(container_memory_usage_bytes{name="jenkins"}) > 1200000000
    for: 30s
    labels:
      severity: warning
    annotations:
      summary: "Jenkins high memory usage"
      description: "Jenkins memory consumption is at {{ humanize $value}}."
```

## Setup alerting

The AlertManager service is responsible for handling alerts sent by Prometheus server.
AlertManager can send notifications via email, Pushover, Slack, HipChat or any other system that exposes a webhook interface.
A complete list of integrations can be found [here](https://prometheus.io/docs/alerting/configuration).

You can view and silence notifications by accessing `http://<host-ip>:9093`.

The notification receivers can be configured in [alertmanager/config.yml](alertmanager/config.yml) file.

To receive alerts via Slack you need to make a custom integration by choose ***incoming web hooks*** in your Slack team app page.
You can find more details on setting up Slack integration [here](http://www.robustperception.io/using-slack-with-the-alertmanager/).

Copy the Slack Webhook URL into the ***api_url*** field and specify a Slack ***channel***.

```yaml
route:
    receiver: 'slack'

receivers:
    - name: 'slack'
      slack_configs:
          - send_resolved: true
            text: "{{ .CommonAnnotations.description }}"
            username: 'Prometheus'
            channel: '#<channel>'
            api_url: 'https://hooks.slack.com/services/<webhook-id>'
```

![Slack Notifications](screens/Slack_Notifications.png)

## Sending metrics to the Pushgateway

The [pushgateway](https://github.com/prometheus/pushgateway) is used to collect data from batch jobs or from services.

To push data, simply execute:

```bash
echo "some_metric 3.14" | curl --data-binary @- http://user:password@localhost:9091/metrics/job/some_job
```

Please replace the `user:password` part with your user and password set in the initial configuration (default: `admin:admin`).

## Updating Caddy to v2

Perform a `docker run --rm caddy caddy hash-password --plaintext 'ADMIN_PASSWORD'` in order to generate a hash for your new password.
ENSURE that you replace `ADMIN_PASSWORD` with new plain text password and `ADMIN_PASSWORD_HASH` with the hashed password references in [docker-compose.yml](./docker-compose.yml) for the caddy container.

---

## Additional Resources

### 📗 Learn More About AI and Observability

- [📝 AWS AI Services-2: Hands-on use cases for Amazon Rekognition](https://cmakkaya.medium.com/aws-ai-services-2-hands-on-use-cases-for-amazon-rekognition-4d98501ddcee)

- [📝 AWS AI Services-1: What are Artificial Intelligence (AI) and AWS AI Services?](https://cmakkaya.medium.com/aws-ai-services-1-what-is-artificial-intelligence-ai-and-aws-ai-services-c5f2adf60243)

- [📝 Developing a Scalable AI Chatbot Using Azure OpenAI (LLM provider), Java Microservices, and MySQL – A Complete Guide](https://medium.com/@cmakkaya/developing-a-scalable-ai-chatbot-using-azure-openai-llm-provider-java-microservices-and-mysql-6c98839bd051)

### 📗 Kubernetes and Microservices

- [📝 Deploying a Microservices Application with RDS MySql DB into Kubernetes Cluster With High Availability, Auto-Healing, Reliability, Auto Scaling, Monitoring, and Securing](https://cmakkaya.medium.com/deploying-a-microservices-application-with-rds-mysql-db-into-kubernetes-cluster-with-high-818c7c51ab12)

<img width="1606" height="898" alt="image" src="https://github.com/user-attachments/assets/521a6174-55ec-4562-9a50-23626df538f9" />

---

## Connect with me

- 🌐 [LinkedIn](https://www.linkedin.com/in/cumhurakkaya/)
- ✏️ [Medium Articles](https://cmakkaya.medium.com/) - 100+ Articles
- 🌐 [GitHub](https://github.com/cmakkaya/)

## License

MIT License - see the [LICENSE](LICENSE) file for details.
