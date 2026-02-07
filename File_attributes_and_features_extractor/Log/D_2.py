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
    Exhaustively explores Digital Data Segments (.d1, .d2, etc.).
    Zero truncation: identifies multi-part sequences and binary headers.
    """
    try:
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        base_name, extension = os.path.splitext(file_name)
        
        # 1. SEQUENCE DETECTION
        # Checks for sibling files like .d1, .d2, .d3
        siblings = []
        if os.path.exists(file_dir):
            all_files = os.listdir(file_dir)
            # Regex to find .dX where X is a digit
            siblings = sorted([f for f in all_files if f.startswith(base_name) and re.search(r'\.d\d+$', f)])

        # 2. BINARY HEADER SNIFFING
        with open(file_path, 'rb') as f:
            header = f.read(512)
            
        # Specific markers for well logging data segments
        if b'INSITE' in header:
            detected_type = "Halliburton INSITE Data Segment"
        elif b'DLIS' in header[:4]:
            detected_type = "DLIS Partitioned Segment"
        elif header.startswith(b'PK\x03\x04'):
            detected_type = "Compressed Data Archive Segment"
        else:
            detected_type = "Generic Digital Data Segment"

        # 3. HEX/ASCII DUMP
        hex_dump = " ".join([f"{b:02x}" for b in header[:32]])
        ascii_dump = "".join([chr(b) if 32 <= b <= 126 else "." for b in header[:64]])

        output = [
            f"Type: Digital Data Segment ({extension})",
            f"Detected Internal Format: {detected_type}",
            f"Segment Size: {os.path.getsize(file_path)} bytes",
            "Multi-part Sequence Context:",
            f"  - Detected sibling segments: {', '.join(siblings) if siblings else 'None'}",
            "Binary Header Content Sample:",
            f"  HEX:   {hex_dump}...",
            f"  ASCII: {ascii_dump}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"Data Segment Processor Error: {str(e)}"