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
    Exhaustively explores .log files for well data or process reports.
    Zero truncation: captures timeline, metadata keywords, and header content.
    """
    try:
        header_preview = []
        timestamps = []
        keywords = {}
        target_keys = ['well', 'rig', 'operator', 'error', 'version', 'field']
        line_count = 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line_count += 1
                clean_line = line.strip()
                if not clean_line:
                    continue

                # 1. Capture Header Preview (First 10 non-empty lines)
                if len(header_preview) < 10:
                    header_preview.append(clean_line)

                # 2. Extract Timestamps (Standard ISO, SQL, or Log formats)
                time_match = re.search(r'(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{2,4})\s(\d{2}:\d{2}:\d{2})', clean_line)
                if time_match:
                    timestamps.append(time_match.group(0))

                # 3. Keyword Search for Metadata
                lower_line = clean_line.lower()
                for key in target_keys:
                    if key in lower_line and key not in keywords:
                        # Extract the rest of the line as the value
                        val = clean_line.split(':')[-1].strip() if ':' in clean_line else clean_line
                        keywords[key] = val

        # 4. Determine if Numeric Log
        is_numeric = False
        if header_preview:
            sample = header_preview[-1].replace(',', ' ').split()
            if sample and all(re.match(r'^-?\d+(\.\d+)?$', p) for p in sample[:3]):
                is_numeric = True

        output = [
            f"Type: {'Numeric Data' if is_numeric else 'Process/Narrative'} Log",
            f"Total Entries: {line_count} lines",
            f"Log Period: {timestamps[0] if timestamps else 'N/A'} to {timestamps[-1] if timestamps else 'N/A'}",
            "Identified Metadata:"
        ]
        
        if keywords:
            for k, v in keywords.items():
                output.append(f"  - {k.capitalize()}: {v}")
        else:
            output.append("  - No standard metadata keys found.")

        output.append("Header Content Preview:")
        output.extend([f"  {line}" for line in header_preview])

        return "\n".join(output)

    except Exception as e:
        return f"Log Extraction Error: {str(e)}"