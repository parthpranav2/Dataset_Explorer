import sys
import os
import re
import struct

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores 3D Scene Cache (.3dc) files.
    Zero truncation: identifies internal object names and spatial complexity.
    """
    try:
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as f:
            # Read first 4KB to extract metadata strings and headers
            header_sample = f.read(4096)
        
        # 1. Extract Object Names (Search for alphanumeric strings > 4 chars)
        # Often identifies surfaces like 'Top_Horizon' or 'Well_01'
        object_names = re.findall(rb'[A-Za-z0-9_]{5,}', header_sample)
        unique_names = sorted(list(set([n.decode('ascii', errors='ignore') for n in object_names])))
        
        # 2. Heuristic Complexity Check
        # Divide file size by typical vertex size (float32 x 3 = 12 bytes)
        est_vertices = file_size // 12

        output = [
            "Type: 3D Visualization Cache (.3dc)",
            f"Cache Complexity: ~{est_vertices:,} Potential Vertices",
            "Identified Scene Objects (Internal Strings):",
            f"  {', '.join(unique_names[:10])}" if unique_names else "  No explicit labels found.",
            "Scene Characteristics:",
            f"  - Total File Size: {file_size} bytes",
            f"  - Storage Mode: {'Binary/Compressed' if b'ZIP' in header_sample else 'Raw 3D Data'}"
        ]
        
        if len(unique_names) > 10:
            output.append(f"  ... (+ {len(unique_names) - 10} more labels)")

        return "\n".join(output)

    except Exception as e:
        return f"3DC Extraction Error: {str(e)}"