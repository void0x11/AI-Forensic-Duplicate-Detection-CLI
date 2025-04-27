from cli_tool.interface.modules_loader import load_all_functions_from_cli_tool

# Load all functions
_loaded_functions = load_all_functions_from_cli_tool()

# Expose a 'modules' object manually
class ModulesNamespace:
    pass

modules = ModulesNamespace()

for name, func in _loaded_functions.items():
    setattr(modules, name, func)
