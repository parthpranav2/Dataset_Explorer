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
    Exhaustively explores .fault interpretation files.
    Zero truncation: identifies fault sticks, vertical range, and metadata.
    """
    try:
        stick_count = 0
        total_points = 0
        z_vals = []
        fault_name = "Unknown Fault"
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                clean_line = line.strip()
                if not clean_line: continue

                # 1. Scrape Header for Fault Identity
                if "name" in clean_line.lower() and "=" in clean_line:
                    fault_name = clean_line.split('=')[-1].strip().replace('"', '')

                # 2. Count Sticks and Points
                # Fault sticks often start with a specific keyword like 'BEGIN' or 'STICK'
                if "STICK" in clean_line.upper() or "BEGIN" in clean_line.upper():
                    stick_count += 1
                
                # 3. Extract Coordinates
                nums = re.findall(r"[-+]?\d*\.\d+|\d+", clean_line)
                if len(nums) >= 3:
                    try:
                        z_vals.append(float(nums[-1]))
                        total_points += 1
                    except ValueError:
                        continue

        output = [
            "Type: Structural Fault Interpretation (.fault)",
            f"Fault Name: {fault_name}",
            f"Geometry: {stick_count} sticks | {total_points} total points",
            f"Vertical Extent: {min(z_vals) if z_vals else 'N/A'} to {max(z_vals) if z_vals else 'N/A'}",
            "Structural Context:",
            f"  - Complex Surface: {'Yes' if total_points > 100 else 'No (Simple Stick Set)'}"
        ]

        return "\n".join(output)

    except Exception as e:
        return f"FAULT Extraction Error: {str(e)}"