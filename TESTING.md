# Testing

Integration tests for the observability stack (Prometheus, Grafana, Loki, Tempo, AlertManager, Node Exporter, OTEL Collector).

## Requirements

`docker` with Compose v2, `curl`, `jq`, `python3` with `pyyaml`. Free host ports: 3000, 3100, 3200, 4317, 4318, 8889, 9090, 9093, 9100, 13133.

## Running locally

```bash
tests/run-all.sh --no-stack      # static tests only (no containers needed)
docker compose up -d
tests/run-all.sh                 # everything
docker compose down -v
```

Individual scripts can be run directly. Each prints `[PASS]`/`[FAIL]` lines with diagnostics and exits non-zero on failure.

URLs and credentials can be overridden via environment variables (see `tests/lib.sh`), e.g. `LOKI_URL`, `GRAFANA_PASSWORD`, `HEALTH_TIMEOUT`.

## Coverage

| Script | Covers |
|--------|--------|
| `config-validation.sh` | YAML/JSON syntax and key settings of all config files |
| `docker-compose-validation.sh` | `docker compose config`, 7 expected services, networks, bind-mount files exist |
| `health-checks.sh` | Health/ready endpoints of all 7 services, Prometheus targets, Grafana login, AlertManager config, Node Exporter metrics, OTLP receivers |
| `service-connectivity.sh` | Prometheus scraping every target, Prometheus→AlertManager, Grafana→Prometheus/Loki/Tempo datasources |
| `data-flow.sh` | Test metric (OTEL→Prometheus), log (OTEL→Loki, LogQL), trace (OTEL→Tempo) using `tests/fixtures/` |

CI: `.github/workflows/integration-tests.yml` (push/PR), `docker-compose-validate.yml` (compose/config changes), `health-check.yml` (daily).

## Troubleshooting

- **Port already in use**: stop whatever holds the port (`ss -ltnp | grep :3100`) or `docker compose down`.
- **Service not healthy / timeouts**: `docker compose ps -a` and `docker compose logs <service>`; raise `HEALTH_TIMEOUT`.
- **Tempo/Loki `permission denied`**: named volumes are root-owned; the compose file runs them as `user: "0:0"`. Recreate with `docker compose down -v`.
- **Grafana login fails**: set `GRAFANA_USER`/`GRAFANA_PASSWORD` if the default `admin`/`admin` was changed.
- **Metric not in Prometheus**: check `curl localhost:9090/api/v1/targets` and that the `otel-collector` target (port 8889) is up.
- **Log/trace not found**: check `docker logs otel-collector` for exporter errors.
