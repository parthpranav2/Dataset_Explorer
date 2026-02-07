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
    Exhaustively explores .md markdown files.
    Zero truncation: identifies hierarchy, code blocks, and links.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # 1. Structural Audit (Headers)
        h1 = len(re.findall(r'^#\s', content, re.M))
        h2 = len(re.findall(r'^##\s', content, re.M))
        h3 = len(re.findall(r'^###\s', content, re.M))

        # 2. Content Density
        code_blocks = len(re.findall(r'```', content)) // 2
        links = len(re.findall(r'\[.*?\]\(.*?\)', content))
        images = len(re.findall(r'!\[.*?\]\(.*?\)', content))

        # 3. Extract Title (First H1 or First Line)
        title_match = re.search(r'^#\s+(.*)', content, re.M)
        title = title_match.group(1).strip() if title_match else "No H1 Title Found"

        output = [
            f"Type: Markdown Documentation (.md)",
            f"Primary Title: {title}",
            "Document Structure:",
            f"  - Hierarchy: {h1} H1 | {h2} H2 | {h3} H3",
            f"  - Technical: {code_blocks} Code Blocks",
            f"  - Assets:    {links} Links | {images} Images",
            f"Reading Estimate: ~{len(content.split()) // 200 + 1} min"
        ]

        return "\n".join(output)

    except Exception as e:
        return f"MD Extraction Error: {str(e)}"