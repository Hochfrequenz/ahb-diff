"""
Functions for reading and writing csv files.
"""

import csv
from pathlib import Path
from typing import List, Tuple

import pandas as pd
from pandas import DataFrame

from ahlbatross.models.ahb import AhbRow


def load_csv_dataframes(previous_ahb_path: Path, subsequent_ahb_path: Path) -> tuple[DataFrame, DataFrame]:
    """
    Read csv input files.
    """
    previous_ahb: DataFrame = pd.read_csv(previous_ahb_path, dtype=str)
    subsequent_ahb: DataFrame = pd.read_csv(subsequent_ahb_path, dtype=str)
    return previous_ahb, subsequent_ahb


def get_csv_files(csv_dir: Path) -> list[Path]:
    """
    Find and return all <pruefid>.csv files in a given directory.
    """
    if not csv_dir.exists():
        return []
    return sorted(csv_dir.glob("*.csv"))


def read_csv_content(file_path: Path, format_version: str) -> List[AhbRow]:
    """
    Read and convert AHB csv content to AhbRow models.
    """
    rows = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ahb_row = AhbRow(
                format_version=format_version,
                section_name=row["Segmentname"],
                segment_group_key=row.get("Segmentgruppe"),
                segment_code=row.get("Segment"),
                data_element=row.get("Datenelement"),
                segment_id=row.get("Segment ID"),
                value_pool_entry=row.get("Code") or row.get("Qualifier"),
                name=row.get("Beschreibung"),
                ahb_expression=row.get("Bedingungsausdruck"),
                conditions=row.get("Bedingung"),
            )
            rows.append(ahb_row)
    return rows


def load_csv_files(
    previous_ahb_path: Path, subsequent_ahb_path: Path, previous_formatversion: str, subsequent_formatversion: str
) -> Tuple[List[AhbRow], List[AhbRow]]:
    """
    Load AHB csv content.
    """

    previous_ahb_rows = read_csv_content(previous_ahb_path, previous_formatversion)
    subsequent_ahb_rows = read_csv_content(subsequent_ahb_path, subsequent_formatversion)

    return previous_ahb_rows, subsequent_ahb_rows
