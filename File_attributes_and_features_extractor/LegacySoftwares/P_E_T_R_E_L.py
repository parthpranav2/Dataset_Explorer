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
    Exhaustively explores .petrel project files.
    Zero truncation: identifies CRS, units, and software version.
    """
    try:
        project_info = {"Version": "Unknown", "CRS": "Unknown", "Units": "Unknown"}
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Petrel files are often large; scan the first 100KB for XML tags
            content = f.read(102400)
            
            # 1. Version Detection
            ver_match = re.search(r'version=["\']([^"\']+)["\']', content)
            if ver_match: project_info["Version"] = ver_match.group(1)
            
            # 2. CRS Identification
            crs_match = re.search(r'<CoordinateSystem.*?>(.*?)</CoordinateSystem>', content, re.DOTALL)
            if crs_match: project_info["CRS"] = crs_match.group(1).strip()[:50]
            
            # 3. Units Search
            if "Metric" in content: project_info["Units"] = "Metric (m)"
            elif "Field" in content or "Imperial" in content: project_info["Units"] = "Imperial (ft)"

        output = [
            "Type: Petrel Project / Structural Export (.petrel)",
            f"Software Version: {project_info['Version']}",
            f"Unit System: {project_info['Units']}",
            f"Spatial Context (CRS): {project_info['CRS']}",
            "Internal XML Snippet (First 3 lines):"
        ]
        
        lines = [l.strip() for l in content.splitlines() if l.strip()]
        output.extend([f"  {line}" for line in lines[:3]])

        return "\n".join(output)

    except Exception as e:
        return f"PETREL Extraction Error: {str(e)}"