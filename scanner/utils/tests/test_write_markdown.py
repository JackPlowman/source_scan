from unittest.mock import MagicMock, call, patch

from source_scan.scanner.utils.write_markdown import write_output_file

FILE_PATH = "source_scan.scanner.utils.write_markdown"


@patch(f"{FILE_PATH}.MarkdownFile")
def test_write_output_file(mock_markdown_file: MagicMock) -> None:
    # Arrange
    content = {
        "summary": [
            {"technology": "Markdown", "count": 1},
            {"technology": "Python", "count": 1},
            {"technology": "Poetry", "count": 1},
            {"technology": "Dependabot", "count": 1},
            {"technology": "GitHub Actions", "count": 1},
        ],
        "repositories": [
            {
                "project_name": "JackPlowman/source_scan",
                "technologies_and_frameworks": [
                    "Markdown",
                    "Python",
                    "Poetry",
                    "Dependabot",
                    "GitHub Actions",
                ],
            },
        ],
    }
    # Act
    write_output_file(content)
    # Assert
    mock_markdown_file.assert_called_once_with(file_path="tech_report.md")
    mock_markdown_file.return_value.add_header.assert_has_calls(
        [
            call(level=1, title="Tech Report"),
            call(level=2, title="Summary"),
            call(level=2, title="Repositories"),
            call(level=3, title="JackPlowman/source_scan"),
        ]
    )
