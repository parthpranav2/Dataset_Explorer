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
    Exhaustively explores WITS drilling data files.
    Zero truncation: identifies all record types and provides raw packet samples.
    """
    try:
        record_map = {
            "01": "General Time-Based",
            "02": "Drilling Depth-Based",
            "07": "MWD Formation Evaluation",
            "08": "MWD Drilling Mechanics",
            "11": "Mud Tank Volumes"
        }
        
        detected_records = set()
        raw_samples = []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read first 100 lines to identify the stream pattern
            lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # WITS items usually look like '0105123.45' 
                # (Record 01, Item 05, Value 123.45)
                match = re.match(r'^(\d{2})\d{2}.*', line)
                if match:
                    rec_id = match.group(1)
                    detected_records.add(rec_id)
                    if len(raw_samples) < 5:
                        raw_samples.append(line)

        # Map IDs to names
        record_names = [f"{rid} ({record_map.get(rid, 'Custom Record')})" for rid in sorted(list(detected_records))]

        output = [
            "Type: Wellsite Information Transfer Specification (WITS)",
            "Detected WITS Records:",
            "\n".join([f"  - {name}" for name in record_names]) if record_names else "  No standard WITS records identified.",
            "Raw Data Packet Preview:",
            "\n".join([f"  {s}" for s in raw_samples]) if raw_samples else "  Empty data stream."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"WITS Extraction Error: {str(e)}"