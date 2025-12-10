"""FastAPI gateway for the Nicole Protocol."""
from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from nicole_protocol import (
    ArtifactExportModule,
    ContextMemoryModule,
    GovernancePipeline,
    IdentityAnchorModule,
    IdentityProfile,
    InMemoryVectorStore,
    NicoleProtocolConfig,
    OutputShapingModule,
    ReasoningEngineModule,
    RiskRealityModule,
    SymbolicOverlayModule,
)

app = FastAPI(title="Nicole Protocol Gateway", version="0.1.0")

# Core module wiring (replace InMemoryVectorStore with a real adapter)
vector_store = InMemoryVectorStore()
identity_module = IdentityAnchorModule()
context_module = ContextMemoryModule(vector_store=vector_store)
reasoning_module = ReasoningEngineModule()
risk_module = RiskRealityModule()
overlay_module = SymbolicOverlayModule()
shaper_module = OutputShapingModule()
export_module = ArtifactExportModule()
pipeline = GovernancePipeline(
    identity_module,
    context_module,
    reasoning_module,
    risk_module,
    overlay_module,
    shaper_module,
    export_module,
)


class IdentityPayload(BaseModel):
    name: str
    birth_data: Optional[Dict[str, str]] = None
    tags: Dict[str, str] = Field(default_factory=dict)


class ChunkPayload(BaseModel):
    content: str
    metadata: Dict[str, str] = Field(default_factory=dict)


class IngestConfig(BaseModel):
    use_symbolic_overlay: bool = False
    symbols_config: Optional[Dict[str, str]] = None
    target_format: str = "spec_document"
    style_prefs: Dict[str, str] = Field(default_factory=dict)


class IngestRequest(BaseModel):
    query: str
    config: IngestConfig = Field(default_factory=IngestConfig)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/identity")
def load_identity(payload: IdentityPayload) -> Dict[str, str]:
    profile = IdentityProfile(
        name=payload.name,
        birth_data=payload.birth_data,
        tags=payload.tags,
    )
    state = pipeline.bootstrap_identity(profile)
    return {"identity": state.name, "tags": state.tags}


@app.post("/api/v1/context")
def add_context(payload: ChunkPayload) -> Dict[str, int]:
    chunk_id = context_module.store_chunk(payload.content, payload.metadata)
    return {"chunk_id": chunk_id}


@app.post("/api/v1/context/search")
def search_context(payload: ChunkPayload) -> List[Dict[str, str]]:
    chunks = context_module.semantic_search(payload.content, k=5)
    return [
        {"content": chunk.content, "metadata": chunk.metadata, "id": chunk.id}
        for chunk in chunks
    ]


@app.post("/api/v1/ingest")
def ingest(request: IngestRequest) -> Dict[str, object]:
    config = NicoleProtocolConfig(
        use_symbolic_overlay=request.config.use_symbolic_overlay,
        symbols_config=request.config.symbols_config,
        target_format=request.config.target_format,
        style_prefs=request.config.style_prefs,
    )
    artifact = pipeline.ingest(request.query, config)
    return {
        "artifact": artifact.payload,
        "artifact_type": artifact.artifact_type,
        "risk": artifact.metadata.get("risk_level"),
        "trace": artifact.metadata.get("trace"),
    }


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Nicole Protocol gateway is running", "version": app.version}
