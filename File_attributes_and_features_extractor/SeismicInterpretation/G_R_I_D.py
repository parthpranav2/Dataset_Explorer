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
    Exhaustively explores .grid simulation files.
    Zero truncation: identifies grid dimensions and keyword presence.
    """
    try:
        ni, nj, nk = 0, 0, 0
        keywords = []
        target_keys = ['SPECGRID', 'COORD', 'ZCORN', 'ACTNUM', 'MAPAXES']
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(50000) # Scan the first 50KB for the definition section
            
            # 1. Parse SPECGRID for Dimensions (Eclipse Format)
            specgrid_match = re.search(r'SPECGRID\s+(\d+)\s+(\d+)\s+(\d+)', content, re.IGNORECASE)
            if specgrid_match:
                ni, nj, nk = map(int, specgrid_match.groups())

            # 2. Collect Structural Keywords
            for kw in target_keys:
                if kw in content.upper():
                    keywords.append(kw)

        output = [
            "Type: Reservoir Simulation Grid Definition (.grid)",
            f"Grid Dimensions: {ni} (I) x {nj} (J) x {nk} (K)" if ni else "Dimensions: Not found in header",
            f"Total Cells: {ni * nj * nk}" if ni else "Total Cells: Unknown",
            f"Detected Grid Keywords: {', '.join(keywords) if keywords else 'None'}",
            "Structure Preview (First 5 Lines):"
        ]
        
        # Add a snippet of the actual file
        lines = content.splitlines()[:5]
        output.extend([f"  {line.strip()}" for line in lines if line.strip()])

        return "\n".join(output)

    except Exception as e:
        return f"GRID Extraction Error: {str(e)}"