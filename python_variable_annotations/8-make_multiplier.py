#!/usr/bin/env python3
# 8-make_multiplier.py
from typing import Callable

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Creates a multiplier function that multiplies its input by a predefined multiplier.

    Parameters:
    multiplier (float): The multiplier value.

    Returns:
    Callable[[float], float]: A function that multiplies a float by the multiplier.
    """
    def multiplier_function(value: float) -> float:
        return value * multiplier
    
    return multiplier_function