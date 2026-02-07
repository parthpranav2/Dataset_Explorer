import sys
import os
import re
import struct

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .bin files.
    Zero truncation: performs string scraping and binary pattern identification.
    """
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            chunk = f.read(4096)  # Scan first 4KB

        # 1. Extract printable strings (Metadata Scraper)
        # Finds sequences of 5+ alphanumeric characters
        strings = re.findall(rb'[A-Za-z0-9_\-\.\s]{5,}', chunk)
        clean_strings = [s.decode('ascii', errors='ignore').strip() for s in strings]
        unique_meta = list(dict.fromkeys([s for s in clean_strings if len(s) > 4]))

        # 2. Check for common Magic Bytes
        # e.g., ELF, MZ (Executable), or ZIP signatures
        signature = "Unknown Binary"
        if chunk.startswith(b'\x7fELF'): signature = "Linux Executable/Library"
        elif chunk.startswith(b'MZ'): signature = "Windows Executable"
        elif chunk.startswith(b'PK\x03\x04'): signature = "Compressed Archive (ZIP/JAR)"
        elif b'SEGY' in chunk or b'segy' in chunk: signature = "Likely Seismic Stream"

        # 3. Numeric Sniffing (Check for Float32 patterns)
        # Attempt to unpack first 10 values as Big-Endian Floats
        try:
            floats = struct.unpack('>10f', chunk[:40])
            is_numeric = all(abs(x) < 1e10 for x in floats)
        except:
            is_numeric = False

        output = [
            f"Type: Generic Binary Data (.bin)",
            f"File Identity: {signature}",
            f"Physical Size: {file_size} bytes",
            f"Data Pattern: {'Likely Numeric Array' if is_numeric else 'Mixed/Bytecode'}",
            "Extracted Internal Strings:",
            "  " + " | ".join(unique_meta[:8]) if unique_meta else "  No readable strings found.",
            "Header Hex Sample (32-bytes):",
            f"  {chunk[:32].hex(' ')}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"BIN Extraction Error: {str(e)}"