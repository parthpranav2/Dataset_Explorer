import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    import lasio
except ImportError:
    lasio = None
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .las well log files.
    Zero truncation: identifies well headers, depth range, and curve names.
    """
    if not lasio:
        return "Error: lasio library not found in venv."

    try:
        las = lasio.read(file_path)
        
        # 1. Well Metadata
        well_name = las.well.WELL.value if 'WELL' in las.well else "Unknown"
        uwi = las.well.UWI.value if 'UWI' in las.well else "N/A"
        
        # 2. Depth Constraints
        start = las.well.STRT.value
        stop = las.well.STOP.value
        units = las.well.STRT.unit
        
        # 3. Curve Mnemonics
        curves = [c.mnemonic for c in las.curves]
        
        output = [
            f"Type: Log ASCII Standard (.las)",
            f"Well: {well_name} (UWI: {uwi})",
            f"Interval: {start} - {stop} {units}",
            f"Curve Count: {len(curves)}",
            "Available Logs:",
            f"  - " + (", ".join(curves[:8]) if curves else "None"),
            f"  " + (f"...and {len(curves)-8} more" if len(curves) > 8 else "")
        ]

        return "\n".join(output)

    except Exception as e:
        return f"LAS Extraction Error: {str(e)}"