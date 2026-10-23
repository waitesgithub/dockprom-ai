# Grafana MCP helper

The `mcp-grafana` Compose service uses Grafana's official MCP server in SSE
mode. Start the Grafana service, create a service-account token, then set
`GRAFANA_SERVICE_ACCOUNT_TOKEN` and run
`docker compose --profile mcp up -d mcp-grafana`. The server is bound to
localhost at `http://localhost:8000/sse`; only give the token the permissions
needed by your MCP client.
