from logging import getLogger
from pathlib import Path

from bs4 import BeautifulSoup
from markdown2 import markdown

logger = getLogger(__name__)


def test_tech_report() -> None:
    # Arrange
    expected_title = "Tech Report"
    expected_l2_titles = ["Summary", "Repositories"]
    # Act
    with Path("tech_report.md").open() as file:
        tech_report = file.read()
    table_html = markdown(tech_report)
    bs4_html = BeautifulSoup(table_html, "html.parser")
    title = bs4_html.find("h1").text
    l2_titles = [h2.text for h2 in bs4_html.find_all("h2")]
    # Assert
    assert title == expected_title
    assert l2_titles == expected_l2_titles
