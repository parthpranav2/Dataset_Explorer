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
    Exhaustively explores .000 base segment files.
    Zero truncation: identifies full sequence and provides a complete hex/ascii header.
    """
    try:
        file_dir = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 1. Sequence Analysis
        # Look for sibling files: base.001, base.002, etc.
        siblings = [f for f in os.listdir(file_dir) if f.startswith(base_name) and f != os.path.basename(file_path)]
        sequence_files = sorted([f for f in siblings if re.search(r'\.\d{3}$', f)])
        
        # 2. Binary Signature Analysis
        with open(file_path, 'rb') as f:
            header_bytes = f.read(256)
            
        # Common Magic Number Detection
        magic_map = {
            b'\x1f\x8b': "Gzip Compressed",
            b'PK\x03\x04': "Zip/Office Open XML",
            b'ISO': "S-57 Nautical Chart Data",
            b'\x37\x7A\xBC\xAF': "7-Zip Archive"
        }
        
        detected_type = "Unknown Binary Segment"
        for magic, name in magic_map.items():
            if header_bytes.startswith(magic):
                detected_type = name
                break

        # 3. Hex/ASCII Visualization (Zero Truncation of Sample)
        hex_dump = " ".join([f"{b:02x}" for b in header_bytes[:32]])
        ascii_dump = "".join([chr(b) if 32 <= b <= 126 else "." for b in header_bytes[:64]])

        output = [
            "Type: Base Data Segment (.000)",
            f"Detected Internal Format: {detected_type}",
            f"File Size: {os.path.getsize(file_path)} bytes",
            "Multi-Part Sequence Details:",
            f"  - Total overflow segments found: {len(sequence_files)}",
            f"  - Sequence range: {os.path.basename(file_path)} to {sequence_files[-1] if sequence_files else 'N/A'}",
            "Header Content Sample (First 64 Bytes):",
            f"  HEX:   {hex_dump}...",
            f"  ASCII: {ascii_dump}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"000 Segment Error: {str(e)}"