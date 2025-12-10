"""Reasoning engine implementing DA styles."""
from dataclasses import dataclass, field
from typing import Dict, List, Sequence

from .context_memory import Chunk


@dataclass
class ReasoningTrace:
    """Trace of reasoning steps for DA_13 and DA_X."""

    style: str
    steps: List[str] = field(default_factory=list)
    synthesis: str = ""


@dataclass
class MetaReasoningTrace:
    """Meta-level trace for DA_13_PI2 (13x13)."""

    style: str
    layers: List[ReasoningTrace] = field(default_factory=list)
    synthesis: str = ""


class ReasoningEngineModule:
    """Runs dialectical alignment routines."""

    def run_da13(self, question: str, context_chunks: Sequence[Chunk], config: Dict) -> ReasoningTrace:
        steps = [
            f"Question: {question}",
            "Collect assumptions",
            "Check contradictions",
            "Run devil's advocate",
            "Stress test with context",
            "Extract supporting signals",
            "Extract opposing signals",
            "Refine hypotheses",
            "Map risks",
            "Map opportunities",
            "Align with Nicole preferences",
            "Draft synthesis",
            "Check for gaps",
            "Finalize answer",
        ]
        synthesis = self._combine(context_chunks, prefix="DA_13 synthesis")
        return ReasoningTrace(style="DA_13", steps=steps, synthesis=synthesis)

    def run_dax(
        self, prompt: str, context_chunks: Sequence[Chunk], depth: int, config: Dict
    ) -> ReasoningTrace:
        depth = max(1, depth)
        steps = [f"Iteration {i+1}: explore and challenge" for i in range(depth)]
        steps.insert(0, f"Prompt: {prompt}")
        synthesis = self._combine(context_chunks, prefix="DA_X synthesis")
        return ReasoningTrace(style="DA_X", steps=steps, synthesis=synthesis)

    def run_da13_pi2(
        self, problem: str, context_chunks: Sequence[Chunk], domains: List[str], config: Dict
    ) -> MetaReasoningTrace:
        layers: List[ReasoningTrace] = []
        for layer_index in range(13):
            sub_steps = [
                f"Layer {layer_index + 1}: domain sweep",
                *[
                    f"Sub-step {layer_index + 1}.{sub_index + 1}: challenge across {domain}"
                    for sub_index, domain in enumerate(domains[:13])
                ],
                "Aggregate layer insights",
            ]
            layer_synthesis = self._combine(context_chunks, prefix=f"Layer {layer_index + 1} synthesis")
            layers.append(
                ReasoningTrace(style="DA_13_PI2_LAYER", steps=sub_steps, synthesis=layer_synthesis)
            )
        synthesis = f"13x13 synthesis for problem: {problem}"
        return MetaReasoningTrace(style="DA_13_PI2", layers=layers, synthesis=synthesis)

    @staticmethod
    def _combine(context_chunks: Sequence[Chunk], prefix: str) -> str:
        if not context_chunks:
            return f"{prefix}: no context provided"
        excerpt = " | ".join(chunk.content[:80] for chunk in context_chunks[:3])
        return f"{prefix}: derived from {len(context_chunks)} chunks -> {excerpt}"
