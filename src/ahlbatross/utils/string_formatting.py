"""
Utility functions for string operations.
"""

import re


def normalize_entries(value: str | None) -> str:
    """
    Normalizes strings of AHB parameters like `Segmentname` by removing all whitespaces, tabs, newlines, etc.
    """
    if value is None:
        return ""
    return re.sub(r"\s+", "", value)
