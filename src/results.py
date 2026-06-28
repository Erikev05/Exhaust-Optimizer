"""
Handles all output from the solver — plots and CSV export.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _to_dataframe(results: dict) -> pd.DataFrame:
    """Convert results dict to a tidy DataFrame."""
    return pd.DataFrame({
        "RPM":                    results["RPM"],
        "Blair (m)":              results["Blair"],
        "Bell (m)":               results["Bell"],
        "Evanschitzky (m)":       results["Evanschitzky"],
        "Evanschitzky Thermal (m)": results["Evanschitzky_Thermal"],
    })


def save_csv(results: dict, output_dir: str = "outputs/") -> None:
    """
    Save solver results to a CSV file.

    Args:
        results:    Output dict from optimizer.run()
        output_dir: Directory to write into (created if it doesn't exist)
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "results.csv")

    df = _to_dataframe(results)
    df.to_csv(path, index=False)

    print(f"Results saved to {path}")


def plot(results: dict, output_dir: str = None) -> None:
    """
    Plot all methods on a single figure.
    Optionally saves the figure if output_dir is provided.

    Args:
        results:    Output dict from optimizer.run()
        output_dir: If provided, saves plot as comparison_plot.png
    """
    fig = plot_figure(results)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "comparison_plot.png")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print(f"Plot saved to {path}")

    plt.show()


def plot_figure(results: dict) -> plt.Figure:
    """
    Build and return the matplotlib Figure without showing or saving it.
    Kept separate so Streamlit and tests can call it without side effects.

    Args:
        results: Output dict from optimizer.run()

    Returns:
        matplotlib Figure object
    """
    RPM = results["RPM"]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(RPM, results["Blair"],               label="Blair",                        linewidth=2)
    ax.plot(RPM, results["Bell"],                label="Bell",                         linewidth=2)
    ax.plot(RPM, results["Evanschitzky"],        label="Evanschitzky",                 linewidth=2)
    ax.plot(RPM, results["Evanschitzky_Thermal"],label="Evanschitzky (thermal)",        linewidth=2, linestyle="--")

    ax.set_title("Exhaust Primary Runner Length vs RPM", fontsize=14, fontweight="bold")
    ax.set_xlabel("Engine Speed (RPM)", fontsize=12)
    ax.set_ylabel("Primary Runner Length (m)", fontsize=12)
    ax.legend(loc="best")
    ax.grid(True, linestyle="--", alpha=0.6)

    fig.tight_layout()
    return fig


def plot_sensitivity(sens_df: pd.DataFrame, output_dir: str = None) -> list[plt.Figure]:
    """
    One heatmap figure per model, saved individually.
    Returns a list of Figure objects.
    """
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import os

    models = sens_df.columns.get_level_values(0).unique()
    cmap = "RdBu_r"
    vmax = sens_df.abs().max().max()
    norm = mcolors.TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

    figs = []
    for model in models:
        sub = sens_df[model].dropna(axis=1, how="all").T  # rows = params, cols = RPM

        fig, ax = plt.subplots(figsize=(12, max(3, len(sub.index) * 0.8)))

        im = ax.imshow(sub.values, aspect="auto", cmap=cmap, norm=norm)
        ax.set_title(f"Sensitivity — {model}", fontsize=13, fontweight="bold")
        ax.set_xticks(range(len(sub.columns)))
        ax.set_xticklabels([int(r) for r in sub.columns], rotation=90, fontsize=8)
        ax.set_yticks(range(len(sub.index)))
        ax.set_yticklabels(sub.index, fontsize=11)
        ax.set_xlabel("RPM", fontsize=10)

        fig.colorbar(im, ax=ax, label="Normalised sensitivity  S = (ΔL/L)/(Δp/p)")
        fig.tight_layout()

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            safe_name = model.lower().replace(" ", "_")
            path = os.path.join(output_dir, f"sensitivity_{safe_name}.png")
            fig.savefig(path, dpi=150, bbox_inches="tight")
            print(f"Saved: {path}")

        figs.append(fig)

    return figs