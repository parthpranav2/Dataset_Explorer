import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import pyogrio

def extract(file_path):
    """
    Exhaustively explores GeoPackage layers and schemas using pyogrio.
    Zero truncation: every layer and every field is displayed.
    """
    try:
        # 1. List all layers in the GeoPackage
        layers = pyogrio.list_layers(file_path)
        
        detail_lines = []
        for i in range(len(layers)):
            layer_name = layers[i, 0]
            geom_type = layers[i, 1]
            
            detail_lines.append(f"Layer: {layer_name} (Type: {geom_type})")
            
            # 2. Get full metadata for the specific layer
            meta = pyogrio.read_info(file_path, layer=layer_name)
            
            detail_lines.append(f"  Feature Count: {meta['features_count']}")
            detail_lines.append(f"  CRS: {meta['crs']}")
            
            # 3. Exhaustive Field Schema
            detail_lines.append("  Full Field Schema:")
            for field, dtype in zip(meta['fields'], meta['dtypes']):
                detail_lines.append(f"    {field} ({dtype})")
            
            # 4. Data Sampling (First feature)
            # No truncation: list all values for the first row
            df_sample = pyogrio.read_dataframe(file_path, layer=layer_name, max_features=1)
            if not df_sample.empty:
                sample_dict = df_sample.iloc[0].to_dict()
                sample_str = " | ".join([f"{k}: {v}" for k, v in sample_dict.items() if k != 'geometry'])
                detail_lines.append(f"  Full Sample Record: {sample_str}")

        output = [
            "Type: OGC GeoPackage (SQLite Container)",
            f"Total Layers Found: {len(layers)}",
            "Exhaustive Layer Details:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"GPKG Error: {str(e)}"