from unittest.mock import MagicMock, patch

import pytest

from detector.application.app import generate_tech_report, summarise_tech_report

FILE_PATH = "detector.application.app"


@patch(f"{FILE_PATH}.summarise_tech_report")
@patch(f"{FILE_PATH}.generate_output_file")
@patch(f"{FILE_PATH}.scrape_technologies")
@patch(f"{FILE_PATH}.retrieve_repositories")
def test_generate_tech_report(
    mock_retrieve_repositories: MagicMock,
    mock_scrape_technologies: MagicMock,
    mock_generate_output_file: MagicMock,
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
    mock_generate_output_file.assert_called_once_with(mock_summarise_tech_report.return_value)


@pytest.mark.parametrize(
    ("technologies_and_frameworks", "expected_summary"),
    [
        (
            [
                {"technologies_and_frameworks": ["Python", "Django", "Docker"]},
                {"technologies_and_frameworks": ["Python", "Flask"]},
                {"technologies_and_frameworks": ["JavaScript", "React", "Node.js"]},
                {"technologies_and_frameworks": ["Python", "Django"]},
            ],
            {
                "summary": [
                    {"technology": "Python", "count": 3},
                    {"technology": "Django", "count": 2},
                    {"technology": "Docker", "count": 1},
                    {"technology": "Flask", "count": 1},
                    {"technology": "JavaScript", "count": 1},
                    {"technology": "React", "count": 1},
                    {"technology": "Node.js", "count": 1},
                ],
                "repositories": [
                    {"technologies_and_frameworks": ["Python", "Django", "Docker"]},
                    {"technologies_and_frameworks": ["Python", "Flask"]},
                    {"technologies_and_frameworks": ["JavaScript", "React", "Node.js"]},
                    {"technologies_and_frameworks": ["Python", "Django"]},
                ],
            },
        ),
        (
            [
                {"technologies_and_frameworks": ["Java", "Spring"]},
                {"technologies_and_frameworks": ["Java", "Hibernate"]},
                {"technologies_and_frameworks": ["JavaScript", "Angular"]},
            ],
            {
                "summary": [
                    {"technology": "Java", "count": 2},
                    {"technology": "Spring", "count": 1},
                    {"technology": "Hibernate", "count": 1},
                    {"technology": "JavaScript", "count": 1},
                    {"technology": "Angular", "count": 1},
                ],
                "repositories": [
                    {"technologies_and_frameworks": ["Java", "Spring"]},
                    {"technologies_and_frameworks": ["Java", "Hibernate"]},
                    {"technologies_and_frameworks": ["JavaScript", "Angular"]},
                ],
            },
        ),
    ],
)
def test_summarise_tech_report(technologies_and_frameworks: list[dict], expected_summary: dict[str, list]) -> None:
    # Act
    result = summarise_tech_report(technologies_and_frameworks)
    # Assert
    assert result == expected_summary
