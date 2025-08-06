import os
import glob
import argparse

from parsers.misconfig_parser import parse_csv
from parsers.framework_parser import parse_framework_csv
from utils.chart_generator import (
    generate_horizontal_bar_chart,
    generate_paginated_bar_pdf,
    generate_framework_bar_chart
)

def clean_output_dir(output_dir):
    """
    Remove all .png and .pdf files in output_dir.
    """
    patterns = [os.path.join(output_dir, "*.png"), os.path.join(output_dir, "*.pdf")]
    removed_any = False
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            try:
                os.remove(filepath)
                print(f"Removed: {filepath}")
                removed_any = True
            except OSError as e:
                print(f"Failed to remove {filepath}: {e}")
    if not removed_any:
        print(f"No existing PNG/PDF files found in '{output_dir}' to remove.")

def main():
    parser = argparse.ArgumentParser(
        description="Generate misconfiguration bar charts and framework posture bar chart."
    )
    parser.add_argument(
        "--input-csv",
        default="data/misconfigurations.csv",
        help="Path to the misconfigurations CSV file."
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where PNG (and optional PDF) files will be written."
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="If set, remove any existing PNG/PDF files in the output directory before generating new charts."
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="If set, also generate PDF versions of each chart."
    )
    parser.add_argument(
        "--all-data",
        action="store_true",
        help="If set, create paginated PDFs containing all misconfiguration entries (10 per page)."
    )
    args = parser.parse_args()

    if args.clean:
        clean_output_dir(args.output_dir)

    os.makedirs(args.output_dir, exist_ok=True)

    # Parse misconfiguration CSV → two dictionaries: (critical_counts, high_counts)
    critical_counts, high_counts = parse_csv(args.input_csv)

    # Generate Top-10 Critical Severity Bar Chart
    generate_horizontal_bar_chart(
        data=critical_counts,
        top_n=10,
        output_basename="misconfig_critical_bar",
        title="Top 10 Critical Severity Misconfigurations",
        output_dir=args.output_dir,
        create_pdf=args.pdf
    )

    # Generate Top-10 High Severity Bar Chart
    generate_horizontal_bar_chart(
        data=high_counts,
        top_n=10,
        output_basename="misconfig_high_bar",
        title="Top 10 High Severity Misconfigurations",
        output_dir=args.output_dir,
        create_pdf=args.pdf
    )

    # Generate paginated all-data PDFs if requested
    if args.all_data:
        generate_paginated_bar_pdf(
            data=critical_counts,
            items_per_page=10,
            output_basename="misconfig_critical_all",
            title_prefix="Critical Severity Misconfigurations",
            output_dir=args.output_dir
        )
        generate_paginated_bar_pdf(
            data=high_counts,
            items_per_page=10,
            output_basename="misconfig_high_all",
            title_prefix="High Severity Misconfigurations",
            output_dir=args.output_dir
        )

    # Generate Framework Posture Bar Chart (sorted by score, colored by range)
    try:
        fw_data = parse_framework_csv(data_dir="data")
    except (FileNotFoundError, KeyError) as e:
        print(f"Skipping framework bar chart: {e}")
    else:
        generate_framework_bar_chart(
            data=fw_data,
            output_basename="framework_bar",
            title="Framework Posture Scores",
            output_dir=args.output_dir,
            create_pdf=args.pdf
        )

if __name__ == "__main__":
    main()
