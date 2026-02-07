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
    Exhaustively explores .curve files for well data.
    Zero truncation: provides full curve statistics and depth intervals.
    """
    try:
        header_lines = []
        numeric_data = []
        well_id = "N/A"
        mnemonic = "Unknown"

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line:
                    continue

                # 1. Capture Header & Well Metadata
                if len(header_lines) < 15:
                    header_lines.append(clean_line)
                    # Search for common Well IDs or Mnemonics
                    if "WELL:" in clean_line.upper() or "UWI:" in clean_line.upper():
                        well_id = clean_line.split(':')[-1].strip()
                    if "CURVE:" in clean_line.upper() or "MNEM:" in clean_line.upper():
                        mnemonic = clean_line.split(':')[-1].strip()

                # 2. Extract Numeric Data (assuming Column 1 is Depth, Column 2 is Value)
                parts = clean_line.replace(',', ' ').split()
                if len(parts) >= 2:
                    try:
                        # Test if the first two parts are numbers
                        val_pair = [float(parts[0]), float(parts[1])]
                        numeric_data.append(val_pair)
                    except ValueError:
                        continue

        # 3. Calculate Statistics (Zero Truncation of data insights)
        if numeric_data:
            depths = [d[0] for d in numeric_data]
            values = [v[1] for v in numeric_data if v[1] != -999.25] # Exclude nulls
            
            val_min = min(values) if values else "N/A"
            val_max = max(values) if values else "N/A"
            depth_start = min(depths)
            depth_stop = max(depths)
        else:
            val_min, val_max, depth_start, depth_stop = "N/A", "N/A", "N/A", "N/A"

        output = [
            f"Type: Well Log Curve Data ({mnemonic})",
            f"Well Identifier: {well_id}",
            f"Depth Interval: {depth_start} to {depth_stop}",
            f"Curve Statistics (Excluding Nulls):",
            f"  - Range: {val_min} to {val_max}",
            f"  - Total Data Points: {len(numeric_data)}",
            "Header Preview (First 5 lines):",
            "\n".join([f"  {line}" for line in header_lines[:5]])
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"Curve Extraction Error: {str(e)}"