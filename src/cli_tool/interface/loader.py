# This script is used to find the project root directory by searching for specific marker files.
# It traverses up the directory tree from the current file's location until it finds a directory containing one of the specified marker files.
# If no such directory is found, it raises a RuntimeError.


# First Detecting the Root Directory of the Project

from pathlib import Path
import importlib.util

def find_project_root(marker_files=("pyproject.toml", ".git", "requirements.txt")):
    current = Path(__file__).resolve()
    for parent in current.parents:
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    return None  # fallback if not found

project_root = find_project_root()
if not project_root:
    raise RuntimeError("Project root not found. Make sure it contains one of the marker files.")

# Importing the Modules Dynamically

module_tree = {
    "resnet18_model": project_root / "src" / "ai_model" / "resnet18_model.py",
    "resnet50_model": project_root / "src" / "ai_model" / "resnet50_model.py",
    "resnet101_model": project_root / "src" / "ai_model" / "resnet101_model.py",
    "efficientnet_b1_model": project_root / "src" / "ai_model" / "efficientnet_b1_model.py",
    "efficientnet_b3_model": project_root / "src" / "ai_model" / "efficientnet_b3_model.py",
    "clip_model": project_root / "src" / "ai_model" / "clip_model.py",
    "dinov2_model": project_root / "src" / "ai_model" / "dinov2_model.py",
    "sbert_model": project_root / "src" / "ai_model" / "sbert_model.py",
    "sbert_deep_model": project_root / "src" / "ai_model" / "sbert_deep_model.py",
    "codebert_model": project_root / "src" / "ai_model" / "codebert_model.py",
    "pcphash": project_root / "src" / "cli_tool" / "hashing" / "perceptual_hash.py",
    "utilhash": project_root / "src" / "cli_tool" / "hashing" / "hash_utils.py",
    "cli_shell": project_root / "src" / "cli_tool" / "interface" / "cli_shell.py",
    "commands": project_root / "src" / "cli_tool" / "interface" / "commands.py",
    "daily_snapshot": project_root / "src" / "cli_tool" / "automation" / "daily_snapshot.py",
    "scan_duplicates": project_root / "src" / "cli_tool" / "automation" / "scan_duplicates.py",
}

# This script dynamically imports modules based on their file paths.
# --- Add dynamic import logic below ---
_loaded_modules = {}

def import_from_path(name: str, file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Module file not found: {file_path}")
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Required for `from loader import restmodel` to work dynamically
def __getattr__(name):
    if name in _loaded_modules:
        return _loaded_modules[name]
    if name in module_tree:
        mod = import_from_path(name, module_tree[name])
        _loaded_modules[name] = mod
        return mod
    raise AttributeError(f"Module '{name}' not found in loader.")


# The script also dynamically imports modules based on their file paths, allowing for flexible module loading.
# The `import_from_path` function is used to import a module from a specified file path, and the `__getattr__` function is defined to handle dynamic attribute access for module loading.
# The script is designed to be used in a project where the directory structure may vary, and it provides a way to load modules dynamically based on their file paths.
# The script is useful for projects with a complex directory structure or when modules are not in standard locations.