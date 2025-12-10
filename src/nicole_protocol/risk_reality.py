"""Risk and reality checking module."""
from dataclasses import dataclass
from typing import List

from .reasoning_engine import ReasoningTrace


@dataclass
class RiskReport:
    """Simple risk descriptor."""

    level: str
    issues: List[str]
    mitigations: List[str]


class RiskRealityModule:
    """Evaluates hallucination and operational risks."""

    def assess_risk(self, reasoning_trace: ReasoningTrace) -> RiskReport:
        issues: List[str] = []
        mitigations: List[str] = []
        if not reasoning_trace.steps:
            issues.append("No reasoning steps captured")
            mitigations.append("Collect trace before issuing outputs")
        if "no context provided" in reasoning_trace.synthesis:
            issues.append("Missing contextual grounding")
            mitigations.append("Inject authoritative context and re-run")
        level = "low" if not issues else "medium"
        return RiskReport(level=level, issues=issues, mitigations=mitigations)
