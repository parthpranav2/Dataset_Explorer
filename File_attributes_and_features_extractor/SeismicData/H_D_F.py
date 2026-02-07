import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import h5py

def extract(file_path):
    """
    Exhaustively explores HDF files.
    Zero truncation: recursively maps all groups, datasets, and attributes.
    """
    try:
        output_lines = []
        
        def visitor(name, obj):
            indent = "  " * (name.count('/') + 1)
            if isinstance(obj, h5py.Group):
                output_lines.append(f"{indent}Group: {name}")
            elif isinstance(obj, h5py.Dataset):
                output_lines.append(f"{indent}Dataset: {name} (Shape: {obj.shape}, Type: {obj.dtype})")
            
            # Extract Attributes for each object
            for attr_name in obj.attrs:
                output_lines.append(f"{indent}  @Attr: {attr_name} = {obj.attrs[attr_name]}")

        with h5py.File(file_path, 'r') as f:
            output_lines.append("Root Hierarchy:")
            f.visititems(visitor)

        output = [
            "Type: Hierarchical Data Format (.hdf)",
            "Internal Data Structure:",
            "\n".join(output_lines) if output_lines else "  Empty HDF structure."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"HDF Extraction Error: {str(e)}"