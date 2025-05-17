import os
from datetime import datetime
from pathlib import Path

def log_command(command: str):
    log_path = Path(__file__).resolve().parents[3] / "src" / "logs" / "cli_commands.log"
    os.makedirs(log_path.parent, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {command.strip()}\n")