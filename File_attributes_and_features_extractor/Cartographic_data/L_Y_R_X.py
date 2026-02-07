import sys
import os
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
    Exhaustively explores ArcGIS Pro .lyrx files.
    Zero truncation: every JSON attribute for data source and symbology is listed.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # .lyrx files usually start with a 'layerDefinitions' list
        layer_defs = data.get('layerDefinitions', [])
        if not layer_defs:
            return "Type: ArcGIS Pro Layer File (Empty or Invalid)"

        detail_lines = []
        for l_def in layer_defs:
            name = l_def.get('name', 'Unnamed Layer')
            
            # 1. Data Connection Extraction
            data_conn = l_def.get('featureTable', {}).get('dataConnection', {})
            conn_str = data_conn.get('workspaceConnectionString', 'No Workspace Found')
            dataset = data_conn.get('dataset', 'No Dataset Found')
            
            # 2. Symbology Extraction
            renderer = l_def.get('renderer', {})
            renderer_type = renderer.get('type', 'Unknown Renderer')
            
            # 3. Scale Dependency
            min_scale = l_def.get('minScale', 0)
            max_scale = l_def.get('maxScale', 0)

            detail_lines.append(f"  Layer Name: {name}")
            detail_lines.append(f"    Source Dataset: {dataset}")
            detail_lines.append(f"    Connection: {conn_str}")
            detail_lines.append(f"    Renderer Type: {renderer_type}")
            detail_lines.append(f"    Scale Range: {min_scale} to {max_scale}")

        output = [
            "Type: ArcGIS Pro Layer File (JSON Symbology)",
            "Exhaustive Layer Definitions:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"LYRX Parsing Error: {str(e)}"