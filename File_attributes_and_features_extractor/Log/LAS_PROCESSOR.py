import sys
import os
import lasio

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Unified processor for LAS 1.2, 2.0, and 3.0.
    Exhaustively extracts well headers, curve mnemonics, and depth ranges.
    """
    try:
        # Load the LAS file
        las = lasio.read(file_path)
        
        # 1. Version and Basic Metadata
        version = las.version.VERS.value if 'VERS' in las.version else "Unknown"
        well_name = las.well.WELL.value if 'WELL' in las.well else "Unknown"
        uwi = las.well.UWI.value if 'UWI' in las.well else "Unknown"
        
        # 2. Depth Constraints (Zero Truncation)
        start = las.well.STRT.value if 'STRT' in las.well else "N/A"
        stop = las.well.STOP.value if 'STOP' in las.well else "N/A"
        step = las.well.STEP.value if 'STEP' in las.well else "N/A"
        units = las.well.STRT.unit if 'STRT' in las.well else "units"

        # 3. Curve Inventory
        # We extract every mnemonic, unit, and description found in the ~Curve section
        curve_list = []
        for curve in las.curves:
            curve_list.append(f"    {curve.mnemonic} [{curve.unit}]: {curve.descr}")

        # 4. Section Audit (Crucial for LAS 3.0 custom sections)
        sections = [s for s in las.sections.keys() if s not in ['Version', 'Well', 'Curves', 'Parameter', 'Other']]
        
        output = [
            f"Type: Log ASCII Standard (LAS) v{version}",
            f"Well: {well_name} | UWI: {uwi}",
            f"Interval: {start} - {stop} {units} (Step: {step})",
            "Curve Inventory (Mnemonics):",
            "\n".join(curve_list) if curve_list else "    No curves found.",
            f"Data Dimensions: {las.data.shape[0]} Rows x {las.data.shape[1]} Columns"
        ]

        if sections:
            output.append(f"Additional Sections: {', '.join(sections)}")
            
        return "\n".join(output)

    except Exception as e:
        return f"LAS Processor Error: {str(e)}"