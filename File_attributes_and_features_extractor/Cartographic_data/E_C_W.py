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
    Exhaustively explores ECW files.
    Zero truncation: every metadata tag and spatial parameter is displayed.
    """
    try:
        with rasterio.open(file_path) as src:
            # 1. Fundamental Image Stats
            width, height = src.width, src.height
            count = src.count
            dtype = src.dtypes[0]
            
            # 2. Coordinate Reference System (CRS)
            crs_info = src.crs.to_string() if src.crs else "Not Georeferenced"
            
            # 3. Spatial Bounds
            bounds = src.bounds
            
            # 4. Metadata and Profile
            # ECW files often store compression info in the profile/tags
            profile = src.profile
            compression = profile.get('compress', 'Wavelet (ECW Standard)')

            output = [
                "Type: Enhanced Compression Wavelet (ECW)",
                f"Resolution: {width} x {height} Pixels",
                f"Bands: {count} | Dtype: {dtype}",
                f"Compression: {compression}",
                f"CRS: {crs_info}",
                "Full Spatial Extent:",
                f"  Left:   {bounds.left}",
                f"  Bottom: {bounds.bottom}",
                f"  Right:  {bounds.right}",
                f"  Top:    {bounds.top}"
            ]

            # 5. Full Tag Dump (Zero Truncation)
            tags = src.tags()
            if tags:
                output.append("Full Metadata Tags:")
                for k, v in tags.items():
                    output.append(f"  {k}: {v}")
            
            return "\n".join(output)

    except Exception as e:
        return f"ECW Error: {str(e)}"