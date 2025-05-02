import os
import platform
import cmd
import random
from ascii_art import random_ascii_art

# Try importing colorama for Windows compatibility, otherwise use plain ANSI
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

# Define some color options
COLORS = [
    "\033[91m",  # Red
    "\033[92m",  # Green
    "\033[93m",  # Yellow
    "\033[94m",  # Blue
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
]

RESET_COLOR = "\033[0m"

def colorful_ascii():
    art = random_ascii_art()
    color = random.choice(COLORS)
    return f"{color}{art}{RESET_COLOR}"

class DuplicateDetectionShell(cmd.Cmd):
    intro = colorful_ascii() + "\nType help or ? to list commands.\n"
    prompt = "dupli-hq> "

    # Session settings
    settings = {
        "path": None,
        "mode": None,
        "strategy": "full"  # default
    }

    def do_set(self, arg):
        "Set an option. Example: set path /folder/path"
        parts = arg.split()
        if len(parts) != 2:
            print("Usage: set <option> <value>")
            return
        key, value = parts
        if key in self.settings:
            self.settings[key] = value
            print(f"[*] {key} set to {value}")
        else:
            print(f"[!] Unknown setting '{key}'")

    def do_show(self, arg):
        "Show current configuration settings."
        print("Current Settings:")
        for k, v in self.settings.items():
            print(f"  {k}: {v}")

    def do_run(self, arg):
        "Run duplicate detection based on current settings."
        print("[*] Running detection...")
        print(f"[*] Mode: {self.settings['mode']}")
        print(f"[*] Path: {self.settings['path']}")
        print(f"[*] Strategy: {self.settings['strategy']}")
        print("[+] Detection completed! (placeholder)")

    def do_exit(self, arg):
        "Exit the CLI Tool."
        print("Exiting...")
        return True

    def do_help(self, arg):
        "List available commands with descriptions."
        super().do_help(arg)

if __name__ == "__main__":
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    DuplicateDetectionShell().cmdloop()
