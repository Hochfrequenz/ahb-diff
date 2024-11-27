"""
Entrypoint for typer and the command line interface.
"""

import logging
import sys
from pathlib import Path

import typer
from rich.console import Console

from ahlbatross.core.ahb_processing import process_ahb_files

logger = logging.getLogger(__name__)

app = typer.Typer(help="ahlbatross diffs machine-readable AHBs")
err_console = Console(stderr=True)  # https://typer.tiangolo.com/tutorial/printing/#printing-to-standard-error


@app.command()
def main(
    input_dir: Path = typer.Option(..., "--input-dir", "-i", help="Directory containing AHB data."),
    output_dir: Path = typer.Option(
        ..., "--output-dir", "-o", help="Destination path to output directory containing processed files."
    ),
) -> None:
    """
    Main entrypoint for AHlBatross.
    """
    try:
        if not input_dir.exists():
            logger.error("❌ Input directory does not exist: %s", input_dir.absolute())
            sys.exit(1)
        process_ahb_files(input_dir, output_dir)
    except FileNotFoundError as e:
        logger.error("❌ Path error: %s", str(e))
        sys.exit(1)
    except PermissionError as e:
        logger.error("❌ Permission denied: %s", str(e))
        sys.exit(1)
    except (OSError, ValueError, IOError) as e:
        logger.exception("❌ Error processing AHB files: %s", str(e))
        sys.exit(1)
    except (RuntimeError, TypeError, AttributeError) as e:
        logger.exception("❌ Unexpected error: %s", str(e))
        sys.exit(1)


def cli() -> None:
    """
    Entry point of the script defined in pyproject.toml
    """
    app()


# to run the script during local development, execute the following command:
# PYTHONPATH=src python -m ahlbatross.main -i data/machine-readable_anwendungshandbuecher -o data/output
if __name__ == "__main__":
    cli()
