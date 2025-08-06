import os
import textwrap
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

def generate_horizontal_bar_chart(
    data: dict,
    top_n: int = 10,
    output_basename: str = "chart_output",
    title: str = "Top Misconfigurations by Frequency",
    output_dir: str = "output",
    create_pdf: bool = False
):
    if not data:
        print(f"No data to plot for '{output_basename}'. Skipping chart.")
        return

    os.makedirs(output_dir, exist_ok=True)
    items = sorted(data.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
    labels, counts = zip(*items)
    counts = [int(c) for c in counts]
    y_positions = list(range(len(labels)))[::-1]
    wrapped_labels = [textwrap.fill(label, width=45) for label in labels]
    lines_per_label = [lbl.count("\n") + 1 for lbl in wrapped_labels]
    total_lines = sum(lines_per_label)
    fig_height = max(6, total_lines * 0.6)

    fig, ax = plt.subplots(figsize=(10, fig_height))
    bars = ax.barh(y_positions, counts, height=0.5, color='purple', edgecolor='black')
    max_count = max(counts)
    ax.set_xlim(0, max_count * 1.1)

    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(
            width + max_count * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{counts[i]}",
            va='center',
            fontsize=9
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(wrapped_labels)
    ax.set_xlabel("Count")
    ax.set_title(title)
    fig.subplots_adjust(left=0.40, right=0.95, top=0.9, bottom=0.05)

    png_path = os.path.join(output_dir, f"{output_basename}.png")
    fig.savefig(png_path)
    print(f"Chart saved as {png_path}")
    if create_pdf:
        pdf_path = os.path.join(output_dir, f"{output_basename}.pdf")
        fig.savefig(pdf_path)
        print(f"Chart saved as {pdf_path}")
    plt.close(fig)


def generate_paginated_bar_pdf(
    data: dict,
    items_per_page: int = 10,
    output_basename: str = "all_data",
    title_prefix: str = "Misconfigurations",
    output_dir: str = "output"
):
    if not data:
        print(f"No data to plot for '{output_basename}'. Skipping paginated PDF.")
        return

    os.makedirs(output_dir, exist_ok=True)
    items = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
    pages = [items[i : i + items_per_page] for i in range(0, len(items), items_per_page)]
    pdf_path = os.path.join(output_dir, f"{output_basename}.pdf")

    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(pdf_path) as pdf:
        for page_idx, chunk in enumerate(pages, start=1):
            labels, counts = zip(*chunk)
            counts = [int(c) for c in counts]
            y_positions = list(range(len(labels)))[::-1]
            wrapped_labels = [textwrap.fill(label, width=45) for label in labels]
            lines_per_label = [lbl.count("\n") + 1 for lbl in wrapped_labels]
            total_lines = sum(lines_per_label)
            fig_height = max(6, total_lines * 0.6)

            fig, ax = plt.subplots(figsize=(10, fig_height))
            bars = ax.barh(y_positions, counts, height=0.5, color='purple', edgecolor='black')
            max_count = max(counts)
            ax.set_xlim(0, max_count * 1.1)

            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax.text(
                    width + max_count * 0.01,
                    bar.get_y() + bar.get_height() / 2,
                    f"{counts[i]}",
                    va='center',
                    fontsize=9
                )

            ax.set_yticks(y_positions)
            ax.set_yticklabels(wrapped_labels)
            ax.set_xlabel("Count")
            ax.set_title(f"{title_prefix} - Page {page_idx}")
            fig.subplots_adjust(left=0.40, right=0.95, top=0.9, bottom=0.05)

            pdf.savefig(fig)
            plt.close(fig)

    print(f"Paginated PDF saved as {pdf_path}")


def generate_framework_bar_chart(
    data: dict,
    output_basename: str = "framework_bar",
    title: str = "Framework Posture Scores",
    output_dir: str = "output",
    create_pdf: bool = False
):
    if not data:
        print(f"No data to plot for '{output_basename}'. Skipping chart.")
        return

    items = sorted(data.items(), key=lambda kv: float(kv[1]), reverse=True)
    labels, scores = zip(*items)
    scores = [float(s) for s in scores]
    wrapped_labels = [textwrap.fill(label, width=15) for label in labels]

    num = len(labels)
    fig_width = max(8, num * 0.4)
    fig_height = 6

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    x_positions = range(len(labels))

    def interp_color(c_low, c_high, t):
        rgb_low = to_rgb(c_low)
        rgb_high = to_rgb(c_high)
        return tuple(rgb_low[i] + (rgb_high[i] - rgb_low[i]) * t for i in range(3))

    bar_colors = []
    for score in scores:
        if score >= 94:
            low_c, high_c = '#add8e6', '#00008b'  # lightblue → darkblue
            rng_min, rng_max = 94, 100
        elif score >= 87:
            low_c, high_c = '#90ee90', '#006400'  # lightgreen → darkgreen
            rng_min, rng_max = 87, 93
        elif score >= 73:
            low_c, high_c = '#ffffe0', '#ffd700'  # lightyellow → gold
            rng_min, rng_max = 73, 86
        elif score >= 68:
            low_c, high_c = '#ffdab9', '#ff8c00'  # papayawhip → darkorange
            rng_min, rng_max = 68, 72
        elif score >= 50:
            low_c, high_c = '#ff9999', '#8b0000'  # lightcoral → darkred
            rng_min, rng_max = 50, 67
        elif score >= 32:
            low_c, high_c = '#dda0dd', '#800080'  # plum → purple
            rng_min, rng_max = 32, 49
        elif score >= 20:
            low_c, high_c = '#deb887', '#8b4513'  # burlywood → saddlebrown
            rng_min, rng_max = 20, 31
        elif score >= 10:
            low_c, high_c = '#d3d3d3', '#696969'  # lightgrey → dimgray
            rng_min, rng_max = 10, 19
        else:
            low_c = high_c = '#ffc0cb'  # pink
            rng_min, rng_max = 0, 9

        raw_t = 0.0 if rng_max == rng_min else (score - rng_min) / (rng_max - rng_min)
        t = max(0.0, min(1.0, raw_t))
        bar_colors.append(interp_color(low_c, high_c, t))

    bars = ax.bar(x_positions, scores, width=0.6, color=bar_colors, edgecolor='white')
    ax.set_ylim(0, 100)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1.0,
            f"{scores[i]:.1f}",
            ha='center',
            va='bottom',
            fontsize=9
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(wrapped_labels, rotation=90, ha='center')
    ax.set_ylabel("Posture Score")
    ax.set_title(title)
    fig.subplots_adjust(bottom=0.30, left=0.10, right=0.95, top=0.90)

    png_path = os.path.join(output_dir, f"{output_basename}.png")
    fig.savefig(png_path)
    print(f"Chart saved as {png_path}")
    if create_pdf:
        pdf_path = os.path.join(output_dir, f"{output_basename}.pdf")
        fig.savefig(pdf_path)
        print(f"Chart saved as {pdf_path}")
    plt.close(fig)
