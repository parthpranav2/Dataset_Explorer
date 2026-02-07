import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
# Get the absolute path of the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Move up one level to the project root (Dataset_Explorer)
project_root = os.path.dirname(current_dir)

# Force Python to look in YOUR specific venv site-packages first
# Based on your screenshot: venv/lib/python3.9/site-packages
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
else:
    # Fallback for Windows if you switch OS
    win_venv = os.path.join(project_root, 'venv', 'Lib', 'site-packages')
    if os.path.exists(win_venv):
        sys.path.insert(0, win_venv)

# Add project root to path as well
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -------------------------------------

import shapefile # This should now find the module successfully

def extract(file_path):
    """
    Extracts geometric metadata and spatial extent from .shp files.
    """
    try:
        # Load the shapefile binary reader
        with shapefile.Reader(file_path) as sf:
            # 1. Map the Shape Type ID
            type_map = {
                0: "Null", 1: "Point", 3: "Polyline", 5: "Polygon", 
                8: "MultiPoint", 11: "PointZ", 13: "PolyLineZ", 15: "PolygonZ"
            }
            geom_type = type_map.get(sf.shapeType, f"Type({sf.shapeType})")
            
            # 2. Get the Feature Count
            count = len(sf.shapes())
            
            # 3. Get the Bounding Box (Extent)
            bbox = sf.bbox
            extent_info = f"({bbox[0]:.2f}, {bbox[1]:.2f}) to ({bbox[2]:.2f}, {bbox[3]:.2f})"
            
            # 4. Complexity Analysis (Total Vertices)
            total_points = sum(len(s.points) for s in sf.shapes())

            # Output lines for the clean tree handler
            output = [
                f"Geometry: {geom_type}",
                f"Features: {count} entities",
                f"Extent: {extent_info}",
                f"Complexity: {total_points} total vertices"
            ]
            
            return "\n".join(output)

    except Exception as e:
        return f"SHP Error: {str(e)}"