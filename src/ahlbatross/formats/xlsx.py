"""
Contains excel export logic.
"""

from pathlib import Path
from typing import Dict, List, Optional

from xlsxwriter import Workbook  # type: ignore
from xlsxwriter.format import Format  # type: ignore
from xlsxwriter.worksheet import Worksheet  # type: ignore

from ahlbatross.enums.diff_types import DiffType
from ahlbatross.logger import logger
from ahlbatross.models.ahb import AhbRow, AhbRowComparison, AhbRowDiff
from ahlbatross.utils.xlsx_formatting import (
    ADDED_LABEL_FORMAT,
    ADDED_LABEL_HIGHLIGHTING,
    AHB_COLUMN_NAMES,
    ALTERING_SEGMENTNAME_FORMAT,
    CELL_FORMAT,
    CUSTOM_COLUMN_WIDTHS,
    DEFAULT_COLUMN_WIDTH,
    DIFF_COLUMN_FORMAT,
    HEADER_FORMAT,
    MODIFIED_LABEL_FORMAT,
    MODIFIED_LABEL_HIGHLIGHTING,
    REMOVED_LABEL_FORMAT,
    REMOVED_LABEL_HIGHLIGHTING,
)

FormatDict = Dict[str, Format]


def _create_headers(sample: AhbRowComparison) -> List[str]:
    """
    Create a list of available headers from merged <pruefid>.csv files.
    """
    previous_formatversion_headers = sample.previous_formatversion.formatversion
    subsequent_formatversion_headers = sample.subsequent_formatversion.formatversion

    return [
        f"Segmentname_{previous_formatversion_headers}",
        f"Segmentgruppe_{previous_formatversion_headers}",
        f"Segment_{previous_formatversion_headers}",
        f"Datenelement_{previous_formatversion_headers}",
        f"Segment ID_{previous_formatversion_headers}",
        f"Code_{previous_formatversion_headers}",
        f"Beschreibung_{previous_formatversion_headers}",
        f"Bedingungsausdruck_{previous_formatversion_headers}",
        f"Bedingung_{previous_formatversion_headers}",
        "Änderung",
        f"Segmentname_{subsequent_formatversion_headers}",
        f"Segmentgruppe_{subsequent_formatversion_headers}",
        f"Segment_{subsequent_formatversion_headers}",
        f"Datenelement_{subsequent_formatversion_headers}",
        f"Segment ID_{subsequent_formatversion_headers}",
        f"Code_{subsequent_formatversion_headers}",
        f"Beschreibung_{subsequent_formatversion_headers}",
        f"Bedingungsausdruck_{subsequent_formatversion_headers}",
        f"Bedingung_{subsequent_formatversion_headers}",
    ]


# pylint:disable=too-many-arguments, too-many-positional-arguments, too-many-locals
def _write_row_entries(
    worksheet: Worksheet,
    row_num: int,
    start_col: int,
    row: AhbRow,
    diff: AhbRowDiff,
    is_new_segment: bool,
    diff_formats: FormatDict,
    highlight_segmentname: FormatDict,
    base_format: Format,
    _is_previous_formatversion: bool = True,
) -> None:
    """
    Writes entries to cells row by row.
    """

    values = [
        row.section_name or "",
        row.segment_group_key or "",
        row.segment_code or "",
        row.data_element or "",
        row.segment_id or "",
        row.value_pool_entry or "",
        row.name or "",
        row.ahb_expression or "",
        row.conditions or "",
    ]

    for col_offset, (column_name, value) in enumerate(zip(AHB_COLUMN_NAMES, values)):
        col = start_col + col_offset
        is_segmentname = col_offset == 0
        format_to_use = _determine_segmentname_format(
            diff_type=diff.diff_type,
            is_segmentname=is_segmentname,
            is_new_segment=is_new_segment,
            diff_formats=diff_formats,
            highlight_segmentname=highlight_segmentname,
            base_format=base_format,
            is_previous_formatversion=_is_previous_formatversion,
            column_name=f"{column_name}_{row.formatversion}",
            changed_entries=diff.changed_entries,
        )
        worksheet.write(row_num, col, str(value), format_to_use)


# pylint:disable=too-many-arguments, too-many-positional-arguments, too-many-return-statements
def _determine_segmentname_format(
    diff_type: str,
    is_segmentname: bool,
    is_new_segment: bool,
    diff_formats: FormatDict,
    highlight_segmentname: FormatDict,
    base_format: Format,
    is_previous_formatversion: bool = True,
    column_name: str = "",
    changed_entries: list[str] | None = None,
) -> Format:
    """
    Determines the appropriate format for `Segmentname` cells depending on whether they are affected by DIFFs
    or the `Segmentname` has changed.
    """
    if diff_type == DiffType.ADDED.value and not is_previous_formatversion:
        if is_segmentname and is_new_segment:
            return highlight_segmentname[diff_type]
        return diff_formats[diff_type]

    if diff_type == DiffType.REMOVED.value and is_previous_formatversion:
        if is_segmentname and is_new_segment:
            return highlight_segmentname[diff_type]
        return diff_formats[diff_type]

    if diff_type == DiffType.MODIFIED.value:
        changed_entries = changed_entries or []
        if column_name in changed_entries:
            if is_segmentname and is_new_segment:
                return highlight_segmentname[diff_type]
            return diff_formats[diff_type]
        return base_format

    if is_new_segment:
        return highlight_segmentname["segmentname_changed"] if is_segmentname else diff_formats["segmentname_changed"]
    return base_format


def _create_diff_label_highlighting_formats(workbook: Workbook) -> FormatDict:
    """
    Create formats for available DIFF states.
    """
    return {
        DiffType.ADDED.value: workbook.add_format(ADDED_LABEL_HIGHLIGHTING),
        DiffType.REMOVED.value: workbook.add_format(REMOVED_LABEL_HIGHLIGHTING),
        DiffType.MODIFIED.value: workbook.add_format(MODIFIED_LABEL_HIGHLIGHTING),
        "segmentname_changed": workbook.add_format(ALTERING_SEGMENTNAME_FORMAT),
        "": workbook.add_format(CELL_FORMAT),
    }


def _create_diff_label_text_formats(workbook: Workbook) -> FormatDict:
    """
    Create formats for available DIFF texts.
    """
    return {
        DiffType.ADDED.value: workbook.add_format(ADDED_LABEL_FORMAT),
        DiffType.REMOVED.value: workbook.add_format(REMOVED_LABEL_FORMAT),
        DiffType.MODIFIED.value: workbook.add_format(MODIFIED_LABEL_FORMAT),
        "": workbook.add_format(DIFF_COLUMN_FORMAT),
    }


def _create_segmentname_highlight_formats(workbook: Workbook) -> FormatDict:
    """
    Create formats for `Segmentname` highlighting.
    """
    return {
        DiffType.ADDED.value: workbook.add_format({**ADDED_LABEL_HIGHLIGHTING, "bold": True}),
        DiffType.REMOVED.value: workbook.add_format({**REMOVED_LABEL_HIGHLIGHTING, "bold": True}),
        DiffType.MODIFIED.value: workbook.add_format({**MODIFIED_LABEL_HIGHLIGHTING, "bold": True}),
        "segmentname_changed": workbook.add_format({**ALTERING_SEGMENTNAME_FORMAT, "bold": True}),
        "": workbook.add_format({**CELL_FORMAT, "bold": True}),
    }


def _set_column_widths(worksheet: Worksheet, headers: List[str]) -> None:
    """
    Sets column width for a given header.
    """
    for col_num, header in enumerate(headers):
        width_px = next(
            (width for prefix, width in CUSTOM_COLUMN_WIDTHS.items() if header.startswith(prefix)), DEFAULT_COLUMN_WIDTH
        )
        worksheet.set_column(col_num, col_num, width_px / 7)


# pylint:disable=too-many-locals
def export_to_xlsx(comparisons: List[AhbRowComparison], output_path_xlsx: str) -> None:
    """
    Exports the merged AHBs as xlsx with highlighted differences.
    """
    sheet_name = Path(output_path_xlsx).stem

    with Workbook(output_path_xlsx) as workbook:
        worksheet = workbook.add_worksheet(sheet_name)

        header_format = workbook.add_format(HEADER_FORMAT)
        base_format = workbook.add_format(CELL_FORMAT)
        diff_formats = _create_diff_label_highlighting_formats(workbook)
        highlight_segmentname = _create_segmentname_highlight_formats(workbook)
        diff_text_formats = _create_diff_label_text_formats(workbook)

        headers = _create_headers(comparisons[0])
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)

        last_segmentname: Optional[str] = None
        for row_num, comp in enumerate(comparisons, start=1):
            current_segmentname = comp.previous_formatversion.section_name or comp.subsequent_formatversion.section_name
            is_new_segment = bool(current_segmentname and current_segmentname != last_segmentname)
            last_segmentname = current_segmentname

            # AHB: previous formatversion - columns
            _write_row_entries(
                worksheet=worksheet,
                row_num=row_num,
                start_col=0,
                row=comp.previous_formatversion,
                diff=comp.diff,
                is_new_segment=is_new_segment,
                diff_formats=diff_formats,
                highlight_segmentname=highlight_segmentname,
                base_format=base_format,
                _is_previous_formatversion=True,
            )

            # DIFF column
            diff_value = comp.diff.diff_type.value if comp.diff.diff_type.value else ""
            worksheet.write(row_num, 9, diff_value, diff_text_formats.get(diff_value, diff_text_formats[""]))

            # AHB: subsequent formatversion - columns
            _write_row_entries(
                worksheet=worksheet,
                row_num=row_num,
                start_col=10,
                row=comp.subsequent_formatversion,
                diff=comp.diff,
                is_new_segment=is_new_segment,
                diff_formats=diff_formats,
                highlight_segmentname=highlight_segmentname,
                base_format=base_format,
                _is_previous_formatversion=False,
            )

        _set_column_widths(worksheet, headers)
        if comparisons:
            worksheet.freeze_panes(1, 0)

        logger.info("✅ Successfully exported XLSX file to: %s", output_path_xlsx)
