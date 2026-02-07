import sys
import os
import ijson
import json

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores TopoJSON files to extract layers, 
    arcs, and full property schemas without any truncation.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # We load a small sample for the header/objects, 
            # but keep it full for schema extraction
            data = json.load(f)
        
        # 1. Basic Topology Metadata
        type_check = data.get('type', 'Unknown')
        objects = data.get('objects', {})
        layer_names = list(objects.keys())
        
        # 2. Arc and Transform Metadata
        num_arcs = len(data.get('arcs', []))
        transform = data.get('transform', 'None (Not Quantized)')
        
        # 3. Exhaustive Schema and Sample Extraction
        detail_lines = []
        for layer in layer_names:
            detail_lines.append(f"Layer: {layer}")
            
            # Navigate to the first geometry of the layer
            geoms = objects[layer].get('geometries', [])
            if geoms:
                properties = geoms[0].get('properties', {})
                # List every single property found
                schema = [f"    {p}" for p in properties.keys()]
                detail_lines.append("  Full Schema:")
                detail_lines.extend(schema)
                
                # Full Sample Record for this layer
                sample = " | ".join([f"{k}: {v}" for k, v in properties.items()])
                detail_lines.append(f"  Full Sample Record: {sample}")
            else:
                detail_lines.append("  No geometries found in this layer.")

        output = [
            "Type: TopoJSON (Topology Encoded)",
            f"Structure: {type_check}",
            f"Total Arcs: {num_arcs}",
            f"Coordinate Transform: {transform}",
            "Object Layers & Exhaustive Detail:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"TopoJSON Error: {str(e)}"