from os import environ
from pathlib import Path
from typing import Self

from structlog import get_logger, stdlib

from .custom_types import TechReport

logger: stdlib.BoundLogger = get_logger()


def write_output_file(tech_report: TechReport) -> None:
    """Write the tech report to a markdown file.

    Args:
        tech_report (TechReport): The tech report to write to a file.
    """
    markdown_file = MarkdownFile()
    markdown_file.add_header(level=1, title="Tech Report")
    markdown_file.add_header(level=2, title="Summary")
    markdown_file.add_table(tech_report["summary"])
    markdown_file.add_header(level=2, title="Repositories")
    repositories_table_contents = [
        {
            "Project Name": f"[{project['project_name']}](https://github.com/{project['project_name']})",
            "Technologies and Frameworks": " ".join(
                technology["badge"]
                for technology in project["technologies_and_frameworks"]
            ),
        }
        for project in tech_report["repositories"]
    ]
    repositories_table_contents.sort(
        key=lambda x: len(x["Technologies and Frameworks"]), reverse=True
    )
    markdown_file.add_table(repositories_table_contents)
    markdown_file.write("tech_report.md")
    if "GITHUB_STEP_SUMMARY" in environ:
        logger.debug("Running in GitHub Actions, generating action summary")
        markdown_file.write(environ["GITHUB_STEP_SUMMARY"])
    else:
        logger.debug(
            "Not running in GitHub Actions, skipping generating action summary"
        )


class MarkdownFile:
    """Generate a markdown file."""

    lines_of_content: list[str]

    def __init__(self: Self) -> None:
        """Initialise the markdown file."""
        self.lines_of_content = []

    def write(self: Self, file_path: str) -> None:
        """Write the content to the markdown file."""
        with Path(file_path).open("w", encoding="utf-8") as file:
            file.writelines(self.lines_of_content)

    def _check_last_line_is_empty(self: Self) -> bool:
        """Check if the last line is empty."""
        return "\n\n" in self.lines_of_content[-1]  # pragma: no mutate

    def add_header(self: Self, level: int, title: str) -> None:
        """Add a header to the markdown file."""
        if self.lines_of_content and not self._check_last_line_is_empty():
            self.lines_of_content[-1] += "\n\n"  # pragma: no mutate
        self.lines_of_content.append(f"{'#' * level} {title}\n\n")  # pragma: no mutate

    def add_paragraph(self: Self, paragraph: str) -> None:
        """Add a paragraph to the markdown file."""
        self.lines_of_content.append(f"{paragraph} \n\n")  # pragma: no mutate

    def add_table(self: Self, table_contents: list[dict]) -> None:
        """Add a table to the markdown file."""
        headers = [header.replace("_", " ").title() for header in table_contents[0]]
        self.lines_of_content.append(
            "|" + "|".join(headers) + "|\n"  # pragma: no mutate
        )
        self.lines_of_content.append(
            "|"
            + "|".join(["-" * len(header) for header in headers])
            + "|\n"  # pragma: no mutate
        )
        for row in table_contents:
            row_values = (str(value) for value in row.values())
            self.lines_of_content.append(
                "|" + "|".join(row_values) + "|\n"  # pragma: no mutate
            )
        self.lines_of_content.append("\n")  # pragma: no mutate
