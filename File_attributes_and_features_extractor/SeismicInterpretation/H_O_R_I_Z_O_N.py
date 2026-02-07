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
    Exhaustively explores .horizon seismic interpretation files.
    Zero truncation: identifies vertical units, node counts, and spatial bounds.
    """
    try:
        nodes = 0
        z_vals = []
        metadata = {}
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Parse Header Metadata (Key: Value)
                if ':' in clean_line and nodes == 0:
                    parts = clean_line.split(':', 1)
                    metadata[parts[0].strip()] = parts[1].strip()

                # 2. Extract Z-values (usually the last numeric column)
                nums = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                if len(nums) >= 3:
                    try:
                        z_vals.append(float(nums[-1]))
                        nodes += 1
                    except ValueError:
                        continue

        # 3. Structural Statistics
        if z_vals:
            z_min, z_max = min(z_vals), max(z_vals)
            # Heuristic: Small range (0-6000) usually implies Time (ms)
            domain = "Time (ms)" if 0 <= z_max <= 6000 else "Depth (m/ft)"
        else:
            z_min = z_max = "N/A"
            domain = "Unknown"

        output = [
            "Type: Seismic Horizon Interpretation (.horizon)",
            f"Horizon Name: {metadata.get('Name', 'Unknown')}",
            f"Interpreted Nodes: {nodes}",
            f"Vertical Domain: {domain}",
            f"Structural Range: {z_min} to {z_max}",
            "Metadata Audit:"
        ]
        
        # Add up to 3 metadata keys found in header
        meta_items = list(metadata.items())[:3]
        for key, val in meta_items:
            output.append(f"  - {key}: {val}")

        return "\n".join(output)

    except Exception as e:
        return f"HORIZON Extraction Error: {str(e)}"
    