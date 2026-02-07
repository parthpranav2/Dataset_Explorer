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
    Exhaustively explores .ts (T-Surf) triangulated surface files.
    Zero truncation: provides mesh counts and 3D spatial boundaries.
    """
    try:
        name = "Unknown Surface"
        v_count = 0
        t_count = 0
        x_coords, y_coords, z_coords = [], [], []

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Identify Surface Name
                if "name:" in clean_line.lower():
                    name = clean_line.split(':')[-1].strip()

                # 2. Count Vertices and Triangles
                if clean_line.startswith("VRTX"):
                    v_count += 1
                    # Extract coordinates for bounding box
                    parts = clean_line.split()
                    if len(parts) >= 5:
                        x_coords.append(float(parts[2]))
                        y_coords.append(float(parts[3]))
                        z_coords.append(float(parts[4]))
                
                elif clean_line.startswith("TRGL"):
                    t_count += 1

        output = [
            f"Type: GOCAD/Petrel Triangulated Surface (.ts)",
            f"Surface Name: {name}",
            f"Mesh Density: {v_count} Vertices | {t_count} Triangles",
            "Spatial Bounding Box:"
        ]

        if x_coords:
            output.append(f"  - X Range: {min(x_coords)} to {max(x_coords)}")
            output.append(f"  - Y Range: {min(y_coords)} to {max(y_coords)}")
            output.append(f"  - Z Range: {min(z_coords)} to {max(z_coords)}")
        else:
            output.append("  - Spatial data not found.")

        return "\n".join(output)

    except Exception as e:
        return f"TS Extraction Error: {str(e)}"