from pathlib import Path

from pandas import DataFrame
from structlog import get_logger, stdlib

from .types import TechReport

logger: stdlib.BoundLogger = get_logger()


def write_output_file(tech_report: TechReport) -> None:
    """Write the tech report to a markdown file.

    Args:
        tech_report (TechReport): The tech report to write to a file.
    """
    markdown_file = MarkdownFile(file_path="tech_report.md")
    markdown_file.add_header(level=1, title="Tech Report")
    markdown_file.add_header(level=2, title="Summary")
    logger.warning(DataFrame(tech_report["summary"]).to_markdown(index=False))
    markdown_file.add_table(DataFrame(tech_report["summary"]))
    markdown_file.add_header(level=2, title="Repositories")
    for repository in tech_report["repositories"]:
        markdown_file.add_header(level=3, title=repository["project_name"])
        markdown_file.add_table(DataFrame(repository["technologies_and_frameworks"]))


class MarkdownFile:
    """Generate a markdown file."""

    lines_of_content: list[str]

    def __init__(self, file_path: str) -> None:
        """Initialise the markdown file."""
        self.file_path = file_path
        self.lines_of_content = []

    def write(self, content: str) -> None:
        """Write the content to the markdown file."""
        with Path(self.file_path).open("w", encoding="utf-8") as file:
            file.writelines(content)

    def _check_last_line_is_empty(self) -> bool:
        """Check if the last line is empty."""
        return self.lines_of_content[-1] == ""

    def add_header(self, level: int, title: str) -> None:
        """Add a header to the markdown file."""
        if self.lines_of_content and not self._check_last_line_is_empty():
            self.lines_of_content.append("")
        self.lines_of_content += [f"{'#' * level} {title}", ""]

    def add_paragraph(self, paragraph: str) -> None:
        """Add a paragraph to the markdown file."""
        self.lines_of_content.append(f"{paragraph}")

    def add_table(self, dataframe: DataFrame) -> None:
        """Add a table to the markdown file."""
        logger.warning(dataframe.to_markdown(index=False))
        self.lines_of_content.append(dataframe.to_markdown(index=False))
        self.lines_of_content.append("")
