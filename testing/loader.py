from pathlib import Path

def find_project_root(marker_files=("pyproject.toml", ".git", "requirements.txt")):
    current = Path(__file__).resolve()
    for parent in current.parents:
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    return None  # Not found

project_root = find_project_root()
print(f"Detected project root: {project_root}")
