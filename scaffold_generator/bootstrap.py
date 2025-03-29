# bootstrap.py

import subprocess
import sys
from pathlib import Path

def setup_virtualenv(project_path: Path):
    """Creates a virtual enviroment inside the project directory"""
    venv_path = project_path / "venv"
    print(f"\nSetting up virtual environment at: {venv_path}")

    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("Virtual environment created.")
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment.")

def install_dependencies(project_path: Path):
    """Install dependencies listed in requirements.txt using pip"""
    req_file = project_path / "requirements.txt"
    venv_bin = project_path / "venv" / "Scripts" / "python.exe"

    if not req_file.exists() or req_file.stat().st_size == 0:
        print("No dependencies to install.")
        return

    print("\nInstalling dependencies from requirements.txt...")

    try:
        subprocess.run([str(venv_bin), "-m", "pip", "install", "-r", str(req_file)], check=True)
        print("✅ Dependencies installed.")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies.")
        return  # Exit early if install failed

    # Define freeze_file before using it
    freeze_file = project_path / "requirements.txt"

    try:
        with freeze_file.open("w") as f:
            subprocess.run([str(venv_bin), "-m", "pip", "freeze"], stdout=f, check=True)
        print("requirements.txt frozen with installed versions.")
    except subprocess.CalledProcessError:
        print("Failed to freeze dependencies.")


def init_git_repo(project_path: Path):
    """Initialize a git repository and makes the first commit"""
    print("\nInitializing Git repository...")

    try:
        subprocess.run(["git", "init"], cwd=str(project_path), check=True)
        subprocess.run(["git", "add", "."], cwd=str(project_path), check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=str(project_path), check=True)
        print("Git repository initialized and first commit made.")
    except subprocess.CalledProcessError:
        print("Git setup failed. Is Git installed?")