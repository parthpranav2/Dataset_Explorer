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
    Exhaustively explores .jp2 satellite and high-res imagery.
    Zero truncation: identifies CRS, band counts, and spatial resolution.
    """
    if not rasterio:
        return "Error: rasterio library not found in venv."

    try:
        with rasterio.open(file_path) as src:
            # 1. Spatial Metadata
            width, height = src.width, src.height
            bands = src.count
            crs = src.crs.to_string() if src.crs else "Non-Georeferenced"
            
            # 2. Resolution Audit (Pixel Size)
            res_x, res_y = src.res
            
            # 3. Data Type
            dtype = src.dtypes[0]

            output = [
                "Type: JPEG 2000 / Satellite Imagery (.jp2)",
                f"Dimensions: {width}x{height} pixels",
                f"Spectral Detail: {bands} Bands | {dtype}",
                f"Spatial Resolution: {res_x:.2f} x {res_y:.2f} units/pixel",
                "Geodetic Context:",
                f"  - CRS: {crs}",
                f"  - Bounds: L:{src.bounds.left:.2f}, R:{src.bounds.right:.2f}, B:{src.bounds.bottom:.2f}, T:{src.bounds.top:.2f}"
            ]

            return "\n".join(output)

    except Exception as e:
        return f"JP2 Extraction Error: {str(e)}"