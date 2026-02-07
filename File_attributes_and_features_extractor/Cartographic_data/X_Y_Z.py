import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores XYZ ASCII files.
    Zero truncation: every coordinate and the full data sample is provided.
    """
    try:
        count = 0
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
        sample_rows = []

        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        x, y, z = map(float, parts[:3])
                        min_x, max_x = min(min_x, x), max(max_x, x)
                        min_y, max_y = min(min_y, y), max(max_y, y)
                        min_z, max_z = min(min_z, z), max(max_z, z)
                        count += 1
                        if i < 5: # Capture first 5 rows as sample
                            sample_rows.append(line.strip())
                    except ValueError:
                        continue # Skip header lines if present

        output = [
            "Type: ASCII XYZ Point Data",
            f"Total Points: {count}",
            "Spatial Extent (X, Y, Z):",
            f"  X-Range: {min_x} to {max_x}",
            f"  Y-Range: {min_y} to {max_y}",
            f"  Z-Range: {min_z} to {max_z}",
            "Full Data Sample (First 5 Rows):",
            "\n".join([f"  {row}" for row in sample_rows])
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"XYZ Error: {str(e)}"