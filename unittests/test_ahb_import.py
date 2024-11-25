import tempfile
from pathlib import Path

import pytest

from ahlbatross.formats.csv import load_csv_files
from ahlbatross.models.ahb import AhbRow

AHB_CSV_HEADER = (
    "Segmentname,Segmentgruppe,Segment,Datenelement,Segment ID,"
    "Code,Qualifier,Beschreibung,Bedingungsausdruck,Bedingung\n"
)


def test_load_csv_files() -> None:
    """
    Test loading of <pruefid>.csv files.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        previous_ahb_csv = temp_dir_path / "previous_pruefid.csv"
        with open(previous_ahb_csv, "w", encoding="utf-8") as f:
            f.write(AHB_CSV_HEADER)
            f.write("Nachrichten-Kopfsegment,SG1,TST,0001,00001,E_0001,,Description 1,Muss,[1] Condition")

        subsequent_ahb_csv = temp_dir_path / "subsequent_pruefid.csv"
        with open(subsequent_ahb_csv, "w", encoding="utf-8") as f:
            f.write(AHB_CSV_HEADER)
            f.write("Nachrichten-Kopfsegment,SG2,TST,0001,00001,E_0002,,Description 2,Muss,[2] Condition")

        previous_ahb_rows, subsequent_ahb_rows = load_csv_files(
            previous_ahb_csv, subsequent_ahb_csv, previous_formatversion="FV2410", subsequent_formatversion="FV2504"
        )

        assert len(previous_ahb_rows) == 1
        assert len(subsequent_ahb_rows) == 1

        assert isinstance(previous_ahb_rows[0], AhbRow)
        assert isinstance(subsequent_ahb_rows[0], AhbRow)

        assert previous_ahb_rows[0].section_name == "Nachrichten-Kopfsegment"
        assert previous_ahb_rows[0].segment_group_key == "SG1"
        assert previous_ahb_rows[0].segment_code == "TST"
        assert previous_ahb_rows[0].data_element == "0001"
        assert previous_ahb_rows[0].segment_id == "00001"
        assert previous_ahb_rows[0].value_pool_entry == "E_0001"
        assert previous_ahb_rows[0].name == "Description 1"
        assert previous_ahb_rows[0].ahb_expression == "Muss"
        assert previous_ahb_rows[0].conditions == "[1] Condition"
        assert previous_ahb_rows[0].format_version == "FV2410"

        assert subsequent_ahb_rows[0].section_name == "Nachrichten-Kopfsegment"
        assert subsequent_ahb_rows[0].segment_group_key == "SG2"
        assert subsequent_ahb_rows[0].segment_code == "TST"
        assert subsequent_ahb_rows[0].data_element == "0001"
        assert subsequent_ahb_rows[0].segment_id == "00001"
        assert subsequent_ahb_rows[0].value_pool_entry == "E_0002"
        assert subsequent_ahb_rows[0].name == "Description 2"
        assert subsequent_ahb_rows[0].ahb_expression == "Muss"
        assert subsequent_ahb_rows[0].conditions == "[2] Condition"
        assert subsequent_ahb_rows[0].format_version == "FV2504"


def test_load_empty_csv() -> None:
    """
    Test loading empty <pruefid>.csv files that contain only headers.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        previous_ahb_csv = temp_dir_path / "previous_pruefid.csv"
        with open(previous_ahb_csv, "w", encoding="utf-8") as f:
            f.write(AHB_CSV_HEADER)

        subsequent_ahb_csv = temp_dir_path / "subsequent_pruefid.csv"
        with open(subsequent_ahb_csv, "w", encoding="utf-8") as f:
            f.write(AHB_CSV_HEADER)

        previous_ahb_rows, subsequent_ahb_rows = load_csv_files(
            previous_ahb_csv, subsequent_ahb_csv, previous_formatversion="FV2410", subsequent_formatversion="FV2504"
        )

        assert len(previous_ahb_rows) == 0
        assert len(subsequent_ahb_rows) == 0


def test_load_csv_missing_optional_fields() -> None:
    """
    Test loading <pruefid>.csv with missing optional AHB properties.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        previous_ahb_csv = temp_dir_path / "previous_pruefid.csv"
        with open(previous_ahb_csv, "w", encoding="utf-8") as f:
            f.write("Segmentname\n")
            f.write("Nachrichten-Kopfsegment")

        subsequent_ahb_csv = temp_dir_path / "subsequent_pruefid.csv"
        with open(subsequent_ahb_csv, "w", encoding="utf-8") as f:
            f.write("Segmentname\n")
            f.write("Nachrichten-Kopfsegment")

        previous_ahb_rows, subsequent_ahb_rows = load_csv_files(
            previous_ahb_csv,
            subsequent_ahb_csv,
            previous_formatversion="FV2410",
            subsequent_formatversion="FV2504",
        )

        assert len(previous_ahb_rows) == 1
        assert len(subsequent_ahb_rows) == 1

        assert previous_ahb_rows[0].segment_group_key is None
        assert previous_ahb_rows[0].segment_code is None
        assert previous_ahb_rows[0].data_element is None
        assert previous_ahb_rows[0].segment_id is None
        assert previous_ahb_rows[0].value_pool_entry is None
        assert previous_ahb_rows[0].name is None
        assert previous_ahb_rows[0].ahb_expression is None
        assert previous_ahb_rows[0].conditions is None

        assert subsequent_ahb_rows[0].segment_group_key is None
        assert subsequent_ahb_rows[0].segment_code is None
        assert subsequent_ahb_rows[0].data_element is None
        assert subsequent_ahb_rows[0].segment_id is None
        assert subsequent_ahb_rows[0].value_pool_entry is None
        assert subsequent_ahb_rows[0].name is None
        assert subsequent_ahb_rows[0].ahb_expression is None
        assert subsequent_ahb_rows[0].conditions is None


def test_load_csv_without_segmentname_column() -> None:
    """
    Test attempt loading <pruefid>.csv with missing `section_name` (Segmentname) column.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        previous_ahb_csv = temp_dir_path / "previous_pruefid.csv"
        with open(previous_ahb_csv, "w", encoding="utf-8") as f:
            f.write("Segmentgruppe\n")
            f.write("SG1")

        subsequent_ahb_csv = temp_dir_path / "subsequent_pruefid.csv"
        with open(subsequent_ahb_csv, "w", encoding="utf-8") as f:
            f.write("Segmentgruppe\n")
            f.write("SG2")

        with pytest.raises(KeyError):
            load_csv_files(
                previous_ahb_csv,
                subsequent_ahb_csv,
                previous_formatversion="FV2410",
                subsequent_formatversion="FV2504",
            )
