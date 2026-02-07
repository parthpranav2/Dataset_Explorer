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

def get_all_keys(dl, prefix=''):
    """Recursively finds all keys in a nested dictionary/list."""
    keys = []
    if isinstance(dl, dict):
        for k, v in dl.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.append(full_key)
            keys.extend(get_all_keys(v, full_key))
    elif isinstance(dl, list):
        for i, item in enumerate(dl):
            # We sample keys from the first few items to keep schema concise but full
            if i < 3: 
                keys.extend(get_all_keys(item, f"{prefix}[{i}]"))
    return list(set(keys))

def extract(file_path):
    """
    Exhaustively explores JSON files and extracts the full schema 
    and full content without any truncation.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. Determine Root Type
        root_type = "Object/Dictionary" if isinstance(data, dict) else "Array/List"
        
        # 2. Extract Exhaustive Schema
        all_keys = sorted(get_all_keys(data))
        schema_lines = [f"  {k}" for k in all_keys]
        
        # 3. Full Content Formatting
        # No truncation: prints the entire beautified JSON string
        full_content = json.dumps(data, indent=2)

        output = [
            f"Type: JSON Data File",
            f"Root Structure: {root_type}",
            "Exhaustive Key Schema:",
            "\n".join(schema_lines),
            "Full File Content:",
            full_content
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"JSON Error: {str(e)}"