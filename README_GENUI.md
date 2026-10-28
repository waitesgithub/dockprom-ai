<p align="center">
  <img src="docs/dockprom-ai-logo.png" alt="Dockprom-AI logo" width="600" />
</p>

<p align="center">
  <b>Dockprom-AI: Generative UI &amp; AIOps Copilot Stack</b><br>
  <sub>OpenUI • OpenIntelligence UI • Chainlit</sub>
</p>

This companion layer extends **Dockprom-AI** with a Generative UI (GenUI),
conversational incident triage, and retrieval-augmented generation over operational
runbooks stored in `pgvector`.

It runs from [`compose-genui.yaml`](compose-genui.yaml) on the external
`monitor-net` Docker network created by the core stack.

- **Open-Intelligent-UI (`localhost:3001`)** renders interactive React components.
- **Chainlit AIOps Copilot (`localhost:8050`)** retrieves runbooks and streams responses from Ollama.
- **Host Ollama gateway (`ollama-gateway:11435`)** provides generation and embeddings.
- **pgvector (`rag_storage`)** stores operational runbooks and their embeddings.

## Architecture

<p align="center">
  <img src="website/static/img/architecture-genui.svg" alt="Dockprom-AI Generative UI and AIOps copilot architecture" width="100%" />
</p>

```text
+----------------------------------------------------------------------------------------------------+
|                                    GENUI ORCHESTRATION PIPELINE                                    |
|                                                                                                    |
|  User query                                                                                        |
|      |                                                                                             |
|      v                                                                                             |
|  Chainlit Copilot (:8050)                                                                          |
|      |                                                                                             |
|      +-- Embed query with nomic-embed-text --> pgvector runbook search                             |
|      |                                                                                             |
|      +-- Generate with Host Ollama through Envoy (:11435)                                          |
|      |                                                                                             |
|      +-- Stream response -------------> Open-Intelligent-UI (:3001)                                |
+----------------------------------------------------------------------------------------------------+
```

The Compose file also supplies the Grafana and Prometheus MCP endpoint URLs to
the copilot container. MCP tool invocation is not yet implemented in
`genui/chainlit/app.py`; those variables reserve the integration points without
claiming that live telemetry was queried.

## Repository layout

```text
dockprom-ai/
├── compose-genui.yaml
└── genui/
    ├── chainlit/
    │   ├── Dockerfile
    │   ├── requirements.txt
    │   └── app.py
    └── open-intelligent-ui/
        └── Dockerfile
```

## Configuration reference

| Variable | Default | Purpose |
| --- | --- | --- |
| `PGVECTOR_URL` | Required | PostgreSQL connection URL for `rag_storage`; keep credentials outside Git. |
| `OLLAMA_MODEL` | `llama3.2` | Ollama generation model used by both services. |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Ollama model used to embed runbook queries. |
| `LLM_REASONING_EFFORT` | `low` | Reasoning setting passed to Open-Intelligent-UI. |
| `OPENUI_PUBLIC_URL` | `http://localhost:3001` | Browser-reachable OpenUI URL linked from Chainlit responses. |
| `OPEN_INTELLIGENT_UI_REF` | Pinned commit | Upstream Open-Intelligent-UI Git revision used for the container build. |

The Open-Intelligent-UI image uses a pinned upstream revision that includes
local Ollama support. Override `OPEN_INTELLIGENT_UI_REF` only after testing the
replacement tag or commit; newer upstream revisions may require Node 24 or
different OpenUI package APIs.

## Prerequisites

Before starting the companion stack:

1. Start the core Dockprom-AI services.
2. Confirm that the external `monitor-net` network exists.
3. Confirm that `ollama-gateway` and the PostgreSQL/pgvector service are attached to that network.
4. Create the `rag_storage` database and `operational_runbooks` table.
5. Pull the configured Ollama generation and embedding models.

## Deploy

Set the database URL without committing it:

```bash
export PGVECTOR_URL='postgresql://<user>:<password>@mattermost-db:5432/rag_storage'
```

Validate and launch the stack:

```bash
docker compose -f compose-genui.yaml config --quiet
docker compose -f compose-genui.yaml up -d --build
docker compose -f compose-genui.yaml ps
```

For larger OpenUI prompts, configure the host Ollama service with an appropriate
context window, then restart it. For example:

```ini
Environment="OLLAMA_CONTEXT_LENGTH=32768"
```

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

## Populate a runbook

The application expects an `operational_runbooks` table with a vector column
matching the embedding model's output dimensions. Insert content only after its
embedding has been generated; inserting text without an embedding will not make
the row retrievable.

## Endpoints

| Service | URL | Description |
| --- | --- | --- |
| Open-Intelligent-UI | `http://localhost:3001` | Full-screen Generative UI surface. |
| Chainlit AIOps Copilot | `http://localhost:8050` | Chat interface backed by Ollama and pgvector retrieval. |

## Security notes

- Never commit `PGVECTOR_URL` or database credentials.
- Published ports bind to `127.0.0.1`; place them behind the authenticated proxy before allowing remote access.
- Pin base images and `OPEN_INTELLIGENT_UI_REF` to immutable digests or commits before production deployment.
- Require explicit operator confirmation before wiring generated UI actions to disruptive tools.
