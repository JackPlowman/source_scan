from diagrams import Diagram
from diagrams.c4 import (
    Container,
    Person,
    Relationship,
    SystemBoundary,
)

with Diagram("docs/diagrams/c4", direction="TB", graph_attr={"splines": "spline"}):
    user = Person(name="User")

    with SystemBoundary("source_scan"):
        scanner = Container(name="Scanner", technology="Python")

        with SystemBoundary("GitHub Pages"):
            rendered_markdown = Container(
                name="Rendered Markdown",
                description="Markdown files rendered to HTML.",
                technology="HTML",
            )

    user >> Relationship("Uses") >> rendered_markdown
    rendered_markdown << Relationship("Generates") << scanner
