"""
AHB file handling as well as data fetching and parsing logic.
"""

import logging
from pathlib import Path
from typing import TypeAlias

from xlsxwriter.format import Format  # type:ignore[import-untyped]

from ahlbatross.core.ahb_comparison import align_columns
from ahlbatross.formats.csv import get_csv_files, load_csv_dataframes
from ahlbatross.formats.excel import export_to_excel
from ahlbatross.utils.formatversion_parsing import parse_formatversions

logger = logging.getLogger(__name__)

XlsxFormat: TypeAlias = Format


def _is_formatversion_dir(path: Path) -> bool:
    """
    Confirm if path is a <formatversion> directory - for instance "FV2504/".
    """
    return path.is_dir() and path.name.startswith("FV") and len(path.name) == 6


def _is_formatversion_dir_empty(root_dir: Path, formatversion: str) -> bool:
    """
    Check if a <formatversion> directory does not contain any <nachrichtenformat> directories.
    """
    formatversion_dir = root_dir / formatversion
    if not formatversion_dir.exists():
        return True

    return len(_get_nachrichtenformat_dirs(formatversion_dir)) == 0


def _get_formatversion_dirs(root_dir: Path) -> list[str]:
    """
    Fetch all available <formatversion> directories, sorted from latest to oldest.
    """
    if not root_dir.exists():
        raise FileNotFoundError(f"❌ Submodule / base directory does not exist: {root_dir}")

    formatversion_dirs = [d.name for d in root_dir.iterdir() if _is_formatversion_dir(d)]
    formatversion_dirs.sort(key=parse_formatversions, reverse=True)
    return formatversion_dirs


def _get_nachrichtenformat_dirs(formatversion_dir: Path) -> list[Path]:
    """
    Fetch all <nachrichtenformat> directories that contain actual csv files.
    """
    if not formatversion_dir.exists():
        raise FileNotFoundError(f"❌ Formatversion directory not found: {formatversion_dir.absolute()}")

    return [d for d in formatversion_dir.iterdir() if d.is_dir() and (d / "csv").exists() and (d / "csv").is_dir()]


def get_formatversion_pairs(root_dir: Path) -> list[tuple[str, str]]:
    """
    Generate pairs of consecutive <formatversion> directories.
    """
    formatversion_list = _get_formatversion_dirs(root_dir)
    formatversion_pairs = []

    for i in range(len(formatversion_list) - 1):
        subsequent_formatversion = formatversion_list[i]
        previous_formatversion = formatversion_list[i + 1]

        # skip if at least one <formatversion> directory is empty.
        if _is_formatversion_dir_empty(root_dir, subsequent_formatversion) or _is_formatversion_dir_empty(
            root_dir, previous_formatversion
        ):
            logger.warning(
                "❗️Skipping empty consecutive formatversions: %s -> %s",
                subsequent_formatversion,
                previous_formatversion,
            )
            continue

        formatversion_pairs.append((subsequent_formatversion, previous_formatversion))

    return formatversion_pairs


# pylint:disable=too-many-locals
def get_matching_csv_files(
    root_dir: Path, previous_formatversion: str, subsequent_formatversion: str
) -> list[tuple[Path, Path, str, str]]:
    """
    Find matching <pruefid>.csv files across <formatversion>/<nachrichtenformat> directories.
    """
    previous_formatversion_dir = root_dir / previous_formatversion
    subsequent_formatversion_dir = root_dir / subsequent_formatversion

    if not all(d.exists() for d in [previous_formatversion_dir, subsequent_formatversion_dir]):
        logger.error("❌ At least one formatversion directory does not exist.")
        return []

    matching_files = []

    previous_nachrichtenformat_dirs = _get_nachrichtenformat_dirs(previous_formatversion_dir)
    subsequent_nachrichtenformat_dirs = _get_nachrichtenformat_dirs(subsequent_formatversion_dir)

    previous_nachrichtenformat_names = {d.name: d for d in previous_nachrichtenformat_dirs}
    subsequent_nachrichtenformat_names = {d.name: d for d in subsequent_nachrichtenformat_dirs}

    common_nachrichtentyp = set(previous_nachrichtenformat_names.keys()) & set(
        subsequent_nachrichtenformat_names.keys()
    )

    for nachrichtentyp in sorted(common_nachrichtentyp):
        previous_csv_dir = previous_nachrichtenformat_names[nachrichtentyp] / "csv"
        subsequent_csv_dir = subsequent_nachrichtenformat_names[nachrichtentyp] / "csv"

        previous_files = {f.stem: f for f in get_csv_files(previous_csv_dir)}
        subsequent_files = {f.stem: f for f in get_csv_files(subsequent_csv_dir)}

        common_ahbs = set(previous_files.keys()) & set(subsequent_files.keys())

        for pruefid in sorted(common_ahbs):
            matching_files.append((previous_files[pruefid], subsequent_files[pruefid], nachrichtentyp, pruefid))

    return matching_files


def _process_files(
    root_dir: Path, previous_formatversion: str, subsequent_formatversion: str, output_dir: Path
) -> None:
    """
    Process all matching ahb/<pruefid>.csv files between two <formatversion> directories.
    """
    matching_files = get_matching_csv_files(root_dir, previous_formatversion, subsequent_formatversion)

    if not matching_files:
        logger.warning("No matching files found to compare")
        return

    output_base = output_dir / f"{subsequent_formatversion}_{previous_formatversion}"

    for previous_pruefid, subsequent_pruefid, nachrichtentyp, pruefid in matching_files:
        logger.info("Processing %s - %s", nachrichtentyp, pruefid)

        try:
            df_of_previous_formatversion, df_of_subsequent_formatversion = load_csv_dataframes(
                previous_pruefid, subsequent_pruefid
            )
            merged_df = align_columns(
                df_of_previous_formatversion,
                df_of_subsequent_formatversion,
                previous_formatversion,
                subsequent_formatversion,
            )

            output_dir = output_base / nachrichtentyp
            output_dir.mkdir(parents=True, exist_ok=True)

            csv_path = output_dir / f"{pruefid}.csv"
            xlsx_path = output_dir / f"{pruefid}.xlsx"

            merged_df.to_csv(csv_path, index=False)
            export_to_excel(merged_df, str(xlsx_path))

            logger.info("✅ Successfully processed %s/%s", nachrichtentyp, pruefid)

        except (ValueError, EOFError) as e:
            logger.error("❌ Empty or corrupted data file for %s/%s: %s", nachrichtentyp, pruefid, str(e))
        except OSError as e:
            logger.error("❌ File system error for %s/%s: %s", nachrichtentyp, pruefid, str(e))


def process_ahb_files(input_dir: Path, output_dir: Path) -> None:
    """
    Processes subdirectories of all valid consecutive <formatversion> pairs.
    """
    logger.info("Found AHB root directory at: %s", input_dir.absolute())
    logger.info("Output directory: %s", output_dir.absolute())

    consecutive_formatversions = get_formatversion_pairs(input_dir)

    if not consecutive_formatversions:
        logger.warning("❗️ No valid consecutive formatversion subdirectories found to compare.")
        return

    for subsequent_formatversion, previous_formatversion in consecutive_formatversions:
        logger.info(
            "⌛ Processing consecutive formatversions: %s -> %s", subsequent_formatversion, previous_formatversion
        )
        try:
            _process_files(
                root_dir=input_dir,
                previous_formatversion=previous_formatversion,
                subsequent_formatversion=subsequent_formatversion,
                output_dir=output_dir,
            )
        except (OSError, IOError, ValueError) as e:
            logger.error(
                "❌ Error processing formatversions %s -> %s: %s",
                subsequent_formatversion,
                previous_formatversion,
                str(e),
            )
            continue
