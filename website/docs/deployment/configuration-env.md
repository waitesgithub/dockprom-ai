---
title: Environment Configuration
description: Environment and build variables used by the GenUI stack.
---

# Environment configuration

Set secrets in the shell or a secret manager before running Compose. Do not
commit database URLs or tokens.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `PGVECTOR_URL` | Yes | None | PostgreSQL URL for the `rag_storage` database. |
| `OLLAMA_MODEL` | No | `llama3.2` | Generation model for Chainlit and Open-Intelligent-UI. |
| `EMBEDDING_MODEL` | No | `nomic-embed-text` | Query-embedding model. |
| `LLM_REASONING_EFFORT` | No | `low` | Open-Intelligent-UI reasoning setting. |
| `OPENUI_PUBLIC_URL` | No | `http://localhost:3001` | Browser-reachable OpenUI URL linked from Chainlit responses. |
| `OPEN_INTELLIGENT_UI_REF` | No | Pinned commit | Upstream source revision used by the image build. |

Example:

```bash
export PGVECTOR_URL='postgresql://<user>:<password>@mattermost-db:5432/rag_storage'
docker compose -f compose-genui.yaml config --quiet
```
