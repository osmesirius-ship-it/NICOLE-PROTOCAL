"""Identity module for the Nicole Protocol.

The identity anchor keeps persistent cognitive anchors that other modules
can query to bind outputs to the intended persona.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class IdentityProfile:
    """Static profile fields that define the Nicole context."""

    name: str
    birth_data: Optional[str] = None
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class IdentityState:
    """Dynamic identity state available to the protocol."""

    profile: IdentityProfile
    session_data: Dict[str, str] = field(default_factory=dict)


class IdentityAnchorModule:
    """Maintains and shares the Nicole identity context."""

    def __init__(self, profile: Optional[IdentityProfile] = None) -> None:
        self._profile = profile
        self._session_data: Dict[str, str] = {}

    def load_profile(self, profile: IdentityProfile) -> IdentityState:
        """Load or replace the active identity profile."""
        self._profile = profile
        return IdentityState(profile=profile, session_data=self._session_data)

    def get_identity_state(self) -> IdentityState:
        """Return the current identity state, raising if unset."""
        if self._profile is None:
            raise ValueError("Identity profile has not been loaded.")
        return IdentityState(profile=self._profile, session_data=self._session_data)

    def update_session_data(self, key: str, value: str) -> IdentityState:
        """Update transient session data bound to the identity."""
        self._session_data[key] = value
        return self.get_identity_state()
