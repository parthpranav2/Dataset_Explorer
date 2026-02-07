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
    Exhaustively explores Digital Elevation Models (DEM).
    Zero truncation: every vertical unit, resolution, and CRS tag is displayed.
    """
    try:
        with rasterio.open(file_path) as src:
            # 1. Grid Dimensions
            width, height = src.width, src.height
            dtype = src.dtypes[0]
            
            # 2. Coordinate Reference System (CRS)
            crs_info = src.crs.to_string() if src.crs else "Not Defined"
            
            # 3. Spatial Resolution (Pixel Size)
            # This represents the horizontal spacing between elevation points
            pixel_w = src.transform[0]
            pixel_h = abs(src.transform[4])
            
            # 4. Elevation Metadata
            # USGS DEMs often store vertical units in tags
            tags = src.tags()
            bounds = src.bounds

            output = [
                "Type: Digital Elevation Model (DEM)",
                f"Grid Resolution: {width} x {height} (Pixels)",
                f"Horizontal Spacing: {pixel_w} x {pixel_h} (Units)",
                f"Data Type: {dtype}",
                f"CRS: {crs_info}",
                "Full Spatial Extent:",
                f"  Left:   {bounds.left}",
                f"  Bottom: {bounds.bottom}",
                f"  Right:  {bounds.right}",
                f"  Top:    {bounds.top}"
            ]

            # 5. Full Tag Dump (Exhaustive Metadata)
            if tags:
                output.append("Exhaustive Header Tags:")
                for k, v in tags.items():
                    output.append(f"  {k}: {v}")
            
            return "\n".join(output)

    except Exception as e:
        return f"DEM Error: {str(e)}"