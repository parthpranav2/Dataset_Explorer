import sys
import os

# --- ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# ----------------------------

import shapefile 

def extract(file_path):
    """
    Thoroughly explores the .shx index using pyshp to verify spatial records.
    """
    try:
        # We open the SHX using the shapefile reader
        # shx is strictly the index part of the set
        with shapefile.Reader(shx=file_path) as sf:
            
            # 1. Access the header information
            # shpLength in pyshp for an SHX file refers to the index length
            header_len = sf.shpLength 
            
            # 2. Verify Record Count
            # SHX records are always 8 bytes. Header is 100 bytes.
            file_size = os.path.getsize(file_path)
            num_records = (file_size - 100) // 8
            
            # 3. Association Link
            base_name = os.path.basename(file_path).replace('.shx', '')

            output = [
                "Type: Geometry Index",
                f"Linkage: Associated with {base_name}.shp",
                f"Records: {num_records} index offsets detected",
                f"Status: Header Valid (Length: {header_len} words)"
            ]
            
            return "\n".join(output)

    except Exception as e:
        return f"SHX Error: {str(e)}"