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
    Exhaustively explores Kingdom (SMT) format interpretation files.
    Zero truncation: identifies survey geometry, Z-domain, and point counts.
    """
    try:
        point_count = 0
        z_vals = []
        inlines = []
        crosslines = []
        horizon_name = "Unknown"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Scrape for Horizon/Fault Name in header
                if i < 10 and ("HORIZON" in clean_line.upper() or "FAULT" in clean_line.upper()):
                    horizon_name = clean_line.replace('"', '').split()[-1]

                # 2. Extract Data (Kingdom 3D exports usually: Line Trace X Y Z)
                parts = clean_line.split()
                if len(parts) >= 5:
                    try:
                        inlines.append(float(parts[0]))
                        crosslines.append(float(parts[1]))
                        z_vals.append(float(parts[-1]))
                        point_count += 1
                    except ValueError:
                        continue

        # 3. Structural Summary
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            il_range = f"{min(inlines)} - {max(inlines)}"
            xl_range = f"{min(crosslines)} - {max(crosslines)}"
            # Standard Kingdom TWT (ms) vs Depth check
            domain = "Time (ms)" if 0 <= z_max <= 6000 else "Depth"
        else:
            z_min = z_max = "N/A"
            il_range = xl_range = "N/A"
            domain = "Unknown"

        output = [
            "Type: Kingdom (SMT) Seismic Interpretation Export",
            f"Object Name: {horizon_name}",
            f"Total Picks: {point_count}",
            f"Vertical Domain: {domain} ({z_min} to {z_max})",
            "Survey Geometry Audit:",
            f"  - Inline Range:    {il_range}",
            f"  - Crossline Range: {xl_range}",
            "Data Sample (First Line):"
        ]
        
        f.seek(0)
        output.append(f"  {f.readline().strip()[:60]}...")

        return "\n".join(output)

    except Exception as e:
        return f"Kingdom Extraction Error: {str(e)}"