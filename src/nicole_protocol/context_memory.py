"""Semantic context memory for the Nicole Protocol."""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, runtime_checkable


@dataclass
class Chunk:
    """Stored content with optional metadata."""

    content: str
    metadata: Dict[str, str] = field(default_factory=dict)
    id: Optional[int] = None


class ContextMemoryModule:
    """In-memory semantic-ish store; replaceable with a vector DB."""

    def __init__(self, vector_store: "VectorStoreProtocol | None" = None) -> None:
        self._chunks: List[Chunk] = []
        self._next_id = 1
        self.vector_store = vector_store

    def store_chunk(self, content: str, metadata: Optional[Dict[str, str]] = None) -> int:
        metadata = metadata or {}
        chunk = Chunk(content=content, metadata=metadata, id=self._next_id)
        self._chunks.append(chunk)
        self._next_id += 1
        if self.vector_store:
            self.vector_store.upsert(content, metadata)
        return chunk.id or 0

    def semantic_search(self, query: str, k: int = 5) -> List[Chunk]:
        """Return chunks ranked by naive overlap or delegate to a vector store."""
        if self.vector_store:
            return self.vector_store.similarity_search(query, k)
        ranked = sorted(
            self._chunks,
            key=lambda c: self._score_chunk(query, c),
            reverse=True,
        )
        return ranked[:k]

    @staticmethod
    def _score_chunk(query: str, chunk: Chunk) -> int:
        query_terms = {term.lower() for term in query.split() if term}
        content_terms = {term.lower() for term in chunk.content.split() if term}
        return len(query_terms & content_terms)


@runtime_checkable
class VectorStoreProtocol(Protocol):
    """Interface for vector database adapters."""

    def upsert(self, content: str, metadata: Dict[str, str]) -> None:
        ...

    def similarity_search(self, query: str, k: int) -> List[Chunk]:
        ...
