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
    Exhaustively explores SIESX (IESX variant) seismic interpretation exports.
    Zero truncation: identifies project origin, object types, and structural range.
    """
    try:
        point_count = 0
        z_vals = []
        objects = set()
        project_name = "Unknown"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Parse SIESX Header
                if i < 20:
                    upper_line = clean_line.upper()
                    if "PROJECT" in upper_line:
                        project_name = clean_line.split()[-1]
                    if "HORIZON" in upper_line or "FAULT" in upper_line:
                        objects.add(clean_line.split()[-1])
                    continue

                # 2. Extract Coordinates (Standard format: Line Trace X Y Z)
                parts = clean_line.split()
                if len(parts) >= 3:
                    try:
                        z_vals.append(float(parts[-1]))
                        point_count += 1
                    except (ValueError, IndexError):
                        continue

        # 3. Structural Summary
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            # Heuristic: 0-7000 is usually TWT (ms)
            domain = "Time (ms)" if 0 <= z_max <= 7000 else "Depth (m/ft)"
        else:
            z_min = z_max = "N/A"
            domain = "Unknown"

        output = [
            "Type: SIESX (GeoFrame) Interpretation Export",
            f"Project Source: {project_name}",
            f"Interpreted Objects: {', '.join(objects) if objects else 'General Point Set'}",
            f"Total Nodes: {point_count}",
            f"Vertical Domain: {domain} ({z_min} to {z_max})",
            "Data Structure Preview:"
        ]
        
        f.seek(0)
        # Skip to first likely data line
        for _ in range(21): f.readline()
        output.append(f"  {f.readline().strip()[:60]}...")

        return "\n".join(output)

    except Exception as e:
        return f"SIESX Extraction Error: {str(e)}"