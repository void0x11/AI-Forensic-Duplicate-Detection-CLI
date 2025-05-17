import os
import platform
import cmd
import random
import time
from loader import logger
from ascii_art import random_ascii_art

# Initialize colorama or fallback
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = MAGENTA = ""
    class Style:
        BRIGHT = RESET_ALL = ""

# Color styles
INFO = Fore.CYAN + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
WARNING = Fore.YELLOW + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
PROMPT = Fore.CYAN + Style.BRIGHT
RESET = Style.RESET_ALL

def colorful_ascii():
    art = random_ascii_art()
    color = random.choice([Fore.MAGENTA, Fore.CYAN, Fore.YELLOW])
    return f"{color}{art}{RESET}"

def check_ai_model(name, loader_func):
    try:
        print(f"{WARNING}🔄 Initializing AI model: {name:<20} {RESET}", end="")
        loader_func()
        print(f"{SUCCESS}[+] OK{RESET}")
        return True
    except Exception as e:
        print(f"{ERROR}[!] Failed: {e}{RESET}")
        return False

def boot_diagnostics():
    from loader import (
        daily_snapshot, scan_duplicates, tracker,
        resnet18_model, resnet50_model, resnet101_model,
        efficientnet_b1_model, efficientnet_b3_model,
        clip_model, dinov2_model,
        sbert_model, sbert_deep_model,
        codebert_model
    )

    print(f"{INFO}[*] Booting Dupli-HQ modules and AI models...\n{RESET}")
    all_ok = True

    core_checks = {
        "daily_snapshot": daily_snapshot,
        "scan_duplicates": scan_duplicates,
        "tracker": tracker,
    }

    for name, mod in core_checks.items():
        print(f"{WARNING}🔄 Loading {name:<25} {RESET}", end="")
        if mod:
            print(f"{SUCCESS}[+] OK{RESET}")
        else:
            print(f"{ERROR}[!] Failed{RESET}")
            all_ok = False

    all_ok &= check_ai_model("resnet18", resnet18_model.load_model)
    all_ok &= check_ai_model("resnet50", resnet50_model.load_model)
    all_ok &= check_ai_model("resnet101", resnet101_model.load_model)
    all_ok &= check_ai_model("efficientnet_b1", efficientnet_b1_model.load_model)
    all_ok &= check_ai_model("efficientnet_b3", efficientnet_b3_model.load_model)
    all_ok &= check_ai_model("clip", clip_model.load_model)
    all_ok &= check_ai_model("dinov2", dinov2_model.load_model)
    all_ok &= check_ai_model("sbert", sbert_model.load_model)
    all_ok &= check_ai_model("sbert_deep", sbert_deep_model.load_model)
    all_ok &= check_ai_model("codebert", lambda: codebert_model.load_model()[1])

    if all_ok:
        print(f"\n{SUCCESS}🧠 AI engines and forensic modules initialized.{RESET}\n")
    else:
        print(f"\n{ERROR}[!] Some components failed to initialize. CLI may be unstable.{RESET}\n")

    return daily_snapshot, scan_duplicates, tracker

class DupliHQShell(cmd.Cmd):
    intro = colorful_ascii() + f"\n{INFO}Welcome to Dupli-HQ. Type help or ? to list commands.{RESET}\n"
    prompt = f"{PROMPT}dupli-hq> {RESET}"

    settings = {
        "path": None,
        "mode": "snapshot",
        "strategy": "full"
    }

    def __init__(self, daily_snapshot, scan_duplicates, tracker):
        super().__init__()
        self.daily_snapshot = daily_snapshot
        self.scan_duplicates = scan_duplicates
        self.tracker = tracker

    def default(self, line):
        logger.log_command(line)
        return super().default(line)

    def do_set(self, arg):
        """
Set a configuration option.

Usage:
  set path <folder_path>
  set mode <snapshot|duplicates|tracker>
  set strategy <full|custom>
        """
        logger.log_command(f"set {arg}")
        parts = arg.split()
        if len(parts) != 2:
            print(f"{ERROR}Usage: set <option> <value>{RESET}")
            return
        key, value = parts
        if key in self.settings:
            self.settings[key] = value
            print(f"{WARNING}[*] {key} set to {value}{RESET}")
        else:
            print(f"{ERROR}[!] Unknown setting '{key}'{RESET}")

    def do_show(self, arg):
        """Show current configuration values."""
        logger.log_command("show")
        print(f"{INFO}Current Settings:{RESET}")
        for k, v in self.settings.items():
            print(f"  {k}: {v}")

    def do_run(self, arg):
        """Run the selected mode using the current configuration."""
        logger.log_command("run")
        mode = self.settings["mode"]
        path = self.settings["path"]

        if not path:
            print(f"{ERROR}[!] Please set path using `set path <folder>`.{RESET}")
            return

        print(f"{INFO}[*] Executing mode: {mode} on path: {path}{RESET}")

        try:
            if mode == "snapshot":
                self.daily_snapshot.main(path)

            elif mode == "duplicates":
                results = self.scan_duplicates.scan_folder_for_duplicates(path)
                if results:
                    print(f"{SUCCESS}🔍 Duplicates Found:{RESET}")
                    for f1, f2, label in results:
                        print(f"{SUCCESS}{label}:{RESET}\n → {f1}\n → {f2}\n")
                    self.scan_duplicates.save_report(results)
                else:
                    print(f"{SUCCESS}✅ No duplicates found.{RESET}")

            elif mode == "tracker":
                print(f"{INFO}🛰️ Starting file tracker...{RESET}\n")
                self.tracker.monitor_folder(path)

            else:
                print(f"{ERROR}[!] Unknown mode: {mode}{RESET}")

        except Exception as e:
            print(f"{ERROR}❌ Error during '{mode}' execution: {e}{RESET}")

    def do_exit(self, arg):
        """Exit the Dupli-HQ CLI tool."""
        logger.log_command("exit")
        print(f"{INFO}Exiting...{RESET}")
        return True

    def do_help(self, arg):
        """List available commands or detailed help on a specific command."""
        logger.log_command("help" if not arg else f"help {arg}")
        super().do_help(arg)

if __name__ == "__main__":
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    # Boot and delay for visual loading
    daily_snapshot, scan_duplicates, tracker = boot_diagnostics()
    print("Loading...")
    time.sleep(5)

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

    DupliHQShell(daily_snapshot, scan_duplicates, tracker).cmdloop()