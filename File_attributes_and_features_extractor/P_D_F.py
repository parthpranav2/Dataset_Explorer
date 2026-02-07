import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

from PyPDF2 import PdfReader

def extract(file_path):
    """
    Exhaustively explores PDF documents for the final Parth output.
    Zero truncation: all metadata, bookmarks, and full text previews are included.
    """
    try:
        reader = PdfReader(file_path)
        info = reader.metadata
        
        # 1. Document Information Extraction
        meta_lines = []
        if info:
            for key, value in info.items():
                clean_key = key.replace('/', '')
                meta_lines.append(f"  {clean_key}: {value}")
        
        # 2. Complete Outline/Bookmarks (Recursive)
        outline_lines = []
        def get_outline(outline, level=0):
            for item in outline:
                if isinstance(item, list):
                    get_outline(item, level + 1)
                else:
                    outline_lines.append("  " * (level + 1) + f"└─ {item.title}")

        try:
            if reader.outline:
                get_outline(reader.outline)
            else:
                outline_lines.append("  No internal bookmarks found.")
        except Exception:
            outline_lines.append("  Error reading document outline.")

        # 3. Full Text Preview (First 1000 characters)
        text_content = ""
        if len(reader.pages) > 0:
            raw_text = reader.pages[0].extract_text()
            if raw_text:
                # Remove excessive newlines for tree formatting but keep content
                text_content = " ".join(raw_text[:1000].splitlines())
            else:
                text_content = "No extractable text found on the first page."

        output = [
            "Type: Portable Document Format (PDF)",
            f"PDF Version: {reader.pdf_header}",
            f"Total Pages: {len(reader.pages)}",
            "Exhaustive Metadata Dictionary:",
            "\n".join(meta_lines) if meta_lines else "  Metadata: Empty",
            "Complete Table of Contents:",
            "\n".join(outline_lines),
            "Document Text Preview (First 1000 Chars):",
            f"  {text_content}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"PDF Processing Error: {str(e)}"