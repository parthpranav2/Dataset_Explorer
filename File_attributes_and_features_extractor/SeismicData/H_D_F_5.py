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
    Exhaustively explores .hdf5 files.
    Zero truncation: recursively visits every item to map hierarchy and metadata.
    """
    try:
        output_lines = []
        
        def h5_visitor(name, obj):
            # Calculate indentation based on depth in the HDF5 tree
            depth = name.count('/')
            indent = "  " * (depth + 1)
            
            if isinstance(obj, h5py.Group):
                output_lines.append(f"{indent}Group: {name.split('/')[-1]}")
            elif isinstance(obj, h5py.Dataset):
                output_lines.append(f"{indent}Dataset: {name.split('/')[-1]} (Shape: {obj.shape}, Type: {obj.dtype})")
            
            # Extract attributes (metadata) for each object
            if obj.attrs:
                for attr_key in obj.attrs:
                    val = obj.attrs[attr_key]
                    output_lines.append(f"{indent}  @Attr: {attr_key} = {val}")

        with h5py.File(file_path, 'r') as f:
            output_lines.append("Internal HDF5 Hierarchy:")
            # visititems explores the entire file structure
            f.visititems(h5_visitor)

        output = [
            "Type: HDF5 Hierarchical Data (.hdf5)",
            "Structure Audit:",
            "\n".join(output_lines) if output_lines else "  No internal groups or datasets detected."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"HDF5 Extraction Error: {str(e)}"