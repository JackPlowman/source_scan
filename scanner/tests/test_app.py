from unittest.mock import MagicMock, patch

import pytest

from source_scan.scanner.app import generate_tech_report, summarise_tech_report

FILE_PATH = "source_scan.scanner.app"


@patch(f"{FILE_PATH}.summarise_tech_report")
@patch(f"{FILE_PATH}.write_output_file")
@patch(f"{FILE_PATH}.scrape_technologies")
@patch(f"{FILE_PATH}.retrieve_repositories")
def test_generate_tech_report(
    mock_retrieve_repositories: MagicMock,
    mock_scrape_technologies: MagicMock,
    mock_write_output_file: MagicMock,
    mock_summarise_tech_report: MagicMock,
) -> None:
    # Arrange
    tech_detective = MagicMock(full_name="JackPlowman/tech-detective")
    mock_retrieve_repositories.return_value = [tech_detective]
    # Act
    generate_tech_report()
    # Assert
    mock_retrieve_repositories.assert_called_once_with()
    mock_scrape_technologies.assert_called_once_with(tech_detective)
    mock_write_output_file.assert_called_once_with(
        mock_summarise_tech_report.return_value
    )


@pytest.mark.parametrize(
    ("technologies_and_frameworks", "expected_summary"),
    [
        (
            [
                {
                    "technologies_and_frameworks": [
                        {"technology": "Python", "badge": "Python"},
                        {"technology": "Django", "badge": "Django"},
                        {"technology": "Docker", "badge": "Docker"},
                    ]
                },
                {
                    "technologies_and_frameworks": [
                        {"technology": "Python", "badge": "Python"},
                        {"technology": "Flask", "badge": "Flask"},
                    ]
                },
                {
                    "technologies_and_frameworks": [
                        {"technology": "JavaScript", "badge": "JavaScript"},
                        {"technology": "React", "badge": "React"},
                        {"technology": "Node.js", "badge": "Node.js"},
                    ]
                },
                {
                    "technologies_and_frameworks": [
                        {"technology": "Python", "badge": "Python"},
                        {"technology": "Django", "badge": "Django"},
                    ],
                },
            ],
            {
                "summary": [
                    {"technology_badge": "Python", "count": 3},
                    {"technology_badge": "Django", "count": 2},
                    {"technology_badge": "Docker", "count": 1},
                    {"technology_badge": "Flask", "count": 1},
                    {"technology_badge": "JavaScript", "count": 1},
                    {"technology_badge": "React", "count": 1},
                    {"technology_badge": "Node.js", "count": 1},
                ],
                "repositories": [
                    {
                        "technologies_and_frameworks": [
                            {"technology": "Python", "badge": "Python"},
                            {"technology": "Django", "badge": "Django"},
                            {"technology": "Docker", "badge": "Docker"},
                        ]
                    },
                    {
                        "technologies_and_frameworks": [
                            {"technology": "Python", "badge": "Python"},
                            {"technology": "Flask", "badge": "Flask"},
                        ]
                    },
                    {
                        "technologies_and_frameworks": [
                            {"technology": "JavaScript", "badge": "JavaScript"},
                            {"technology": "React", "badge": "React"},
                            {"technology": "Node.js", "badge": "Node.js"},
                        ]
                    },
                    {
                        "technologies_and_frameworks": [
                            {"technology": "Python", "badge": "Python"},
                            {"technology": "Django", "badge": "Django"},
                        ]
                    },
                ],
            },
        ),
        (
            # Empty list test case
            [],
            {
                "summary": [],
                "repositories": [],
            },
        ),
        (
            # Single repository with single technology
            [
                {
                    "technologies_and_frameworks": [
                        {"technology": "Python", "badge": "Python"},
                    ]
                },
            ],
            {
                "summary": [
                    {"technology_badge": "Python", "count": 1},
                ],
                "repositories": [
                    {
                        "technologies_and_frameworks": [
                            {"technology": "Python", "badge": "Python"},
                        ]
                    },
                ],
            },
        ),
        (
            # Multiple repositories with same technologies in different order
            [
                {
                    "technologies_and_frameworks": [
                        {"technology": "Python", "badge": "Python"},
                        {"technology": "Django", "badge": "Django"},
                    ]
                },
                {
                    "technologies_and_frameworks": [
                        {"technology": "Django", "badge": "Django"},
                        {"technology": "Python", "badge": "Python"},
                    ]
                },
            ],
            {
                "summary": [
                    {"technology_badge": "Python", "count": 2},
                    {"technology_badge": "Django", "count": 2},
                ],
                "repositories": [
                    {
                        "technologies_and_frameworks": [
                            {"technology": "Python", "badge": "Python"},
                            {"technology": "Django", "badge": "Django"},
                        ]
                    },
                    {
                        "technologies_and_frameworks": [
                            {"technology": "Django", "badge": "Django"},
                            {"technology": "Python", "badge": "Python"},
                        ]
                    },
                ],
            },
        ),
    ],
)
def test_summarise_tech_report(
    technologies_and_frameworks: list[dict], expected_summary: dict[str, list]
) -> None:
    # Act
    result = summarise_tech_report(technologies_and_frameworks)
    # Assert
    assert result == expected_summary
