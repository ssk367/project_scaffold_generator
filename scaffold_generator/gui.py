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
        self.root.geometry("800x800")
        # Center the window on display
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
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
        self.template_combo.set("Select Type") # Default
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

        ttk.Checkbutton(self.root, text="Create virtual enviroment", variable=self.venv_var, command=self.update_preview).pack(pady=5)
        ttk.Checkbutton(self.root, text="Install dependencies", variable=self.install_var, command=self.update_preview).pack(pady=5)
        ttk.Checkbutton(self.root, text="Initialize Git repository", variable=self.git_var, command=self.update_preview).pack(pady=5)

        # Preview label
        ttk.Label(self.root, text="Folder Structure Preview:").pack(pady=(10, 0))

        # Text box (read-only)
        self.preview_box = tk.Text(self.root, height=15, width=75, state="disabled", background="#1e1e1e", foreground="white")
        self.preview_box.pack(pady=5)

        # Generate button
        self.generate_btn = ttk.Button(self.root, text="Generate Project", command=self.generate)
        self.generate_btn.pack(pady=5)

        # Status label
        self.status_label = ttk.Label(self.root, text="", foreground="green")
        self.status_label.pack(pady=10)

        # Log panel
        ttk.Label(self.root, text= "Log Output:").pack(pady=(10, 0))

        log_frame = ttk.Frame(self.root)
        log_frame.pack(pady=(0, 10), fill="both", expand=False)

        self.log_text = tk.Text (
            log_frame,
            height=6,
            width=80,
            state="disabled",
            background="#1e1e1e",
            foreground="white",
            font=("courier New", 9),
            wrap="word"
            )
        
        self.log_text.pack(side="left", fill="both", expand=True)

        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=log_scrollbar.set)

    def append_log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

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

            self.append_log(f"Project '{name}' scaffold generated successfully")

            if self.venv_var.get():
                self.append_log("→ Creating virtual enviroment...")
                setup_virtualenv(project_root)
            
            if self.install_var.get():
                self.append_log("→ Installing dependencies")
                install_dependencies(project_root)

            if self.git_var.get():
                self.append_log("→ Initializing Git repository")
                init_git_repo(project_root)

            self.status_label.config(text=f"Project '{name}' created!", foreground="green")
        
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", foreground="red") 
            self.append_log(f"Error: {e}")
    
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
        extras = ["\n Optional Actions:"]
        extras.append(f"{'✓' if self.venv_var.get() else '✗'} Create virtual environment")
        extras.append(f"{'✓' if self.install_var.get() else '✗'} Install dependencies")
        extras.append(f"{'✓' if self.git_var.get() else '✗'} Initialize Git repository")

        full_preview = preview + "\n" + "\n".join(extras)

        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, full_preview)
        self.preview_box.config(state="disabled")

if __name__ == "__main__":
    root = ttk.Window(themename="cyborg")
    app = ScaffoldApp(root)
    root.mainloop() 