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
    Exhaustively explores GeoTIFF files for spatial integrity.
    Zero truncation: every coordinate parameter and GeoKey is displayed.
    """
    try:
        with rasterio.open(file_path) as src:
            # 1. Geographic Identity
            crs = src.crs
            is_valid_geo = crs is not None
            
            # 2. Transform Matrix (Affine)
            # This contains: [a, b, c, d, e, f] where a=width, e=height
            t = src.transform
            affine_details = f"a={t.a}, b={t.b}, c={t.c}, d={t.d}, e={t.e}, f={t.f}"
            
            # 3. Exhaustive Metadata Gathering
            output = [
                "Type: GeoTIFF (Georeferenced Raster)",
                f"CRS Name: {crs.to_string() if is_valid_geo else 'Undefined'}",
                f"Dimensions: {src.width}w x {src.height}h",
                f"Band Count: {src.count} | Dtype: {src.dtypes[0]}",
                "Affine Transform Matrix:",
                f"  {affine_details}",
                "Full Spatial Extent:",
                f"  Left: {src.bounds.left} | Bottom: {src.bounds.bottom}",
                f"  Right: {src.bounds.right} | Top: {src.bounds.top}"
            ]

            # 4. Zero Truncation Tag Dump
            tags = src.tags()
            if tags:
                output.append("Full GeoKey/Metadata Tags:")
                for k, v in tags.items():
                    output.append(f"  {k}: {v}")
                    
            return "\n".join(output)

    except Exception as e:
        return f"GeoTIFF Error: {str(e)}"