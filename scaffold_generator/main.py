# main.py

from scaffold_generator.generator import generate_project
from scaffold_generator.templates import TEMPLATES


def main():
    print("🔧 Python Project Scaffold Generator 🔧\n")

    # Step 1: Ask for project name
    project_name = input("Enter project name: ").strip()
    if not project_name:
        print("Project name cannot be empty.")
        return

    # Step 2: Show template options
    templates = list(TEMPLATES.keys())

    print("\nAvailable Templates:")
    for idx, template in enumerate(templates, start=1):
        print(f"{idx}. {template}")

    # Step 3: Get user choice
    choice = input("\nChoose a template type (1-3): ").strip()
    try:
        template_type = templates[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Please choose a number from the list")
        return

    modules_input = input(
        "\nOptional: List required libraries (comma-seperated, eg., requests,numpy: )"
    ).strip()
    requirements = [pkg.strip() for pkg in modules_input.split(",") if pkg.strip()]

    print(f"\n→ Generating a '{template_type}' project named '{project_name}'...\n")
    generate_project(project_name, template_type, requirements)
    print("\nProject scaffold created successfully.")


if __name__ == "__main__":
    main()
