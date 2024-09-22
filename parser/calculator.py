from typing import List

from parser import parser
from parser.dtos import SequenceDiagram, ActivityDiagram

act_failures = set()


def calculate_path_weight(seq_diag: SequenceDiagram) -> int:
    """Calculate the raw weight of a sequence diagram."""
    path_weight: int = 0
    act_diags: List[ActivityDiagram] = parser.get_activity_diagrams(seq_diag=seq_diag)
    for act_diag in act_diags:
        path_weight += sum([flow.path_weight for flow in act_diag.flows])
    return path_weight


def calculate_feature_weight(seq_diag: SequenceDiagram) -> int:
    feature_weight: int = 0
    act_diags: List[ActivityDiagram] = parser.get_activity_diagrams(seq_diag=seq_diag)
    for act_diag in act_diags:
        feature_weight += sum([flow.feature_weight for flow in act_diag.flows])
    return feature_weight


def calculate_failure_hash(diag_name: str, diag_version: str, path: List[str]) -> int:
    return hash(diag_name) ^ hash(diag_version) ^ hash(tuple(path))


def calculate_failure_weight(failure_hash: int) -> int:
    global act_failures
    if failure_hash not in act_failures:
        act_failures.add(failure_hash)
        return 10
    return 5
