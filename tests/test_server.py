from fastapi.testclient import TestClient

from server.main import app, context_module, pipeline

client = TestClient(app)


def reset_state() -> None:
    # FastAPI app uses module-level state; clear between tests for determinism.
    context_module._chunks.clear()
    context_module._next_id = 1
    if context_module.vector_store:
        context_module.vector_store._chunks.clear()  # type: ignore[attr-defined]
    pipeline.identity_module.profile = None


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_identity_and_ingest_flow() -> None:
    reset_state()

    identity_payload = {"name": "Nicole", "tags": {"role": "Architect"}}
    response = client.post("/api/v1/identity", json=identity_payload)
    assert response.status_code == 200
    assert response.json()["identity"] == "Nicole"

    context_payload = {"content": "DA_13 uses thirteen steps", "metadata": {"topic": "da"}}
    response = client.post("/api/v1/context", json=context_payload)
    assert response.status_code == 200
    chunk_id = response.json()["chunk_id"]
    assert chunk_id == 1

    search_response = client.post("/api/v1/context/search", json={"content": "DA_13"})
    assert search_response.status_code == 200
    search_results = search_response.json()
    assert len(search_results) == 1
    assert search_results[0]["metadata"]["topic"] == "da"

    ingest_request = {
        "query": "Explain DA_13",
        "config": {
            "use_symbolic_overlay": False,
            "target_format": "spec_document",
            "style_prefs": {"tone": "direct"},
        },
    }
    ingest_response = client.post("/api/v1/ingest", json=ingest_request)
    assert ingest_response.status_code == 200
    payload = ingest_response.json()
    assert payload["artifact_type"] == "spec_document"
    assert payload["risk"] is not None
    assert "DA_13" in payload["artifact"]


def test_symbolic_overlay_is_opt_in() -> None:
    reset_state()
    client.post("/api/v1/identity", json={"name": "Nicole"})
    client.post("/api/v1/context", json={"content": "tarot context"})

    ingest_request = {"query": "test overlay", "config": {"use_symbolic_overlay": False}}
    response = client.post("/api/v1/ingest", json=ingest_request)
    assert response.status_code == 200
    assert "symbolic" not in (response.json().get("artifact", "").lower())

    ingest_request["config"]["use_symbolic_overlay"] = True
    response_with_overlay = client.post("/api/v1/ingest", json=ingest_request)
    assert response_with_overlay.status_code == 200
    assert "symbolic" in response_with_overlay.json().get("artifact", "").lower()
