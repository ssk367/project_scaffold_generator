import shutil
from pathlib import Path
from scaffold_generator.generator import generate_project

def test_generate_app_template(tmp_path):
    # Setup test environment
    project_name = "TestApp"
    template_type = "app"
    requirements = []

    # Act
    generate_project(project_name, template_type, requirements, base_path=tmp_path)

    # Assert: check that the project root folder and some files exist
    project_path = tmp_path / project_name
    expected_files = [
        project_path / "main.py",
        project_path / "README.md",
        project_path / "requirements.txt",
        project_path / ".gitignore",
        project_path / "app" / "__init__.py",
        project_path / "tests" / "test_basic.py",
    ]

    for file in expected_files:
        assert file.exists(), f"Expected file does not exist: {file}"

    # Clean up
    shutil.rmtree(project_path, ignore_errors=True)
