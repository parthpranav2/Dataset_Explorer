import pandas as pd
import numpy as np
import textwrap
import os

def extract(file_path, indent_level=""):
    """
    Exhaustively explores every sheet and column in an Excel (.xlsx) workbook.
    Zero truncation: Lists all features with alignment protection to prevent 
    cutting the directory tree branching.
    """
    try:
        # Load the Excel file to access all sheets
        xl = pd.ExcelFile(file_path, engine='openpyxl')
        sheet_names = xl.sheet_names
        
        output = [f"Type: Excel Workbook (.xlsx) | Total Sheets: {len(sheet_names)}"]
        
        # Calculate the wrap indent to keep vertical tree bars aligned
        # Subsequent lines will be pushed right to stay under the metadata block
        wrap_indent = indent_level + " " * 2

        for sheet in sheet_names:
            # Read a sample to extract metadata without heavy memory usage
            # Preserving the same logic used in your CSV extractor
            df = pd.read_excel(xl, sheet_name=sheet, nrows=1000)
            
            if df.empty:
                output.append(f" Sheet: [{sheet}] (Empty)")
                continue

            cols = df.columns.tolist()
            num_rows = len(df)
            
            output.append(f" Sheet: [{sheet}] ({num_rows} rows sampled)")

            for col in cols:
                dtype = str(df[col].dtype)
                null_count = df[col].isnull().sum()
                null_pct = (null_count / num_rows) * 100 if num_rows > 0 else 0
                
                # Feature Exploration (Your original statistical logic)
                if pd.api.types.is_numeric_dtype(df[col]):
                    c_min = df[col].min()
                    c_max = df[col].max()
                    c_mean = df[col].mean()
                    # Handling NaN cases in summary
                    summary = f"num(min:{c_min:.2f}, max:{c_max:.2f}, avg:{c_mean:.2f})" if not np.isnan(c_mean) else "num(all NaN)"
                else:
                    unique_count = df[col].nunique()
                    # Safely handle mode for categorical data
                    mode_val = df[col].mode()
                    top_val = str(mode_val.iloc[0])[:15] if not mode_val.empty else "N/A"
                    summary = f"cat(uniques:{unique_count}, top:'{top_val}')"
                
                # Format the feature line
                feature_text = f"   {col}: [{dtype}, {null_pct:.1f}% null, {summary}]"
                
                # Apply intelligent wrapping to protect the tree branching
                # width set to 100 to balance readability and directory depth
                wrapper = textwrap.TextWrapper(
                    width=100, 
                    subsequent_indent=wrap_indent + "      "
                )
                output.append(wrapper.fill(feature_text))

        return "\n".join(output)

    except Exception as e:
        return f"XLSX Extraction Error: {str(e)}".replace('\n', ' ')