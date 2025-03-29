# generator.py

import os
import subprocess
import sys
from pathlib import Path

from scaffold_generator.bootstrap import init_git_repo, install_dependencies, setup_virtualenv
from scaffold_generator.templates import TEMPLATES


def generate_project(project_name: str, template_type: str, requirements: list[str], base_path: Path = None):
    """Generates the project structure based on the selected template"""
    if template_type not in TEMPLATES:
        raise ValueError(f"Unknown template type: {template_type}")

    # Get the structure for the selected template
    structure = TEMPLATES[template_type]

    # Define root path for the new project
    if base_path is None:
        base_path = Path.cwd
    root = base_path / project_name
    print(f"Creating project at: {root}")

    # Create each directory and file
    for folder, files in structure.items():
        folder_path = root / folder
        folder_path.mkdir(parents=True, exist_ok=True)

        for file in files:
            file_path = folder_path / file
            file_path.touch()  # creates an empty file

            if file == "main.py":
                file_path.write_text(
                    f'"""Entry point for the {project_name} project."""\n\n\ndef main():\n     print("Hello from {project_name}!")\n\n\nif __name__ == "__main__":\n   main()\n'
                )
            elif file == "README.md":
                file_path.write_text(
                    f"# {project_name}\n\nGenerated with the Python Project Scaffold Generator.\n"
                )
            elif file == ".gitignore":
                file_path.write_text("__pycache__/\n.env\n*.pyc\nvenv/\n")
            elif file == "requirements.txt":
                if requirements:
                    file_path.write_text("\n".join(requirements) + "\n")
                else:
                    file_path.touch()

            print(f"Created: {file_path}")

            # Run project extras
            setup_virtualenv(root)
            install_dependencies(root)
            init_git_repo(root)
