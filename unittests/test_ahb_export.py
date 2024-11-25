import os
import tempfile
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from ahlbatross.core.ahb_comparison import align_columns
from ahlbatross.formats.excel import export_to_excel


def test_dataframe_export_formats() -> None:
    """
    test csv and xlsx exports with example pruefid files.
    """
    test_data_dir = Path(__file__).parent / "test_data"

    previous_formatversion = "FV2410"
    subsequent_formatversion = "FV2504"

    pruefid_old = pd.read_csv(test_data_dir / f"{previous_formatversion}_55001.csv", dtype=str)
    pruefid_new = pd.read_csv(test_data_dir / f"{subsequent_formatversion}_55001.csv", dtype=str)

    df_merged = align_columns(
        pruefid_old,
        pruefid_new,
        previous_formatversion=previous_formatversion,
        subsequent_formatversion=subsequent_formatversion,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = temp_dir
        csv_path = Path(temp_dir) / "merge.csv"
        xlsx_path = Path(temp_dir) / "merge.xlsx"

        df_merged.to_csv(str(csv_path), index=False)
        export_to_excel(df_merged, str(xlsx_path))

        csv_df = pd.read_csv(csv_path, na_filter=False)
        assert_frame_equal(df_merged, csv_df)

        assert os.path.exists(xlsx_path)
        assert os.path.getsize(xlsx_path) > 0

    assert not os.path.exists(temp_dir_path)


def test_empty_dataframe_export() -> None:
    """
    test exporting an empty dataframe.
    """
    previous_formatversion = "FV2410"
    subsequent_formatversion = "FV2504"

    df = pd.DataFrame(
        columns=[f"Segmentname_{previous_formatversion}", "Änderung", f"Segmentname_{subsequent_formatversion}"]
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        xlsx_path = Path(temp_dir) / "test.xlsx"
        export_to_excel(df, str(xlsx_path))

        assert os.path.exists(xlsx_path)
        assert os.path.getsize(xlsx_path) > 0
