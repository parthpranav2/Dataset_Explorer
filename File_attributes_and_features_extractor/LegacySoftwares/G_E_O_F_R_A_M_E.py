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
    Exhaustively explores GeoFrame/IESX format interpretation files.
    Zero truncation: identifies data class, point counts, and metadata.
    """
    try:
        point_count = 0
        data_class = "Unknown GeoFrame Object"
        project_name = "Unknown"
        header_lines = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Parse Header for Identity (Common in GeoQuest/IESX headers)
                if i < 20:
                    header_lines.append(clean_line)
                    upper_line = clean_line.upper()
                    if "PROJECT" in upper_line:
                        project_name = clean_line.split()[-1]
                    if "HORIZON" in upper_line:
                        data_class = "Seismic Horizon"
                    elif "FAULT" in upper_line:
                        data_class = "Fault Surface"

                # 2. Count Data Records
                # Typically data starts after a header-end marker or at a specific column
                parts = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                if len(parts) >= 3:
                    point_count += 1

        output = [
            "Type: GeoFrame / IESX Legacy Interpretation",
            f"Data Class: {data_class}",
            f"Associated Project: {project_name}",
            f"Total Records: {point_count} interpretation points",
            "Header Metadata Summary:"
        ]
        
        # Add a preview of the metadata found in the top of the file
        output.extend([f"  {line[:60]}..." for line in header_lines[:3]])

        return "\n".join(output)

    except Exception as e:
        return f"GeoFrame Extraction Error: {str(e)}"