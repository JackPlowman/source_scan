from json import dump
from pathlib import Path

from .types import TechReport


def generate_output_file(tech_report: TechReport) -> None:
    """Generate the output json file.

    Args:
        tech_report (TechReport): The technology report.
    """
    with Path.open("../project_technologies_and_frameworks.json", "w") as output_file:
        dump(tech_report, output_file)
