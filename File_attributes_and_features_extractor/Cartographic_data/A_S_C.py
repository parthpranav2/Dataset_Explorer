import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores ASCII Grid files.
    Zero truncation: every header line is parsed and displayed.
    """
    try:
        header_info = {}
        # We only need to read the first 6-10 lines to get the full header
        with open(file_path, 'r') as f:
            for _ in range(10):
                line = f.readline().split()
                if not line:
                    break
                # Common keys: ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value
                if len(line) == 2:
                    header_info[line[0].lower()] = line[1]

        # 1. Coordinate and Dimension Extraction
        cols = header_info.get('ncols', 'Unknown')
        rows = header_info.get('nrows', 'Unknown')
        x_ll = header_info.get('xllcorner', 'Unknown')
        y_ll = header_info.get('yllcorner', 'Unknown')
        cellsize = header_info.get('cellsize', 'Unknown')
        nodata = header_info.get('nodata_value', 'Unknown')

        output = [
            "Type: Esri ASCII Grid (Raster)",
            f"Dimensions: {cols} (Cols) x {rows} (Rows)",
            f"Cell Size: {cellsize} units",
            f"Origin (Lower-Left): X={x_ll}, Y={y_ll}",
            f"NoData Flag: {nodata}",
            "Exhaustive Header Schema:",
            *[f"  {k}: {v}" for k, v in header_info.items()]
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"ASCII Grid Error: {str(e)}"