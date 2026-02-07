import sys
import os
import numpy as np

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores HGT (SRTM) files.
    Calculates resolution from file size and extracts elevation statistics.
    """
    try:
        file_size = os.path.getsize(file_path)
        # SRTM-3 is 1201x1201 (2.8MB), SRTM-1 is 3601x3601 (25.9MB)
        if file_size == 12967202 * 2: # 1-arc-second
            dim = 3601
            res = "1-arc-second (~30m)"
        elif file_size == 1442401 * 2: # 3-arc-second
            dim = 1201
            res = "3-arc-second (~90m)"
        else:
            return f"Error: Unexpected file size ({file_size} bytes) for HGT format."

        # Read binary data (Big-Endian 16-bit signed integers)
        data = np.fromfile(file_path, dtype='>i2').reshape((dim, dim))
        
        # Filter out voids (-32768)
        valid_data = data[data != -32768]
        
        # Filename parsing for coordinates (e.g., N23E079.hgt)
        fname = os.path.basename(file_path).upper()
        lat = fname[0:3]
        lon = fname[3:7]

        output = [
            "Type: SRTM Digital Elevation Model (.hgt)",
            f"Resolution: {res}",
            f"Grid Dimensions: {dim} x {dim}",
            f"Reference Corner (Lower-Left): {lat}, {lon}",
            "Elevation Statistics (Excluding Voids):",
            f"  Min Elevation: {np.min(valid_data)}m",
            f"  Max Elevation: {np.max(valid_data)}m",
            f"  Mean Elevation: {np.mean(valid_data):.2f}m",
            f"  Void Count (-32768): {np.sum(data == -32768)}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"HGT Error: {str(e)}"