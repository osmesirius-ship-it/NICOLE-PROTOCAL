"""Export module for Nicole Protocol artifacts."""
from dataclasses import dataclass
from typing import Dict

from .output_shaping import ShapedOutput


@dataclass
class Artifact:
    """Representation of exported artifacts for downstream systems."""

    artifact_type: str
    payload: Dict[str, str]


class ArtifactExportModule:
    """Packages shaped outputs into artifacts."""

    def export_artifact(self, shaped_output: ShapedOutput, artifact_type: str) -> Artifact:
        payload = {
            "format": shaped_output.target_format,
            "tone": shaped_output.tone,
            "content": shaped_output.content,
        }
        return Artifact(artifact_type=artifact_type, payload=payload)
