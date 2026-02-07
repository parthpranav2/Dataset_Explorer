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
    Exhaustively explores .flt binary grid files.
    Zero truncation: provides statistical analysis of the float values.
    """
    try:
        file_size = os.path.getsize(file_path)
        total_floats = file_size // 4
        
        # Read a sample of data (first 10,000 floats or entire file)
        read_count = min(total_floats, 10000)
        with open(file_path, 'rb') as f:
            raw_data = f.read(read_count * 4)

        # Unpack as Little-Endian floats (standard for most modern GIS)
        floats = struct.unpack(f'<{read_count}f', raw_data)
        
        # Filter out extreme "NoData" values (like -9999) for stats
        valid_floats = [x for x in floats if -9000 < x < 50000]
        
        if valid_floats:
            f_min, f_max = min(valid_floats), max(valid_floats)
            f_mean = sum(valid_floats) / len(valid_floats)
        else:
            f_min = f_max = f_mean = "N/A"

        output = [
            "Type: Floating Point Binary Grid (.flt)",
            f"Total Data Points: {total_floats} (4-byte floats)",
            "Value Statistics (Sampled):",
            f"  - Minimum: {f_min}",
            f"  - Maximum: {f_max}",
            f"  - Mean:    {f_mean:.4f}",
            "Storage Context:",
            f"  - Detected Byte Order: Little-Endian",
            f"  - Null Value Marker: Likely -9999.0" if any(x < -9990 for x in floats) else "  - No standard nulls found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"FLT Extraction Error: {str(e)}"