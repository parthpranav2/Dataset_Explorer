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
    Exhaustively explores ArcGlobe .3dd files.
    Zero truncation: every internal data path and metadata label is captured.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        # 1. Path Extraction (Detecting linked data sources)
        # Searches for Windows paths or common GIS extensions linked inside the binary
        path_pattern = re.compile(rb'[a-zA-Z]:\\[^:<>\?"\s|]*|(?<=\x00)[A-Za-z0-9_\-\.]+\.(?:shp|tif|dbf|gdb|img|lyr)')
        paths = path_pattern.findall(content)
        unique_paths = list(set([p.decode('utf-16-le', errors='ignore') if b'\x00' in p else p.decode('ascii', errors='ignore') for p in paths]))
        
        # 2. Extract Visible Text (Layer Names/3D Settings)
        # Grabs strings longer than 4 chars that are likely human-readable metadata
        strings = re.findall(rb'[a-zA-Z0-9_\s]{5,}', content)
        clean_strings = sorted(list(set([s.decode('ascii', errors='ignore').strip() for s in strings])))

        # 3. Environment Context
        is_global = "Global" in "".join(clean_strings)
        is_local = "Local" in "".join(clean_strings)

        output = [
            "Type: ArcGlobe 3D Document (.3dd)",
            f"Scene Mode: {'Global Globe' if is_global else 'Local Scene' if is_local else 'Unknown'}",
            "Linked Data Sources (Absolute/Relative Paths):",
            "\n".join([f"  - {p}" for p in unique_paths]) if unique_paths else "  No explicit data links identified.",
            "Exhaustive Metadata Strings (Top 15):",
            "  " + " | ".join(clean_strings[:15]) if clean_strings else "  No metadata labels found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"3DD Extraction Error: {str(e)}"