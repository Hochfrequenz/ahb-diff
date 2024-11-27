from dataclasses import dataclass
from pathlib import Path

import pytest

from ahlbatross.enums.diff_types import DiffType
from ahlbatross.models.ahb import AhbRow, AhbRowComparison, AhbRowDiff


@dataclass(frozen=True)
class FormatVersions:
    previous_formatversion: str = "FV2410"
    subsequent_formatversion: str = "FV2504"


@pytest.fixture
def formatversions() -> FormatVersions:
    return FormatVersions()


@pytest.fixture
def temp_excel_file(tmp_path: Path) -> Path:
    return tmp_path / "pruefid.xlsx"


@pytest.fixture
def basic_ahb_row(formatversions: FormatVersions) -> AhbRow:
    return AhbRow(
        formatversion=formatversions.previous_formatversion,
        section_name="Nachrichten-Kopfsegment",
        segment_group_key="SG1",
        segment_code="AAA",
        data_element="111",
        segment_id="0001",
        value_pool_entry="00001",
        name="Beschreibung",
        ahb_expression="[0]",
        conditions="Bedingung",
    )


@pytest.fixture
def ahb_row_comparison_single_column(formatversions: FormatVersions) -> list[AhbRowComparison]:
    return [
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG1",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
            diff=AhbRowDiff(diff_type=DiffType.UNCHANGED),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG1",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
        ),
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="Beginn der Nachricht",
                segment_group_key="SG1",
                segment_code="YYY",
                value_pool_entry=None,
                name=None,
            ),
            diff=AhbRowDiff(
                diff_type=DiffType.MODIFIED,
                changed_entries=[
                    f"segment_group_key_{formatversions.previous_formatversion}",
                    f"segment_group_key_{formatversions.subsequent_formatversion}",
                ],
            ),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="Beginn der Nachricht",
                segment_group_key="SG2",
                segment_code="YYY",
                value_pool_entry=None,
                name=None,
            ),
        ),
    ]


@pytest.fixture
def ahb_row_comparison_multiple_columns(formatversions: FormatVersions) -> list[AhbRowComparison]:
    return [
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="X",
                segment_code="X",
                data_element="X",
                segment_id="X",
                value_pool_entry="X",
                name="Beschreibung_alt",
                ahb_expression="X",
                conditions="Bedingung_alt",
            ),
            diff=AhbRowDiff(
                diff_type=DiffType.MODIFIED,
                changed_entries=[
                    f"name_{formatversions.previous_formatversion}",
                    f"name_{formatversions.subsequent_formatversion}",
                    f"conditions_{formatversions.previous_formatversion}",
                    f"conditions_{formatversions.subsequent_formatversion}",
                ],
            ),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="X",
                segment_code="X",
                data_element="X",
                segment_id="X",
                value_pool_entry="X",
                name="Beschreibung_neu",
                ahb_expression="X",
                conditions="Bedingung_neu",
            ),
        ),
    ]


@pytest.fixture
def all_diff_types_ahb_row_comparisons(formatversions: FormatVersions) -> list[AhbRowComparison]:
    return [
        # UNCHANGED
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG1",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
            diff=AhbRowDiff(diff_type=DiffType.UNCHANGED),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG1",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
        ),
        # MODIFIED
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG1",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
            diff=AhbRowDiff(
                diff_type=DiffType.MODIFIED,
                changed_entries=[
                    f"segment_group_key_{formatversions.previous_formatversion}",
                    f"segment_group_key_{formatversions.subsequent_formatversion}",
                ],
            ),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG2",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
        ),
        # ADDED
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="",
                value_pool_entry=None,
                name=None,
            ),
            diff=AhbRowDiff(diff_type=DiffType.ADDED),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG2",
                segment_code="YYY",
                value_pool_entry=None,
                name=None,
            ),
        ),
        # REMOVED
        AhbRowComparison(
            previous_formatversion=AhbRow(
                formatversion=formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="SG1",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
            diff=AhbRowDiff(diff_type=DiffType.REMOVED),
            subsequent_formatversion=AhbRow(
                formatversion=formatversions.subsequent_formatversion,
                section_name="",
                value_pool_entry=None,
                name=None,
            ),
        ),
    ]
