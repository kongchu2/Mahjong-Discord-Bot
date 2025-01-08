import importlib
import os
import sys


def import_all_modules_from_folder(folder_path):
    if folder_path not in sys.path:
        sys.path.insert(0, folder_path)

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                importlib.import_module(module_name)
                print(f"Successfully imported {module_name}")
            except Exception as e:
                print(f"Failed to import {module_name}: {e}")
