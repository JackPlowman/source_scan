from pathlib import Path

from detector.application.utils.output_file import generate_output_file


def test_generate_output_file() -> None:
    # Arrange
    file = Path("../project_technologies_and_frameworks.json")
    if file.exists():
        file.unlink()
    project_technologies_and_frameworks = ["TypeScript", "Astro", "Python", "Poetry", "Dependabot", "GitHub Actions"]
    # Act
    generate_output_file(project_technologies_and_frameworks)
    # Assert
    with Path.open("../project_technologies_and_frameworks.json") as file:
        file_contents = file.read()
    assert file_contents == '["TypeScript", "Astro", "Python", "Poetry", "Dependabot", "GitHub Actions"]'
    # Cleanup
    Path("../project_technologies_and_frameworks.json").unlink()
