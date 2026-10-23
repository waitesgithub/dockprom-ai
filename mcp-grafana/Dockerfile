ARG MCP_GRAFANA_VERSION=v2.1.1

FROM --platform=$BUILDPLATFORM golang:1.27-bookworm AS builder
ARG TARGETOS
ARG TARGETARCH
ARG MCP_GRAFANA_VERSION

RUN apt-get update && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /src
RUN git clone --depth 1 --branch "${MCP_GRAFANA_VERSION}" https://github.com/grafana/mcp-grafana.git .
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -ldflags="-s -w" -o /out/mcp-grafana ./cmd/mcp-grafana

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --system --uid 1000 --create-home mcp-grafana
WORKDIR /app
COPY --from=builder --chown=1000:1000 /out/mcp-grafana /app/mcp-grafana
USER mcp-grafana
EXPOSE 8000
ENTRYPOINT ["/app/mcp-grafana", "--transport", "sse", "--address", "0.0.0.0:8000"]
