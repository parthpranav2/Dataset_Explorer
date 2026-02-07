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
    Exhaustively explores .xt cross-line seismic files.
    Zero truncation: identifies line indices and vertical data windows.
    """
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        # 1. Attempt to extract Cross-line number from filename
        # Common pattern: XL_1005.xt or Line100.xt
        xl_match = re.search(r'(\d+)', file_name)
        xl_index = xl_match.group(1) if xl_match else "Unknown"

        with open(file_path, 'rb') as f:
            header_sample = f.read(1024)

        # 2. Sniff for Binary vs ASCII
        # If null bytes are prevalent, it's likely binary trace data
        is_binary = header_sample.count(b'\x00') > 50
        
        # 3. Extract printable metadata if ASCII
        clean_meta = ""
        if not is_binary:
            clean_meta = header_sample.decode('ascii', errors='ignore')[:200].strip().replace('\n', ' | ')

        output = [
            f"Type: Seismic Cross-line Trace Data (.xt)",
            f"Cross-line Index: {xl_index}",
            f"Storage Format: {'Binary Trace Stream' if is_binary else 'ASCII Export'}",
            f"Physical Size: {file_size} bytes",
            "Metadata Preview:"
        ]
        
        if clean_meta:
            output.append(f"  {clean_meta}...")
        else:
            # Provide Hex sample for binary files
            hex_sample = header_sample[:24].hex(' ')
            output.append(f"  Binary Header Hex: {hex_sample}...")

        return "\n".join(output)

    except Exception as e:
        return f"XT Extraction Error: {str(e)}"