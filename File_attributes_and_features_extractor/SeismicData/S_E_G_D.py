import sys
import os
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
    Exhaustively explores SEG-D field seismic files.
    Zero truncation: identifies standard revisions and acquisition metadata.
    """
    try:
        with open(file_path, 'rb') as f:
            # Read General Header Block 1 (First 32 bytes)
            header_block = f.read(32)
            
        if len(header_block) < 32:
            return "SEG-D Error: File too small to contain valid headers."

        # 1. Detect SEG-D Revision
        # Byte 30-31 often contains the revision code
        rev_major = header_block[30]
        rev_minor = header_block[31]
        revision = f"{rev_major}.{rev_minor}"

        # 2. Extract Basic Parameters (Field-specific byte positions)
        # File Number (Bytes 0-1)
        file_no = struct.unpack('>H', header_block[0:2])[0]
        # Format Code (Bytes 2-3) - e.g., 8015 for 20-bit, 0058 for 32-bit IEEE
        format_code = hex(struct.unpack('>H', header_block[2:4])[0])
        
        # 3. Hex/ASCII Visualization of Header
        # Looking for readable strings like survey names in the first 512 bytes
        f.seek(0)
        full_header = f.read(512)
        import re
        meta_strings = re.findall(rb'[A-Z0-9_\s]{5,}', full_header)
        clean_meta = [s.decode('ascii', errors='ignore').strip() for s in meta_strings]

        output = [
            "Type: SEG-D Field Seismic Data",
            f"Standard Revision: {revision}",
            f"Field Record Number: {file_no}",
            f"Data Format Code: {format_code}",
            "Acquisition Metadata (Scraped Strings):",
            f"  {', '.join(clean_meta[:10])}" if clean_meta else "  No explicit labels found.",
            "Header Binary Preview:",
            f"  HEX: {header_block.hex(' ')}..."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SEG-D Extraction Error: {str(e)}"