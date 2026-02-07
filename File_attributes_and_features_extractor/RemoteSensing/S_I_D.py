import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    import rasterio
except ImportError:
    rasterio = None
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .sid (MrSID) geospatial raster files.
    Zero truncation: identifies CRS, dimensions, and spatial resolution.
    """
    if not rasterio:
        return "Error: rasterio/gdal library not found in venv."

    try:
        # Note: Opening .sid often requires the GDAL MrSID driver
        with rasterio.open(file_path) as src:
            width, height = src.width, src.height
            bands = src.count
            crs = src.crs.to_string() if src.crs else "Non-Georeferenced"
            res_x, res_y = src.res
            dtype = src.dtypes[0]

            output = [
                "Type: MrSID Compressed Raster (.sid)",
                f"Dimensions: {width}x{height} pixels",
                f"Spectral Detail: {bands} Bands | {dtype}",
                f"Spatial Resolution: {res_x:.4f} x {res_y:.4f} units/pixel",
                "Geodetic Context:",
                f"  - CRS: {crs}",
                f"  - Bounding Box: {src.bounds}"
            ]

            return "\n".join(output)

    except Exception as e:
        # Provide a more descriptive error if the driver is missing
        if "driver" in str(e).lower():
            return "SID Extraction Error: MrSID driver not found in GDAL environment."
        return f"SID Extraction Error: {str(e)}"