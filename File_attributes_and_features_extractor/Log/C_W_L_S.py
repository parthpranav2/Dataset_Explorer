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
    Exhaustively explores CWLS Parameter (.cwls) files.
    Zero truncation: identifies all metadata mnemonics and operational values.
    """
    try:
        parameters = []
        well_info = {}
        line_count = 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line_count += 1
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue

                # 1. Detect Well Identification
                if any(x in clean_line.upper() for x in ['WELL', 'UWI', 'API']):
                    parts = clean_line.split(':')
                    if len(parts) >= 2:
                        key = parts[0].strip()
                        val = parts[1].strip().split()[0] # Get value before units/desc
                        well_info[key] = val

                # 2. Extract Structured Parameters
                # Pattern: MNEM.UNIT VALUE: DESCRIPTION
                param_match = re.match(r'^([A-Z0-9_]+)\.([^\s]*)\s+([^:]+):\s*(.*)$', clean_line)
                if param_match:
                    mnem, unit, val, desc = param_match.groups()
                    parameters.append(f"  - {mnem} ({desc.strip()}): {val.strip()} {unit.strip()}")

        output = [
            "Type: CWLS Log Parameter Metadata (.cwls)",
            f"Total Parameters Recorded: {len(parameters)}",
            "Identified Entity Context:"
        ]

        if well_info:
            for k, v in well_info.items():
                output.append(f"  {k}: {v}")
        else:
            output.append("  No explicit Well/UWI tags found.")

        output.append("Exhaustive Parameter List:")
        if parameters:
            output.extend(parameters)
        else:
            output.append("  No structured parameters detected.")

        return "\n".join(output)

    except Exception as e:
        return f"CWLS Extraction Error: {str(e)}"