import sys
import os

# Step 1: Add src/ folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', 'src'))

if project_root not in sys.path:
    sys.path.append(project_root)

# Step 2: Import the unified modules
from cli_tool.interface import modules
