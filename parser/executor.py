from typing import Callable, Optional, Any

from parser.tokens import START_NODE, END_NODE
from scenarios import steps


def find_scenario(act_name: str) -> Optional[Callable]:
    if act_name in (START_NODE, END_NODE):
        return
    maybe_scn: Optional[Any] = getattr(steps, act_name, None)
    return maybe_scn if callable(maybe_scn) else None


def exec_scenario(scn_func: Callable) -> Optional[Any]:
    return scn_func()
