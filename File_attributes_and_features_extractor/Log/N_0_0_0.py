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
    Full-proof extractor for sequential segments (.000, .001, etc.).
    Identifies binary signatures and multi-part data relationships.
    """
    try:
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        # Separate the name from the numeric extension
        base_name, extension = os.path.splitext(file_name)
        
        # 1. SEQUENCE ANALYSIS
        # Look for sibling segments like .001, .002 in the same directory
        siblings = []
        if os.path.exists(file_dir):
            all_files = os.listdir(file_dir)
            siblings = sorted([f for f in all_files if f.startswith(base_name) and re.search(r'\.\d{3}$', f)])

        # 2. BINARY SIGNATURE SNIFFING
        with open(file_path, 'rb') as f:
            header = f.read(512)
            
        # Common signatures found in Petroleum/GIS datasets
        magic_map = {
            b'PK\x03\x04': "ZIP / Office Open XML (Compressed)",
            b'\x1f\x8b': "GZIP / Compressed Data",
            b'%PDF-': "PDF Document (Segmented)",
            b'\x7fELF': "Linux Executable/Object",
            b'RIFF': "Multimedia Container (WAV/AVI)",
            b'BM': "Bitmap Image Data",
            b'\xff\xd8\xff': "JPEG Image Data",
            b'S-57': "IHO S-57 Nautical Chart Data",
            b'\x00\x00\x01\xba': "MPEG Video Segment"
        }
        
        detected_type = "Generic Binary Segment"
        for magic, label in magic_map.items():
            if header.startswith(magic):
                detected_type = label
                break

        # 3. HEX/ASCII DUMP FOR MANUAL AUDIT
        # First 32 bytes in Hex
        hex_dump = " ".join([f"{b:02x}" for b in header[:32]])
        # First 64 bytes in printable ASCII
        ascii_dump = "".join([chr(b) if 32 <= b <= 126 else "." for b in header[:64]])

        output = [
            f"Type: Sequential Data Segment ({extension})",
            f"Detected Internal Format: {detected_type}",
            f"Segment Size: {os.path.getsize(file_path)} bytes",
            "Multi-part Sequence Context:",
            f"  - Part of sequence: {base_name}.[000...999]",
            f"  - Total segments detected in folder: {len(siblings)}",
            "Binary Header Content Sample:",
            f"  HEX:   {hex_dump}...",
            f"  ASCII: {ascii_dump}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"Segment Processor Error: {str(e)}"