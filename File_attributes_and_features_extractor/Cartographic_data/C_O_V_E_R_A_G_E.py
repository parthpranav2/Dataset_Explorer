import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import fiona

def extract(folder_path):
    """
    Exhaustively explores Esri Coverages.
    Zero truncation: every topological layer and field is listed.
    """
    try:
        # Coverages are opened by pointing to the folder
        layers = fiona.listlayers(folder_path)
        
        detail_lines = []
        for layer_name in layers:
            with fiona.open(folder_path, layer=layer_name) as src:
                detail_lines.append(f"Component: {layer_name}")
                detail_lines.append(f"  Geometry: {src.schema['geometry']}")
                detail_lines.append(f"  Feature Count: {len(src)}")
                
                # Full Attribute Schema
                detail_lines.append("  Full Attribute Schema:")
                for field, dtype in src.schema['properties'].items():
                    detail_lines.append(f"    {field} ({dtype})")
                
                # Full Sample Record
                first = next(iter(src), None)
                if first:
                    sample_dict = dict(first['properties'])
                    sample_str = " | ".join([f"{k}: {v}" for k, v in sample_dict.items()])
                    detail_lines.append(f"  Full Sample Record: {sample_str}")

        output = [
            "Type: Esri Vector Coverage (Folder-based)",
            f"Total Components: {len(layers)}",
            "Exhaustive Topology Details:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"Coverage Error: {str(e)}"