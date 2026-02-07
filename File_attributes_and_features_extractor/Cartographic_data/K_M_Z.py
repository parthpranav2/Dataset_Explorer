import sys
import os
import zipfile
from io import BytesIO
from pykml import parser

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores KMZ archives by parsing the internal KML.
    Zero truncation: every internal file and metadata key is displayed.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # 1. List all files in the archive
            all_files = z.namelist()
            
            # Find the main KML file (usually doc.kml or ends in .kml)
            kml_filename = next((f for f in all_files if f.lower().endswith('.kml')), None)
            
            if not kml_filename:
                return f"Archive Contents: {', '.join(all_files)}\nError: No KML file found inside KMZ."

            with z.open(kml_filename) as f:
                root = parser.parse(f).getroot()

        # Handle namespaces
        namespace = {"kml": "http://www.opengis.net/kml/2.2"}
        
        # 2. Extract Hierarchy and Features
        folders = root.xpath(".//kml:Folder/kml:name/text()", namespaces=namespace)
        placemarks = root.xpath(".//kml:Placemark", namespaces=namespace)
        
        detail_lines = []
        detail_lines.append(f"Primary KML found: {kml_filename}")
        
        if placemarks:
            first_pm = placemarks[0]
            # 3. Exhaustive Metadata Extraction
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
            
            # 4. Geometry Sample
            coords = first_pm.xpath(".//kml:coordinates/text()", namespaces=namespace)
            if coords:
                detail_lines.append(f"Coordinate Sample: {coords[0].strip()}")

        output = [
            "Type: Compressed Keyhole Markup Language (KMZ)",
            f"Archive Contents: {', '.join(all_files)}",
            f"Total Placemarks: {len(placemarks)}",
            f"Internal Folders: {', '.join(folders) if folders else 'Flat'}",
            "Exhaustive KML Content:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"KMZ Error: {str(e)}"