# pylint:disable=too-many-lines

import pytest

from ahlbatross.core.ahb_comparison import align_ahb_rows
from ahlbatross.enums.diff_types import DiffType
from ahlbatross.models.ahb import AhbRow
from unittests.conftest import FormatVersions


class TestSingleColumnComparisons:
    """
    Test cases for AHBs containing only `section_name` entries (Segmentname).
    """

    formatversions: FormatVersions

    @pytest.fixture(autouse=True)
    def setup(self, formatversions: FormatVersions) -> None:
        self.formatversions = formatversions

    def test_remove_whitespace_space(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg ment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg ment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg ment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg ment",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        for comparison in result:
            assert comparison.diff.diff_type == DiffType.UNCHANGED
            assert not comparison.diff.changed_entries

    def test_remove_whitespace_newline(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\nment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\nment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\nment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\nment",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        for comparison in result:
            assert comparison.diff.diff_type == DiffType.UNCHANGED
            assert not comparison.diff.changed_entries

    def test_remove_whitespace_tab(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\tment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\tment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\tment",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\tment",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        for comparison in result:
            assert comparison.diff.diff_type == DiffType.UNCHANGED
            assert not comparison.diff.changed_entries

    def test_align_rows(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="3",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="4",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="3",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="5",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 5
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.REMOVED
        assert result[2].diff.diff_type == DiffType.UNCHANGED
        assert result[3].diff.diff_type == DiffType.REMOVED
        assert result[4].diff.diff_type == DiffType.ADDED

    def test_align_rows_empty_ahbs(self) -> None:
        result = align_ahb_rows([], [])
        assert len(result) == 0

    def test_align_rows_one_empty_ahb(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, [])

        assert len(result) == 2
        assert all(comp.diff.diff_type == DiffType.REMOVED for comp in result)
        assert all(comp.subsequent_formatversion.section_name == "" for comp in result)

    def test_align_rows_full_offset(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="3",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="4",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="5",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="6",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 6
        assert result[0].diff.diff_type == DiffType.REMOVED
        assert result[1].diff.diff_type == DiffType.REMOVED
        assert result[2].diff.diff_type == DiffType.REMOVED
        assert result[3].diff.diff_type == DiffType.ADDED
        assert result[4].diff.diff_type == DiffType.ADDED
        assert result[5].diff.diff_type == DiffType.ADDED

    def test_align_rows_duplicate_segments(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="4",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.REMOVED
        assert result[3].diff.diff_type == DiffType.ADDED

    def test_align_rows_repeating_segments(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="3",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="3",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="3",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="4",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 6
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.UNCHANGED
        assert result[3].diff.diff_type == DiffType.REMOVED
        assert result[4].diff.diff_type == DiffType.REMOVED
        assert result[5].diff.diff_type == DiffType.ADDED


class TestMultiColumnComparisons:
    """
    Test cases for AHBs containing multiple columns.
    """

    formatversions: FormatVersions

    @pytest.fixture(autouse=True)
    def setup(self, formatversions: FormatVersions) -> None:
        self.formatversions = formatversions

    def test_remove_whitespace_space(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg ment",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg ment",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                segment_group_key="c",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                segment_group_key="",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg ment",
                segment_group_key="d",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg ment",
                segment_group_key="d",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[2].diff.changed_entries)
        assert result[3].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[3].diff.changed_entries)

    def test_remove_whitespace_newline(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\nment",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\nment",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                segment_group_key="c",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                segment_group_key="",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\nment",
                segment_group_key="d",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\nment",
                segment_group_key="d",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[2].diff.changed_entries)
        assert result[3].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[3].diff.changed_entries)

    def test_remove_whitespace_tab(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\tment",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Seg\tment",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                segment_group_key="c",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Segment",
                segment_group_key="",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Segment",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\tment",
                segment_group_key="d",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Seg\tment",
                segment_group_key="d",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 4
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[2].diff.changed_entries)
        assert result[3].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[3].diff.changed_entries)

    def test_align_rows(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="3",
                segment_group_key="c",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="4",
                segment_group_key="",
                segment_code="W",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="5",
                segment_group_key="e",
                segment_code="V",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="6",
                segment_group_key="f",
                segment_code="U",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="9",
                segment_group_key="g",
                segment_code="T",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="10",
                segment_group_key="h",
                segment_code="S",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                segment_group_key="a",
                segment_code="X",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                segment_group_key="b",
                segment_code="Y",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="3",
                segment_group_key="d",
                segment_code="Z",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="5",
                segment_group_key="d",
                segment_code="V",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="6",
                segment_group_key="d",
                segment_code="U",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="7",
                segment_group_key="e",
                segment_code="R",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="8",
                segment_group_key="f",
                segment_code="Q",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="9",
                segment_group_key="a",
                segment_code="T",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="10",
                segment_group_key="b",
                segment_code="S",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 10
        assert result[0].diff.diff_type == DiffType.UNCHANGED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.MODIFIED
        assert result[3].diff.diff_type == DiffType.REMOVED
        assert result[4].diff.diff_type == DiffType.MODIFIED
        assert result[5].diff.diff_type == DiffType.MODIFIED
        assert result[6].diff.diff_type == DiffType.ADDED
        assert result[7].diff.diff_type == DiffType.ADDED
        assert result[8].diff.diff_type == DiffType.MODIFIED
        assert result[9].diff.diff_type == DiffType.MODIFIED

        assert "segment_group_key" in str(result[2].diff.changed_entries)
        assert "segment_group_key" in str(result[4].diff.changed_entries)
        assert "segment_group_key" in str(result[5].diff.changed_entries)
        assert "segment_group_key" in str(result[8].diff.changed_entries)
        assert "segment_group_key" in str(result[9].diff.changed_entries)

    def test_align_rows_multiple_entries_per_section_name(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                segment_group_key="a",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                segment_group_key="a",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                segment_group_key="a",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                segment_group_key="b",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                segment_group_key="b",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                segment_group_key="b",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                segment_group_key="x",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                segment_group_key="a",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="1",
                segment_group_key="x",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                segment_group_key="x",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                segment_group_key="b",
                value_pool_entry=None,
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                segment_group_key="x",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 6
        assert result[0].diff.diff_type == DiffType.MODIFIED
        assert result[1].diff.diff_type == DiffType.UNCHANGED
        assert result[2].diff.diff_type == DiffType.MODIFIED
        assert result[3].diff.diff_type == DiffType.MODIFIED
        assert result[4].diff.diff_type == DiffType.UNCHANGED
        assert result[5].diff.diff_type == DiffType.MODIFIED

        assert "segment_group_key" in str(result[0].diff.changed_entries)
        assert not result[1].diff.changed_entries
        assert "segment_group_key" in str(result[2].diff.changed_entries)
        assert "segment_group_key" in str(result[3].diff.changed_entries)
        assert not result[4].diff.changed_entries
        assert "segment_group_key" in str(result[5].diff.changed_entries)

    def test_align_rows_different_column_sets(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="1",
                segment_group_key="a",
                data_element="x",
                value_pool_entry="XY",
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="2",
                segment_group_key="b",
                data_element="y",
                value_pool_entry="YZ",
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="2",
                segment_group_key="b",
                data_element="m",
                value_pool_entry="XY",
                name=None,
            ),
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="3",
                segment_group_key="c",
                data_element="n",
                value_pool_entry="",
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 3
        # Check sequence: removed, modified, added
        assert result[0].diff.diff_type == DiffType.REMOVED
        assert result[1].diff.diff_type == DiffType.MODIFIED
        assert result[2].diff.diff_type == DiffType.ADDED

        # Verify specific changes in the modified row
        changed_entries = str(result[1].diff.changed_entries)
        assert "data_element" in changed_entries
        assert "value_pool_entry" in changed_entries
        assert "segment_group_key" not in changed_entries

    def test_single_changed_ahb_property(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="AAA",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="BBB",
                segment_code="XXX",
                value_pool_entry=None,
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 1
        assert result[0].diff.diff_type == DiffType.MODIFIED
        assert "segment_group_key" in str(result[0].diff.changed_entries)

    def test_multiple_changed_ahb_properties(self) -> None:
        previous_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.previous_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="AAA",
                data_element="111",
                value_pool_entry="XXX",
                name=None,
            ),
        ]
        subsequent_ahb_rows = [
            AhbRow(
                formatversion=self.formatversions.subsequent_formatversion,
                section_name="Nachrichten-Kopfsegment",
                segment_group_key="BBB",
                data_element="222",
                value_pool_entry="XXX",
                name=None,
            ),
        ]

        result = align_ahb_rows(previous_ahb_rows, subsequent_ahb_rows)

        assert len(result) == 1
        assert result[0].diff.diff_type == DiffType.MODIFIED
        changed_entries = result[0].diff.changed_entries
        assert "segment_group_key" in str(changed_entries)
        assert "data_element" in str(changed_entries)
        assert "value_pool_entry" not in str(changed_entries)
