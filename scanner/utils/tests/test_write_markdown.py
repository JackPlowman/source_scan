from unittest.mock import MagicMock, mock_open, patch

from source_scan.scanner.utils.write_markdown import write_output_file


@patch("builtins.open", new_callable=mock_open)
def test_write_output_file(mock_open: MagicMock) -> None:
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
                "technologies_and_frameworks": ["Markdown", "Python", "Poetry", "Dependabot", "GitHub Actions"],
            },
        ],
    }
    # Act
    write_output_file(content)
    # Assert
    mock_open.assert_called_with("tech_report.md", "w", encoding="utf-8")
    mock_open().write.assert_called_once()
