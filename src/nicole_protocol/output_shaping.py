"""Output shaping module for Nicole preferences and target formats."""
from dataclasses import dataclass
from typing import Dict

from .reasoning_engine import ReasoningTrace
from .risk_reality import RiskReport


@dataclass
class ShapedOutput:
    """Structured output ready for export."""

    target_format: str
    content: str
    tone: str


class OutputShapingModule:
    """Shapes reasoning into final deliverables."""

    def shape_output(
        self,
        reasoning_trace: ReasoningTrace,
        risk_report: RiskReport,
        target_format: str,
        style_prefs: Dict[str, str],
    ) -> ShapedOutput:
        tone = style_prefs.get("tone", "direct")
        caution = " | Risks: " + ", ".join(risk_report.issues) if risk_report.issues else ""
        content = f"[{reasoning_trace.style}] {reasoning_trace.synthesis}{caution}"
        return ShapedOutput(target_format=target_format, content=content, tone=tone)
