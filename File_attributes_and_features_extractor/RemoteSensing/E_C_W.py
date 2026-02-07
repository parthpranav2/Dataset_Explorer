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
    Exhaustively explores .ecw (Enhanced Compression Wavelet) raster files.
    Zero truncation: identifies CRS, compression stats, and spatial resolution.
    """
    if not rasterio:
        return "Error: rasterio/gdal library not found in venv."

    try:
        # Note: Opening .ecw requires the GDAL ECW driver
        with rasterio.open(file_path) as src:
            width, height = src.width, src.height
            bands = src.count
            crs = src.crs.to_string() if src.crs else "Non-Georeferenced"
            res_x, res_y = src.res
            
            output = [
                "Type: Enhanced Compression Wavelet (.ecw)",
                f"Dimensions: {width}x{height} pixels",
                f"Spectral Detail: {bands} Bands",
                f"Spatial Resolution: {res_x:.4f} x {res_y:.4f} units/pixel",
                "Geodetic Context:",
                f"  - CRS: {crs}",
                f"  - Bounding Box: {src.bounds.left:.1f}, {src.bounds.bottom:.1f} to {src.bounds.right:.1f}, {src.bounds.top:.1f}",
                f"Driver: {src.driver}"
            ]

            return "\n".join(output)

    except Exception as e:
        if "driver" in str(e).lower():
            return "ECW Extraction Error: ECW driver not found in GDAL environment."
        return f"ECW Extraction Error: {str(e)}"