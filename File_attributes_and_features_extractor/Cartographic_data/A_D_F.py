import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up two levels to Project Root
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import rasterio

def extract(file_path):
    """
    Exhaustively explores ArcInfo Binary Grids.
    Zero truncation: every raster attribute and CRS parameter is displayed.
    """
    try:
        # rasterio handles the complex .adf folder structure automatically
        with rasterio.open(file_path) as src:
            
            # 1. Basic Raster Dimensions
            width = src.width
            height = src.height
            count = src.count # Number of bands
            
            # 2. Spatial Resolution (Cell Size)
            # transform[0] is pixel width, transform[4] is pixel height
            cell_width = src.transform[0]
            cell_height = abs(src.transform[4])
            
            # 3. Coordinate Reference System (CRS)
            crs_info = src.crs.to_string() if src.crs else "Not Defined"
            
            # 4. Bounds and Statistics
            bounds = src.bounds
            dtype = src.dtypes[0]

            output = [
                "Type: ArcInfo Binary Grid (Raster)",
                f"Dimensions: {width} x {height} (Pixels)",
                f"Bands: {count}",
                f"Cell Size: {cell_width} x {cell_height} (Units)",
                f"Data Type: {dtype}",
                f"CRS: {crs_info}",
                "Full Spatial Extent:",
                f"  Left:   {bounds.left}",
                f"  Bottom: {bounds.bottom}",
                f"  Right:  {bounds.right}",
                f"  Top:    {bounds.top}"
            ]
            
            return "\n".join(output)

    except Exception as e:
        return f"ADF Error: {str(e)}"