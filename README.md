# 📂 Dataset Explorer (Geoscience & Engineering Edition)

This repository contains a Python toolkit designed to generate comprehensive text-based documentation of large dataset structures that cannot be directly analyzed by LLMs due to their size.

## Project Goal

The main objective is to create **telescopic hierarchy visualizations** of complex datasets and save them as lightweight `.txt` files. This edition is specifically optimized for **Petroleum Engineering and Geoscience** workflows.

### The Problem
Large subsurface datasets often contain thousands of files with domain-specific extensions (.segy, .las, .petrel) that general-purpose file explorers cannot describe meaningfully.

### Our Solution
A **Zero Truncation Extraction** system. Instead of just listing filenames, the tool peers inside the headers of technical files to extract physical parameters (depths, coordinates, sensor metadata), providing a "structural snapshot" that carries geological context.

## 🛠️ Advanced Subsurface Support

The toolkit features specialized logic for over **110+ extensions**. Below are the key supported formats:

### 🛢️ Petroleum & Well Engineering
| Extension | Description | Extraction Focus |
| :--- | :--- | :--- |
| `.las` / `.dlis` | Log ASCII / Binary | Well headers, curve mnemonics, depth intervals. |
| `.well` / `.wtg` | Well Geometry | Casing points, hole diameters, equipment specs. |
| `.witsml` | Drilling Data | Real-time rig sensor parameters and timestamps. |
| `.dev` | Deviation Surveys | MD, TVD, Azimuth, and Inclination stats. |

### 🌎 Geoscience & Seismic Interpretation
| Extension | Description | Extraction Focus |
| :--- | :--- | :--- |
| `.segy` / `.sgy` | Seismic Data | EBCDIC header scraping, sample rates, byte orders. |
| `.hrz` / `.horizon`| Seismic Horizons | Interpretation density, Z-range (ms vs. meters). |
| `.fault` | Fault Sticks | Fault names, vertical reach, geometry complexity. |
| `.petrel` | Petrel Projects | Software version, CRS mapping, unit systems. |
| `.dim` / `.safe` | Sentinel / SNAP | Satellite mission ID, polarization, acquisition date. |
| `.jp2` / `.sid` | Geo-Rasters | Coordinate systems (CRS), spatial resolution. |

### 📊 Data Science & Machine Learning
| Extension | Description | Extraction Focus |
| :--- | :--- | :--- |
| `.npy` / `.npz` | NumPy Arrays | Array shape, dtype, and numerical distribution. |
| `.pb` / `.h5` | ML Models | Signatures, tensor geometry, Keras metadata. |
| `.netcdf` | Scientific Data | Global attributes, coordinate variables, units. |
| `.csv` / `.json` | Structured Data | Column headers, row counts, key-value samples. |

### 📄 Academic & Documentation
| Extension | Description | Extraction Focus |
| :--- | :--- | :--- |
| `.docx` / `.pptx` | MS Office | Author, revision history, table/image counts. |
| `.tex` / `.bib` | LaTeX / BibTeX | Math environments, packages, citation keys. |
| `.md` | Markdown | Heading hierarchy, code blocks, link density. |



## Features

✅ **Deep ZIP Exploration** - Recursively analyzes nested ZIPs without extraction.  
✅ **Zero Truncation Metadata** - Extracts units, CRS, and ranges for technical files.  
✅ **Extension Analytics** - Generates statistical summaries of file types and sizes.  
✅ **LLM-Ready Context** - Produces lightweight text reports for easy AI analysis.  
✅ **Batch Processing** - Automatically documents multiple datasets in one run.  

## Dataset Structure Example
```text
📂 Oil_Field_Alpha
├── 📁 Seismic
│   ├── 📄 Survey_3D.sgy {Size: 2.4GB, Type: SEGY, SampleRate: 4ms}
│   └── 📄 Top_Reservoir.horizon {Size: 12MB, Nodes: 45k, Domain: Time}
├── 📁 Well_Logs
│   ├── 📄 Well_01.las {Size: 5MB, Curves: [GR, NPHI, RHOB, DT]}
│   └── 🗜️ Core_Photos.zip
│       └── 📄 Core_Sample_A1.jp2 {Res: 10cm, CRS: UTM45N}

## How It Works: A 3-Step Workflow

### 1. Tree Structure Generation
The `print_tree()` function recursively traverses directories and ZIP files, building a visual tree structure with:
- Directory hierarchy using box-drawing characters (`├──`, `└──`, `│`)
- Visual indicators for folders (📁) and ZIPs (🗜️)
- Complete file metadata for every item

### 2. Extension Analysis
The `count_extensions()` function scans all files (including those inside ZIPs) and generates:
- Count of files per extension
- Cumulative size per file type
- Percentage distribution statistics

**Example Output:**
```
📊 Extension Summary
================================================================================
Extension            Count   Percentage      Total Size
--------------------------------------------------------------------------------
.csv                    45       35.7%        125.43 MB
.xlsx                   32       25.4%         87.21 MB
.json                   28       22.2%         45.67 MB
.zip                    21       16.7%        234.89 MB
--------------------------------------------------------------------------------
TOTAL                  126      100.0%        493.20 MB
================================================================================
```

### 3. Batch Processing & Auto-Save
The `process_batch_datasets()` function:
- Scans one directory level for datasets (folders or ZIPs)
- Processes each dataset independently
- Saves individual `.txt` reports alongside each dataset
- Shows progress as it works through multiple datasets

## Key Technologies Used

* **Python 3**
* **zipfile & BytesIO** (For ZIP exploration without extraction)
* **os & pathlib** (For file system navigation)
* **collections.defaultdict** (For efficient extension counting)
* **datetime** (For timestamp formatting)
* **Jupyter Notebook** (Interactive development environment)

## Usage

### For Single Dataset Analysis
```python
# Set your dataset path (directory or ZIP file)
path = "/Volumes/PPS32/UKCS/Pressure.zip"

# Generate tree structure
print_tree(save_to_string=True)

# Count extensions
count_extensions(show_zip_contents=True)

# Save to file
base_name = os.path.splitext(os.path.basename(path))[0]
output_filename = f"directory_tree_{base_name}.txt"
save_tree_to_file(output_filename, tree_output, include_summary=True)
```

### For Batch Processing
```python
# Set parent directory containing multiple datasets
parent_directory = "/Volumes/PPS32/UKCS"

# Process all datasets automatically
process_batch_datasets(parent_directory, show_zip_contents=True)
```

## Output Files

Each analysis generates a `.txt` file containing:
1. **Extension Summary** - Statistical breakdown of file types
2. **Directory Structure** - Complete telescopic hierarchy with metadata

Files are saved at the same level as the analyzed datasets for easy organization.

## Sample Output File
```
📊 Extension Summary
================================================================================
Extension            Count   Percentage      Total Size
--------------------------------------------------------------------------------
.las                   156       45.2%        2.34 GB
.csv                    98       28.4%        876.23 MB
.xlsx                   67       19.4%        543.12 MB
.zip                    24        7.0%        1.23 GB
--------------------------------------------------------------------------------
TOTAL                  345      100.0%        4.99 GB
================================================================================

Directory Structure:
============================================================
📂 Pressure
├── 📁 Well_Logs
│   ├── 📄 Well_A.las {Size: 15.2MB, Type: LAS, Modified: 2024-01-15}
│   ├── 📄 Well_B.las {Size: 12.8MB, Type: LAS, Modified: 2024-01-16}
│   └── 🗜️ Archive_2023.zip
│       ├── 📄 Q1_data.csv {Size: 45.6MB, Modified: 2023-03-30}
│       └── 📄 Q2_data.csv {Size: 52.3MB, Modified: 2023-06-30}
...
============================================================
```

## Why This Matters

This tool bridges the gap between **massive datasets** and **AI-assisted analysis**. By creating lightweight structural documentation, you can:
- 🤖 Feed dataset context to LLMs without hitting token limits
- 👥 Share dataset structures with collaborators instantly
- 📝 Version control your data organization
- 🔍 Quickly audit and validate data integrity
- 📊 Generate documentation for research papers or reports

## Repository Structure
```
📂 dataset-structure-analyzer/
├── 📄 tree_generator.py          # Core tree visualization functions
├── 📄 extension_counter.py       # Extension analysis and statistics
├── 📄 batch_processor.py         # Batch processing for multiple datasets
├── 📄 file_saver.py              # Output file generation
├── 📓 analysis_notebook.ipynb    # Jupyter notebook with complete workflow
└── 📄 README.md                  # This file
```

## License

This project is open source and available for educational and research purposes.

---

**Built for researchers, data scientists, and anyone dealing with complex dataset hierarchies that need to be understood before they can be analyzed.**
