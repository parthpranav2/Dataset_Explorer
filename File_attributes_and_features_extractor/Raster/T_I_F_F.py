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
    Exhaustively explores TIFF files. 
    Handles both GeoTIFFs and standard TIFF images with zero truncation.
    """
    try:
        with rasterio.open(file_path) as src:
            # 1. Image Dimensions and Bands
            width, height = src.width, src.height
            count = src.count
            dtype = src.dtypes[0]
            
            # 2. Check for Geospatial Information
            is_spatial = src.crs is not None
            crs_info = src.crs.to_string() if is_spatial else "None (Standard Image)"
            
            output = [
                f"Type: {'GeoTIFF (Spatial Raster)' if is_spatial else 'TIFF Image'}",
                f"Resolution: {width} x {height} (Pixels)",
                f"Bands: {count}",
                f"Data Type: {dtype}"
            ]

            # 3. Exhaustive Spatial Metadata (GeoTIFF only)
            if is_spatial:
                bounds = src.bounds
                pixel_w = src.transform[0]
                pixel_h = abs(src.transform[4])
                output.extend([
                    f"CRS: {crs_info}",
                    f"Pixel Size: {pixel_w} x {pixel_h}",
                    "Full Spatial Extent:",
                    f"  Left:   {bounds.left}",
                    f"  Bottom: {bounds.bottom}",
                    f"  Right:  {bounds.right}",
                    f"  Top:    {bounds.top}"
                ])

            # 4. Full Tag Dump (Zero Truncation)
            all_tags = src.tags()
            if all_tags:
                output.append("Full Metadata Tags:")
                for k, v in all_tags.items():
                    output.append(f"  {k}: {v}")
            
            return "\n".join(output)

    except Exception as e:
        return f"TIFF Error: {str(e)}"