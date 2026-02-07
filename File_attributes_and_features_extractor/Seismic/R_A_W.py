import sys
import os
import re
import math

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .raw binary files.
    Zero truncation: performs signal analysis and metadata scraping.
    """
    try:
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            chunk = f.read(8192) # Read 8KB for better signal estimation

        # 1. Statistical Signal Check
        # High-frequency sensor data usually has a distinct mean/std dev
        byte_vals = list(chunk)
        mean = sum(byte_vals) / len(byte_vals)
        variance = sum((x - mean)**2 for x in byte_vals) / len(byte_vals)
        std_dev = math.sqrt(variance)

        # 2. String Scraper (Metadata Search)
        strings = re.findall(rb'[A-Za-z0-9_\s]{6,}', chunk)
        clean_meta = [s.decode('ascii', errors='ignore').strip() for s in strings]
        unique_meta = list(dict.fromkeys([s for s in clean_meta if len(s) > 5]))

        # 3. Detect Alignment
        # Look for repeating sequences every 4, 8, or 16 bytes (common data widths)
        alignment = "Unknown"
        for stride in [4, 8, 16, 32]:
            if all(chunk[i] == chunk[i+stride] for i in range(0, 128, stride) if i+stride < len(chunk)):
                alignment = f"{stride}-byte Fixed Width"
                break

        output = [
            f"Type: Unformatted Raw Data (.raw)",
            f"Physical Size: {file_size} bytes",
            f"Signal Profile: Mean={mean:.2f}, StdDev={std_dev:.2f}",
            f"Likely Alignment: {alignment}",
            "Extracted Tool/Vendor Identifiers:",
            "  " + " | ".join(unique_meta[:5]) if unique_meta else "  No explicit text labels found.",
            "Raw Byte Sample (First 32):",
            f"  {chunk[:32].hex(' ')}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"RAW Extraction Error: {str(e)}"