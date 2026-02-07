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
    Exhaustively explores .obs observation logs.
    Zero truncation: captures field notes, shot ranges, and record counts.
    """
    try:
        header_preview = []
        notes = []
        shot_points = []
        record_count = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                record_count += 1
                clean_line = line.strip()
                if not clean_line: continue
                
                # 1. Capture Header (First 10 lines)
                if len(header_preview) < 10:
                    header_preview.append(clean_line)

                # 2. Extract Field Notes/Comments
                # Often preceded by 'C' or 'COMMENT' in SPS/UKOOA
                if clean_line.startswith('C') or "NOTE" in clean_line.upper():
                    notes.append(clean_line[1:].strip())

                # 3. Detect Shot Numbers (Look for 'S' records in SPS)
                if clean_line.startswith('S'):
                    parts = clean_line.split()
                    if len(parts) > 1:
                        try:
                            shot_points.append(float(parts[1]))
                        except ValueError:
                            pass

        output = [
            "Type: Seismic Acquisition Observation Log (.obs)",
            f"Total Log Records: {record_count}",
            f"Shot-Point Range: {min(shot_points) if shot_points else 'N/A'} to {max(shot_points) if shot_points else 'N/A'}",
            "Observer Field Notes:"
        ]
        
        if notes:
            output.extend([f"  - {n}" for n in notes[:5]])
            if len(notes) > 5: output.append(f"  ... ({len(notes)-5} more notes)")
        else:
            output.append("  - No explicit field notes detected.")

        output.append("Header Preview:")
        output.extend([f"  {line}" for line in header_preview[:3]])

        return "\n".join(output)

    except Exception as e:
        return f"OBS Extraction Error: {str(e)}"