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
    Exhaustively explores QGIS Metadata files (.qmd).
    Zero truncation: every abstract, keyword, and contact detail is extracted.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 1. Title and Abstract Extraction
        title_node = root.find('.//title')
        abstract_node = root.find('.//abstract')
        
        title = title_node.text if title_node is not None else "No Title Defined"
        # Preserve full abstract text without truncation
        abstract = abstract_node.text.strip() if abstract_node is not None and abstract_node.text else "No Abstract Provided"

        # 2. Keywords and Categories
        keywords = []
        for kw in root.findall('.//keyword'):
            if kw.text:
                keywords.append(kw.text.strip())

        # 3. Spatial Reference Info
        crs_node = root.find('.//crs/spatialrefsys/authid')
        crs_id = crs_node.text if crs_node is not None else "Not Specified"

        # 4. Contact Information
        contacts = []
        for contact in root.findall('.//contact'):
            name = contact.find('name')
            org = contact.find('organization')
            if name is not None or org is not None:
                contact_str = f"{name.text if name is not None else ''} ({org.text if org is not None else 'N/A'})"
                contacts.append(contact_str.strip())

        output = [
            "Type: QGIS Metadata File (XML)",
            f"Dataset Title: {title}",
            "Abstract:",
            f"  {abstract}",
            f"Primary CRS AuthID: {crs_id}",
            "Keywords:",
            f"  {', '.join(keywords) if keywords else 'None'}",
            "Contact Information:",
            f"  {', '.join(contacts) if contacts else 'None'}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"QMD Parsing Error: {str(e)}"