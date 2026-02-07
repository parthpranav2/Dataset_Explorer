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
    Exhaustively explores IESX (GeoFrame) format seismic exports.
    Zero truncation: identifies data type, survey bounds, and vertical domain.
    """
    try:
        point_count = 0
        z_vals = []
        survey_name = "Unknown"
        object_name = "Unknown IESX Object"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Parse IESX Header (First 15 lines)
                if i < 15:
                    upper_line = clean_line.upper()
                    if "SURVEY" in upper_line:
                        survey_name = clean_line.split()[-1]
                    if "HORIZON" in upper_line or "FAULT" in upper_line:
                        object_name = clean_line.split()[-1]
                    continue

                # 2. Data Extraction (Fixed Column or Space Delimited)
                parts = clean_line.split()
                if len(parts) >= 3:
                    try:
                        # Common format: Inline Crossline X Y Z
                        z_vals.append(float(parts[-1]))
                        point_count += 1
                    except ValueError:
                        continue

        # 3. Structural Analysis
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            # Heuristic: 0-7000 is likely Time (ms), larger is Depth
            domain = "Time (ms)" if 0 <= z_max <= 7000 else "Depth"
        else:
            z_min = z_max = "N/A"
            domain = "Unknown"

        output = [
            "Type: IESX (GeoFrame) Seismic Export",
            f"Object Identity: {object_name}",
            f"Associated Survey: {survey_name}",
            f"Total Picks: {point_count}",
            f"Vertical Domain: {domain} ({z_min} to {z_max})",
            "Data Preview (First Point):"
        ]
        
        # Seek back to find first data line for sample
        f.seek(0)
        for _ in range(16): f.readline() # Skip header
        output.append(f"  {f.readline().strip()}")

        return "\n".join(output)

    except Exception as e:
        return f"IESX Extraction Error: {str(e)}"