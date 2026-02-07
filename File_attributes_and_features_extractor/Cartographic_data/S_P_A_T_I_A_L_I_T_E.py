import sys
import os
import sqlite3

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up two levels (GIS -> File_attributes_and_features_extractor -> Project Root)
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores SpatiaLite databases.
    Lists every table, spatial metadata, and full samples with zero truncation.
    """
    try:
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        
        # 1. Get all tables from the master catalog
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        # 2. Get spatial metadata to identify geometry columns
        spatial_meta = {}
        try:
            cursor.execute("SELECT f_table_name, f_geometry_column, type, srid FROM geometry_columns;")
            for row in cursor.fetchall():
                spatial_meta[row[0]] = {"col": row[1], "type": row[2], "srid": row[3]}
        except:
            pass # Not a SpatiaLite-initialized file or table missing

        detail_lines = []
        for table in tables:
            is_spatial = table in spatial_meta
            header = f"Table: {table} " + (f"[Spatial: {spatial_meta[table]['type']}, SRID: {spatial_meta[table]['srid']}]" if is_spatial else "[Relational]")
            detail_lines.append(header)
            
            # 3. Full Schema Extraction
            cursor.execute(f"PRAGMA table_info('{table}');")
            columns = cursor.fetchall()
            detail_lines.append("  Full Schema:")
            for col in columns:
                detail_lines.append(f"    {col[1]} ({col[2]}) {'[PK]' if col[5] else ''}")
            
            # 4. Full Data Sample (First Record)
            cursor.execute(f"SELECT * FROM '{table}' LIMIT 1;")
            row = cursor.fetchone()
            if row:
                col_names = [c[1] for c in columns]
                # No truncation: show all values. For geometry, show a snippet or 'BLOB'
                sample_parts = []
                for name, val in zip(col_names, row):
                    if is_spatial and name == spatial_meta[table]['col']:
                        sample_parts.append(f"{name}: [GEOMETRY BLOB]")
                    else:
                        sample_parts.append(f"{name}: {val}")
                detail_lines.append(f"  Full Sample Record: {' | '.join(sample_parts)}")
            else:
                detail_lines.append("  Sample: Table is empty")
        
        conn.close()

        output = [
            "Type: SpatiaLite Geographic Database",
            f"Total Tables: {len(tables)}",
            "Exhaustive Database Exploration:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SpatiaLite Error: {str(e)}"