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
    Exhaustively explores .sv seismic velocity files.
    Zero truncation: identifies velocity types and profiles.
    """
    try:
        header_lines = []
        velocity_pairs = []
        v_type = "Unknown"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue
                
                # 1. Header & Type Detection
                if len(header_lines) < 10:
                    header_lines.append(clean_line)
                    upper = clean_line.upper()
                    if "RMS" in upper: v_type = "RMS Velocity (Vrms)"
                    elif "INT" in upper: v_type = "Interval Velocity (Vint)"
                    elif "AVG" in upper: v_type = "Average Velocity (Vavg)"

                # 2. Extract Numeric Pairs (Depth/Time vs Velocity)
                parts = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                if len(parts) >= 2:
                    try:
                        velocity_pairs.append((float(parts[0]), float(parts[1])))
                    except ValueError:
                        continue

        # 3. Calculate Profile Stats
        if velocity_pairs:
            z_vals = [p[0] for p in velocity_pairs]
            v_vals = [p[1] for p in velocity_pairs]
            v_min, v_max = min(v_vals), max(v_vals)
            z_min, z_max = min(z_vals), max(z_vals)
        else:
            v_min = v_max = z_min = z_max = "N/A"

        output = [
            f"Type: Seismic Velocity Profile (.sv)",
            f"Velocity Category: {v_type}",
            f"Vertical Extent: {z_min} to {z_max} (units match header)",
            f"Velocity Range: {v_min} to {v_max}",
            f"Data Summary: {len(velocity_pairs)} velocity nodes detected.",
            "Header Metadata Preview:"
        ]
        output.extend([f"  {line}" for line in header_lines[:3]])

        return "\n".join(output)

    except Exception as e:
        return f"Velocity Extraction Error: {str(e)}"