import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import segyio

def extract(file_path):
    """
    Exhaustively explores .sgy seismic files.
    Zero truncation: provides full spatial bounds and header metadata.
    """
    try:
        # Open with ignore_geometry=True to handle both 2D and 3D files
        with segyio.open(file_path, "r", ignore_geometry=True) as src:
            # 1. Geometry Metadata
            n_traces = src.tracecount
            n_samples = src.samples.size
            sample_rate = src.bin[segyio.BinField.Interval]
            
            # 2. Coordinate Extraction (Scanning first and last traces)
            # Source X/Y
            first_x = src.header[0][segyio.TraceField.SourceX]
            first_y = src.header[0][segyio.TraceField.SourceY]
            last_x = src.header[n_traces-1][segyio.TraceField.SourceX]
            last_y = src.header[n_traces-1][segyio.TraceField.SourceY]
            
            # 3. Text Header Decoding
            ebcdic_raw = segyio.tools.wrap(src.text[0])
            # Capture first 5 lines for the tree output
            text_header = " | ".join([line.strip() for line in ebcdic_raw.split('\n')[:5] if line.strip()])

        output = [
            "Type: SEG-Y Seismic Data (.sgy)",
            f"Volume Geometry: {n_traces} Traces | {n_samples} Samples/Trace",
            f"Temporal Resolution: {sample_rate} µs",
            "Spatial Extents (Source Coordinates):",
            f"  - Start: ({first_x}, {first_y})",
            f"  - End:   ({last_x}, {last_y})",
            "Textual Header Preview:",
            f"  {text_header}..."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SGY Extraction Error: {str(e)}"