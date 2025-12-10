"""Nicole Protocol package.

Provides modular components for the Nicole Protocol governance layer.
"""

from .identity import IdentityAnchorModule, IdentityProfile, IdentityState
from .context_memory import Chunk, ContextMemoryModule
from .reasoning_engine import ReasoningEngineModule, ReasoningTrace, MetaReasoningTrace
from .risk_reality import RiskRealityModule, RiskReport
from .symbolic_overlay import SymbolicOverlayModule, SymbolicReport
from .output_shaping import OutputShapingModule, ShapedOutput
from .artifact_export import ArtifactExportModule, Artifact
from .governance import GovernancePipeline, NicoleProtocolConfig
from .vector_store import InMemoryVectorStore

__all__ = [
    "IdentityAnchorModule",
    "IdentityProfile",
    "IdentityState",
    "Chunk",
    "ContextMemoryModule",
    "InMemoryVectorStore",
    "ReasoningEngineModule",
    "ReasoningTrace",
    "MetaReasoningTrace",
    "RiskRealityModule",
    "RiskReport",
    "SymbolicOverlayModule",
    "SymbolicReport",
    "OutputShapingModule",
    "ShapedOutput",
    "ArtifactExportModule",
    "Artifact",
    "GovernancePipeline",
    "NicoleProtocolConfig",
]
