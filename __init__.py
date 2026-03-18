import importlib.util
import glob
import os
import sys
from .pysssss import init, get_ext_dir

#  High-Compatibility ANSI Colors
MAGENTA_BRIGHT = "\033[95m"
BLUE_BRIGHT    = "\033[94m"
CYAN_BRIGHT    = "\033[96m"
GREEN          = "\033[1;32m"
CYAN           = "\033[1;36m"
MAGENTA        = "\033[1;35m"
RESET          = "\033[0m"

#  5-Line Gradient ASCII Header: EmAySee (Block Style)
#  Each line is wrapped individually to force the color shift
banner = f"""
{MAGENTA_BRIGHT} ███████╗███╗   ███╗ █████╗ ██╗   ██╗ ██████╗███████╗███████╗{RESET}
{MAGENTA_BRIGHT} ██╔════╝████╗ ████║██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝██╔════╝{RESET}
{BLUE_BRIGHT} █████╗  ██╔████╔██║███████║ ╚████╔╝ ╚█████╗ █████╗  █████╗  {RESET}
{CYAN_BRIGHT} ██╔══╝  ██║╚██╔╝██║██╔══██║  ╚██╔╝   ╚═══██╗██╔══╝  ██╔══╝  {RESET}
{CYAN_BRIGHT} ███████╗██║ ╚═╝ ██║██║  ██║   ██║   ██████╔╝███████╗███████╗{RESET}
{CYAN_BRIGHT} ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═════╝ ╚══════╝╚══════╝{RESET}"""

print(banner)
print(f"{MAGENTA}----------------------------------------------------------{RESET}")
print(f"{GREEN}Initializing SPECTRE v5.0 | EmAySee Custom Nodes Active{RESET}")
print(f"{MAGENTA}----------------------------------------------------------{RESET}")
print(f"{CYAN}Starting Diagnostic System Check...{RESET}")

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if init():
    py = get_ext_dir("py")
    files = glob.glob(os.path.join(py, "*.py"), recursive=False)
    
    for file in files:
        module_name = os.path.splitext(os.path.basename(file))[0]
        if module_name == "__init__":
            continue
            
        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            if hasattr(module, "NODE_CLASS_MAPPINGS") and getattr(module, "NODE_CLASS_MAPPINGS") is not None:
                NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                #  Success Checkmark
                print(f"  {GREEN}[✓]{RESET} {module_name}")
                
                if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS") and getattr(module, "NODE_DISPLAY_NAME_MAPPINGS") is not None:
                    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            
        except Exception as e:
            #  Failure Cross
            print(f"  \033[1;31m[✗]\033[0m {module_name} : Error -> {str(e)}")

print(f"{MAGENTA}----------------------------------------------------------{RESET}")
print(f"{GREEN}SPECTRE Online: {len(NODE_CLASS_MAPPINGS)} Nodes Mapped.{RESET}\n")

WEB_DIRECTORY = "./web"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
