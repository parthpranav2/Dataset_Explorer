import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores CPG files.
    Zero truncation: the full encoding string is identified and described.
    """
    try:
        with open(file_path, 'r', encoding='ascii', errors='ignore') as f:
            encoding_raw = f.read().strip()

        # Mapping common CPG strings to descriptive names
        encoding_map = {
            'UTF-8': 'Unicode (UTF-8) - Supports all global characters',
            'UTF8': 'Unicode (UTF-8) - Supports all global characters',
            '1252': 'Windows-1252 (Western European)',
            'ISO-8859-1': 'Latin-1 (Western European)',
            'UTF-16': 'Unicode (UTF-16)',
            'SJIS': 'Shift-JIS (Japanese)',
            '936': 'GB2312 (Simplified Chinese)'
        }

        description = encoding_map.get(encoding_raw.upper(), "Custom or Legacy Encoding")

        output = [
            "Type: Shapefile Character Encoding File (.cpg)",
            f"Raw Identifier: {encoding_raw}",
            f"Encoding Description: {description}",
            "Status: Critical for correct attribute rendering"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"CPG Error: {str(e)}"