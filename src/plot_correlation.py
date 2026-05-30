import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FormatStrFormatter

import numpy as np
import pandas as pd
import seaborn as sns

from scipy import stats


# =========================================================
# Project Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_CSV = BASE_DIR / "data" / "example_data.csv"

OUTPUT_DIR = BASE_DIR / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================
# Global Settings
# =========================================================

CORR_METHOD = "pearson"

FIG_DPI = 300

PALETTE = [
    "#eaf3e2",
    "#b4deb6",
    "#7bc6be",
    "#439cc4",
    "#0868a6",
]

GREEN = "#7aa06a"
PINK = "#d65a7f"


# =========================================================
# Style
# =========================================================

def setup_style():

    plt.rcParams["font.sans-serif"] = [
        "Arial",
        "DejaVu Sans",
        "SimHei",
    ]

    plt.rcParams["font.serif"] = [
        "Times New Roman",
    ]

    plt.rcParams["font.family"] = ["sans-serif"]

    plt.rcParams["axes.unicode_minus"] = False

    plt.rcParams["font.size"] = 12

    plt.rcParams["axes.linewidth"] = 0.8


# =========================================================
# Data Loading
# =========================================================

def load_numeric_data(csv_path):

    df = pd.read_csv(csv_path)

    numeric_df = df.select_dtypes(include=np.number)

    if numeric_df.shape[1] < 2:
        raise ValueError(
            "At least two numeric columns are required."
        )

    return numeric_df


# =========================================================
# Correlation Matrix
# =========================================================

def calculate_correlation(df):

    corr = df.corr(method=CORR_METHOD)

    corr.to_csv(
        OUTPUT_DIR / "correlation_matrix.csv",
        encoding="utf-8-sig"
    )

    return corr


# =========================================================
# Significance Stars
# =========================================================

def significance_stars(p):

    if p < 0.001:
        return "***"

    if p < 0.01:
        return "**"

    if p < 0.05:
        return "*"

    return ""


# =========================================================
# Correlation Bubble Plot
# =========================================================

def plot_bubble_correlation(corr):

    features = list(corr.columns)

    records = []

    for y in features[::-1]:

        for x in features:

            records.append({
                "x": x,
                "y": y,
                "r": corr.loc[y, x],
                "abs_r": abs(corr.loc[y, x]),
            })

    data = pd.DataFrame(records)

    cmap = LinearSegmentedColormap.from_list(
        "corr_palette",
        PALETTE
    )

    fig, ax = plt.subplots(figsize=(8.5, 7.5))

    x_map = {
        feature: idx
        for idx, feature in enumerate(features)
    }

    y_map = {
        feature: idx
        for idx, feature in enumerate(features[::-1])
    }

    scatter = ax.scatter(
        data["x"].map(x_map),
        data["y"].map(y_map),

        c=data["r"],

        s=data["abs_r"] * 720 + 20,

        cmap=cmap,

        vmin=-1,
        vmax=1,

        marker="s",

        edgecolors="white",

        linewidths=0.5,
    )

    ax.set_xticks(range(len(features)))

    ax.set_xticklabels(
        features,
        rotation=45,
        ha="right",
        fontname="Times New Roman"
    )

    ax.set_yticks(range(len(features)))

    ax.set_yticklabels(
        features[::-1],
        fontname="Times New Roman"
    )

    ax.set_xlim(-0.5, len(features) - 0.5)
    ax.set_ylim(-0.5, len(features) - 0.5)

    ax.set_facecolor("#f7f7f7")

    ax.set_xticks(
        np.arange(-0.5, len(features), 1),
        minor=True
    )

    ax.set_yticks(
        np.arange(-0.5, len(features), 1),
        minor=True
    )

    ax.grid(
        which="minor",
        color="white",
        linewidth=1.0
    )

    ax.tick_params(
        top=False,
        right=False,
        length=0
    )

    for spine in ax.spines.values():
        spine.set_color("#bdbdbd")

    cbar = fig.colorbar(
        scatter,
        ax=ax,
        fraction=0.045,
        pad=0.03
    )

    cbar.set_label(
        f"{CORR_METHOD.capitalize()} correlation",
        fontsize=12,
        fontname="Times New Roman"
    )

    cbar.ax.yaxis.set_major_formatter(
        FormatStrFormatter("%.1f")
    )

    fig.tight_layout()

    output_path = OUTPUT_DIR / "correlation_bubble_plot.png"

    fig.savefig(
        output_path,
        dpi=FIG_DPI,
        bbox_inches="tight",
        facecolor="white"
    )

    plt.close(fig)

    return output_path


# =========================================================
# Pairwise Relationship Matrix
# =========================================================

def plot_pairwise_matrix(df, corr):

    features = list(df.columns)

    n = len(features)

    fig, axes = plt.subplots(
        n,
        n,
        figsize=(15, 15)
    )

    for i, y_feature in enumerate(features):

        for j, x_feature in enumerate(features):

            ax = axes[i, j]

            ax.tick_params(
                left=False,
                bottom=False,
                labelleft=False,
                labelbottom=False,
                top=False,
                right=False
            )

            for spine in ax.spines.values():
                spine.set_color("#cccccc")
                spine.set_linewidth(0.7)

            # =================================================
            # Diagonal: Histogram
            # =================================================

            if i == j:

                sns.histplot(
                    df[x_feature],

                    bins=8,

                    kde=True,

                    color=GREEN,

                    edgecolor="white",

                    ax=ax
                )

                ax.set_xlabel("")
                ax.set_ylabel("")

            # =================================================
            # Lower Triangle: Scatter + Regression
            # =================================================

            elif i > j:

                x = df[x_feature].to_numpy(float)

                y = df[y_feature].to_numpy(float)

                ax.scatter(
                    x,
                    y,

                    s=12,

                    alpha=0.45,

                    color=PINK,

                    edgecolors="none"
                )

                if np.nanstd(x) > 0 and np.nanstd(y) > 0:

                    coefficients = np.polyfit(x, y, 1)

                    x_predict = np.linspace(
                        np.nanmin(x),
                        np.nanmax(x),
                        100
                    )

                    y_predict = np.poly1d(coefficients)(
                        x_predict
                    )

                    ax.plot(
                        x_predict,
                        y_predict,

                        color=PINK,

                        linewidth=1.2
                    )

                ax.set_xlabel("")
                ax.set_ylabel("")

            # =================================================
            # Upper Triangle: Correlation Values
            # =================================================

            else:

                r = corr.loc[y_feature, x_feature]

                _, p = stats.pearsonr(
                    df[x_feature],
                    df[y_feature]
                )

                color = PINK if r >= 0 else GREEN

                alpha = min(
                    0.90,
                    0.18 + abs(r) * 0.72
                )

                ax.set_facecolor(color)

                ax.patch.set_alpha(alpha)

                ax.text(
                    0.5,
                    0.58,

                    f"{r:.2f}",

                    transform=ax.transAxes,

                    ha="center",
                    va="center",

                    fontsize=11,

                    fontweight="bold",

                    fontname="Times New Roman",

                    color="black"
                )

                star = significance_stars(p)

                if star:

                    ax.text(
                        0.5,
                        0.34,

                        star,

                        transform=ax.transAxes,

                        ha="center",
                        va="center",

                        fontsize=9,

                        fontweight="bold",

                        fontname="Times New Roman",

                        color="black"
                    )

            # =================================================
            # Bottom Labels
            # =================================================

            if i == n - 1:

                ax.set_xlabel(
                    x_feature,

                    rotation=45,

                    ha="right",

                    fontsize=10,

                    fontname="Times New Roman"
                )

            # =================================================
            # Left Labels
            # =================================================

            if j == 0:

                ax.set_ylabel(
                    y_feature,

                    rotation=0,

                    ha="right",
                    va="center",

                    fontsize=10,

                    fontname="Times New Roman"
                )

    # =========================================================
    # Colorbar
    # =========================================================

    cmap = LinearSegmentedColormap.from_list(
        "pairwise_corr",

        [GREEN, "#f5f5f5", PINK]
    )

    scalar_map = plt.cm.ScalarMappable(
        cmap=cmap,
        norm=plt.Normalize(-1, 1)
    )

    scalar_map.set_array([])

    cax = fig.add_axes([
        0.90,
        0.15,
        0.018,
        0.70
    ])

    cbar = fig.colorbar(
        scalar_map,
        cax=cax
    )

    cbar.set_label(
        f"{CORR_METHOD.capitalize()} correlation",

        fontsize=12,

        fontname="Times New Roman"
    )

    cbar.ax.yaxis.set_major_formatter(
        FormatStrFormatter("%.1f")
    )

    fig.subplots_adjust(
        wspace=0.08,
        hspace=0.08,

        right=0.88,

        bottom=0.11,

        left=0.11,

        top=0.98
    )

    output_path = (
        OUTPUT_DIR /
        "pairwise_relationship_matrix.png"
    )

    fig.savefig(
        output_path,

        dpi=FIG_DPI,

        bbox_inches="tight",

        facecolor="white"
    )

    plt.close(fig)

    return output_path


# =========================================================
# Main
# =========================================================

def main(data_csv=None, output_dir=None, corr_method=None):

    setup_style()

    # Apply CLI overrides if provided
    if data_csv:
        global DATA_CSV
        DATA_CSV = Path(data_csv)
    if output_dir:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(output_dir)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if corr_method:
        global CORR_METHOD
        CORR_METHOD = corr_method

    print(f"Input:  {DATA_CSV}")
    print(f"Output: {OUTPUT_DIR.resolve()}")
    print(f"Method: {CORR_METHOD}")
    print("-" * 40)

    df = load_numeric_data(DATA_CSV)

    corr = calculate_correlation(df)

    bubble_path = plot_bubble_correlation(corr)

    pairwise_path = plot_pairwise_matrix(df, corr)

    print(f"Bubble plot saved to: {bubble_path}")

    print(f"Pairwise matrix saved to: {pairwise_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Publication-quality correlation visualization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/plot_correlation.py
  python src/plot_correlation.py --data my_data.csv
  python src/plot_correlation.py --data my_data.csv --method spearman
  python src/plot_correlation.py --data my_data.csv --out ./results --method kendall
        """,
    )

    parser.add_argument(
        "--data", "-d",
        default=None,
        help="Path to input CSV (default: data/example_data.csv)",
    )

    parser.add_argument(
        "--out", "-o",
        default=None,
        help="Output directory (default: figures/)",
    )

    parser.add_argument(
        "--method", "-m",
        choices=["pearson", "spearman", "kendall"],
        default=None,
        help="Correlation method (default: pearson)",
    )

    args = parser.parse_args()

    main(data_csv=args.data, output_dir=args.out, corr_method=args.method)
