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
