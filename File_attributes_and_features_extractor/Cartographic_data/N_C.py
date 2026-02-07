import sys
import os
import netCDF4 as nc

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores NetCDF files.
    Zero truncation: every dimension, variable, and attribute is displayed.
    """
    try:
        ds = nc.Dataset(file_path, mode='r')
        
        detail_lines = []
        
        # 1. Dimensions (Axes)
        detail_lines.append("Dimensions (Axis):")
        for dim in ds.dimensions.values():
            detail_lines.append(f"  {dim.name}: Size {len(dim)}")
            
        # 2. Variables (Data Layers)
        detail_lines.append("Variables & Metadata:")
        for var_name, var in ds.variables.items():
            # Get variable-specific attributes (units, scale, etc.)
            var_attrs = [f"{k}={v}" for k, v in var.__dict__.items()]
            detail_lines.append(f"  {var_name} {var.dimensions}: {var.dtype}")
            if var_attrs:
                detail_lines.append(f"    Attrs: {', '.join(var_attrs)}")
        
        # 3. Global Attributes (File Metadata)
        global_attrs = ds.__dict__
        if global_attrs:
            detail_lines.append("Global Attributes:")
            for k, v in global_attrs.items():
                detail_lines.append(f"  {k}: {v}")

        ds.close()

        output = [
            "Type: NetCDF (Network Common Data Form)",
            f"Format: {ds.file_format}",
            "Exhaustive Scientific Metadata:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"NetCDF Error: {str(e)}"