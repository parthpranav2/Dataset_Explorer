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
    Exhaustively explores .pol polygon/polyline files.
    Zero truncation: provides segment counts, vertex density, and spatial bounds.
    """
    try:
        segments = 0
        total_points = 0
        current_segment_points = 0
        x_coords, y_coords, z_coords = [], [], []
        meta_name = "Unknown"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Detect Header/Name
                if "name:" in clean_line.lower():
                    meta_name = clean_line.split(':')[-1].strip()

                # 2. Detect Segment Start (Standard GOCAD/Petrel markers)
                if any(x in clean_line for x in ['VRTX', 'PVRTX']):
                    total_points += 1
                    current_segment_points += 1
                    parts = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                    if len(parts) >= 3:
                        x_coords.append(float(parts[-3]))
                        y_coords.append(float(parts[-2]))
                        z_coords.append(float(parts[-1]))
                
                # 3. Detect Segment End or Break
                if "END" in clean_line.upper() or "SEG" in clean_line.upper():
                    segments += 1
                    current_segment_points = 0

        # If no explicit segment markers, treat as a single segment
        if segments == 0 and total_points > 0: segments = 1

        output = [
            f"Type: Geoscience Polygon/Polyline (.pol)",
            f"Boundary Name: {meta_name}",
            f"Geometry: {segments} Segments | {total_points} Total Vertices",
            "Spatial Extents:"
        ]

        if x_coords:
            output.append(f"  - X Range: {min(x_coords)} to {max(x_coords)}")
            output.append(f"  - Y Range: {min(y_coords)} to {max(y_coords)}")
            output.append(f"  - Z Range: {min(z_coords)} to {max(z_coords)}")
        else:
            output.append("  - No valid coordinate points found.")

        return "\n".join(output)

    except Exception as e:
        return f"POL Extraction Error: {str(e)}"