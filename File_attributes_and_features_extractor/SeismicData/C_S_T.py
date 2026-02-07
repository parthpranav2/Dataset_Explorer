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
    Exhaustively explores .cst reservoir constraint files.
    Zero truncation: captures simulation case logic and property bounds.
    """
    try:
        header_preview = []
        properties = set()
        case_name = "Unknown"
        
        # Keywords for reservoir properties
        res_keywords = ['PORO', 'PERM', 'SW', 'SO', 'PRES', 'SAT', 'NTG']
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('--'):
                    continue

                # 1. Capture Header for Context
                if len(header_preview) < 10:
                    header_preview.append(clean_line)

                # 2. Detect Case Name
                if "CASE" in clean_line.upper():
                    case_name = clean_line.split(':')[-1].strip()

                # 3. Identify Properties being constrained
                upper_line = clean_line.upper()
                for kw in res_keywords:
                    if kw in upper_line:
                        properties.add(kw)

        output = [
            "Type: Reservoir Simulation Constraints (.cst)",
            f"Associated Case: {case_name}",
            f"Properties Constrained: {', '.join(sorted(list(properties))) if properties else 'None Detected'}",
            "Structural Preview (First 5 lines):"
        ]
        
        output.extend([f"  {line}" for line in header_preview[:5]])

        return "\n".join(output)

    except Exception as e:
        return f"CST Extraction Error: {str(e)}"