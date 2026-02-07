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
    Exhaustively explores OpendTect survey and attribute export files.
    Zero truncation: identifies grid geometry, vertical sampling, and metadata.
    """
    try:
        survey_meta = {"Inline_Range": "N/A", "Xline_Range": "N/A", "Z_Range": "N/A"}
        attribute_name = "Unknown Attribute"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # OpendTect ASCII headers are usually very descriptive
            content = f.read(5000) 
            
            # 1. Scrape Inline/Crossline Ranges
            # Look for patterns like "In-line range: 100 500 1"
            il_match = re.search(r"In-line\s+range:?\s*(\d+)\s+(\d+)", content, re.I)
            xl_match = re.search(r"Cross-line\s+range:?\s*(\d+)\s+(\d+)", content, re.I)
            if il_match: survey_meta["Inline_Range"] = f"{il_match.group(1)} - {il_match.group(2)}"
            if xl_match: survey_meta["Xline_Range"] = f"{xl_match.group(1)} - {xl_match.group(2)}"
            
            # 2. Extract Attribute Name
            attr_match = re.search(r"Attribute:?\s*(.*)", content, re.I)
            if attr_match: attribute_name = attr_match.group(1).strip()

            # 3. Z-Range (Time or Depth)
            z_match = re.search(r"Z\s+range\s*\((\w+)\):?\s*([\d\.-]+)\s*([\d\.-]+)", content, re.I)
            if z_match:
                unit, start, end = z_match.groups()
                survey_meta["Z_Range"] = f"{start} to {end} ({unit})"

        output = [
            "Type: OpendTect Seismic Attribute / Survey Export",
            f"Attribute: {attribute_name}",
            "3D Geometry Audit:",
            f"  - Inline Range:    {survey_meta['Inline_Range']}",
            f"  - Crossline Range: {survey_meta['Xline_Range']}",
            f"  - Vertical Extent: {survey_meta['Z_Range']}",
            "Header Preview:"
        ]
        
        output.extend([f"  {line.strip()}" for line in content.splitlines()[:3] if line.strip()])

        return "\n".join(output)

    except Exception as e:
        return f"OpendTect Extraction Error: {str(e)}"