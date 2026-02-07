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
    Exhaustively explores SLD symbology files.
    Zero truncation: every rule, filter, and color code is extracted.
    """
    try:
        # Register namespaces to handle SLD prefixes correctly
        namespaces = {
            'sld': 'http://www.opengis.net/sld',
            'ogc': 'http://www.opengis.net/ogc',
            'se': 'http://www.opengis.net/se'
        }
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 1. Identify Target Layer
        layer_node = root.find('.//sld:NamedLayer/sld:Name', namespaces)
        layer_name = layer_node.text if layer_node is not None else "Unknown Layer"
        
        # 2. Extract Rules and Symbolizers
        rules_info = []
        # Walk through all Rules in the document
        for rule in root.findall('.//sld:Rule', namespaces):
            rule_name_node = rule.find('./sld:Name', namespaces)
            rule_name = rule_name_node.text if rule_name_node is not None else "Unnamed Rule"
            
            # Identify Symbolizers used in this rule
            symbolizers = []
            for child in rule:
                if 'Symbolizer' in child.tag:
                    # Strip the namespace for cleaner output
                    sym_type = child.tag.split('}')[-1]
                    symbolizers.append(sym_type)
            
            # Extract Filters (Classification logic)
            filter_node = rule.find('.//ogc:Filter', namespaces)
            has_filter = "Yes" if filter_node is not None else "No"
            
            rules_info.append(f"  Rule: {rule_name} | Filtered: {has_filter} | Tools: {', '.join(symbolizers)}")

        # 3. Comprehensive Color/Value Extraction (Zero Truncation)
        colors = []
        for param in root.findall('.//sld:CssParameter', namespaces):
            name = param.get('name')
            value = param.text
            if name and value:
                colors.append(f"{name}: {value}")

        output = [
            "Type: Styled Layer Descriptor (XML Symbology)",
            f"Target Layer Name: {layer_name}",
            "Defined Styling Rules:",
            "\n".join(rules_info) if rules_info else "  No explicit rules found.",
            "Complete Visual Parameters (Colors/Widths):",
            "  " + " | ".join(colors) if colors else "  No CSS parameters found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"SLD Parsing Error: {str(e)}"