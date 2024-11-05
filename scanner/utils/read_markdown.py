from __future__ import annotations

from re import findall

from structlog import get_logger, stdlib

logger: stdlib.BoundLogger = get_logger()


def find_technologies_and_frameworks(file_contents: str) -> list[str]:
    """Find the technologies and frameworks used in a repository.

    Args:
        file_contents (str): The contents of the file to find technologies and frameworks in.

    Returns:
        list[str]: The list of technologies and frameworks used in the repository.
    """
    file_lines = file_contents.split("\n")
    header_index = find_project_technologies_and_frameworks_header(file_lines)
    if header_index == -1:
        logger.debug("No Project Technologies and Frameworks header found")
        return []

    table_start_index = find_table_data_start_index(header_index, file_lines)

    technologies_and_frameworks = []
    for file_line in file_lines[table_start_index:]:
        logger.debug(file_line)
        if not file_line.startswith("|"):
            # Assume once table starts any lines without a pipe is after the table
            break
        technologies_and_frameworks.extend(find_markdown_badges(file_line))
    return technologies_and_frameworks


def find_project_technologies_and_frameworks_header(
    file_contents_lines: list[str],
) -> int:
    """Find the index of the Project Technologies and Frameworks header.

    Args:
        file_contents_lines (list[str]): The lines of the file to find the header in.

    Returns:
        int: The index of the header.
    """
    tech_and_frameworks_header = [
        index for index, line in enumerate(file_contents_lines) if "# Project Technologies and Frameworks" in line
    ]
    if not tech_and_frameworks_header:
        return -1
    return tech_and_frameworks_header[-1]


def find_table_data_start_index(header_index: int, file_contents_lines: list[str]) -> int:
    """Find the index of the start of the table data.

    Args:
        header_index (int): The index of the header.
        file_contents_lines (list[str]): The lines of the file to find the start of the table data in.

    Returns:
        int: The index of the start of the table data.
    """
    start_index = header_index
    # Iterate through lines until table starts
    while not file_contents_lines[start_index].startswith("|"):
        start_index += 1
    # Assume next line is the separator between the header and the table
    return start_index + 2


def find_markdown_badges(line_contents: str) -> list[str]:
    """Find the markdown badges in a line.

    Args:
        line_contents (str): The contents of the line to find the badges in.

    Returns:
        list[str]: The list of technologies and frameworks used in the repository.
    """
    badge_matches = findall(r"!\[(.*?)\]", line_contents)
    if not badge_matches:
        return []
    logger.debug("Found badges", badges=badge_matches)
    return badge_matches
