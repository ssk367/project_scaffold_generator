import platform

from scaffold_generator.generator import generate_project


def test_virtualenv_created(tmp_path):
    project_name = "TestEnvApp"
    template_type = "app"
    requirements = []

    generate_project(project_name, template_type, requirements, base_path=tmp_path)

    venv_path = tmp_path / project_name / "venv"

    # Check that venv folder exists
    assert venv_path.exists(), "Venv folder was not created"

    # Check that python executable exists
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "Python.exe"
    else:
        python_exe = venv_path / "bin" / "python"

    assert python_exe.exists(), "Python exe not found in venv"


def test_git_repo_initialized(tmp_path):
    project_name = "TestGitApp"
    template_type = "app"
    requirements = []

    generate_project(project_name, template_type, requirements, base_path=tmp_path)

    git_path = tmp_path / project_name / ".git"
    head_file = git_path / "HEAD"

    # Check that .git/ folder was created
    assert git_path.exists() and git_path.is_dir(), ".git folder was not created"

    # Check that HEAD file exists (should always exist in a git repo)
    assert (
        head_file.exists()
    ), "HEAD file does not exist - repo might not initialized properly"
