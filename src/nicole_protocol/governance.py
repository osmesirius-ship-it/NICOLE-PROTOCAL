"""Governance pipeline orchestrating Nicole Protocol modules."""
from dataclasses import dataclass
from typing import Dict, List, Optional

from .artifact_export import Artifact, ArtifactExportModule
from .context_memory import Chunk, ContextMemoryModule
from .identity import IdentityAnchorModule, IdentityProfile, IdentityState
from .output_shaping import OutputShapingModule, ShapedOutput
from .reasoning_engine import MetaReasoningTrace, ReasoningEngineModule, ReasoningTrace
from .risk_reality import RiskRealityModule, RiskReport
from .symbolic_overlay import SymbolicOverlayModule, SymbolicReport


@dataclass
class NicoleProtocolConfig:
    """Top-level configuration for the governance pipeline."""

    use_symbolic_overlay: bool = False
    symbols_config: Optional[Dict[str, str]] = None
    target_format: str = "spec_document"
    style_prefs: Dict[str, str] = None


class GovernancePipeline:
    """Coordinates module calls following Nicole Protocol governance rules."""

    def __init__(
        self,
        identity: IdentityAnchorModule,
        context: ContextMemoryModule,
        reasoning: ReasoningEngineModule,
        risk: RiskRealityModule,
        overlay: SymbolicOverlayModule,
        shaper: OutputShapingModule,
        exporter: ArtifactExportModule,
    ) -> None:
        self.identity = identity
        self.context = context
        self.reasoning = reasoning
        self.risk = risk
        self.overlay = overlay
        self.shaper = shaper
        self.exporter = exporter

    def ingest(self, query: str, config: NicoleProtocolConfig) -> Artifact:
        identity_state = self.identity.get_identity_state()
        context_chunks = self.context.semantic_search(query, k=10)
        reasoning_trace = self._run_reasoning(query, context_chunks, config)
        risk_report = self.risk.assess_risk(reasoning_trace)

        symbolic_report: Optional[SymbolicReport] = None
        if config.use_symbolic_overlay and config.symbols_config:
            symbolic_report = self.overlay.apply_symbolic_overlay(
                reasoning_trace, config.symbols_config
            )
            reasoning_trace.steps.append(
                f"Symbolic overlay applied with symbols: {symbolic_report.symbols_applied}"
            )

        shaped = self.shaper.shape_output(
            reasoning_trace,
            risk_report,
            target_format=config.target_format,
            style_prefs=config.style_prefs or {},
        )
        artifact = self.exporter.export_artifact(
            shaped_output=shaped, artifact_type=config.target_format
        )
        return artifact

    def _run_reasoning(
        self, query: str, context_chunks: List[Chunk], config: NicoleProtocolConfig
    ) -> ReasoningTrace | MetaReasoningTrace:
        """Pick a DA style; defaults to DA_13."""
        style = (config.style_prefs or {}).get("da_style", "DA_13")
        if style == "DA_X":
            depth = int((config.style_prefs or {}).get("da_depth", 3))
            return self.reasoning.run_dax(query, context_chunks, depth=depth, config={})
        if style == "DA_13_PI2":
            domains = (config.style_prefs or {}).get("domains", ["general"])
            return self.reasoning.run_da13_pi2(query, context_chunks, domains=domains, config={})
        return self.reasoning.run_da13(query, context_chunks, config={})

    def bootstrap_identity(self, profile: IdentityProfile) -> IdentityState:
        return self.identity.load_profile(profile)
