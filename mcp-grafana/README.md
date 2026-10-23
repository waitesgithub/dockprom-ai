# Grafana MCP server

The Compose stack builds the Grafana MCP server using its HTTP transport on
`http://localhost:8000`. Set `MCP_GRAFANA_SERVER_TOKEN` to a random bearer token
in the environment before starting the stack. After Grafana is running, set
`GRAFANA_SERVICE_ACCOUNT_TOKEN` to a Grafana service-account token in the
environment. Neither token belongs in tracked files; HTTP requests must include
the bearer token and a localhost Host header.

The Dockerfile builds the Go server from the upstream `v2.1.1` module release.
The implementation remains maintained in
[grafana/mcp-grafana](https://github.com/grafana/mcp-grafana), rather than
vendoring its source into this repository.
