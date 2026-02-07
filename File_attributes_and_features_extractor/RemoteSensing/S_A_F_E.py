import sys
import os
import xml.etree.ElementTree as ET

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .SAFE Sentinel product directories.
    Zero truncation: identifies satellite mission, processing level, and date.
    """
    try:
        # Resolve the manifest file path
        manifest_path = file_path
        if os.path.isdir(file_path):
            manifest_path = os.path.join(file_path, 'manifest.safe')
        
        if not os.path.exists(manifest_path):
            return "SAFE Error: manifest.safe not found in directory."

        # Parse the manifest XML
        tree = ET.parse(manifest_path)
        root = tree.getroot()
        
        # Simple extraction from the filename usually works for Sentinel products
        folder_name = os.path.basename(file_path.rstrip('/'))
        parts = folder_name.split('_')
        
        mission = parts[0] if len(parts) > 0 else "Unknown"
        level = parts[1] if len(parts) > 1 else "Unknown"
        sensing_time = parts[2] if len(parts) > 2 else "Unknown"

        output = [
            "Type: Sentinel Standard Archive Format (.SAFE)",
            f"Satellite Mission: {mission} (Sentinel-{'1' if 'S1' in mission else '2' if 'S2' in mission else '?'})",
            f"Processing Level: {level}",
            f"Acquisition Date: {sensing_time}",
            "Internal Components:",
            f"  - Manifest Source: {os.path.basename(manifest_path)}"
        ]
        
        # Check for granules/measurements subfolders
        content_types = []
        if os.path.isdir(file_path):
            for d in ['GRANULE', 'MEASUREMENT', 'AUX_DATA']:
                if os.path.exists(os.path.join(file_path, d)):
                    content_types.append(d)
        
        if content_types:
            output.append(f"  - Key Folders: {', '.join(content_types)}")

        return "\n".join(output)

    except Exception as e:
        return f"SAFE Extraction Error: {str(e)}"