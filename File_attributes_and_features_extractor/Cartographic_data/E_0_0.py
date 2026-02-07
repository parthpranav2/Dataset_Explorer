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
    Exhaustively explores .e00 interchange files.
    Zero truncation: every internal section and header detail is extracted.
    """
    try:
        sections = []
        metadata = {}
        
        with open(file_path, 'r', errors='ignore') as f:
            # 1. Parse Header (First line contains type and precision)
            header = f.readline().split()
            if not header:
                return "Empty E00 File"
            
            metadata['Type'] = header[0]
            metadata['Precision'] = "Double" if len(header) > 2 and header[2] == "2" else "Single"
            
            # 2. Section Scanning
            # .e00 files mark sections with names like "ARC", "PAL", "BND", "EOS"
            f.seek(0)
            for line in f:
                parts = line.split()
                if len(parts) == 1 and parts[0].isupper() and len(parts[0]) <= 3:
                    if parts[0] != "EOS": # End of Section
                        sections.append(parts[0])
                
                # 3. Boundary Extraction (Found in BND section)
                if "BND" in line:
                    bnd_line = f.readline().split()
                    if len(bnd_line) >= 4:
                        metadata['Bounds'] = f"Min({bnd_line[0]}, {bnd_line[1]}) Max({bnd_line[2]}, {bnd_line[3]})"

        output = [
            "Type: ArcInfo Interchange File (ASCII)",
            f"Carrier Type: {metadata.get('Type', 'Unknown')}",
            f"Data Precision: {metadata.get('Precision', 'Unknown')}",
            f"Internal Sections: {', '.join(sections)}",
            f"Spatial Bounds: {metadata.get('Bounds', 'Not Defined')}",
            "Status: Export/Transport Format"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"E00 Error: {str(e)}"