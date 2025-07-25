from logging import getLogger

from playwright.sync_api import Page

from .variables import PROJECT_URL

logger = getLogger(__name__)


def test_title(page: Page) -> None:
    """Test the repositories title."""
    # Act
    page.goto(PROJECT_URL)
    # Assert
    assert page.title() == "Tech Report | source_scan"


def test_headers(page: Page) -> None:
    """Test the repositories title."""
    # Act
    page.goto(PROJECT_URL)
    # Assert
    assert page.locator("h1").all_inner_texts() == [
        "source_scan",
        "Tech Report",
    ]
    assert page.locator("text='source_scan'").get_attribute("href") == f"{PROJECT_URL}/"


def test_for_2_tables(page: Page) -> None:
    """Test the repositories title."""
    # Act
    page.goto(PROJECT_URL)
    # Assert
    assert page.locator("table").count() == 2


def test_summary_table(page: Page) -> None:
    """Test the summary table."""
    # Act
    page.goto(PROJECT_URL)
    # Assert
    summary_table = page.locator("table").nth(0)
    assert summary_table.count() > 0
    assert summary_table.locator("th").count() == 2
    assert summary_table.locator("th").all_inner_texts() == [
        "Technology Badge",
        "Count",
    ]
    assert summary_table.locator("tr").count() == 15


def test_repositories_table(page: Page) -> None:
    """Test the repositories table."""
    # Act
    page.goto(PROJECT_URL)
    # Assert
    repositories_table = page.locator("table").nth(1)
    assert repositories_table.count() > 0
    assert repositories_table.locator("th").count() == 2
    assert repositories_table.locator("th").all_inner_texts() == [
        "Project Name",
        "Technologies And Frameworks",
    ]
    assert repositories_table.locator("tr").count() == 35
