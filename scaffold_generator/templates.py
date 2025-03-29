# templates.py

TEMPLATES = {
    "app": {
        "app/": ["__init__.py"],
        "tests/": ["test_basic.py"],
        "": ["main.py", "README.md", "requirements.txt", ".gitignore"]
    }, 
    "game": {
        "game/": ["__init__.py", "engine.py"],
        "assets/images/": [],
        "": ["main.py", "README.md", "requirements.txt", ".gitignore"]
    },
    "data-analysis": {
        "data/raw/": [],
        "data/processed/": [],
        "notebooks/": ["exploration.ipynb"],
        "analysis/": ["__init__.py"],
        "": ["main.py", "README.md", "requirements.txt", ".gitignore"]
    }
}