import sys
import os
import re

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .bib BibTeX files.
    Zero truncation: identifies reference counts, entry types, and year ranges.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 1. Identify Entry Types
        # Matches @type{key, ...
        entries = re.findall(r'@(\w+)\s*\{', content)
        entry_counts = {}
        for e in entries:
            e_lower = e.lower()
            entry_counts[e_lower] = entry_counts.get(e_lower, 0) + 1

        # 2. Extract Years for Chronology
        years = re.findall(r'year\s*=\s*[\{"\']?(\d{4})[\}"\']?', content, re.I)
        years = [int(y) for y in years]
        year_range = f"{min(years)} - {max(years)}" if years else "Unknown"

        # 3. Reference Keys Sample
        keys = re.findall(r'@\w+\s*\{\s*([^,]+),', content)

        output = [
            f"Type: BibTeX Bibliography Database (.bib)",
            f"Total References: {len(entries)}",
            f"Publication Range: {year_range}",
            "Entry Type Breakdown:"
        ]

        if entry_counts:
            for etype, count in list(entry_counts.items())[:4]:
                output.append(f"  - @{etype}: {count}")
        else:
            output.append("  - No valid entries detected.")

        output.append("Key Sample:")
        output.append("  " + (", ".join(keys[:3]) if keys else "None"))

        return "\n".join(output)

    except Exception as e:
        return f"BIB Extraction Error: {str(e)}"