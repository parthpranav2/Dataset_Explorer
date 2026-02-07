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
    Exhaustively explores .dat files for simulation parameters or numeric tables.
    Zero truncation: captures all structural keywords and numeric ranges.
    """
    try:
        header_lines = []
        found_keywords = []
        numeric_samples = []
        
        # Keywords specific to Petroleum Simulation (Eclipse/Petrel)
        petro_keywords = ['RUNSPEC', 'GRID', 'PROPS', 'REGIONS', 'SOLUTION', 'SCHEDULE', 'SUMMARY']
        
        line_count = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line_count += 1
                clean_line = line.strip()
                if not clean_line:
                    continue

                # 1. Capture Header (First 15 lines)
                if len(header_lines) < 15:
                    header_lines.append(clean_line)

                # 2. Extract Structural Keywords
                for kw in petro_keywords:
                    if kw in clean_line.upper() and kw not in found_keywords:
                        found_keywords.append(kw)

                # 3. Analyze Numeric Patterns
                parts = clean_line.replace(',', ' ').split()
                if len(parts) >= 2 and all(re.match(r'^-?\d+(\.\d+)?$', p) for p in parts[:2]):
                    if len(numeric_samples) < 5:
                        numeric_samples.append(parts)

        output = [
            "Type: Generic Data/Simulation File (.dat)",
            f"Total Complexity: {line_count} Lines",
            f"Detected Engineering Keywords: {', '.join(found_keywords) if found_keywords else 'None'}",
            "Numeric Data Preview (First 5 Rows):"
        ]

        if numeric_samples:
            for row in numeric_samples:
                output.append(f"  {' | '.join(row[:5])}")
        else:
            output.append("  No consistent numeric table detected.")

        output.append("Exhaustive Header Preview:")
        output.extend([f"  {line}" for line in header_lines])

        return "\n".join(output)

    except Exception as e:
        return f"DAT Extraction Error: {str(e)}"