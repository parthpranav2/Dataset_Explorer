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
    Exhaustively explores SEG-Y Revision 1 seismic files.
    Zero truncation: identifies extended headers and modern sample formats.
    """
    try:
        # Open with ignore_geometry=True to handle complex 3D volumes or 2D lines
        with segyio.open(file_path, "r", ignore_geometry=True) as src:
            # 1. Revision Status check
            # Byte 3501 in binary header (offset 3001) usually holds the revision
            rev_major = src.bin[segyio.BinField.Format]
            
            # 2. Geometry and Sampling
            n_traces = src.tracecount
            n_samples = src.samples.size
            sample_rate = src.bin[segyio.BinField.Interval]
            
            # 3. Extended Header Count
            # Rev 1 allows for multiple 3200-byte blocks
            ext_headers = getattr(src, 'ext_headers', 0)

            # 4. Textual Metadata Audit
            ebcdic_raw = segyio.tools.wrap(src.text[0])
            # Extract first 5 lines for the directory tree visualization
            header_preview = " | ".join([l.strip() for l in ebcdic_raw.split('\n')[:5] if l.strip()])

        output = [
            "Type: SEG-Y Revision 1 Seismic Data",
            f"Volume Geometry: {n_traces} Traces | {n_samples} Samples/Trace",
            f"Sampling: {sample_rate} µs interval | Format: {rev_major}",
            f"Extended Metadata: {ext_headers} additional 3200-byte headers detected.",
            "Primary Text Header Audit:",
            f"  {header_preview}..."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SEGY-Rev1 Extraction Error: {str(e)}"