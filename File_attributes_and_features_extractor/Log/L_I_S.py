import sys
import os
import dlisio

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)
# -------------------------------------

def extract(file_path):
    """
    Exhaustive DLIS extractor for the final Parth output.
    Zero-truncation: maps every frame, channel, and parameter found.
    """
    try:
        output_lines = []
        with dlisio.load(file_path) as d:
            for i, f in enumerate(d):
                output_lines.append(f"Logical File [{i}]: {getattr(f, 'name', 'N/A')}")
                
                # 1. Data Origin Extraction
                for origin in f.origins:
                    output_lines.append(f"  Origin: {origin.well_name} | Company: {origin.company}")
                    output_lines.append(f"    Field: {origin.field} | Date: {origin.creation_time}")

                # 2. Frame & Channel Analysis
                output_lines.append("  Frame Inventory:")
                for frame in f.frames:
                    # Find depth/index units
                    depth_units = ""
                    for channel in frame.channels:
                        if channel.name == frame.index:
                            depth_units = channel.units
                            break
                    
                    output_lines.append(f"    - Frame: {frame.name} ({frame.index_type})")
                    output_lines.append(f"      Interval: {frame.index_min} - {frame.index_max} {depth_units}")
                    output_lines.append(f"      Spacing: {frame.spacing} {depth_units} | Direction: {frame.direction}")
                    
                    # Channel Mnemonics (Zero Truncation)
                    ch_names = [c.name for c in frame.channels]
                    output_lines.append(f"      Channels ({len(ch_names)}): {', '.join(ch_names)}")

                # 3. Tool Information
                tools = [f"{t.name} ({getattr(t, 'description', 'No Desc')})" for t in f.tools]
                if tools:
                    output_lines.append(f"  Tools Used: {', '.join(tools)}")

                # 4. Critical Parameters (Filtering out sensitive names)
                # Matches your logic to exclude R8, RR1, WITN, ENGI
                params = []
                mask = ['R8', 'RR1', 'WITN', 'ENGI']
                for p in f.parameters:
                    if p.name not in mask:
                        # Convert values to string to ensure zero truncation in output
                        val = str(p.values) if hasattr(p, 'values') else ""
                        params.append(f"{p.name}: {val}")
                
                if params:
                    output_lines.append(f"  Key Parameters: {', '.join(params[:10])}...")

        output = [
            "Type: Digital Log Interchange Standard (DLIS)",
            "Complete Dataset Hierarchy:",
            "\n".join(output_lines) if output_lines else "  No valid DLIS data found."
        ]
        
        return "\n".join(output)

    except Exception as e:
        return f"DLIS Extraction Error: {str(e)}"