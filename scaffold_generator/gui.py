# gui.py

import tkinter as tk
from tkinter import ttk
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

        # Generate button
        self.generate_btn = ttk.Button(self.root, text="Generate Project", command=self.generate)
        self.generate_btn.pack(pady=5)

        # Status label
        self.status_label = ttk.Label(self.root, text="", foreground="green")
        self.status_label.pack(pady=5)

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
            self.status_label.config(text=f"Project '{name}' created!", foreground="green")
        except Exception as e:
            self.status_label.config(f"Error: {e}", foreground="red") 

if __name__ == "__main__":
    root = tk.Tk()
    app = ScaffoldApp(root)
    root.mainloop() 