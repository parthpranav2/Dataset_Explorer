import pandas as pd
import numpy as np

def extract(file_path):
    """
    Generalized CSV feature extractor.
    Returns a newline-separated string of column metadata for the tree generator.
    """
    try:
        # Read a representative sample
        df_sample = pd.read_csv(file_path, nrows=1000)
        
        if df_sample.empty:
            return "Empty CSV"

        num_rows = len(df_sample)
        cols = df_sample.columns.tolist()
        
        # Limit columns to prevent overwhelming the LLM
        MAX_COLS = 30 
        display_cols = cols[:MAX_COLS]
        
        stats = []
        for col in display_cols:
            dtype = str(df_sample[col].dtype)
            null_count = df_sample[col].isnull().sum()
            null_pct = (null_count / num_rows) * 100
            
            # Feature Exploration
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
            
            # Format each feature as a single distinct line
            stats.append(f"{col} [{dtype}, {null_pct:.1f}% null, {summary}]")

        # Add a counter for remaining columns if truncated
        if len(cols) > MAX_COLS:
            stats.append(f"... (+{len(cols) - MAX_COLS} more columns)")

        # Join with newlines to trigger the multi-line tree handler
        return "\n".join(stats)

    except Exception as e:
        return f"Error extracting: {str(e)}".replace('\n', ' ')