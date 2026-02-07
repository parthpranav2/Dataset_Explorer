import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Note: Since this is in a SUB-FOLDER (GIS), go up TWO levels to project root
project_root = os.path.dirname(os.path.dirname(current_dir))

# Target your specific Python 3.9 venv
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

from pyproj import CRS

def extract(file_path):
    """
    Thoroughly explores the .prj file to identify the Coordinate Reference System (CRS).
    Displays all identified parameters without any truncation.
    """
    try:
        if not os.path.exists(file_path):
            return "File not found"

        with open(file_path, 'r') as f:
            wkt_text = f.read().strip()
        
        if not wkt_text:
            return "Empty Projection File"

        # Use pyproj to explore the binary-like WKT string
        crs = CRS.from_wkt(wkt_text)
        
        # Build the exhaustive output list
        output = [
            f"Type: Coordinate Reference System",
            f"System Name: {crs.name}",
            f"Horizontal Datum: {crs.datum.name if crs.datum else 'Unknown'}",
            f"Spheroid: {crs.ellipsoid.name if crs.ellipsoid else 'Unknown'}",
            f"Prime Meridian: {crs.prime_meridian.name if crs.prime_meridian else 'Unknown'}",
            f"Measurement Units: {crs.axis_info[0].unit_name}",
            f"Area of Use: {crs.area_of_use.name if crs.area_of_use else 'Global'}",
            f"Is Geographic: {crs.is_geographic}",
            f"Is Projected: {crs.is_projected}",
            f"WKT String: {wkt_text}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"PRJ Error: {str(e)}"