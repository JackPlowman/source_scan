from logging import getLogger
from pathlib import Path
from re import search

from bs4 import BeautifulSoup
from markdown2 import markdown

logger = getLogger(__name__)


def test_tech_report() -> None:
    # Arrange
    expected_title = "Tech Report"
    expected_l2_titles = ["Summary", "Repositories"]
    expected_summary_headers = ["Technology Badge", "Count"]
    expected_repositories_headers = ["Project Name", "Technologies And Frameworks"]

    # Act
    with Path("tech_report.md").open() as file:
        tech_report = file.read()
    table_html = markdown(tech_report)
    bs4_html = BeautifulSoup(table_html, "html.parser")
    # Get basic structure
    title = bs4_html.find("h1").text
    l2_titles = [h2.text for h2 in bs4_html.find_all("h2")]
    # Get tables
    tables = bs4_html.find_all("p")
    summary_table = tables[0]
    repositories_table = tables[1]
    # Get headers
    summary_headers = list(
        search(r"\|(.*)\|(.*)\|", summary_table.text.split("\n")[0]).groups()
    )
    repositories_headers = list(
        search(r"\|(.*)\|(.*)\|", repositories_table.text.split("\n")[0]).groups()
    )
    # # Get row counts
    summary_rows = len(summary_table.text.split("\n")[2:])
    repositories_rows = len(repositories_table.text.split("\n")[2:])
    # Assert
    assert title == expected_title
    assert l2_titles == expected_l2_titles
    assert summary_headers == expected_summary_headers
    assert repositories_headers == expected_repositories_headers
    assert summary_rows > 0, "Summary table should have at least one row"
    assert repositories_rows > 0, "Repositories table should have at least one row"
