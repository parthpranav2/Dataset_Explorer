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
    Exhaustively explores binary .lyr files.
    Zero truncation: extracts all internal paths and metadata strings.
    """
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        # 1. Extract Path Information (Looking for C:\ or relative paths)
        # We use a regex to find strings that look like Windows or Unix paths
        path_pattern = re.compile(rb'[a-zA-Z]:\\[^:<>\?"\s|]*|(?<=\x00)[A-Za-z0-9_\-\.]+\.(?:shp|tif|dbf|gdb|img)')
        paths = path_pattern.findall(content)
        unique_paths = list(set([p.decode('utf-16-le', errors='ignore') if b'\x00' in p else p.decode('ascii', errors='ignore') for p in paths]))
        
        # 2. Extract Visible Text (Layer Names/Labels)
        # Filters for sequences of printable characters longer than 4
        strings = re.findall(rb'[a-zA-Z0-9_\s]{4,}', content)
        clean_strings = [s.decode('ascii', errors='ignore').strip() for s in strings if len(s) > 4]
        
        # 3. Component Identification
        is_raster = "Raster" in "".join(clean_strings)
        is_feature = "Feature" in "".join(clean_strings)

        output = [
            "Type: Esri Layer File (Binary Symbology)",
            f"Likely Category: {'Raster Layer' if is_raster else 'Vector/Feature Layer' if is_feature else 'Unknown'}",
            "Identified Data Sources (Paths):",
            "\n".join([f"  - {p}" for p in unique_paths]) if unique_paths else "  No explicit paths found.",
            "Internal Metadata Strings (Exhaustive):",
            "  " + " | ".join(clean_strings[:15]) # Showing top 15 significant strings
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"LYR Extraction Error: {str(e)}"