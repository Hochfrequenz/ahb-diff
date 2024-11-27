"""
Functions for reading and writing csv files.
"""

import csv
from pathlib import Path
from typing import List, Tuple

from ahlbatross.models.ahb import AhbRow, AhbRowComparison


def get_csv_files(csv_dir: Path) -> list[Path]:
    """
    Find and return all <pruefid>.csv files in a given directory.
    """
    if not csv_dir.exists():
        return []
    return sorted(csv_dir.glob("*.csv"))


def read_csv_content(file_path: Path, formatversion: str) -> List[AhbRow]:
    """
    Read and convert AHB csv content to AhbRow models.
    """
    rows = []
    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ahb_row = AhbRow(
                formatversion=formatversion,
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


def export_to_csv(comparisons: list[AhbRowComparison], csv_path: Path) -> None:
    """
    Exports the merged AHBs as csv.
    """
    with open(csv_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        first_comp = comparisons[0]
        previous_fv = first_comp.previous_formatversion.formatversion
        subsequent_fv = first_comp.subsequent_formatversion.formatversion

        headers = [
            f"Segmentname_{previous_fv}",
            f"Segmentgruppe_{previous_fv}",
            f"Segment_{previous_fv}",
            f"Datenelement_{previous_fv}",
            f"Segment ID_{previous_fv}",
            f"Code_{previous_fv}",
            f"Beschreibung_{previous_fv}",
            f"Bedingungsausdruck_{previous_fv}",
            f"Bedingung_{previous_fv}",
            "Änderung",
            f"Segmentname_{subsequent_fv}",
            f"Segmentgruppe_{subsequent_fv}",
            f"Segment_{subsequent_fv}",
            f"Datenelement_{subsequent_fv}",
            f"Segment ID_{subsequent_fv}",
            f"Code_{subsequent_fv}",
            f"Beschreibung_{subsequent_fv}",
            f"Bedingungsausdruck_{subsequent_fv}",
            f"Bedingung_{subsequent_fv}",
        ]
        writer.writerow(headers)

        for comp in comparisons:
            row = [
                comp.previous_formatversion.section_name or "",
                comp.previous_formatversion.segment_group_key or "",
                comp.previous_formatversion.segment_code or "",
                comp.previous_formatversion.data_element or "",
                comp.previous_formatversion.segment_id or "",
                comp.previous_formatversion.value_pool_entry or "",
                comp.previous_formatversion.name or "",
                comp.previous_formatversion.ahb_expression or "",
                comp.previous_formatversion.conditions or "",
                comp.diff.diff_type.value,
                comp.subsequent_formatversion.section_name or "",
                comp.subsequent_formatversion.segment_group_key or "",
                comp.subsequent_formatversion.segment_code or "",
                comp.subsequent_formatversion.data_element or "",
                comp.subsequent_formatversion.segment_id or "",
                comp.subsequent_formatversion.value_pool_entry or "",
                comp.subsequent_formatversion.name or "",
                comp.subsequent_formatversion.ahb_expression or "",
                comp.subsequent_formatversion.conditions or "",
            ]
            writer.writerow(row)
