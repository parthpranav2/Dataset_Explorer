import sys
import os
import textwrap

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    import pyogrio
except ImportError:
    pyogrio = None
# -------------------------------------

def extract(file_path, indent_level=""):
    """
    Exhaustively explores .fgb spatial files.
    Zero truncation: lists every attribute column and metadata property
    with alignment protection to prevent cutting the directory tree.
    """
    if not pyogrio:
        return "Error: pyogrio library not found in venv."

    try:
        # read_info provides a fast way to get metadata without loading all features
        meta = pyogrio.read_info(file_path)
        
        # 1. Spatial & Structural Metadata
        geom_type = meta.get('geometry_type', 'Unknown')
        crs = meta.get('crs', 'Unknown CRS')
        feat_count = meta.get('features_count', 0)
        fields = meta.get('fields', [])
        field_types = meta.get('field_types', [])
        
        output = [
            f"Type: FlatGeobuf Binary Spatial Data (.fgb)",
            f"Geometry Type: {geom_type}",
            f"Coordinate System: {crs}",
            f"Total Features: {feat_count}",
            f"Attribute Schema ({len(fields)} columns):"
        ]

        # 2. Exhaustive Attribute Schema (Zero Truncation)
        # Create a list of "ColumnName (DataType)"
        schema_items = [f"{name} ({dtype})" for name, dtype in zip(fields, field_types)]
        schema_text = ", ".join(schema_items)

        # 3. Intelligent Wrapping to protect the tree branching
        # wrap_indent matches the current metadata block indentation
        wrap_indent = indent_level + " " * 2
        
        wrapper = textwrap.TextWrapper(
            width=100, 
            subsequent_indent=wrap_indent + "  "
        )
        
        if schema_items:
            output.append(wrapper.fill(schema_text))
        else:
            output.append("  (No attributes found)")

        return "\n".join(output)

    except Exception as e:
        return f"FGB Extraction Error: {str(e)}".replace('\n', ' ')