#!/usr/bin/env python3
# 7-to_kv.py
from typing import Tuple, Union

def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Takes a string and an int or float, returns a tuple of the string and the square of the number as a float.

    Parameters:
    k (str): The string component of the tuple.
    v (Union[int, float]): The numeric component to be squared.

    Returns:
    Tuple[str, float]: A tuple where the first element is the string k and the second element is the square of v as a float.
    """
    return (k, float(v ** 2))