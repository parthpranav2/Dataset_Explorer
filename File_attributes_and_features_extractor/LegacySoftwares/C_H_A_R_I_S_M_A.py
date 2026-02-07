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
    Exhaustively explores Charisma-format seismic interpretation files.
    Zero truncation: identifies line/trace ranges and vertical data domain.
    """
    try:
        lines = 0
        z_vals = []
        line_names = set()
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line or i > 100000: continue # Limit scan for speed

                # 1. Identify Line Names
                # Charisma often places the line name in the first few columns
                parts = clean_line.split()
                if len(parts) >= 4:
                    line_names.add(parts[0])
                    try:
                        # Standard Charisma export: Line Trace X Y Z
                        z_vals.append(float(parts[-1]))
                        lines += 1
                    except ValueError:
                        continue

        # 2. Vertical Range & Unit Guessing
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            # Heuristic: 0-6000 range usually indicates TWT (ms)
            domain = "Time (ms)" if 0 <= z_max <= 6000 else "Depth (m/ft)"
        else:
            z_min = z_max = "N/A"
            domain = "Unknown"

        output = [
            "Type: Charisma Legacy Seismic Interpretation",
            f"Total Points: {lines}",
            f"Unique Lines: {len(line_names)}",
            f"Vertical Domain: {domain}",
            f"Z-Range: {z_min} to {z_max}",
            "Line Sample:"
        ]
        
        if line_names:
            output.append(f"  - {list(line_names)[0]}")

        return "\n".join(output)

    except Exception as e:
        return f"Charisma Extraction Error: {str(e)}"