import sys
import os
import struct

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up two levels (GIS -> File_attributes_and_features_extractor -> Project Root)
project_root = os.path.dirname(os.path.dirname(current_dir))

# Target your specific Python 3.9 venv found in your Dataset_Explorer
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores the .sbx binary index extension.
    Extracts all header metadata with zero truncation for the clean tree view.
    """
    try:
        file_size = os.path.getsize(file_path)
        if file_size < 100:
            return "Invalid SBX: File too small for standard header"

        with open(file_path, 'rb') as f:
            header = f.read(100)
            
            # 1. Verify Magic Number (Big-endian integer at byte 0)
            file_code = struct.unpack('>i', header[0:4])[0]
            
            # 2. Extract Bounding Box (Big-endian doubles from offset 36)
            # Order: Xmin, Ymin, Xmax, Ymax
            bbox = struct.unpack('>dddd', header[36:68])
            
            # 3. Extract Word Length (Big-endian integer at offset 24)
            word_length = struct.unpack('>i', header[24:28])[0]
            
            base_name = os.path.basename(file_path).replace('.sbx', '')

            # Build the exhaustive output list
            output = [
                "Type: Spatial Index Extension (Binary)",
                f"Signature: {'Valid (9994)' if file_code == 9994 else f'Unknown ({file_code})'}",
                f"Linkage: Companion for {base_name}.sbn / {base_name}.shp",
                f"Bounding Box Min: X={bbox[0]:.6f}, Y={bbox[1]:.6f}",
                f"Bounding Box Max: X={bbox[2]:.6f}, Y={bbox[3]:.6f}",
                f"Header Word Length: {word_length}",
                f"File Size on Disk: {file_size} bytes"
            ]
            
            return "\n".join(output)

    except Exception as e:
        return f"SBX Error: {str(e)}"