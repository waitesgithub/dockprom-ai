---
title: Host Prerequisites
description: Prepare Docker, the shared network, Ollama, and pgvector.
---

# Host prerequisites

Install Docker Engine with the Compose plugin and ensure the operator can run
`docker compose`. The GenUI stack also requires:

- an external Docker network named `monitor-net`;
- an Ollama-compatible gateway reachable as `ollama-gateway:11435`;
- PostgreSQL with the `vector` extension and a `rag_storage` database;
- the generation and embedding models configured in the environment.

## Ollama context window

Open-Intelligent-UI uses a large system prompt. Configure an adequate context
window for the host Ollama service:

```ini
Environment="OLLAMA_CONTEXT_LENGTH=32768"
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Confirm the external network before deployment:

```bash
docker network inspect monitor-net
```
