import lasio

def extract(file_path):
    """
    Extracts LAS metadata into a newline-separated list for clean tree formatting.
    No temporary files are created during this process.
    """
    try:
        # read_header=True is optimized for speed
        las = lasio.read(file_path, ignore_data=True)
        
        # 1. Identity Information
        well = las.well.WELL.value if 'WELL' in las.well else "Unknown"
        uwi = las.well.UWI.value if 'UWI' in las.well else "Unknown"
        
        # 2. Depth Range and Step
        start = las.well.STRT.value
        stop = las.well.STOP.value
        step = las.well.STEP.value
        unit = las.well.STRT.unit if las.well.STRT.unit else "m"
        
        # 3. Curve Mnemonics
        # We list these line-by-line for the 'clean' appearance you requested
        curve_list = [f"  {c.mnemonic}({c.unit if c.unit else ''})" for c in las.curves]
        
        # 4. Assemble the final multi-line output
        lines = [
            f"Well: {well} | UWI: {uwi}",
            f"Range: {start}-{stop} {unit} @ {step} step",
            "Payload Curves:"
        ]
        lines.extend(curve_list)
        
        return "\n".join(lines)

    except Exception as e:
        return f"LAS Error: {str(e)}"