import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up two levels to Project Root
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import pyogrio

def extract(file_path):
    """
    Exhaustively explores File Geodatabase layers and schemas.
    Zero truncation: every feature class and field is displayed in full.
    """
    try:
        # 1. List all feature classes (layers) within the GDB
        layers = pyogrio.list_layers(file_path)
        
        detail_lines = []
        for i in range(len(layers)):
            layer_name = layers[i, 0]
            geom_type = layers[i, 1]
            
            detail_lines.append(f"Feature Class: {layer_name} (Geometry: {geom_type})")
            
            # 2. Extract detailed layer info
            meta = pyogrio.read_info(file_path, layer=layer_name)
            
            detail_lines.append(f"  Total Features: {meta['features_count']}")
            detail_lines.append(f"  Coordinate Reference System: {meta['crs']}")
            
            # 3. Exhaustive Field Schema (No truncation)
            detail_lines.append("  Full Attribute Schema:")
            for field, dtype in zip(meta['fields'], meta['dtypes']):
                detail_lines.append(f"    {field} ({dtype})")
            
            # 4. Full Data Sample (First record)
            df_sample = pyogrio.read_dataframe(file_path, layer=layer_name, max_features=1)
            if not df_sample.empty:
                sample_dict = df_sample.iloc[0].to_dict()
                # Build sample string excluding the geometry blob
                sample_str = " | ".join([f"{k}: {v}" for k, v in sample_dict.items() if k != 'geometry'])
                detail_lines.append(f"  Full Sample Record: {sample_str}")

        output = [
            "Type: Esri File Geodatabase (Folder-based)",
            f"Total Feature Classes Found: {len(layers)}",
            "Exhaustive GDB Contents:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"GDB Error: {str(e)}"