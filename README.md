# Misconfiguration Chart Generator

This project parses a CSV of misconfiguration findings, aggregates counts for “Critical” and “High” severities, and produces horizontal bar charts (PNG by default, with an optional PDF flag) showing the top 10 misconfigurations by frequency.

---

## Directory Structure

```
project-root/
├── data/
│   └── misconfigurations.csv    # Input CSV with columns including "Severity" and "Misconfiguration Name"
│
├── parsers/
│   └── misconfig_parser.py      # Reads CSV, filters by severity, counts first-4 words of each name
│
├── utils/
│   └── chart_generator.py       # Generates horizontal bar charts (PNG ± PDF) in purple
│
├── main.py                      # Entry point: parses CLI args, invokes parser + chart routines
└── README.md                    # This documentation file
```

- **`data/`**  
  Contains your source CSV file(s). The default filename is `misconfigurations.csv`. You can override the path via a CLI argument.

- **`parsers/misconfig_parser.py`**  
  - Reads the CSV into a Pandas DataFrame.  
  - Normalizes “Severity” to lowercase (to match “critical” or “high”).  
  - For each row in “Critical” or “High,” extracts the first four words of the “Misconfiguration Name” (in original casing) and increments a counter.  
  - Returns two Python dictionaries:  
    1. `critical_counts` → `{ truncated_name: count }`  
    2. `high_counts`     → `{ truncated_name: count }`

- **`utils/chart_generator.py`**  
  - Provides a function `generate_horizontal_bar_chart(...)` which:  
    1. Sorts the input `dict(label → count)` in descending order.  
    2. Selects the top N (default 10) items.  
    3. Plots a horizontal bar chart (bars in **purple**), with longest bar at the top.  
    4. Saves a PNG (always) and optionally a PDF (if `create_pdf=True`) into a target output directory.

- **`main.py`**  
  - Parses command-line arguments:  
    - `--input-csv` (path to CSV; default: `data/misconfigurations.csv`)  
    - `--output-dir` (directory where charts are written; default: `output/`)  
    - `--clean` (flag to remove existing PNG/PDF files in `output-dir` before generating new ones)  
    - `--pdf` (flag to also generate PDF versions alongside PNGs)  
  - If `--clean` is set, deletes `*.png` and `*.pdf` under `output-dir` before proceeding.  
  - Calls `parse_csv(...)` → obtains two dicts (`critical_counts`, `high_counts`).  
  - Invokes `generate_horizontal_bar_chart(...)` twice: once for “Critical” and once for “High,” each time outputting top 10 bars in purple.  

---

## High-Level Workflow

1. **Prepare Your CSV**  
   - Place (or generate) your `misconfigurations.csv` inside the `data/` folder.  
   - Ensure it has at least these columns:  
     - `Severity` (e.g. “Critical,” “High,” “Medium,” etc.)  
     - `Misconfiguration Name` (free-form description string)

2. **Run `main.py`**  
   - By default:  
     ```bash
     python main.py
     ```  
     - Reads `data/misconfigurations.csv`.  
     - Creates `output/` if it doesn’t exist.  
     - Generates two PNG bar charts:  
       - `output/misconfig_critical_bar.png` (Top 10 Critical)  
       - `output/misconfig_high_bar.png`     (Top 10 High)

3. **Optional Flags**  
   - **`--input-csv PATH`**  
     Use this to point to a differently named CSV or alternate directory.  
     ```bash
     python main.py --input-csv path/to/other_file.csv
     ```
   - **`--output-dir DIR`**  
     Specify where to place generated charts (PNG/PDF). If the directory doesn’t exist, it will be created.  
     ```bash
     python main.py --output-dir custom_output
     ```
   - **`--clean`**  
     If provided, the script first removes any `*.png` and `*.pdf` under `--output-dir`.  
     ```bash
     python main.py --clean
     ```
   - **`--pdf`**  
     By default, only PNGs are emitted. This flag instructs the script to also save each chart as a PDF.  
     ```bash
     python main.py --pdf
     ```
   - **Combining Flags**  
     You can chain these flags in any order. For example, to clean a custom output folder and generate both PNGs and PDFs:  
     ```bash
     python main.py        --input-csv data/misconfigurations.csv        --output-dir output_charts        --clean        --pdf
     ```

---

## CLI Arguments Summary

| Argument         | Type      | Default                                 | Description                                                                                                                                           |
|------------------|-----------|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--input-csv`    | `string`  | `data/misconfigurations.csv`            | Path to your input CSV file. Must contain columns `Severity` and `Misconfiguration Name`.                                                            |
| `--output-dir`   | `string`  | `output`                                | Directory to which PNG (and optionally PDF) files will be written. Created automatically if it doesn’t exist.                                         |
| `--clean`        | flag      | (not set)                               | If present, deletes any existing `*.png` and `*.pdf` in `--output-dir` before generating new charts.                                                  |
| `--pdf`          | flag      | (not set)                               | If present, each bar chart is saved as both `<basename>.png` and `<basename>.pdf`. Otherwise, only PNG is created.                                    |

---

## Examples

1. **Generate only PNGs** (default behavior):
   ```bash
   python main.py
   ```
   Output:
   ```
   output/
   ├── misconfig_critical_bar.png
   └── misconfig_high_bar.png
   ```

2. **Generate PNGs + PDFs**, saving to a custom directory:
   ```bash
   python main.py --output-dir charts --pdf
   ```
   Output:
   ```
   charts/
   ├── misconfig_critical_bar.png
   ├── misconfig_critical_bar.pdf
   ├── misconfig_high_bar.png
   └── misconfig_high_bar.pdf
   ```

3. **Clean existing charts before generating new ones**:
   ```bash
   python main.py --clean
   ```
   - Removes all `*.png` and `*.pdf` under `output/`.  
   - Writes fresh `misconfig_critical_bar.png` and `misconfig_high_bar.png` into `output/`.

4. **Point to a different CSV file**:
   ```bash
   python main.py --input-csv data/other_misconfigs.csv --pdf
   ```
   - Reads `data/other_misconfigs.csv` instead of the default.  
   - Creates both PNG and PDF charts in `output/`.

---

## Installation / Prerequisites

1. **Python 3.7+**  
2. **Recommended**: Create a virtual environment and install dependencies. From project root:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Linux/macOS
   # venv\Scripts\activate.bat   # Windows
   pip install pandas matplotlib
   ```
3. **If you need PDF output**, ensure the Matplotlib backend supports PDF. On most systems, the default backend works out of the box. No extra dependencies are typically required.

---

## What the Script Does (High Level)

1. **CSV Parsing**  
   - Reads every row in the specified CSV.  
   - Filters entries by `Severity == "critical"` and `Severity == "high"` (case-insensitive).  
   - Extracts the first four words of each `Misconfiguration Name` (preserving original case).  
   - Aggregates counts for each truncated label—**duplicates counted individually**.

2. **Chart Generation**  
   - For **each severity** (`critical` and `high`), sorts the labels by count (descending).  
   - Selects the **top 10** labels.  
   - Renders a **horizontal bar chart** (bars in purple, longest at top) with those top 10.  
   - Saves the chart as a PNG in `--output-dir`. If `--pdf` is set, also saves a PDF.

3. **Optional Cleanup**  
   - If `--clean` is passed, deletes any existing `*.png` and `*.pdf` files in `--output-dir` prior to chart creation.

---

## Notes

- If your CSV contains fewer than 10 distinct truncated labels for a given severity, the chart will show only those available.
- If a severity has zero matching rows, the script will skip plotting that chart.
- The first four words of a misconfiguration name are used to group similar names. For example, “Weak SSH Key Detected on Host” and “Weak SSH Key Detected in Container” both become “Weak SSH Key Detected” and share counts.

---

Feel free to adjust colors, figure sizes, or the “top N” threshold by editing `utils/chart_generator.py`. This README covers everything necessary to understand and run the script.
