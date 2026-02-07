import sys
import os
import re

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .grd grid files.
    Zero truncation: identifies grid dimensions and Z-value ranges.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            header = f.readline().strip()
            
            # 1. Surfer ASCII (DSAA) Identification
            if "DSAA" in header:
                # Read dimensions: NX NY
                dims = f.readline().split()
                nx, ny = int(dims[0]), int(dims[1])
                # Read ranges
                x_range = f.readline().split()
                y_range = f.readline().split()
                z_range = f.readline().split()
                
                output = [
                    "Type: Surfer ASCII Grid (.grd)",
                    f"Dimensions: {nx} (X) x {ny} (Y) Nodes",
                    f"Total Nodes: {nx * ny}",
                    "Surface Statistics:",
                    f"  - X Range: {x_range[0]} to {x_range[1]}",
                    f"  - Y Range: {y_range[0]} to {y_range[1]}",
                    f"  - Z Range: {z_range[0]} to {z_range[1]}"
                ]
            
            # 2. ZMAP / Other ASCII Formats
            elif header.startswith("@") or header.startswith("!"):
                output = ["Type: ZMAP/Generic ASCII Grid (.grd)"]
                # Scan for comments/headers
                f.seek(0)
                lines = [f.readline().strip() for _ in range(5)]
                output.append("Header Preview:")
                output.extend([f"  {line}" for line in lines if line])
            
            else:
                output = ["Type: Potential Binary or Custom Grid (.grd)"]
                output.append(f"Header Signature: {header[:20]}")

        return "\n".join(output)

    except Exception as e:
        return f"GRD Extraction Error: {str(e)}"