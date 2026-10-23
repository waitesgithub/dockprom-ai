FROM golang:1.27-bookworm AS builder

ARG MCP_GRAFANA_VERSION=v2.1.1
RUN CGO_ENABLED=0 go install github.com/grafana/mcp-grafana/v2/cmd/mcp-grafana@${MCP_GRAFANA_VERSION}

FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 1000 --create-home mcp-grafana

COPY --from=builder --chown=1000:1000 /go/bin/mcp-grafana /usr/local/bin/mcp-grafana

USER mcp-grafana
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/mcp-grafana", "--transport", "sse", "--address", "0.0.0.0:8000"]
