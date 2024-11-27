"""
AHB file handling as well as data fetching and parsing logic.
"""

import logging
from pathlib import Path

from ahlbatross.core.ahb_comparison import align_ahb_rows
from ahlbatross.formats.csv import export_to_csv, get_csv_files, load_csv_files
from ahlbatross.formats.xlsx import export_to_xlsx
from ahlbatross.utils.formatversion_parsing import parse_formatversions

logger = logging.getLogger(__name__)


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
    logger.debug("Found formatversions: %s", formatversion_list)  # Debug all found versions

    consecutive_formatversions = []
    for i in range(len(formatversion_list) - 1):
        subsequent_formatversion = formatversion_list[i]
        previous_formatversion = formatversion_list[i + 1]

        is_subsequent_empty = _is_formatversion_dir_empty(root_dir, subsequent_formatversion)
        is_previous_empty = _is_formatversion_dir_empty(root_dir, previous_formatversion)
        logger.debug(
            "⌛ Checking pair %s -> %s (empty: %s, %s)",
            subsequent_formatversion,
            previous_formatversion,
            is_subsequent_empty,
            is_previous_empty,
        )

        if is_subsequent_empty or is_previous_empty:
            logger.warning(
                "❗️Skipping empty consecutive formatversions: %s -> %s",
                subsequent_formatversion,
                previous_formatversion,
            )
            continue

        consecutive_formatversions.append((subsequent_formatversion, previous_formatversion))

    logger.debug("Consecutive formatversions: %s", consecutive_formatversions)
    return consecutive_formatversions


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


def process_ahb_files(input_dir: Path, output_dir: Path) -> None:
    """
    Process all matching ahb/<pruefid>.csv files between two <formatversion> directories including respective
    subdirectories of all valid consecutive <formatversion> pairs.
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
            matching_files = get_matching_csv_files(input_dir, previous_formatversion, subsequent_formatversion)

            if not matching_files:
                logger.warning("No matching files found to compare")
                continue

            for previous_pruefid, subsequent_pruefid, nachrichtentyp, pruefid in matching_files:
                logger.info("Processing %s - %s", nachrichtentyp, pruefid)

                try:
                    previous_rows, subsequent_rows = load_csv_files(
                        previous_pruefid, subsequent_pruefid, previous_formatversion, subsequent_formatversion
                    )

                    comparisons = align_ahb_rows(previous_rows, subsequent_rows)

                    output_dir_path = (
                        output_dir / f"{subsequent_formatversion}_{previous_formatversion}" / nachrichtentyp
                    )
                    output_dir_path.mkdir(parents=True, exist_ok=True)

                    csv_path = output_dir_path / f"{pruefid}.csv"
                    xlsx_path = output_dir_path / f"{pruefid}.xlsx"

                    export_to_csv(comparisons, csv_path)
                    export_to_xlsx(comparisons, str(xlsx_path))

                    logger.info("✅ Successfully processed %s/%s", nachrichtentyp, pruefid)

                except (OSError, IOError, ValueError) as e:
                    logger.error("❌ Error processing %s/%s: %s", nachrichtentyp, pruefid, str(e))
                    continue

        except (OSError, IOError, ValueError) as e:
            logger.error(
                "❌ Error processing formatversions %s -> %s: %s",
                subsequent_formatversion,
                previous_formatversion,
                str(e),
            )
            continue
