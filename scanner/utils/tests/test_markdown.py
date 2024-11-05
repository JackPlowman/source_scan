from pathlib import Path

import pytest

from detector.application.utils.markdown import (
    find_markdown_badges,
    find_project_technologies_and_frameworks_header,
    find_table_data_start_index,
    find_technologies_and_frameworks,
)


def test_find_technologies_and_frameworks() -> None:
    # Arrange
    with Path.open("../README.md") as file:
        file_contents = file.read()

    # Act
    technologies_and_frameworks = find_technologies_and_frameworks(file_contents)

    # Assert
    assert technologies_and_frameworks == ["TypeScript", "Astro", "Python", "Poetry", "Dependabot", "GitHub Actions"]


@pytest.mark.parametrize(
    ("lines", "expected_index"),
    [
        (["# Project Technologies and Frameworks"], 0),
        (["## Project Technologies and Frameworks"], 0),
        (["### Project Technologies and Frameworks"], 0),
        (["#### Project Technologies and Frameworks"], 0),
        (["##### Project Technologies and Frameworks"], 0),
        (["# Project Technologies and Frameworks", "This is a test line"], 0),
        (["This is a test line", "# Project Technologies and Frameworks"], 1),
        (["This is a test line", "# Project Technologies and Frameworks", "This is another test line"], 1),
    ],
)
def test_find_project_technologies_and_frameworks_header(lines: list[str], expected_index: int) -> None:
    # Act
    response = find_project_technologies_and_frameworks_header(lines)
    # Assert
    assert response == expected_index


def test_find_table_data_start_index() -> None:
    # Arrange
    lines = [
        "## Project Technologies and Frameworks",
        "",
        "This project uses the following technologies and frameworks:",
        "",
        "| Catagory | Technologies and Frameworks                                                                                                                                                                                                                             |",
        "| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |",
        "| Frontend | ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white) ![Astro](https://img.shields.io/badge/astro-%232C2052.svg?style=for-the-badge&logo=astro&logoColor=white)                      |",
        "| Backend  | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Poetry](https://img.shields.io/badge/poetry-%23150458.svg?style=for-the-badge&logo=poetry&logoColor=white)                                     |",
        "| CI/CD    | ![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) |",
        "",
    ]
    # Act
    response = find_table_data_start_index(0, lines)
    # Assert
    assert response == 6


@pytest.mark.parametrize(
    ("line_contents", "expected"),
    [
        (
            "| Frontend | ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white) ![Astro](https://img.shields.io/badge/astro-%232C2052.svg?style=for-the-badge&logo=astro&logoColor=white)                      |",
            ["TypeScript", "Astro"],
        ),
        (
            "| Backend  | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Poetry](https://img.shields.io/badge/poetry-%23150458.svg?style=for-the-badge&logo=poetry&logoColor=white)                                     |",
            ["Python", "Poetry"],
        ),
        (
            "| CI/CD    | ![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) |",
            ["Dependabot", "GitHub Actions"],
        ),
        ("", []),
    ],
)
def test_find_markdown_badges(line_contents: str, expected: list[str]) -> None:
    # Act
    actual = find_markdown_badges(line_contents)

    # Assert
    assert actual == expected
