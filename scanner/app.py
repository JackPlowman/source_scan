from structlog import get_logger, stdlib

from .utils.custom_types import (
    ProjectTechnologiesAndFrameworks,
    SummaryOfTechnologiesAndFrameworks,
    TechReport,
)
from .utils.github_interactions import retrieve_repositories, scrape_technologies
from .utils.write_markdown import write_output_file

logger: stdlib.BoundLogger = get_logger()


def generate_tech_report() -> None:
    """Generate a report on the technologies used in the repository."""
    repositories = retrieve_repositories()
    projects = [scrape_technologies(repository) for repository in repositories]
    tech_report = summarise_tech_report(projects)
    write_output_file(tech_report)


def summarise_tech_report(
    technologies_and_frameworks: list[ProjectTechnologiesAndFrameworks],
) -> TechReport:
    """Summarise the technologies used in the repository.

    Args:
        technologies_and_frameworks (list[ProjectTechnologiesAndFrameworks]):
            The list of project technologies and frameworks.
    """
    summary: dict[str, int] = {}
    for project in technologies_and_frameworks:
        for technology in project["technologies_and_frameworks"]:
            if technology["badge"] in summary:
                summary[technology["badge"]] += 1
            else:
                summary[technology["badge"]] = 1

    summary_list: list[SummaryOfTechnologiesAndFrameworks] = [
        {"technology_badge": technology, "count": count}
        for technology, count in summary.items()
    ]
    summary_list.sort(key=lambda x: x["count"], reverse=True)

    return {"summary": summary_list, "repositories": technologies_and_frameworks}
