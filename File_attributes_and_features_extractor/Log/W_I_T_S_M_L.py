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
    Exhaustively explores WITSML drilling data files.
    Zero truncation: identifies the object type and core operational metadata.
    """
    try:
        # Standard XML parsing
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 1. Detect WITSML Version and Object Type
        # Tags usually look like {http://www.witsml.org/schemas/131}wells
        namespace = ""
        if '}' in root.tag:
            namespace = root.tag.split('}')[0] + '}'
            obj_type = root.tag.split('}')[1]
        else:
            obj_type = root.tag

        # 2. Extract Key Identity Data (using wildcards for namespaces)
        well_name = root.findtext('.//{*}nameWell') or root.findtext('.//{*}name') or "Unknown"
        wellbore_name = root.findtext('.//{*}nameWellbore') or "N/A"
        
        # 3. Component Inventory (Count sub-objects like logs or trajectories)
        child_count = len(root.findall(f"./{namespace}*"))
        
        # 4. Extract Timing and Versioning
        version = root.get('version', 'Unknown')
        created = root.findtext('.//{*}creationDate') or "N/A"

        output = [
            f"Type: WITSML Drilling Data ({obj_type.capitalize()})",
            f"WITSML Schema Version: {version}",
            f"Entity Hierarchy: Well: {well_name} | Wellbore: {wellbore_name}",
            f"Data Summary:",
            f"  - Total sub-objects: {child_count}",
            f"  - Document Created: {created}",
            f"  - Namespace: {namespace.strip('{}')}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"WITSML Extraction Error: {str(e)}"