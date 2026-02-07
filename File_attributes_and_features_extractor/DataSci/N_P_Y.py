import sys
import os

# --- RIGOROUS ENVIRONMENT PROTOCOL ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
venv_site_packages = os.path.join(project_root, 'venv', 'lib', 'python3.9', 'site-packages')

if os.path.exists(venv_site_packages):
    sys.path.insert(0, venv_site_packages)

try:
    import numpy as np
except ImportError:
    np = None
# -------------------------------------

def extract(file_path):
    """
    Exhaustively explores .npy NumPy binary files.
    Zero truncation: identifies array shape, dtype, and numerical distribution.
    """
    if not np:
        return "Error: NumPy library not found in venv."

    try:
        # Load with mmap_mode to avoid loading massive arrays entirely into RAM
        data = np.load(file_path, mmap_mode='r')
        
        # 1. Structural Metadata
        shape = data.shape
        dtype = data.dtype
        size_bytes = os.path.getsize(file_path)
        
        # 2. Numerical Audit (Sampled if array is massive)
        if data.size > 1000000:
            sample = data.flatten()[:1000000]
            note = " (Sampled first 1M elements)"
        else:
            sample = data
            note = ""

        f_min, f_max = np.min(sample), np.max(sample)
        f_mean = np.mean(sample)

        output = [
            "Type: NumPy Binary Array (.npy)",
            f"Array Shape: {shape}",
            f"Data Type:   {dtype}",
            f"Memory Footprint: {size_bytes / (1024**2):.2f} MB",
            f"Numerical Range{note}:",
            f"  - Min:  {f_min}",
            f"  - Max:  {f_max}",
            f"  - Mean: {f_mean:.4f}",
            f"Layout: {'Fortran-order' if np.isfortran(data) else 'C-order'}"
        ]

        return "\n".join(output)

    except Exception as e:
        return f"NPY Extraction Error: {str(e)}"