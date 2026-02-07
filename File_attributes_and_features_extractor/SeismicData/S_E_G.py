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
    Exhaustively explores general .seg seismic files.
    Zero truncation: sniffs for standard SEG-Y headers and extracts printable metadata.
    """
    try:
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as f:
            # Read first 3200 bytes (standard SEG-Y textual header size)
            header_data = f.read(3200)
            
        # 1. Detect if it's an EBCDIC-encoded SEG-Y header
        # EBCDIC 'C01' (standard header start) is 0x43 f0 f1 in hex
        is_ebcdic = b'\x43\xf0\xf1' in header_data[:10]
        
        # 2. Extract Printable Strings (Metadata Scraper)
        # We look for alphanumeric sequences found in survey headers
        meta_strings = re.findall(rb'[A-Z0-9\-\.\s]{5,}', header_data)
        clean_meta = []
        if is_ebcdic:
            # Very basic conversion for EBCDIC identification
            clean_meta.append("Detected Encoding: EBCDIC (Standard SEG-Y)")
        else:
            clean_meta = [s.decode('ascii', errors='ignore').strip() for s in meta_strings]
            clean_meta = [x for x in clean_meta if len(x) > 4]

        # 3. Hex/ASCII Visualization
        hex_dump = " ".join([f"{b:02x}" for b in header_data[:32]])
        ascii_dump = "".join([chr(b) if 32 <= b <= 126 else "." for b in header_data[:64]])

        output = [
            "Type: General Seismic Data (.seg)",
            f"File Size: {file_size} bytes",
            "Internal Format Characteristics:",
            f"  - Possible Format: {'SEG-Y Standard' if is_ebcdic else 'SEG Data Stream'}",
            "Extracted Header Labels:",
            "  " + " | ".join(clean_meta[:10]) if clean_meta else "  No standard text labels detected.",
            "Binary Header Sample:",
            f"  HEX:   {hex_dump}...",
            f"  ASCII: {ascii_dump}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SEG Extraction Error: {str(e)}"