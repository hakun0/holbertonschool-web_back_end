#!/usr/bin/env python3
# 9-element_length.py
from typing import Iterable, Sequence, List, Tuple

def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    Returns a list of tuples containing elements from the input iterable and their lengths.

    Parameters:
    lst (Iterable[Sequence]): An iterable of sequences.

    Returns:
    List[Tuple[Sequence, int]]: A list of tuples where each tuple consists of a sequence and its length.
    """
    return [(i, len(i)) for i in lst]