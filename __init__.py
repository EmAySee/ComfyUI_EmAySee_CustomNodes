import os
import importlib
from pathlib import Path

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

# Define the author
__author__ = "EmAySee"

# Get a list of all Python files in subdirectories, using pathlib
module_paths = []
for root, _, files in os.walk(Path(__file__).parent):
    for file in files:
        if file.endswith(".py") and file != "__init__.py":
            module_paths.append(Path(root) / file)

for module_path in module_paths:
    try:
        # Construct the module spec.  This is the critical part for subfolders.
        relative_path = module_path.relative_to(Path(__file__).parent)
        module_name = str(relative_path).replace(os.sep, ".")[:-3]  # Convert path to dot notation
        module = importlib.import_module(f".{module_name}", package=__package__)

        # Check for the required dictionaries and merge them
        if hasattr(module, "NODE_CLASS_MAPPINGS") and hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            print(f"Loaded nodes from {module_name}")
        else:
            print(f"Warning: {module_name} does not contain NODE_CLASS_MAPPINGS or NODE_DISPLAY_NAME_MAPPINGS. Skipping.")

    except ImportError as e:
        print(f"Error importing {module_name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {module_name}: {e}")

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
