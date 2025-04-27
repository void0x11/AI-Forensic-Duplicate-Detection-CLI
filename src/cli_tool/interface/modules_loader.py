import importlib
import inspect
import os

def load_all_functions_from_cli_tool():
    loaded_functions = {}
    cli_tool_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    base_package = 'cli_tool'

    for root, dirs, files in os.walk(cli_tool_root):
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__'):
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, cli_tool_root)
                module_name = os.path.splitext(relative_path)[0].replace(os.sep, '.')
                module_path = f"{base_package}.{module_name}"

                try:
                    module = importlib.import_module(module_path)
                    for name, obj in inspect.getmembers(module):
                        if inspect.isfunction(obj):
                            loaded_functions[name] = obj
                except ModuleNotFoundError as e:
                    print(f"Warning: Couldn't import {module_path}: {e}")

    return loaded_functions
