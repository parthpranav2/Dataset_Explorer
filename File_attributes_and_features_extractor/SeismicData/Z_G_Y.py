import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import openzgy

def extract(file_path):
    """
    Exhaustively explores .zgy compressed seismic volumes.
    Zero truncation: provides 3D geometry, spatial origin, and amplitude stats.
    """
    try:
        with openzgy.ZgyReader(file_path) as reader:
            # 1. Geometry Metadata
            size = reader.size
            start = reader.annotstart
            inc = reader.annotinc
            
            # 2. Spatial Mapping
            corners = reader.corners
            
            # 3. Value Statistics
            stats = reader.statistics
            
            # 4. Data Format
            datatype = reader.datatype

        output = [
            "Type: ZGY Compressed Seismic Volume",
            f"3D Dimensions: {size[0]} Inlines x {size[1]} Crosslines x {size[2]} Samples",
            "Annotation Range:",
            f"  - Inline: {start[0]} to {start[0] + (size[0]-1)*inc[0]} (Inc: {inc[0]})",
            f"  - Crossline: {start[1]} to {start[1] + (size[1]-1)*inc[1]} (Inc: {inc[1]})",
            "Spatial Context:",
            f"  - World Origin (X,Y): {corners[0][0]}, {corners[0][1]}",
            "Amplitude Statistics:",
            f"  - Range: {stats.min} to {stats.max}",
            f"  - Data Type: {datatype}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"ZGY Extraction Error: {str(e)}"