"""Optional symbolic overlays (tarot, astrology, numerology)."""
from dataclasses import dataclass
from typing import Dict, List

from .reasoning_engine import ReasoningTrace


@dataclass
class SymbolicReport:
    """Lightweight symbolic lens on top of the reasoning trace."""

    symbols_applied: List[str]
    notes: List[str]


class SymbolicOverlayModule:
    """Applies symbolic overlays when explicitly enabled."""

    def apply_symbolic_overlay(
        self, reasoning_trace: ReasoningTrace, symbols_config: Dict[str, str]
    ) -> SymbolicReport:
        symbols = list(symbols_config.keys())
        notes = [
            f"Applied {symbol} with setting={value}" for symbol, value in symbols_config.items()
        ]
        return SymbolicReport(symbols_applied=symbols, notes=notes)
