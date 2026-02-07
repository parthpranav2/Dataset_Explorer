import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Note: Since this is in a SUB-FOLDER (GIS), go up TWO levels to project root
project_root = os.path.dirname(os.path.dirname(current_dir))

venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

from dbfread import DBF

def extract(file_path):
    """
    Explores the .dbf attribute table and extracts ALL fields and the FULL 
    first record sample without any truncation or "..." markers.
    """
    try:
        # Load table without loading all records into memory (streaming mode)
        table = DBF(file_path, load=False)
        
        # 1. Dimensions
        num_records = len(table)
        num_fields = len(table.fields)
        
        # 2. Exhaustive Schema Extraction
        # This will list every field (e.g., OBJECTID, AGE, LITHOLOGIC, etc.)
        schema_lines = [f"  {f.name} ({f.type})" for f in table.fields]
            
        # 3. Full Data Sampling (First Record)
        sample_line = "No data found"
        for record in table:
            # Captures every single key-value pair for the record without limit
            sample_parts = [f"{k}: {v}" for k, v in record.items()]
            sample_line = " | ".join(sample_parts)
            break

        output = [
            "Type: Attribute Table (dBase)",
            f"Rows: {num_records} | Fields: {num_fields}",
            "Full Schema:",
            "\n".join(schema_lines),
            f"Full Sample Record: {sample_line}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"DBF Error: {str(e)}"