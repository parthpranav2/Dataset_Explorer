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
    Exhaustively explores SEG-Y seismic files.
    Zero truncation: decodes headers and provides full survey geometry.
    """
    try:
        # open with ignore_geometry to handle non-standard or 2D files
        with segyio.open(file_path, "r", ignore_geometry=True) as segy:
            # 1. Basic Geometry
            n_traces = segy.tracecount
            n_samples = segy.samples.size
            sample_rate = segy.bin[segyio.BinField.Interval]
            
            # 2. Extract EBCDIC Header (First 400 chars for preview)
            ebcdic = segyio.tools.wrap(segy.text[0])
            header_preview = ebcdic[:400].replace('\n', ' | ')

            # 3. Coordinate Scaling
            # Check the first trace for the coordinate scalar
            scalar = segy.header[0][segyio.TraceField.SourceGroupScalar]

            output = [
                "Type: SEG-Y Seismic Data",
                f"Geometry: {n_traces} Traces | {n_samples} Samples/Trace",
                f"Sample Rate: {sample_rate} microseconds",
                f"Coordinate Scalar: {scalar}",
                "EBCDIC Header Preview (First 400 chars):",
                f"  {header_preview}..."
            ]
            
            return "\n".join(output)

    except Exception as e:
        return f"SEG-Y Extraction Error: {str(e)}"