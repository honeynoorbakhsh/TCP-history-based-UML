import functools
from typing import Any


class SCNException(Exception):
    pass


def scn_check(check: Any):
    """Check scenario return result with provided check argument"""

    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result != check:
                raise SCNException(f"{result} not equal to {check}")

        return wrapper

    return decorate


def monkey_patch(returns: Any):
    """Monkey Patch any scenario step with optional return result"""

    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return returns

        return wrapper

    return decorate
