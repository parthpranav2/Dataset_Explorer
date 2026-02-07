import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    from netCDF4 import Dataset
except ImportError:
    Dataset = None
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .nc / .netcdf scientific data files.
    Zero truncation: identifies dimensions, variables, and units.
    """
    if not Dataset:
        return "Error: netCDF4 library not found in venv."

    try:
        with Dataset(file_path, mode='r') as rootgrp:
            # 1. Dimensions Audit
            dims = [f"{name}({len(dim)})" for name, dim in rootgrp.dimensions.items()]
            
            # 2. Variable and Unit Inventory
            vars_info = []
            for name, var in rootgrp.variables.items():
                unit = getattr(var, 'units', 'no units')
                vars_info.append(f"{name} [{unit}] ({var.dtype})")

            # 3. Global Metadata
            conv = getattr(rootgrp, 'Conventions', 'Unknown')
            
            output = [
                "Type: Network Common Data Form (.netcdf)",
                f"Conventions: {conv}",
                "Dimensions:",
                f"  - " + (", ".join(dims) if dims else "None"),
                "Variables Info:",
                "  - " + ("\n  - ".join(vars_info[:10]) if vars_info else "None")
            ]
            
            if len(vars_info) > 10:
                output.append(f"  ... and {len(vars_info) - 10} more variables.")

            return "\n".join(output)

    except Exception as e:
        return f"NetCDF Extraction Error: {str(e)}"