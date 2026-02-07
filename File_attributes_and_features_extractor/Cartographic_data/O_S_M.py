import sys
import os
import xml.etree.ElementTree as ET

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores OSM XML files.
    Zero truncation: every unique tag key and entity count is displayed.
    """
    try:
        counts = {'node': 0, 'way': 0, 'relation': 0}
        unique_keys = set()
        bounds = "Not Defined"
        sample_tags = []

        # Use iterparse to handle potentially large XML files efficiently
        context = ET.iterparse(file_path, events=('start', 'end'))
        
        for event, elem in context:
            if event == 'start':
                if elem.tag == 'bounds':
                    bounds = f"Min(Lat:{elem.get('minlat')}, Lon:{elem.get('minlon')}) Max(Lat:{elem.get('maxlat')}, Lon:{elem.get('maxlon')})"
                
                if elem.tag in counts:
                    counts[elem.tag] += 1
                
                if elem.tag == 'tag':
                    k = elem.get('k')
                    unique_keys.add(k)
                    # Capture a few samples for context
                    if len(sample_tags) < 5:
                        sample_tags.append(f"{k}={elem.get('v')}")
            
            # Clear element to save memory
            if event == 'end':
                elem.clear()

        output = [
            "Type: OpenStreetMap XML (.osm)",
            f"Spatial Bounds: {bounds}",
            "Entity Inventory:",
            f"  Nodes: {counts['node']}",
            f"  Ways: {counts['way']}",
            f"  Relations: {counts['relation']}",
            "Exhaustive Tag Schema (Unique Keys):",
            f"  {', '.join(sorted(list(unique_keys)))}",
            "Metadata Samples:",
            f"  {', '.join(sample_tags)}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"OSM Error: {str(e)}"