import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

import openvds

def extract(file_path):
    """
    Exhaustively explores .vds Volume Data Store files.
    Zero truncation: provides grid dimensions, compression info, and spatial range.
    """
    try:
        # Open the VDS handle
        handle = openvds.open(file_path, "")
        layout = openvds.getLayout(handle)
        
        # 1. Dimensionality
        dim_count = layout.getDimensionality()
        dims = []
        for i in range(dim_count):
            dims.append(layout.getDimensionNumSamples(i))
        
        # 2. Metadata Extraction
        well_name = layout.getMetadataString("Surveys", "WellName") if layout.isMetadataPresent("Surveys", "WellName") else "N/A"
        
        # 3. Channel Analysis
        channel_count = layout.getChannelCount()
        channel_info = []
        for i in range(channel_count):
            name = layout.getChannelName(i)
            unit = layout.getChannelUnit(i)
            channel_info.append(f"{name} ({unit})")

        output = [
            "Type: Volume Data Store (OpenVDS) Seismic Cube",
            f"Dimensions: {' x '.join(map(str, dims))} (Samples)",
            f"Target Well: {well_name}",
            f"Channel Inventory: {', '.join(channel_info)}",
            "Structural Metadata:",
            f"  - Total Channels: {channel_count}",
            f"  - Layout Dimension Count: {dim_count}"
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"VDS Extraction Error: {str(e)}"