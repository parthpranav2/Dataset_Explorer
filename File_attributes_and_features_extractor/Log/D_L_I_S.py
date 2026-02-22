"""
DLIS File Extractor for Directory Tree Analysis
Extracts comprehensive metadata from .dlis files using dlisio library
Author: Expert Python Developer specializing in Petroleum Engineering data standards
"""

from dlisio import dlis
import numpy as np


def extract(file_path):
    """
    Extract comprehensive metadata from a DLIS file.

    Args:
        file_path (str): Path to the .dlis file

    Returns:
        str: Formatted string with all extracted metadata, indented with 2 spaces per line
    """
    try:
        # Load the DLIS file using the required syntax
        f, *tail = dlis.load(file_path)

        output_lines = []

        # ===================================================================
        # SECTION 1: ORIGIN DATA
        # ===================================================================
        if f.origins:
            origin = f.origins[0]
            output_lines.append("Origin Data:")

            # Extract well name
            try:
                well_name = origin.well_name if hasattr(origin, 'well_name') else "N/A"
                output_lines.append(f"  Well Name: {well_name}")
            except:
                output_lines.append("  Well Name: N/A")

            # Extract field name
            try:
                field = origin.field_name if hasattr(origin, 'field_name') else "N/A"
                output_lines.append(f"  Field: {field}")
            except:
                output_lines.append("  Field: N/A")

            # Extract company/producer
            try:
                company = origin.producer_name if hasattr(origin, 'producer_name') else "N/A"
                output_lines.append(f"  Company: {company}")
            except:
                output_lines.append("  Company: N/A")

            # Extract creation date
            try:
                creation_date = origin.creation_time if hasattr(origin, 'creation_time') else "N/A"
                output_lines.append(f"  Creation Date: {creation_date}")
            except:
                output_lines.append("  Creation Date: N/A")

            # Additional origin metadata
            try:
                if hasattr(origin, 'producer_code'):
                    output_lines.append(f"  Producer Code: {origin.producer_code}")
            except:
                pass

            try:
                if hasattr(origin, 'order_number'):
                    output_lines.append(f"  Order Number: {origin.order_number}")
            except:
                pass

            try:
                if hasattr(origin, 'file_set_name'):
                    output_lines.append(f"  File Set Name: {origin.file_set_name}")
            except:
                pass

            try:
                if hasattr(origin, 'file_set_number'):
                    output_lines.append(f"  File Set Number: {origin.file_set_number}")
            except:
                pass

            try:
                if hasattr(origin, 'file_number'):
                    output_lines.append(f"  File Number: {origin.file_number}")
            except:
                pass

            try:
                if hasattr(origin, 'file_type'):
                    output_lines.append(f"  File Type: {origin.file_type}")
            except:
                pass

        else:
            output_lines.append("Origin Data: Not Available")

        output_lines.append("")

        # ===================================================================
        # SECTION 2: FILE SUMMARY
        # ===================================================================
        output_lines.append("File Summary:")

        # Count frames
        frame_count = len(f.frames) if f.frames else 0
        output_lines.append(f"  Total Frames: {frame_count}")

        # Count channels
        channel_count = len(f.channels) if f.channels else 0
        output_lines.append(f"  Total Channels: {channel_count}")

        # Additional file metadata
        try:
            if hasattr(f, 'fileheader') and f.fileheader:
                fh = f.fileheader
                if hasattr(fh, 'id'):
                    output_lines.append(f"  Logical File ID: {fh.id}")
        except:
            pass

        # Count other objects
        try:
            if f.tools:
                output_lines.append(f"  Total Tools: {len(f.tools)}")
        except:
            pass

        try:
            if f.parameters:
                output_lines.append(f"  Total Parameters: {len(f.parameters)}")
        except:
            pass

        try:
            if f.comments:
                output_lines.append(f"  Total Comments: {len(f.comments)}")
        except:
            pass

        output_lines.append("")

        # ===================================================================
        # SECTION 3: FRAME INVENTORY
        # ===================================================================
        if f.frames:
            output_lines.append("Frame Inventory:")

            for frame_idx, frame in enumerate(f.frames, 1):
                output_lines.append(f"  Frame #{frame_idx}:")

                # Frame name
                frame_name = frame.name if hasattr(frame, 'name') else "N/A"
                output_lines.append(f"    Name: {frame_name}")

                # Index type
                try:
                    index_type = frame.index_type if hasattr(frame, 'index_type') else "N/A"
                    output_lines.append(f"    Index Type: {index_type}")
                except:
                    output_lines.append("    Index Type: N/A")

                # Get index channel units by matching frame.index with channel names
                index_units = "N/A"
                try:
                    if hasattr(frame, 'index') and hasattr(frame, 'channels'):
                        for channel in frame.channels:
                            if channel.name == frame.index:
                                index_units = channel.units if hasattr(channel, 'units') else "N/A"
                                break
                except:
                    pass

                # Depth/Time interval
                try:
                    index_min = frame.index_min if hasattr(frame, 'index_min') else None
                    index_max = frame.index_max if hasattr(frame, 'index_max') else None

                    if index_min is not None and index_max is not None:
                        output_lines.append(f"    Interval: {index_min} to {index_max} {index_units}")
                    else:
                        output_lines.append("    Interval: N/A")
                except:
                    output_lines.append("    Interval: N/A")

                # Spacing
                try:
                    spacing = frame.spacing if hasattr(frame, 'spacing') else None
                    if spacing is not None:
                        output_lines.append(f"    Spacing: {spacing} {index_units}")
                    else:
                        output_lines.append("    Spacing: N/A")
                except:
                    output_lines.append("    Spacing: N/A")

                # Direction
                try:
                    direction = frame.direction if hasattr(frame, 'direction') else "N/A"
                    output_lines.append(f"    Direction: {direction}")
                except:
                    output_lines.append("    Direction: N/A")

                # Number of channels in this frame
                try:
                    frame_channel_count = len(frame.channels) if hasattr(frame, 'channels') else 0
                    output_lines.append(f"    Channel Count: {frame_channel_count}")
                except:
                    output_lines.append("    Channel Count: 0")

                output_lines.append("")

        else:
            output_lines.append("Frame Inventory: No frames found")
            output_lines.append("")

        # ===================================================================
        # SECTION 4: CHANNEL INVENTORY (ALL CHANNELS FOR EVERY FRAME)
        # ===================================================================
        if f.frames:
            output_lines.append("Channel Inventory:")

            for frame_idx, frame in enumerate(f.frames, 1):
                output_lines.append(f"  Frame #{frame_idx} ({frame.name}):")

                if hasattr(frame, 'channels') and frame.channels:
                    for channel in frame.channels:
                        try:
                            ch_name = channel.name if hasattr(channel, 'name') else "Unknown"
                            ch_long_name = channel.long_name if hasattr(channel, 'long_name') else ""
                            ch_units = channel.units if hasattr(channel, 'units') else ""
                            ch_dimension = channel.dimension if hasattr(channel, 'dimension') else []

                            # Format channel info
                            ch_info = f"    {ch_name}"

                            if ch_long_name:
                                ch_info += f" - {ch_long_name}"

                            if ch_units:
                                ch_info += f" [{ch_units}]"

                            if ch_dimension and len(ch_dimension) > 0:
                                dim_str = "x".join(str(d) for d in ch_dimension)
                                ch_info += f" (dim: {dim_str})"

                            output_lines.append(ch_info)
                        except:
                            output_lines.append(f"    {channel} (metadata extraction failed)")
                else:
                    output_lines.append("    No channels in this frame")

                output_lines.append("")

        else:
            output_lines.append("Channel Inventory: No frames found")
            output_lines.append("")

        # ===================================================================
        # SECTION 5: TOOL INVENTORY
        # ===================================================================
        if f.tools:
            output_lines.append("Tool Inventory:")

            for tool in f.tools:
                try:
                    tool_name = tool.name if hasattr(tool, 'name') else "Unknown"
                    tool_desc = tool.description if hasattr(tool, 'description') else "No description"

                    output_lines.append(f"  {tool_name}:")
                    output_lines.append(f"    Description: {tool_desc}")

                    # Try to extract tool parameters if available
                    try:
                        if hasattr(tool, 'parameters') and tool.parameters:
                            output_lines.append(f"    Parameters: {len(tool.parameters)}")

                            # List ALL parameters - no truncation
                            for param in tool.parameters:
                                try:
                                    param_name = param.name if hasattr(param, 'name') else "Unknown"
                                    param_long_name = param.long_name if hasattr(param, 'long_name') else ""
                                    param_values = param.values if hasattr(param, 'values') else []

                                    param_info = f"      {param_name}"
                                    if param_long_name:
                                        param_info += f" ({param_long_name})"
                                    if param_values:
                                        param_info += f": {param_values}"

                                    output_lines.append(param_info)
                                except:
                                    continue
                    except:
                        pass

                    # Try to extract tool channels if available
                    try:
                        if hasattr(tool, 'channels') and tool.channels:
                            output_lines.append(f"    Channels: {len(tool.channels)}")
                    except:
                        pass

                except Exception as e:
                    output_lines.append(f"  Tool (name extraction failed): {str(e)[:50]}")

                output_lines.append("")

        else:
            output_lines.append("Tool Inventory: No tools found")
            output_lines.append("")

        # ===================================================================
        # SECTION 6: DATA INTEGRITY (frame.curves() analysis)
        # ===================================================================
        if f.frames:
            output_lines.append("Data Integrity Check:")

            for frame_idx, frame in enumerate(f.frames, 1):
                output_lines.append(f"  Frame #{frame_idx} ({frame.name}):")

                try:
                    # Get curves data
                    curves = frame.curves()

                    # Calculate total data points
                    if curves is not None:
                        # curves is a structured numpy array
                        total_rows = len(curves)
                        total_channels = len(curves.dtype.names) if hasattr(curves, 'dtype') else 0
                        total_data_points = total_rows * total_channels

                        output_lines.append(f"    Total Rows: {total_rows}")
                        output_lines.append(f"    Total Columns: {total_channels}")
                        output_lines.append(f"    Total Data Points: {total_data_points}")

                        # Calculate statistics for each channel
                        if hasattr(curves, 'dtype') and hasattr(curves.dtype, 'names'):
                            output_lines.append("    Channel Statistics:")

                            for ch_name in curves.dtype.names:
                                try:
                                    ch_data = curves[ch_name]

                                    # Count valid (non-null) values
                                    # Common null values in DLIS: -999.25, -999, nan, inf
                                    valid_mask = ~np.isnan(ch_data) & ~np.isinf(ch_data)
                                    valid_mask = valid_mask & (ch_data != -999.25) & (ch_data != -999)

                                    valid_count = np.sum(valid_mask)
                                    total_count = len(ch_data)
                                    null_count = total_count - valid_count

                                    output_lines.append(f"      {ch_name}: {valid_count} valid, {null_count} null/invalid")

                                    # Add min/max for valid data
                                    if valid_count > 0:
                                        valid_data = ch_data[valid_mask]
                                        ch_min = np.min(valid_data)
                                        ch_max = np.max(valid_data)
                                        ch_mean = np.mean(valid_data)
                                        output_lines.append(f"        Range: {ch_min:.4f} to {ch_max:.4f}, Mean: {ch_mean:.4f}")
                                except Exception as ch_error:
                                    output_lines.append(f"      {ch_name}: Error extracting stats - {str(ch_error)[:50]}")
                    else:
                        output_lines.append("    No curve data available")

                except Exception as e:
                    output_lines.append(f"    Error reading curves: {str(e)[:100]}")

                output_lines.append("")

        else:
            output_lines.append("Data Integrity Check: No frames found")
            output_lines.append("")

        # ===================================================================
        # SECTION 7: ADDITIONAL METADATA
        # ===================================================================
        # Parameters summary
        if f.parameters:
            output_lines.append("Additional Parameters:")
            output_lines.append(f"  Total Parameters: {len(f.parameters)}")

            # List ALL parameters with values - no truncation
            for param in f.parameters:
                try:
                    param_name = param.name if hasattr(param, 'name') else "Unknown"
                    param_long_name = param.long_name if hasattr(param, 'long_name') else ""
                    param_values = param.values if hasattr(param, 'values') else []

                    param_info = f"  {param_name}"
                    if param_long_name:
                        param_info += f" ({param_long_name})"
                    if param_values:
                        # Format values nicely
                        if isinstance(param_values, (list, tuple, np.ndarray)):
                            if len(param_values) > 0:
                                param_info += f": {param_values[0]}"
                        else:
                            param_info += f": {param_values}"

                    output_lines.append(param_info)
                except:
                    continue

            output_lines.append("")

        # Comments if available
        if f.comments:
            output_lines.append("Comments:")
            # List ALL comments - no truncation
            for idx, comment in enumerate(f.comments, 1):
                try:
                    comment_text = str(comment)
                    # Keep full comment text, but limit to 200 chars per comment for readability
                    if len(comment_text) > 200:
                        comment_text = comment_text[:200] + "..."
                    output_lines.append(f"  Comment {idx}: {comment_text}")
                except:
                    output_lines.append(f"  Comment {idx}: Unable to extract")

            output_lines.append("")

        # Return the complete formatted string
        return "\n".join(output_lines)

    except FileNotFoundError:
        return f"  Error: File not found - {file_path}"
    except Exception as e:
        error_msg = str(e)
        return f"  Error: Failed to extract DLIS data - {error_msg[:200]}"


# Example usage and testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Extracting data from: {file_path}\n")
        result = extract(file_path)
        print(result)
    else:
        print("DLIS File Extractor")
        print("Usage: python dlis_extractor.py <path_to_dlis_file>")
        print("\nThis script extracts comprehensive metadata from DLIS files including:")
        print("  - Origin data (well name, field, company, creation date)")
        print("  - File summary (frame and channel counts)")
        print("  - Frame inventory (name, index type, interval, spacing)")
        print("  - Channel inventory (all channels with units and dimensions)")
        print("  - Tool inventory (names, descriptions, parameters)")
        print("  - Data integrity (curve analysis with statistics)")