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
    Exhaustively explores Meta Raster Format (MRF) files.
    Zero truncation: every raster dimension, tile setting, and CRS tag is displayed.
    """
    try:
        # rasterio handles the internal XML parsing of the .mrf file
        with rasterio.open(file_path) as src:
            
            # 1. Fundamental Dimensions
            width, height = src.width, src.height
            count = src.count
            dtype = src.dtypes[0]
            
            # 2. MRF Specifics (Tiling and Compression)
            # block_shapes provides the tile dimensions
            tiles = src.block_shapes[0] if src.block_shapes else "Not Tiled"
            compression = src.profile.get('compress', 'None')
            
            # 3. Spatial Georeferencing
            crs_info = src.crs.to_string() if src.crs else "Not Defined"
            bounds = src.bounds

            output = [
                "Type: Meta Raster Format (MRF)",
                f"Resolution: {width} x {height} Pixels",
                f"Bands: {count} | Dtype: {dtype}",
                f"Tiling Schema: {tiles}",
                f"Compression: {compression}",
                f"CRS: {crs_info}",
                "Full Spatial Extent:",
                f"  Left:   {bounds.left}",
                f"  Bottom: {bounds.bottom}",
                f"  Right:  {bounds.right}",
                f"  Top:    {bounds.top}"
            ]

            # 4. Comprehensive Tag Dump
            tags = src.tags()
            if tags:
                output.append("Full Metadata Tags:")
                for k, v in tags.items():
                    output.append(f"  {k}: {v}")
            
            return "\n".join(output)

    except Exception as e:
        return f"MRF Error: {str(e)}"