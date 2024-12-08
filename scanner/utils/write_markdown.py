from pathlib import Path
from typing import Self

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
    #     markdown_file.add_paragraph("""

    # | Priority apples | Second priority | Third priority |
    # |-------|--------|---------|
    # | ambrosia | gala | red delicious |
    # | pink lady | jazz | macintosh |
    # | honeycrisp | granny smith | fuji |

    # """)
    markdown_file.add_header(level=2, title="Summary")
    logger.warning(tech_report["summary"])

    markdown_file.add_table(tech_report["summary"])
    markdown_file.add_header(level=2, title="Repositories")
    for repository in tech_report["repositories"]:
        markdown_file.add_header(level=3, title=repository["project_name"])
        # markdown_file.add_table(DataFrame(repository["technologies_and_frameworks"]))
    markdown_file.write()


class MarkdownFile:
    """Generate a markdown file."""

    file_path: str
    lines_of_content: list[str]

    def __init__(self: Self, file_path: str) -> None:
        """Initialise the markdown file."""
        self.file_path = file_path
        self.lines_of_content = []

    def write(self: Self) -> None:
        """Write the content to the markdown file."""
        with Path(self.file_path).open("w", encoding="utf-8") as file:
            file.writelines(self.lines_of_content)

    def _check_last_line_is_empty(self: Self) -> bool:
        """Check if the last line is empty."""
        return "\n" in self.lines_of_content[-1]

    def add_header(self: Self, level: int, title: str) -> None:
        """Add a header to the markdown file."""
        if self.lines_of_content and not self._check_last_line_is_empty():
            self.lines_of_content[-1] += "\n"
        self.lines_of_content.append(f"{'#' * level} {title}\n")

    def add_paragraph(self: Self, paragraph: str) -> None:
        """Add a paragraph to the markdown file."""
        self.lines_of_content.append(f"{paragraph}")

    def add_table(self: Self, table_contents: list[dict]) -> None:
        """Add a table to the markdown file."""
        headers = table_contents[0].keys()
        self.lines_of_content.append("| " + " | ".join(headers) + " |\n")
        self.lines_of_content.append("|" + "|".join(["-" * len(header) for header in headers]) + "|\n")
        for row in table_contents:
            row_values = (str(value) for value in row.values())
            self.lines_of_content.append("|" + "|".join(row_values) + "|\n")
        logger.warning(self.lines_of_content)
