from pathlib import Path

import pytest

from scanner.utils.read_markdown import (
    find_markdown_badges,
    find_project_technologies_and_frameworks_header,
    find_table_data_start_index,
    find_technologies_and_frameworks,
)


def test_find_technologies_and_frameworks() -> None:
    # Arrange
    with Path.open("docs/PROJECT_TECHNOLOGIES.md") as file:
        file_contents = file.read()

    # Act
    technologies_and_frameworks = find_technologies_and_frameworks(file_contents)

    # Assert
    assert technologies_and_frameworks == [
        {
            "technology": "Markdown",
            "badge": "![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)",
        },
        {
            "technology": "Python",
            "badge": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
        },
        {
            "technology": "UV",
            "badge": "![UV](https://img.shields.io/badge/uv-%23150458.svg?style=for-the-badge&logo=uv&logoColor=white)",
        },
        {
            "technology": "Dependabot",
            "badge": "![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white)",
        },
        {
            "technology": "GitHub Actions",
            "badge": "![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)",
        },
        {
            "technology": "GitHub Pages",
            "badge": "![GitHub Pages](https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=white)",
        },
    ]


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
        (
            [
                "This is a test line",
                "# Project Technologies and Frameworks",
                "This is another test line",
            ],
            1,
        ),
    ],
)
def test_find_project_technologies_and_frameworks_header(
    lines: list[str], expected_index: int
) -> None:
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
        "| Category | Technologies and Frameworks                                                                                                                                                                                                                             |",  # noqa: E501
        "| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |",  # noqa: E501
        "| Frontend | ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white) ![Astro](https://img.shields.io/badge/astro-%232C2052.svg?style=for-the-badge&logo=astro&logoColor=white)                      |",  # noqa: E501
        "| Backend  | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![UV](https://img.shields.io/badge/uv-%23150458.svg?style=for-the-badge&logo=uv&logoColor=white)                                     |",  # noqa: E501
        "| CI/CD    | ![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white) |",  # noqa: E501
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
            "| Frontend | ![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript"
            "&logoColor=white) ![Astro](https://img.shields.io/badge/astro-%232C2052.svg?style=for-the-badge&logo=astro"
            "&logoColor=white)                      |",
            [
                {
                    "technology": "TypeScript",
                    "badge": "![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)",
                },
                {
                    "technology": "Astro",
                    "badge": "![Astro](https://img.shields.io/badge/astro-%232C2052.svg?style=for-the-badge&logo=astro&logoColor=white)",
                },
            ],
        ),
        (
            "| Backend  | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python"
            "&logoColor=ffdd54) ![UV](https://img.shields.io/badge/uv-%23150458.svg?style=for-the-badge"
            "&logo=uv&logoColor=white)                                     |",
            [
                {
                    "technology": "Python",
                    "badge": "![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)",
                },
                {
                    "technology": "UV",
                    "badge": "![UV](https://img.shields.io/badge/uv-%23150458.svg?style=for-the-badge&logo=uv&logoColor=white)",
                },
            ],
        ),
        (
            "| CI/CD    | ![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot"
            "&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge"
            "&logo=githubactions&logoColor=white) |",
            [
                {
                    "technology": "Dependabot",
                    "badge": "![Dependabot](https://img.shields.io/badge/dependabot-025E8C?style=for-the-badge&logo=dependabot&logoColor=white)",
                },
                {
                    "technology": "GitHub Actions",
                    "badge": "![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)",
                },
            ],
        ),
        ("", []),
    ],
)
def test_find_markdown_badges(line_contents: str, expected: list[str]) -> None:
    # Act
    actual = find_markdown_badges(line_contents)
    # Assert
    assert actual == expected
