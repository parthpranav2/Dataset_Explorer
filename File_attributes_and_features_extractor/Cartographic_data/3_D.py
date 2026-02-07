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
    Exhaustively explores 3D coordinate and grid files.
    Zero truncation: provides full volumetric bounds and point samples.
    """
    try:
        count = 0
        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
        sample_rows = []

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                # Clean and split the line (handles space, comma, or tab)
                parts = line.replace(',', ' ').split()
                
                # Looking for X Y Z structure
                if len(parts) >= 3:
                    try:
                        x, y, z = map(float, parts[:3])
                        min_x, max_x = min(min_x, x), max(max_x, x)
                        min_y, max_y = min(min_y, y), max(max_y, y)
                        min_z, max_z = min(min_z, z), max(max_z, z)
                        count += 1
                        
                        if len(sample_rows) < 5:
                            sample_rows.append(line.strip())
                    except ValueError:
                        continue # Skip headers

        output = [
            "Type: 3D Spatial Data (Point Cloud/Grid)",
            f"Total Vertices: {count}",
            "Volumetric Extent:",
            f"  X (Easting): {min_x} to {max_x}",
            f"  Y (Northing): {min_y} to {max_y}",
            f"  Z (Depth/Elev): {min_z} to {max_z}",
            "Raw Coordinate Samples (First 5):",
            "\n".join([f"  {row}" for row in sample_rows]) if sample_rows else "  No valid numeric data found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"3D Extraction Error: {str(e)}"