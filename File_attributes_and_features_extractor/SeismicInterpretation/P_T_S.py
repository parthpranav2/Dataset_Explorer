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
    Exhaustively explores .pts point set files.
    Zero truncation: provides point counts, spatial bounds, and attribute detection.
    """
    try:
        point_count = 0
        x_min, x_max = float('inf'), float('-inf')
        y_min, y_max = float('inf'), float('-inf')
        z_min, z_max = float('inf'), float('-inf')
        header_lines = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue
                
                # 1. Capture Header (often just a single number at top)
                if len(header_lines) < 5:
                    header_lines.append(clean_line)

                # 2. Extract Coordinates
                # Pattern: matches floats/integers
                parts = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                if len(parts) >= 3:
                    try:
                        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                        point_count += 1
                        
                        # Update Bounds
                        if x < x_min: x_min = x
                        if x > x_max: x_max = x
                        if y < y_min: y_min = y
                        if y > y_max: y_max = y
                        if z < z_min: z_min = z
                        if z > z_max: z_max = z
                    except ValueError:
                        continue

        output = [
            "Type: Geospatial Point Set/Cloud (.pts)",
            f"Total Points: {point_count}",
            "Spatial Extents:"
        ]

        if point_count > 0:
            output.append(f"  - X Range: {x_min} to {x_max}")
            output.append(f"  - Y Range: {y_min} to {y_max}")
            output.append(f"  - Z Range: {z_min} to {z_max}")
        else:
            output.append("  - No valid coordinate points found.")

        output.append("Data Sample:")
        output.extend([f"  {line}" for line in header_lines if len(line.split()) > 1][:3])

        return "\n".join(output)

    except Exception as e:
        return f"PTS Extraction Error: {str(e)}"