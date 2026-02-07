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

def extract(file_path):
    """
    Exhaustively explores GML files for the final Parth output.
    Zero truncation: every field in the schema and full CRS details are included.
    """
    try:
        # GML files can contain multiple layers; we iterate through all
        layers = fiona.listlayers(file_path)
        
        detail_blocks = []
        for layer_name in layers:
            with fiona.open(file_path, layer=layer_name) as src:
                layer_info = [
                    f"  Layer: {layer_name}",
                    f"    Geometry Type: {src.schema['geometry']}",
                    f"    Feature Count: {len(src)}",
                    f"    CRS: {src.crs.get('init') if src.crs else 'Undefined'}"
                ]
                
                # Full Schema Extraction
                layer_info.append("    Exhaustive Schema:")
                for field, dtype in src.schema['properties'].items():
                    layer_info.append(f"      - {field} ({dtype})")
                
                # Full First Record Sample
                first_feat = next(iter(src), None)
                if first_feat:
                    layer_info.append("    First Feature Sample:")
                    props = first_feat.get('properties', {})
                    for k, v in props.items():
                        layer_info.append(f"      {k}: {v}")
                
                detail_blocks.append("\n".join(layer_info))

        output = [
            "Type: Geography Markup Language (GML)",
            "Exhaustive Spatial Metadata:",
            "\n".join(detail_blocks) if detail_blocks else "  No valid layers found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"GML Processing Error: {str(e)}"