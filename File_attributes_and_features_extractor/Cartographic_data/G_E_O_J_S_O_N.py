import sys
import os
import ijson # Optimized for large JSON files

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores GeoJSON files using streaming to extract 
    full schema and geometry metadata without truncation.
    """
    try:
        with open(file_path, 'rb') as f:
            # 1. Detect Geometry Type from the first feature
            # We use ijson.items to stream only the first 'feature'
            features = ijson.items(f, 'features.item')
            first_feature = next(features, None)
            
            if not first_feature:
                return "Empty GeoJSON: No features found"
            
            geom_type = first_feature.get('geometry', {}).get('type', 'Unknown')
            properties = first_feature.get('properties', {})
            
            # 2. Get Full Property Schema (Every single key)
            # No truncation allowed here.
            schema_lines = [f"  {key}" for key in properties.keys()]
            
            # 3. Full Sample Record
            sample_parts = [f"{k}: {v}" for k, v in properties.items()]
            sample_line = " | ".join(sample_parts)
            
            # 4. Count total features (requires a separate pass for accuracy)
            f.seek(0)
            count = 0
            for _ in ijson.items(f, 'features.item'):
                count += 1

        output = [
            "Type: Geographic JSON (Standard)",
            f"Geometry Type: {geom_type}",
            f"Total Features: {count}",
            "Full Property Schema:",
            "\n".join(schema_lines),
            f"Full Sample Record: {sample_line}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"GeoJSON Error: {str(e)}"