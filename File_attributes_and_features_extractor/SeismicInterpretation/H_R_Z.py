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
    Exhaustively explores .hrz seismic horizon files.
    Zero truncation: identifies vertical units and structural extents.
    """
    try:
        nodes = 0
        z_vals = []
        horizon_name = "Unknown"
        header_sample = []

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Scrape Header for Metadata
                if len(header_sample) < 10:
                    header_sample.append(clean_line)
                    if "HORIZON" in clean_line.upper() or "NAME" in clean_line.upper():
                        horizon_name = clean_line.split()[-1]

                # 2. Extract Z-values (usually the 3rd or 5th column)
                parts = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                if len(parts) >= 3:
                    try:
                        # Standard formats: X Y Z or Inline Crossline Time
                        z_vals.append(float(parts[-1]))
                        nodes += 1
                    except ValueError:
                        continue

        # 3. Unit and Range Analysis
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            # Heuristic: Large positive/negative values usually imply Depth (m/ft)
            # Small positive values (0-5000) often imply Time (ms)
            is_time = 0 <= z_max <= 6000 and 0 <= z_min <= 6000
            unit = "ms (Time)" if is_time else "m/ft (Depth)"
        else:
            z_min = z_max = "N/A"
            unit = "Unknown"

        output = [
            f"Type: Seismic Horizon Interpretation (.hrz)",
            f"Horizon Identity: {horizon_name}",
            f"Data Density: {nodes} interpreted nodes",
            f"Vertical Domain: {unit}",
            f"Structural Range: {z_min} to {z_max}",
            "Header Preview:"
        ]
        output.extend([f"  {line}" for line in header_sample[:3]])

        return "\n".join(output)

    except Exception as e:
        return f"HRZ Extraction Error: {str(e)}"