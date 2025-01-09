from typing import TypedDict


class ProjectTechnologiesAndFrameworks(TypedDict):
    """TypedDict for the project technologies and frameworks."""

    project_name: str
    technologies_and_frameworks: list[str]


class SummaryOfTechnologiesAndFrameworks(TypedDict):
    """TypedDict for the summary of technologies and frameworks."""

    technology: str
    count: int


class TechReport(TypedDict):
    """TypedDict for the technology report."""

    summary: list[SummaryOfTechnologiesAndFrameworks]
    repositories: list[ProjectTechnologiesAndFrameworks]
