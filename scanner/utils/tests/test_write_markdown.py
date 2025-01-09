from os import environ
from unittest.mock import MagicMock, call, patch

import pytest

from source_scan.scanner.utils.write_markdown import MarkdownFile, write_output_file

FILE_PATH = "source_scan.scanner.utils.write_markdown"


@patch(f"{FILE_PATH}.MarkdownFile")
def test_write_output_file(mock_markdown_file: MagicMock) -> None:
    # Arrange
    if "GITHUB_STEP_SUMMARY" in environ:
        del environ["GITHUB_STEP_SUMMARY"]
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
    mock_markdown_file.assert_called_once_with()
    mock_markdown_file.return_value.add_header.assert_has_calls(
        [
            call(level=1, title="Tech Report"),
            call(level=2, title="Summary"),
        ]
    )
    mock_markdown_file.return_value.add_table.assert_called_once_with(
        content["summary"]
    )
    mock_markdown_file.return_value.write.assert_called_once_with("tech_report.md")


@patch(f"{FILE_PATH}.MarkdownFile")
def test_write_output_file__github_summary(mock_markdown_file: MagicMock) -> None:
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
    environ["GITHUB_STEP_SUMMARY"] = "test.md"
    # Act
    write_output_file(content)
    # Assert
    mock_markdown_file.assert_called_once_with()
    mock_markdown_file.return_value.add_header.assert_has_calls(
        [
            call(level=1, title="Tech Report"),
            call(level=2, title="Summary"),
        ]
    )
    mock_markdown_file.return_value.add_table.assert_called_once_with(
        content["summary"]
    )
    mock_markdown_file.return_value.write.assert_has_calls(
        [call("tech_report.md"), call("test.md")]
    )
    # Cleanup
    del environ["GITHUB_STEP_SUMMARY"]


class TestMarkdownFile:
    def test_init(self) -> None:
        # Act
        markdown_file = MarkdownFile()
        # Assert
        assert markdown_file.lines_of_content == []

    @patch(f"{FILE_PATH}.Path")
    def test_write(self, mock_path: MagicMock) -> None:
        # Arrange
        markdown_file = MarkdownFile()
        file_name = "test.md"
        # Act
        markdown_file.write(file_path=file_name)
        # Assert
        mock_path.assert_called_once_with(file_name)
        mock_path.return_value.open.assert_called_once_with("w", encoding="utf-8")
        mock_path.return_value.open.return_value.__enter__.return_value.writelines.assert_called_once_with(
            markdown_file.lines_of_content
        )

    @pytest.mark.parametrize(
        ("lines_of_content", "expected_result"),
        [
            (["# Test\n"], False),
            (["# Test\\n\\n"], False),
            (["# Test\n\n"], True),
            (["\n\n"], True),
        ],
    )
    def test_check_last_line_is_empty(
        self, lines_of_content: list[str], expected_result: bool
    ) -> None:
        # Arrange
        markdown_file = MarkdownFile()
        markdown_file.lines_of_content = lines_of_content
        # Act
        response = markdown_file._check_last_line_is_empty()
        # Assert
        assert response == expected_result

    @pytest.mark.parametrize(
        ("level", "title", "lines_of_content", "expected_result"),
        [
            (1, "Test", [], ["# Test\n\n"]),
            (2, "Test", ["# Test\n\n"], ["# Test\n\n", "## Test\n\n"]),
            (1, "Test", ["# Test\n\n"], ["# Test\n\n", "# Test\n\n"]),
        ],
    )
    def test_add_header(
        self,
        level: int,
        title: str,
        lines_of_content: list[str],
        expected_result: list[str],
    ) -> None:
        # Arrange
        markdown_file = MarkdownFile()
        markdown_file.lines_of_content = lines_of_content
        # Act
        markdown_file.add_header(level, title)
        # Assert
        assert markdown_file.lines_of_content == expected_result

    @pytest.mark.parametrize(
        ("paragraph", "lines_of_content", "expected_result"),
        [
            ("Test", [], ["Test \n\n"]),
            ("Test", ["Test \n\n"], ["Test \n\n", "Test \n\n"]),
        ],
    )
    def test_add_paragraph(
        self, paragraph: str, lines_of_content: list[str], expected_result: list[str]
    ) -> None:
        # Arrange
        markdown_file = MarkdownFile()
        markdown_file.lines_of_content = lines_of_content
        # Act
        markdown_file.add_paragraph(paragraph)
        # Assert
        assert markdown_file.lines_of_content == expected_result

    @pytest.mark.parametrize(
        ("table_contents", "expected_result"),
        [
            (
                [
                    {"technology": "Markdown", "count": 1},
                    {"technology": "Python", "count": 1},
                ],
                [
                    "|Technology|Count|\n",
                    "|----------|-----|\n",
                    "|Markdown|1|\n",
                    "|Python|1|\n",
                    "\n",
                ],
            ),
            (
                [
                    {
                        "technology": "Markdown",
                        "count": 1,
                        "image": "test.png",
                        "link": "test.com",
                    },
                    {
                        "technology": "Python",
                        "count": 2,
                        "image": "test2.png",
                        "link": "test2.com",
                    },
                    {
                        "technology": "JavaScript",
                        "count": 3,
                        "image": "test3.png",
                        "link": "test3.com",
                    },
                    {
                        "technology": "TypeScript",
                        "count": 4,
                        "image": "test4.png",
                        "link": "test4.com",
                    },
                ],
                [
                    "|Technology|Count|Image|Link|\n",
                    "|----------|-----|-----|----|\n",
                    "|Markdown|1|test.png|test.com|\n",
                    "|Python|2|test2.png|test2.com|\n",
                    "|JavaScript|3|test3.png|test3.com|\n",
                    "|TypeScript|4|test4.png|test4.com|\n",
                    "\n",
                ],
            ),
        ],
    )
    def test_add_table(
        self, table_contents: list[dict], expected_result: list[str]
    ) -> None:
        # Arrange
        markdown_file = MarkdownFile()
        # Act
        markdown_file.add_table(table_contents)
        # Assert
        assert markdown_file.lines_of_content == expected_result
