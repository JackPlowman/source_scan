from mdutils.mdutils import MdUtils
from structlog import get_logger, stdlib

from .types import TechReport

logger: stdlib.BoundLogger = get_logger()


def write_output_file(tech_report: TechReport) -> None:
    """Write the tech report to a markdown file.

    Args:
        tech_report (TechReport): The tech report to write to a file.
    """
    md_file = MdUtils(file_name="tech_report", title="Tech Report")
    md_file.new_header(level=1, title="Tech Report")
    md_file.new_line("This report summarises the technologies and frameworks used in the repositories.")
    md_file.new_header(level=2, title="Summary")
    md_file.new_line("The following is a summary of the technologies and frameworks used in the repositories.")
    rows = ["Technology/Framework", "Count"]
    for summary in tech_report["summary"]:
        rows.append(summary["technology"])
        rows.append(str(summary["count"]))
    md_file.new_table(columns=2, rows=len(tech_report["summary"]) + 1, text=rows, text_align="center")
    md_file.create_md_file()
