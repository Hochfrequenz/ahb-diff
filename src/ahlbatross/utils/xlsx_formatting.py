"""
Contains xlsx formatting constants and type definitions.
"""

from typing import TypedDict


class FormattingOptions(TypedDict, total=False):
    """
    Type definition for styling options.
    """

    bold: bool
    bg_color: str
    border: int
    align: str
    text_wrap: bool
    color: str


CELL_FORMAT: FormattingOptions = {
    "border": 1,
    "text_wrap": True,
}

HEADER_FORMAT: FormattingOptions = {
    **CELL_FORMAT,
    "bold": True,
    "bg_color": "#D9D9D9",
    "align": "center",
}

DIFF_COLUMN_FORMAT: FormattingOptions = {
    **CELL_FORMAT,
    "bg_color": "#D9D9D9",
    "align": "center",
}

ADDED_LABEL_HIGHLIGHTING: FormattingOptions = {
    **CELL_FORMAT,
    "bg_color": "#C6EFCE",
}

REMOVED_LABEL_HIGHLIGHTING: FormattingOptions = {
    **CELL_FORMAT,
    "bg_color": "#FFC7CE",
}

MODIFIED_LABEL_HIGHLIGHTING: FormattingOptions = {
    **CELL_FORMAT,
    "bg_color": "#F5DC98",
}

ALTERING_SEGMENTNAME_FORMAT: FormattingOptions = {
    **CELL_FORMAT,
    "bg_color": "#D9D9D9",
}

TEXT_FORMAT_BASE: FormattingOptions = {
    **DIFF_COLUMN_FORMAT,
    "bold": True,
}

ADDED_LABEL_FORMAT: FormattingOptions = {
    **TEXT_FORMAT_BASE,
    "color": "#7AAB8A",
}

REMOVED_LABEL_FORMAT: FormattingOptions = {
    **TEXT_FORMAT_BASE,
    "color": "#E94C74",
}

MODIFIED_LABEL_FORMAT: FormattingOptions = {
    **TEXT_FORMAT_BASE,
    "color": "#B8860B",
}

DEFAULT_COLUMN_WIDTH = 100
CUSTOM_COLUMN_WIDTHS = {
    "Segmentname_": 175,
    "Beschreibung_": 150,
    "Bedingung_": 250,
}

AHB_COLUMN_NAMES = [
    "section_name",
    "segment_group_key",
    "segment_code",
    "data_element",
    "segment_id",
    "value_pool_entry",
    "name",
    "ahb_expression",
    "conditions",
]

AHB_PROPERTIES = [name for name in AHB_COLUMN_NAMES if name != "section_name"]
