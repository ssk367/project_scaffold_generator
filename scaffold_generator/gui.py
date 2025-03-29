# gui.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from pathlib import Path

from  scaffold_generator.generator import generate_project
from scaffold_generator.templates import TEMPLATES

class ScaffoldApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Project Scaffold Generator")
        self.root.geometry("480x300")
        self.root.resizable(False, False)

        self.create_widgets() 

    def create_widgets(self):
        # Project name
        ttk.Label(self.root, text="Project Name:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self.root, width=40)
        self.name_entry.pack(pady=5)

        # Template type dropdown
        ttk.Label(self.root, text="Template Type:").pack(pady=(10, 0))
        self.template_combo = ttk.Combobox(self.root, values=list(TEMPLATES.keys()), state="readonly")
        self.template_combo.set("app") # Default

        # Requirements entry
        ttk.Label(self.root, text="Requirements (comma seperated):").pack(pady=(10, 0))
        self.reqs_entry = ttk.Entry(self.root, width=40)
        self.reqs_entry.pack(pady=15)

        # Optional steps (checkboxes)
        self.venv_var = ttk.BooleanVar(value=True)
        self.install_var = ttk.BooleanVar(value=True)
        self.git_var = ttk.BooleanVar(value=True)

        ttk.Checkbutton(self.root, text="Create virtual enviroment", variable=self.venv_var).pack(pady=(5,0))
        ttk.Checkbutton(self.root, text="Install dependencies", variable=self.install_var).pack(pady=(5,0))
        ttk.Checkbutton(self.root, text="Initialize Git repository", variable=self.git_var).pack(pady=(5,0))

        # Generate button
        self.generate_btn = ttk.Button(self.root, text="Generate Project", command=self.generate)
        self.generate_btn.pack(pady=5)

        # Status label
        self.status_label = ttk.Label(self.root, text="", foreground="green")
        self.status_label.pack(pady=10)

    def generate(self):
        name = self.name_entry.get().strip()
        template = self.template_combo.get()
        reqs_input = self.reqs_entry.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Project name is required.")

        requirements = [pkg.strip() for pkg in reqs_input.split(",") if pkg.strip()]
        project_path = Path.cwd() 

        try:
            generate_project(name, template, requirements, base_path=project_path)
            
            # Optionally run extras
            from scaffold_generator.bootstrap import (
                setup_virtualenv,
                install_dependencies,
                init_git_repo
            )
            
            project_root = project_path / name

            if self.venv_var.get():
                setup_virtualenv(project_root)
            
            if self.install_var.get():
                install_dependencies(project_root)

            if self.git_var.get():
                init_git_repo(project_root)

            self.status_label.config(text=f"Project '{name}' created!", foreground="green")
        
        except Exception as e:
            self.status_label.config(f"Error: {e}", foreground="red") 

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ScaffoldApp(root)
    root.mainloop() 