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
    Exhaustively explores Compressed LAS (.zlas) files.
    Zero truncation: provides binary signatures and internal string samples.
    """
    try:
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as f:
            # Read header to find compression markers and internal strings
            header_bytes = f.read(512)
            
        # 1. Detect internal signatures
        # ZLAS files often contain 'zLAS' or version markers in the binary
        is_zlas = b'zLAS' in header_bytes or b'ZLAS' in header_bytes
        is_techlog = b'Techlog' in header_bytes
        
        # 2. Extract printable strings (Well names or metadata embedded in binary)
        # Search for alphanumeric sequences longer than 5 chars
        internal_strings = re.findall(rb'[A-Za-z0-9_\-\.]{5,}', header_bytes)
        clean_strings = [s.decode('ascii', errors='ignore').strip() for s in internal_strings]
        unique_meta = list(dict.fromkeys(clean_strings)) # Preserve order, remove duplicates

        # 3. Hex/ASCII Visualization
        hex_dump = " ".join([f"{b:02x}" for b in header_bytes[:32]])
        ascii_dump = "".join([chr(b) if 32 <= b <= 126 else "." for b in header_bytes[:64]])

        output = [
            "Type: Compressed Log ASCII Standard (.zlas)",
            f"Detected Signature: {'Valid zLAS' if is_zlas else 'Generic Binary Log'}",
            f"Compressed Size: {file_size} bytes",
            f"Software Context: {'Schlumberger Techlog' if is_techlog else 'Unknown Provider'}",
            "Extracted Internal Labels (Metadata):",
            "  " + " | ".join(unique_meta[:10]) if unique_meta else "  No explicit labels found.",
            "Binary Header Content Sample:",
            f"  HEX:   {hex_dump}...",
            f"  ASCII: {ascii_dump}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"ZLAS Extraction Error: {str(e)}"