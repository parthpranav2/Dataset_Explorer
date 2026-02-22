import sys
import os
import textwrap

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

def extract(file_path, indent_level=""):
    """
    Exhaustively explores .las files with intelligent line wrapping.
    Prevents the branching structure from being cut or misaligned.
    """
    if not lasio:
        return "Error: lasio library not found in venv."

    try:
        las = lasio.read(file_path)
        
        # 1. Metadata Extraction
        well_name = las.well.WELL.value if 'WELL' in las.well else "Unknown"
        uwi = las.well.UWI.value if 'UWI' in las.well else "N/A"
        company = las.well.COMP.value if 'COMP' in las.well else "N/A"
        start = las.well.STRT.value
        stop = las.well.STOP.value
        units = las.well.STRT.unit
        
        # 2. Curve Mnemonic Processing
        all_curves = [c.mnemonic for c in las.curves]
        curve_raw_text = ", ".join(all_curves)
        
        # 3. Intelligent Wrapping
        # We assume a standard width of 80 chars for the curves section
        # The prefix ensures the vertical tree lines are maintained on wrapped lines
        wrapper = textwrap.TextWrapper(width=80, 
                                       subsequent_indent=indent_level + " " * 16)
        wrapped_curves = wrapper.fill(f"Available Logs: {curve_raw_text}")

        output = [
            f"Type: Log ASCII Standard (.las)",
            f"Well: {well_name} | Company: {company}",
            f"UWI: {uwi}",
            f"Interval: {start} - {stop} {units}",
            f"Total Curves: {len(all_curves)}",
            wrapped_curves
        ]

        return "\n".join(output)

    except Exception as e:
        return f"LAS Extraction Error: {str(e)}"