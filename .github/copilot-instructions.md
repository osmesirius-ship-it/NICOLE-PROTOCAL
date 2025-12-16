<!-- copilot-instructions.md: guidance for AI coding agents working on NICOLE-PROTOCAL -->
# Nicole Protocol — Copilot instructions

Purpose: quick, actionable guidance so AI coding agents can be immediately productive in this repo.

## Quick context (big picture)
- Project is a modular governance layer that wraps LLM reasoning into a pipeline: identity → context → DA reasoning (DA_13/DA_X/DA_13_PI2) → risk → optional symbolic overlay → output shaping → artifact export.
- Key orchestration lives in `src/nicole_protocol/governance.py` (class `GovernancePipeline`). The FastAPI gateway wiring is in `src/server/main.py` and uses `uvicorn server.main:app --reload --app-dir src` to run locally.

## Primary modules & where to look
- Identity: `src/nicole_protocol/identity.py` (IdentityProfile / IdentityAnchorModule)
- Context & vectors: `src/nicole_protocol/context_memory.py` (ContextMemoryModule, `VectorStoreProtocol`) and `src/nicole_protocol/vector_store.py` (InMemoryVectorStore)
- Reasoning: `src/nicole_protocol/reasoning_engine.py` (DA implementations: `run_da13`, `run_dax`, `run_da13_pi2`)
- Risk: `src/nicole_protocol/risk_reality.py` (returns `RiskReport` based on trace content)
- Overlay & shaping: `src/nicole_protocol/symbolic_overlay.py`, `src/nicole_protocol/output_shaping.py`
- Export: `src/nicole_protocol/artifact_export.py` (exports `Artifact` with `payload` keys: `format`, `tone`, `content`)

## Important behavioral details & conventions (be precise)
- Default DA style is `DA_13`. The pipeline selects DA style using `NicoleProtocolConfig.style_prefs` (see `GovernancePipeline._run_reasoning`).
- Symbolic overlay is explicitly opt-in (config flag `use_symbolic_overlay` + `symbols_config`). Do not enable by default.
- The `RiskRealityModule` inspects `reasoning_trace.synthesis` for the literal substring `"no context provided"` to flag missing grounding — keep semantic outputs compatible with this check if you modify synthesis formatting.
- `ContextMemoryModule` delegates to a `VectorStoreProtocol` when present; implement `upsert(content, metadata)` and `similarity_search(query, k)` when adding a real vector DB adapter.
- Modules tend to use `dataclasses` for payloads and return simple typed objects (`ReasoningTrace`, `MetaReasoningTrace`, `ShapedOutput`, `Artifact`, `RiskReport`). Follow these shapes when creating tests or extensions.

## Tests & test patterns
- Run tests with `pytest` after `pip install -r requirements.txt` (Python 3.11+).
- Tests import `server.main` and use `fastapi.testclient.TestClient`. The suite relies on module-level state (e.g., `context_module._chunks` and `pipeline.identity_module`), so tests manually reset state for determinism — follow the pattern in `tests/test_server.py` when adding tests.

## Extension points & change guidance
- To add a real vector DB: implement `VectorStoreProtocol` and wire it into `ContextMemoryModule` (see `src/nicole_protocol/vector_store.py` for the in-memory example). Update `server/main.py` wiring accordingly.
- To replace reasoning engine steps with an LLM: keep the same `ReasoningTrace` / `MetaReasoningTrace` contract (fields: `style`, `steps` or `layers`, `synthesis`) so downstream modules (risk, shaper, exporter) continue to work.
- When changing artifact payload shape, update `ArtifactExportModule` and the FastAPI response in `src/server/main.py` together, and add tests asserting response keys (`artifact`, `artifact_type`, `risk`, `trace`).

## Debugging & PR guidance
- If a failing test references missing identity, ensure `pipeline.bootstrap_identity` is called in tests or API flows — `IdentityAnchorModule.get_identity_state()` raises if unset.
- Preserve the explicit opt-in behavior for symbolic overlays and DA style defaults when refactoring.
- Include unit tests that assert trace content and risk outcomes (see `tests/test_server.py` for examples).

## Small reminders (do / don't)
- ✅ Do: Keep `synthesis` strings compatible with `RiskRealityModule` checks.
- ✅ Do: Use `NicoleProtocolConfig` for ingest configuration; tests should exercise both overlay on/off paths.
- ❌ Don't: Rely on implicit global state in new modules; if you must, add test reset helpers like `reset_state()`.

---
If anything here is unclear or you want more detail about a specific file or flow, tell me which part to expand and I will iterate. 🙌
