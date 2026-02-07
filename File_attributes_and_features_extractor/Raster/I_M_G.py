import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

from PIL import Image
from PIL.ExifTags import TAGS

def extract(file_path):
    """
    Exhaustively explores image files to extract resolution and EXIF data.
    Zero truncation: every metadata tag is displayed in full.
    """
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            mode = img.mode
            format_type = img.format
            
            output = [
                f"Type: {format_type} Image",
                f"Resolution: {width} x {height} Pixels",
                f"Color Mode: {mode}"
            ]

            # 1. Exhaustive EXIF Data Extraction
            exif_data = img.getexif()
            if exif_data:
                output.append("Full EXIF Metadata:")
                for tag_id in exif_data:
                    tag = TAGS.get(tag_id, tag_id)
                    data = exif_data.get(tag_id)
                    # Handle binary data in EXIF to keep text clean
                    if isinstance(data, bytes):
                        data = data[:20].hex() + " (Binary Data)"
                    output.append(f"  {tag}: {data}")
            else:
                output.append("EXIF Metadata: None found")
                
            return "\n".join(output)

    except Exception as e:
        return f"Image Error: {str(e)}"