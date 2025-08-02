from typing import Any, Callable


def iterate(state: Any, is_done:Callable[[Any], bool], transform: Callable[[Any], Any]):
    if is_done(state):
        return state
    
    return iterate(transform(state), is_done, transform)


def sqrt(x):
    return iterate(
        1.0, 
        lambda g: abs(g * g - x) / x < 0.00001,
        lambda g: (g + x / g) / 2.0
    )