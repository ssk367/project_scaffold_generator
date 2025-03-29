# gui.py

import tkinter as tk
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
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.create_widgets() 

    def create_widgets(self):
        # Project name
        ttk.Label(self.root, text="Project Name:").pack(pady=(10, 0))
        self.name_entry = ttk.Entry(self.root, width=40)
        self.name_entry.pack(pady=5)

        # Template type dropdown
        ttk.Label(self.root, text="Template Type:").pack(pady=(10, 0))
        self.template_combo = ttk.Combobox(self.root, values=list(TEMPLATES.keys()), bootstyle="primary", state="readonly", width=37)
        self.template_combo.pack(pady=5)
        self.template_combo.set("app") # Default
        self.template_combo.bind("<<ComboboxSelected>>", self.update_preview)
        self.name_entry.bind("<KeyRelease>", self.update_preview)

        # Requirements entry
        ttk.Label(self.root, text="Requirements (comma seperated):").pack(pady=(10, 0))
        self.reqs_entry = ttk.Entry(self.root, width=40)
        self.reqs_entry.pack(pady=15)

        # Optional steps (checkboxes)
        self.venv_var = ttk.BooleanVar(value=True)
        self.install_var = ttk.BooleanVar(value=True)
        self.git_var = ttk.BooleanVar(value=True)

        ttk.Checkbutton(self.root, text="Create virtual enviroment", variable=self.venv_var).pack(pady=5)
        ttk.Checkbutton(self.root, text="Install dependencies", variable=self.install_var).pack(pady=5)
        ttk.Checkbutton(self.root, text="Initialize Git repository", variable=self.git_var).pack(pady=5)

        # Folder structure preview label
        ttk.Label(self.root, text="Folder Structure Preview:").pack(pady=(10, 0))

        # Text box (read-only)
        self.preview_box = tk.Text(self.root, height=8, width=50, state="disabled", background="#1e1e1e", foreground="white")
        self.preview_box.pack(pady=5)

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
            self.status_label.config(text=f"Error: {e}", foreground="red") 
    
    def update_preview(self, *args):
        template_name = self.template_combo.get()
        structure = TEMPLATES.get(template_name, {})
        project_name = self.name_entry.get() or "YourProject"

        lines = [f"{self.name_entry.get() or 'YourProject'}/"]

        for folder, files in structure.items():
            folder_indent = "├── " if folder else ""
            if folder:
                lines.append(f"├── {folder}")
            for file in files:
                if folder:
                    lines.append(f"│   └── {folder}/{file}")
                else:
                    lines.append(f"├── {file}")

        preview = "\n".join(lines)

        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, preview)
        self.preview_box.config(state="disabled")

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = ScaffoldApp(root)
    root.mainloop() 