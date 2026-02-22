import pandas as pd
import numpy as np
import textwrap

def extract(file_path, indent_level=""):
    """
    Generalized CSV feature extractor.
    Returns every single column metadata without cutting the branching structure.
    """
    try:
        # Read a representative sample (Your original logic)
        df_sample = pd.read_csv(file_path, nrows=1000)
        
        if df_sample.empty:
            return "Empty CSV"

        num_rows = len(df_sample)
        cols = df_sample.columns.tolist()
        
        # --- MODIFICATION: Removed MAX_COLS limit to show all features ---
        
        stats = []
        # Calculate the wrapping indent to match the current tree branching
        # We add extra spaces to align under the start of the text
        wrap_indent = indent_level + " " * 2 

        for col in cols:
            dtype = str(df_sample[col].dtype)
            null_count = df_sample[col].isnull().sum()
            null_pct = (null_count / num_rows) * 100
            
            # Feature Exploration (Your original logic)
            if pd.api.types.is_numeric_dtype(df_sample[col]):
                # Numerical summary: Range and Average
                c_min = df_sample[col].min()
                c_max = df_sample[col].max()
                c_mean = df_sample[col].mean()
                summary = f"num(min:{c_min:.2f}, max:{c_max:.2f}, avg:{c_mean:.2f})"
            else:
                # Categorical summary: Cardinality and Top Example
                unique_count = df_sample[col].nunique()
                top_val = str(df_sample[col].mode().iloc[0])[:15] if not df_sample[col].mode().empty else "N/A"
                summary = f"cat(uniques:{unique_count}, top:'{top_val}')"
            
            # Create the feature string
            feature_text = f"{col} [{dtype}, {null_pct:.1f}% null, {summary}]"
            
            # --- MODIFICATION: Line wrapping to prevent cutting the branching ---
            # subsequnt_indent ensures wrapped lines stay within the metadata block
            wrapper = textwrap.TextWrapper(
                width=100, 
                subsequent_indent=wrap_indent + "  "
            )
            stats.append(wrapper.fill(feature_text))

        # Join with newlines to trigger the multi-line tree handler
        return "\n".join(stats)

    except Exception as e:
        return f"Error extracting: {str(e)}".replace('\n', ' ')