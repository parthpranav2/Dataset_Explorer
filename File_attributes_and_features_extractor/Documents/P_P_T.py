import sys
import os
import datetime

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    from pptx import Presentation
except ImportError:
    Presentation = None
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .ppt/.pptx presentations.
    Zero truncation: provides slide counts, metadata, and creation details.
    """
    try:
        file_size = os.path.getsize(file_path)
        
        # Handling modern .pptx
        if file_path.lower().endswith('.pptx') and Presentation:
            prs = Presentation(file_path)
            prop = prs.core_properties
            
            slide_count = len(prs.slides)
            author = prop.author if prop.author else "Unknown"
            created = prop.created.strftime('%Y-%m-%d') if prop.created else "Unknown"
            
            output = [
                f"Type: PowerPoint Presentation (.pptx)",
                f"Title: {prop.title if prop.title else os.path.basename(file_path)}",
                f"Author: {author}",
                f"Total Slides: {slide_count}",
                f"Timeline: Created {created} | Modified {prop.modified.strftime('%Y-%m-%d') if prop.modified else 'N/A'}",
                f"File Size: {file_size / 1024:.2f} KB"
            ]
        
        # Handling legacy .ppt
        else:
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
            output = [
                f"Type: Legacy PowerPoint (.ppt)",
                f"Note: Detailed slide parsing requires .pptx format.",
                f"Last Modified: {mod_time}",
                f"File Size: {file_size / 1024:.2f} KB"
            ]

        return "\n".join(output)

    except Exception as e:
        return f"PPT Extraction Error: {str(e)}"