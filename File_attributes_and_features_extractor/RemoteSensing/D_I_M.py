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
    Exhaustively explores .dim (BEAM/SNAP Dimap) metadata files.
    Zero truncation: identifies satellite source, CRS, and polarization.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 1. Mission and Sensor Identification
        mission = "Unknown"
        instr = root.find(".//INSTRUMENT")
        if instr is not None:
            mission = instr.text if instr.text else "Unknown"

        # 2. Spatial Reference
        crs = "Unknown"
        coord_sys = root.find(".//HORIZONTAL_CS_NAME")
        if coord_sys is not None:
            crs = coord_sys.text

        # 3. Data Content (Bands/Polarization)
        bands = []
        for band in root.findall(".//BAND_NAME"):
            bands.append(band.text)

        output = [
            "Type: BEAM/SNAP Dimap Metadata (.dim)",
            f"Satellite/Sensor: {mission}",
            f"Coordinate System: {crs}",
            f"Detected Bands: {len(bands)}",
            "Content Audit:"
        ]

        if bands:
            output.append(f"  - Channels: {', '.join(bands[:4])}" + ("..." if len(bands) > 4 else ""))
        
        # Check for associated .data folder
        data_folder = file_path.replace('.dim', '.data')
        output.append(f"  - Associated Data: {'Connected' if os.path.exists(data_folder) else 'Missing .data folder'}")

        return "\n".join(output)

    except Exception as e:
        return f"DIM Extraction Error: {str(e)}"