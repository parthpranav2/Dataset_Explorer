import sys
import os
import zipfile
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
    Exhaustively explores QGZ project files.
    Zero truncation: every layer name, data source path, and project setting is extracted.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # Find the internal .qgs XML file
            qgs_filename = [f for f in z.namelist() if f.endswith('.qgs')][0]
            with z.open(qgs_filename) as f:
                tree = ET.parse(f)
                root = tree.getroot()

        # 1. Project-wide Metadata
        title_node = root.find('.//title')
        project_title = title_node.text if title_node is not None else "Untitled Project"
        
        crs_node = root.find('.//projectCrs/spatialrefsys/authid')
        project_crs = crs_node.text if crs_node is not None else "Not Set"

        # 2. Layer and Data Source Extraction (Complete List)
        layers_info = []
        for layer in root.findall('.//maplayer'):
            l_name = layer.find('layername').text if layer.find('layername') is not None else "Unknown"
            l_source = layer.find('datasource').text if layer.find('datasource') is not None else "No Source"
            l_type = layer.get('type', 'Unknown')
            layers_info.append(f"  - [{l_type.upper()}] {l_name}")
            layers_info.append(f"    Source: {l_source}")

        # 3. Layouts (Print Maps)
        layouts = [l.get('name') for l in root.findall('.//Layout')]

        output = [
            "Type: QGIS Zipped Project (.qgz)",
            f"Project Title: {project_title}",
            f"Project CRS: {project_crs}",
            "Complete Layer Inventory & Sources:",
            "\n".join(layers_info) if layers_info else "  No layers found in project.",
            "Print Layouts (Map Sheets):",
            f"  {', '.join(layouts) if layouts else 'None defined'}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"QGZ Extraction Error: {str(e)}"