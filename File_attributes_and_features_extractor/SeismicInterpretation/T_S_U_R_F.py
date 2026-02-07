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
    Exhaustively explores .tsurf GOCAD surface files.
    Zero truncation: identifies property arrays and mesh topology.
    """
    try:
        header_info = {}
        properties = []
        counts = {'VRTX': 0, 'TRGL': 0, 'BORD': 0}
        bounds = {'x': [float('inf'), float('-inf')], 
                  'y': [float('inf'), float('-inf')], 
                  'z': [float('inf'), float('-inf')]}

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue

                # 1. Parse Header Attributes
                if ':' in line and counts['VRTX'] == 0:
                    key, val = line.split(':', 1)
                    header_info[key.strip()] = val.strip()

                # 2. Identify Property Definitions
                if line.startswith("PROPERTY "):
                    properties.append(line.split()[1])

                # 3. Component Counting and Bounding
                prefix = line.split()[0]
                if prefix in counts:
                    counts[prefix] += 1
                    if prefix == 'VRTX':
                        parts = line.split()
                        if len(parts) >= 5:
                            x, y, z = float(parts[2]), float(parts[3]), float(parts[4])
                            bounds['x'] = [min(bounds['x'][0], x), max(bounds['x'][1], x)]
                            bounds['y'] = [min(bounds['y'][0], y), max(bounds['y'][1], y)]
                            bounds['z'] = [min(bounds['z'][0], z), max(bounds['z'][1], z)]

        output = [
            f"Type: GOCAD Triangulated Surface (.tsurf)",
            f"Surface Identity: {header_info.get('name', 'Unknown')}",
            f"Topology: {counts['VRTX']} Vertices | {counts['TRGL']} Triangles",
            f"Mapped Properties: {', '.join(properties) if properties else 'None'}",
            "Spatial Extents:"
        ]

        if counts['VRTX'] > 0:
            output.append(f"  - X Range: {bounds['x'][0]} to {bounds['x'][1]}")
            output.append(f"  - Y Range: {bounds['y'][0]} to {bounds['y'][1]}")
            output.append(f"  - Z Range: {bounds['z'][0]} to {bounds['z'][1]}")
        else:
            output.append("  - No geometry data found.")

        return "\n".join(output)

    except Exception as e:
        return f"TSURF Extraction Error: {str(e)}"
