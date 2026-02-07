import sys
import os
from pykml import parser
from lxml import etree

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up two levels (GIS -> File_attributes_and_features_extractor -> Project Root)
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores KML files to extract hierarchy and extended metadata.
    No truncation: every folder and data key is displayed in full.
    """
    try:
        with open(file_path, 'rb') as f:
            root = parser.parse(f).getroot()

        # Handle namespaces for XML searching
        namespace = {"kml": "http://www.opengis.net/kml/2.2"}
        
        # 1. Map Hierarchy (Folders)
        folders = root.xpath(".//kml:Folder/kml:name/text()", namespaces=namespace)
        
        # 2. Extract Placemark Details
        placemarks = root.xpath(".//kml:Placemark", namespaces=namespace)
        count = len(placemarks)
        
        detail_lines = []
        if placemarks:
            # Analyze the first placemark for the schema
            first_pm = placemarks[0]
            pm_name = first_pm.find(".//kml:name", namespaces=namespace)
            detail_lines.append(f"Primary Feature Example: {pm_name.text if pm_name is not None else 'Unnamed'}")
            
            # 3. Exhaustive ExtendedData Schema (The Petroleum Metadata)
            extended_data = first_pm.xpath(".//kml:Data", namespaces=namespace)
            if extended_data:
                detail_lines.append("Full Metadata Schema (ExtendedData):")
                sample_parts = []
                for data in extended_data:
                    name = data.get("name")
                    val = data.find(".//kml:value", namespaces=namespace)
                    detail_lines.append(f"  {name}")
                    sample_parts.append(f"{name}: {val.text if val is not None else 'None'}")
                
                detail_lines.append(f"Full Sample Record: {' | '.join(sample_parts)}")
            
            # 4. Geometry Check
            coords = first_pm.xpath(".//kml:coordinates/text()", namespaces=namespace)
            if coords:
                detail_lines.append(f"Coordinate Sample: {coords[0].strip()}")

        output = [
            "Type: Keyhole Markup Language (KML/XML)",
            f"Total Features: {count}",
            f"Internal Folders: {', '.join(folders) if folders else 'None (Flat Structure)'}",
            "Exhaustive Feature Details:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"KML Error: {str(e)}"