<p align="center">
  <img src="docs/dockprom-ai-logo.png" alt="Dockprom-AI logo" width="600" />
</p>

<p align="center">
  <b>Dockprom-AI: Generative UI & AIOps Copilot Stack</b><br>
  <sub>OpenUI • OpenIntelligence UI • Chainlit</sub>
</p>

This companion repository layer extends **Dockprom-AI** with dynamic Generative UI (GenUI), conversational multi-turn triage, and RAG over incident postmortems using `pgvector`.

It runs via `compose-genui.yaml` on top of the shared `monitor-net` Docker network.

- **Open-Intelligent-UI (Port `3001`)** — Thesys OpenUI streaming web application rendering live interactive React widgets on the fly.
- **Chainlit AIOps Copilot (Port `8050`)** — Interactive conversational control plane equipped with step-by-step reasoning, vector similarity search, and embedded Generative UI previews.
- **Host Ollama Integration** — GPU inference routed via the Envoy gateway (`:11435`).
- **pgvector Integration** — High-concurrency embeddings storage (`rag_storage`) co-located inside the primary PostgreSQL 17 instance.

---

## Architecture Flow

<p align="center">
  <img src="website/static/img/architecture-genui.svg" alt="Dockprom-AI Generative UI and AIOps copilot architecture" width="100%" />
</p>

The companion services connect to the core stack as shown below:

<p align="center">
  <img src="website/static/img/architecture-core.svg" alt="Dockprom-AI core observability and AIOps architecture" width="100%" />
</p>
