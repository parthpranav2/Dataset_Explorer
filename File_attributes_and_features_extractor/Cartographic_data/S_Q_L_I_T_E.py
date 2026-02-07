import sys
import os
import sqlite3

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
# Moves up two levels to Project Root
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores SQLite databases.
    Lists every table, every column, and full samples for zero truncation.
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        
        # 1. Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        detail_lines = []
        for table in tables:
            detail_lines.append(f"Table: {table}")
            
            # 2. Get Full Column Schema
            cursor.execute(f"PRAGMA table_info('{table}');")
            columns = cursor.fetchall()
            detail_lines.append("  Full Schema:")
            for col in columns:
                # cid, name, type, notnull, dflt_value, pk
                detail_lines.append(f"    {col[1]} ({col[2]}) {'[PK]' if col[5] else ''}")
            
            # 3. Full Data Sample (First Record)
            cursor.execute(f"SELECT * FROM '{table}' LIMIT 1;")
            row = cursor.fetchone()
            if row:
                col_names = [c[1] for c in columns]
                sample_parts = [f"{name}: {val}" for name, val in zip(col_names, row)]
                detail_lines.append(f"  Full Sample Record: {' | '.join(sample_parts)}")
            else:
                detail_lines.append("  Sample: Table is empty")
        
        conn.close()

        output = [
            "Type: SQLite Relational Database",
            f"Total Tables Found: {len(tables)}",
            "Exhaustive Database Content:",
            "\n".join(detail_lines)
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SQLite Error: {str(e)}"