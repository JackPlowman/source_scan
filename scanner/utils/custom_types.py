from typing import TypedDict


class TechnologiesAndFrameworksDetail(TypedDict):
    """TypedDict for the technologies and frameworks detail."""

    technology: str
    badge: str


class ProjectTechnologiesAndFrameworks(TypedDict):
    """TypedDict for the project technologies and frameworks."""

    project_name: str
    technologies_and_frameworks: list[TechnologiesAndFrameworksDetail]


class SummaryOfTechnologiesAndFrameworks(TypedDict):
    """TypedDict for the summary of technologies and frameworks."""

    technology_badge: str
    count: int


class TechReport(TypedDict):
    """TypedDict for the technology report."""

    summary: list[SummaryOfTechnologiesAndFrameworks]
    repositories: list[ProjectTechnologiesAndFrameworks]
