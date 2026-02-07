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
    Exhaustively explores 3D Look-Up Table (.3dl) files.
    Zero truncation: every grid dimension and header comment is extracted.
    """
    try:
        header_lines = []
        data_points = []
        grid_size = "Unknown"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 1. Extract Comments and Metadata
                if line.startswith('#'):
                    header_lines.append(line.lstrip('#').strip())
                    continue
                
                # 2. Detect Grid Size (Commonly the first non-comment line)
                if grid_size == "Unknown" and re.match(r'^\d+$', line):
                    grid_size = line
                    continue
                
                # 3. Collect Data Samples (RGB/Value Triplets)
                parts = line.split()
                if len(parts) == 3:
                    try:
                        data_points.append([float(p) for p in parts])
                    except ValueError:
                        continue

        # Calculate Min/Max values across the whole LUT
        if data_points:
            import numpy as np
            arr = np.array(data_points)
            val_min = np.min(arr)
            val_max = np.max(arr)
        else:
            val_min, val_max = "N/A", "N/A"

        output = [
            "Type: 3D Look-Up Table (Symbology/Color LUT)",
            f"Grid Resolution: {grid_size}x{grid_size}x{grid_size}",
            f"Mapping Range: {val_min} to {val_max}",
            "Exhaustive Header Comments:",
            "\n".join([f"  - {h}" for h in header_lines]) if header_lines else "  No header comments found.",
            "Raw Sample (First 3 mapping points):",
            "\n".join([f"  {p}" for p in data_points[:3]]) if data_points else "  No numeric mapping found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"3DL Processing Error: {str(e)}"