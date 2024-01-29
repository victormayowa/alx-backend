#!/usr/bin/env python3
"""
Module with a simple helper function for pagination
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Return a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for pagination.

    Parameters:
    - page: The current page number (1-indexed).
    - page_size: The number of items per page.

    Returns:
    A tuple (start_index, end_index).
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
