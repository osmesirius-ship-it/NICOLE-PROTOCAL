# NICOLE-PROTOCAL

A modular, model-agnostic governance layer that wraps language models with Nicole's
identity, dialectical reasoning styles (DA_13, DA_X, DA_13_PI2), risk checks, and
exportable artifacts. The symbolic overlay is **off by default** and only used when
explicitly requested.

## Why this exists

Nicole Protocol treats LLMs as interchangeable engines operating under a cognitive
OS. It binds responses to Nicole's identity, retrieves semantically relevant context,
runs dialectical alignment loops, evaluates risks, shapes outputs for specific
formats, and exports deliverables for downstream systems.

## Architecture overview

The project is organized into modular components under `src/nicole_protocol`:

- **IdentityAnchorModule (`identity.py`)**: Stores Nicole's profile and session data.
- **ContextMemoryModule (`context_memory.py`)**: Naive semantic store; replaceable with a
  vector DB.
- **ReasoningEngineModule (`reasoning_engine.py`)**: Implements DA_13, DA_X, and
  DA_13_PI2 reasoning flows.
- **RiskRealityModule (`risk_reality.py`)**: Checks outputs for grounding and highlights
  mitigations.
- **SymbolicOverlayModule (`symbolic_overlay.py`)**: Optional overlays (tarot/astrology);
  disabled unless explicitly enabled.
- **OutputShapingModule (`output_shaping.py`)**: Shapes tone/format and applies risk
  tags.
- **ArtifactExportModule (`artifact_export.py`)**: Packages shaped output for downstream
  consumers.
- **GovernancePipeline (`governance.py`)**: Orchestrates ingestion → identity binding →
  semantic retrieval → DA reasoning → risk → optional symbolic overlay → shaping →
  export.

## Reasoning governance rules

- Always run at least one DA style; defaults to **DA_13**.
- Symbolic overlay is opt-in and off by default.
- Every request passes through risk evaluation before export.

## Getting started

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .  # Optional if you package this repo
pip install -r requirements.txt
```

### Run the FastAPI gateway

```bash
uvicorn server.main:app --reload --app-dir src
```

Endpoints (all return JSON):

- `POST /api/v1/identity` — load identity profile
- `POST /api/v1/context` — store a context chunk (will upsert into the vector store if provided)
- `POST /api/v1/context/search` — query semantic context
- `POST /api/v1/ingest` — full pipeline (identity → context → DA reasoning → risk → optional symbolic overlay → shaping → export)
- `GET /health` — healthcheck

### Try the HTML/JS demo

Open `web/index.html` in a browser while the FastAPI server is running on `localhost:8000`.
The page lets you:

- load identity metadata
- store context chunks
- call the ingest endpoint with configurable DA style and optional symbolic overlay

### Run the test suite

Install dependencies from `requirements.txt` and run:

```bash
pytest
```

## Example workflow (minimal, in-memory)

```python
from nicole_protocol import (
    ArtifactExportModule,
    ContextMemoryModule,
    GovernancePipeline,
    IdentityAnchorModule,
    IdentityProfile,
    OutputShapingModule,
    ReasoningEngineModule,
    RiskRealityModule,
    SymbolicOverlayModule,
    NicoleProtocolConfig,
)

# Initialize modules
identity = IdentityAnchorModule()
context = ContextMemoryModule()
reasoning = ReasoningEngineModule()
risk = RiskRealityModule()
overlay = SymbolicOverlayModule()
shaper = OutputShapingModule()
exporter = ArtifactExportModule()
pipeline = GovernancePipeline(identity, context, reasoning, risk, overlay, shaper, exporter)

# Bootstrap identity and context
pipeline.bootstrap_identity(IdentityProfile(name="Nicole", tags={"role": "Recursive Systems Architect"}))
context.store_chunk("DA_13 requires a 13-step dialectical loop with risk mapping.")

# Run a request
config = NicoleProtocolConfig(target_format="spec_document", style_prefs={"tone": "direct"})
artifact = pipeline.ingest("Explain how DA_13 applies to investor memos", config)
print(artifact)
```

## Extending

- Replace `ContextMemoryModule` with a vector database-backed implementation.
- Swap the `InMemoryVectorStore` wired in `server/main.py` with a real adapter (e.g., pgvector, Pinecone) that matches the `VectorStoreProtocol` interface in `context_memory.py`.
- Swap the reasoning engine with calls to external LLMs while preserving the interfaces.
- Wire `ArtifactExportModule` to your builder/renderer for decks, whitepapers, or PRDs.

## License

This project is licensed under the terms of the accompanying [LICENSE](LICENSE) file.
