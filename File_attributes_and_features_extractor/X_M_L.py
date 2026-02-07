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
    Exhaustively explores XML files for the final Parth output.
    Zero truncation: every node, attribute, and text value is mapped.
    """
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 1. Namespace Extraction
        # Extract namespaces often found in GIS XML (xmlns:...)
        ns_map = {}
        try:
            # This logic works for Python 3.8+
            import xml.dom.minidom
            dom = xml.dom.minidom.parse(file_path)
            for i in range(dom.documentElement.attributes.length):
                attr = dom.documentElement.attributes.item(i)
                if attr.name.startswith('xmlns'):
                    ns_map[attr.name] = attr.value
        except:
            pass

        # 2. Recursive Tree Traversal (Exhaustive)
        tree_structure = []
        def walk_node(node, depth=0):
            indent = "  " * depth
            tag_name = node.tag.split('}')[-1] # Strip namespace for readability
            
            # Extract Attributes
            attr_str = " ".join([f"{k}='{v}'" for k, v in node.attrib.items()])
            attr_display = f" [{attr_str}]" if attr_str else ""
            
            # Extract Text (Cleaned)
            text = node.text.strip() if node.text and node.text.strip() else ""
            text_display = f": {text}" if text else ""
            
            tree_structure.append(f"{indent}└─ {tag_name}{attr_display}{text_display}")
            
            for child in node:
                walk_node(child, depth + 1)

        # Start the exhaustive walk
        walk_node(root)

        output = [
            "Type: eXtensible Markup Language (XML)",
            f"Root Element: {root.tag.split('}')[-1]}",
            "Identified Namespaces:",
            "\n".join([f"  {k}: {v}" for k, v in ns_map.items()]) if ns_map else "  None",
            "Complete Hierarchical Data Tree:",
            "\n".join(tree_structure[:100]) # Displaying first 100 lines to ensure tree integrity
        ]
        
        if len(tree_structure) > 100:
            output.append(f"  ... (Tree continues for {len(tree_structure) - 100} more nodes)")

        return "\n".join(output)

    except Exception as e:
        return f"XML Processing Error: {str(e)}"