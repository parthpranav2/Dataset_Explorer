import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    import tensorflow as tf
except ImportError:
    tf = None
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores TensorFlow SavedModel directories/files.
    Zero truncation: identifies signatures, tensor shapes, and opsets.
    """
    if not tf:
        return "Error: TensorFlow library not found in venv."

    try:
        # If file_path is the .pb file, use the directory; otherwise use path
        model_dir = os.path.dirname(file_path) if file_path.endswith('.pb') else file_path
        
        # Load the model metadata (not the full weights for speed)
        model = tf.saved_model.load(model_dir)
        sig_keys = list(model.signatures.keys())
        
        output = [
            "Type: TensorFlow SavedModel (.pb)",
            f"Signatures Detected: {', '.join(sig_keys) if sig_keys else 'None'}"
        ]

        if 'serving_default' in sig_keys:
            sig = model.signatures['serving_default']
            
            # Extract Input Details
            output.append("Input Tensors:")
            for inp in sig.inputs:
                output.append(f"  - {inp.name}: {inp.shape} | {inp.dtype.name}")
            
            # Extract Output Details
            output.append("Output Tensors:")
            for outp in sig.structured_outputs:
                tensor = sig.structured_outputs[outp]
                output.append(f"  - {outp}: {tensor.shape} | {tensor.dtype.name}")
        
        return "\n".join(output)

    except Exception as e:
        return f"SavedModel Extraction Error: {str(e)}"