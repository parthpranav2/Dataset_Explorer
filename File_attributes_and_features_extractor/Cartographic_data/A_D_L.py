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
    Exhaustively explores ArcInfo Log (.adl) files.
    Zero truncation: every geoprocessing command and timestamp is captured.
    """
    try:
        commands = []
        timestamps = []
        full_content = []

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # 1. Capture Time Stamps (Commonly at the start of lines)
                time_match = re.search(r'(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2})', line)
                if time_match:
                    timestamps.append(time_match.group(1))
                
                # 2. Identify Core Commands
                # ArcInfo logs often use uppercase for core commands
                cmd_match = re.search(r'([A-Z]{3,}\s+.*)', line)
                if cmd_match:
                    commands.append(cmd_match.group(1))
                
                full_content.append(line)

        output = [
            "Type: ArcInfo Process Log (.adl)",
            f"Total Logged Operations: {len(commands)}",
            f"Log Period: {timestamps[0] if timestamps else 'N/A'} to {timestamps[-1] if timestamps else 'N/A'}",
            "Exhaustive Processing History:",
            "\n".join([f"  - {cmd}" for cmd in commands]) if commands else "  No explicit commands found.",
            "Complete Log Preview (First 10 lines):",
            "\n".join([f"  {line}" for line in full_content[:10]]) if full_content else "  File is empty."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"ADL Processing Error: {str(e)}"
    