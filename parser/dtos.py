from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ActivityFailure:
    act_diag: Optional[str] = None
    version: Optional[int] = None
    path: List[int] = field(default_factory=list)

    def __hash__(self):
        return hash(self.act_diag) ^ hash(self.path) ^ hash(self.version)


@dataclass
class Diagram:
    name: str
    version: str


@dataclass
class Activity:
    id: str
    name: str


@dataclass
class Flow:
    from_activity: str
    to_activity: str
    path_weight: int = 0
    feature_weight: int = 0


@dataclass
class ActivityDiagram(Diagram):
    activities: List[Activity] = field(default_factory=list)
    flows: List[Flow] = field(default_factory=list)


@dataclass
class Participant:
    id: str
    name: str


@dataclass
class Message:
    from_participant: str
    to_participant: str
    name: str


@dataclass
class SequenceDiagram(Diagram):
    path_weight: int = 0
    feature_weight: int = 0
    failure_weight: int = 0
    participants: List[Participant] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)
