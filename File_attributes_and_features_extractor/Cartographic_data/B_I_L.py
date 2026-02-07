import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import rasterio

def extract(file_path):
    """
    Exhaustively explores BIL raster files and their headers.
    Zero truncation: every raster property and CRS parameter is displayed.
    """
    try:
        # rasterio automatically looks for the .hdr file with the same name
        with rasterio.open(file_path) as src:
            
            # 1. Image Dimensions
            width, height = src.width, src.height
            count = src.count
            dtype = src.dtypes[0]
            nodata = src.nodata
            
            # 2. Interleaving and Driver Info
            driver = src.driver
            
            # 3. Spatial Reference (CRS)
            crs_info = src.crs.to_string() if src.crs else "Not Georeferenced"
            
            # 4. Affine Transform and Bounds
            t = src.transform
            bounds = src.bounds

            output = [
                "Type: BIL Raster (Band Interleaved by Line)",
                f"Driver: {driver}",
                f"Resolution: {width} x {height} (Pixels)",
                f"Bands: {count} | Data Type: {dtype}",
                f"NoData Value: {nodata}",
                f"CRS: {crs_info}",
                "Full Spatial Extent:",
                f"  Left:   {bounds.left}",
                f"  Bottom: {bounds.bottom}",
                f"  Right:  {bounds.right}",
                f"  Top:    {bounds.top}",
                "Affine Transform:",
                f"  {t}"
            ]
            
            # Exhaustive Tag Extraction
            if src.tags():
                output.append("Full Header Tags:")
                for k, v in src.tags().items():
                    output.append(f"  {k}: {v}")
            
            return "\n".join(output)

    except Exception as e:
        return f"BIL Error: {str(e)}"