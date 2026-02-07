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
    Exhaustively explores .tex LaTeX source files.
    Zero truncation: identifies document class, packages, and math environments.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 1. Identify Document Class
        class_match = re.search(r'\\documentclass(?:\[.*?\])?\{(.*?)\}', content)
        doc_class = class_match.group(1) if class_match else "Unknown"

        # 2. Package Audit
        packages = re.findall(r'\\usepackage(?:\[.*?\])?\{(.*?)\}', content)
        unique_pkgs = list(dict.fromkeys(packages))

        # 3. Structural & Math Density
        math_env = len(re.findall(r'\\begin\{equation\}|\\begin\{align\}|\$\$', content))
        inline_math = len(re.findall(r'(?<!\\)\$', content)) // 2
        figures = len(re.findall(r'\\includegraphics', content))
        citations = len(re.findall(r'\\cite\{', content))

        output = [
            f"Type: LaTeX Source Document (.tex)",
            f"Document Class: {doc_class}",
            f"Package Count: {len(unique_pkgs)} packages loaded",
            "Technical Density:",
            f"  - Math: {math_env} Display Envs | {inline_math} Inline Math",
            f"  - Assets: {figures} Figures | {citations} Citations",
            "Core Packages:",
            "  " + (", ".join(unique_pkgs[:5]) if unique_pkgs else "None detected")
        ]

        return "\n".join(output)

    except Exception as e:
        return f"TEX Extraction Error: {str(e)}"