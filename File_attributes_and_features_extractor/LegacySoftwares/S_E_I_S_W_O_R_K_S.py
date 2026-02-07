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
    Exhaustively explores SeisWorks (Landmark) format interpretation exports.
    Zero truncation: identifies project origin, survey geometry, and structural range.
    """
    try:
        point_count = 0
        z_vals = []
        lines_seen = set()
        object_name = "Unknown Landmark Object"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Parse Landmark Header
                if i < 15:
                    if "HORIZON" in clean_line.upper():
                        object_name = "Horizon: " + clean_line.split()[-1]
                    elif "FAULT" in clean_line.upper():
                        object_name = "Fault: " + clean_line.split()[-1]
                    continue

                # 2. Extract Data (SeisWorks 3D: Line Trace X Y Z or similar)
                parts = clean_line.split()
                if len(parts) >= 3:
                    try:
                        # Collect Line/Trace for geometry audit
                        lines_seen.add(parts[0])
                        # Collect Z-value for vertical domain check
                        z_vals.append(float(parts[-1]))
                        point_count += 1
                    except (ValueError, IndexError):
                        continue

        # 3. Structural Summary
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            # Standard Landmark heuristic: 0-7000 is likely TWT (ms)
            domain = "Time (ms)" if 0 <= z_max <= 7000 else "Depth (m/ft)"
        else:
            z_min = z_max = "N/A"
            domain = "Unknown"

        output = [
            "Type: SeisWorks (Landmark) Interpretation Export",
            f"Object Identity: {object_name}",
            f"Total Picks: {point_count}",
            f"Vertical Domain: {domain}",
            f"Structural Extent: {z_min} to {z_max}",
            f"Survey Scope: Found {len(lines_seen)} unique lines/inlines."
        ]

        return "\n".join(output)

    except Exception as e:
        return f"SeisWorks Extraction Error: {str(e)}"