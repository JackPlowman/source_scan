from __future__ import annotations

from os import getenv
from typing import TYPE_CHECKING

from github import Github, GithubException, PaginatedList, Repository
from structlog import get_logger, stdlib

from .read_markdown import find_technologies_and_frameworks

if TYPE_CHECKING:
    from github.Repository import Repository

    from .custom_types import ProjectTechnologiesAndFrameworks

logger: stdlib.BoundLogger = get_logger()


def retrieve_repositories() -> PaginatedList[Repository]:
    """Retrieve the list of repositories to analyse.

    Returns:
        PaginatedList[Repository]: The list of repositories.
    """
    github = Github()
    repository_owner = getenv("GITHUB_REPOSITORY_OWNER")
    repositories = github.search_repositories(
        query=f"user:{repository_owner} archived:false is:public",
    )
    logger.info(
        "Retrieved repositories to analyse",
        repositories_count=repositories.totalCount,
        repositories=[repository.full_name for repository in repositories],
    )
    return repositories


def scrape_technologies(repository: Repository) -> ProjectTechnologiesAndFrameworks:
    """Scrape the technologies used in a repository.

    Args:
        repository (Repository): The repository to scrape.

    Returns:
        ProjectTechnologiesAndFrameworks: The project technologies and frameworks.
    """
    project_technologies_and_frameworks: ProjectTechnologiesAndFrameworks = {
        "project_name": repository.full_name,
        "technologies_and_frameworks": [],
    }
    try:
        file = repository.get_contents("docs/PROJECT_TECHNOLOGIES.md")
        logger.debug("Found file", file=file.name, repository=repository.full_name)
        project_technologies_and_frameworks["technologies_and_frameworks"] = (
            find_technologies_and_frameworks(file.decoded_content.decode())
        )
    except GithubException:
        logger.debug("No file found", repository=repository.full_name)
    return project_technologies_and_frameworks
