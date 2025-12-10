"""Vector store adapter stubs for plugging in real databases."""
from __future__ import annotations

from typing import Dict, List

from .context_memory import Chunk, VectorStoreProtocol


class InMemoryVectorStore(VectorStoreProtocol):
    """Drop-in stand-in for a true vector database.

    This keeps a local list of chunks and does naive similarity by term overlap.
    Replace this with a real client (e.g., pgvector, Pinecone, Weaviate) that
    respects the same interface.
    """

    def __init__(self) -> None:
        self._chunks: List[Chunk] = []

    def upsert(self, content: str, metadata: Dict[str, str]) -> None:
        self._chunks.append(Chunk(content=content, metadata=metadata))

    def similarity_search(self, query: str, k: int) -> List[Chunk]:
        terms = {term.lower() for term in query.split() if term}
        ranked = sorted(
            self._chunks,
            key=lambda c: len(terms & {term.lower() for term in c.content.split() if term}),
            reverse=True,
        )
        return ranked[:k]
