import matplotlib.pyplot as plt
import numpy as np


def plot_histogram(values):
    plt.hist(values)
    plt.yscale("log")

    plt.show()


def plot_boxplot(values):
    plt.boxplot(
        values,
    )
    plt.show()


def plot_scatter(x_axis, y_axis, outliers=None):
    x = np.asarray(x_axis)
    y = np.asarray(y_axis)

    if outliers is None:
        plt.scatter(x, y)
        plt.show()
        return

    # Convert to numpy
    outliers = np.array(outliers)

    # CASE 1: floats → match by value
    if np.issubdtype(outliers.dtype, np.floating):
        mask_out = np.isin(y, outliers)

    # CASE 2: boolean mask
    elif outliers.dtype == bool and len(outliers) == len(y):
        mask_out = outliers

    # CASE 3: integer indices
    elif np.issubdtype(outliers.dtype, np.integer):
        mask_out = np.zeros_like(y, dtype=bool)
        mask_out[outliers] = True

    else:
        raise ValueError("Unsupported outliers type")

    plt.scatter(x[~mask_out], y[~mask_out])
    plt.scatter(x[mask_out], y[mask_out], color="red", marker="x")

    plt.yscale("log")
    plt.show()


def plot_grouped_barplot(
    df,
    categories_col,
    group_col,
    values_col=None,
    top_n=10,
    figsize=(10, 5),
    colors=None,
    xlabel=None,
    ylabel=None,
    title=None,
):
    """
    Creates a grouped bar plot for comparing groups across categories

    args:
        df: DataFrame with MultiIndex or columns for grouping
        categories_col: Column name or index level for x-axis categories
        group_col: Column name or index level for grouped bars
        values_col: Column name for values (None if df is already aggregated)
        top_n: Number of top categories to display
        figsize: Figure size tuple
        colors: List of colors for each group
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Plot title
    """
    # Handle already grouped data (like from get_ICD_groups)
    if values_col is None:
        data = df
    else:
        data = df.groupby([categories_col, group_col])[values_col].nunique().unstack()

    # Get top N categories
    if "total" in data.columns:
        top_data = data.nlargest(top_n, "total").drop(columns="total")
    else:
        data["_total"] = data.sum(axis=1)
        top_data = data.nlargest(top_n, "_total").drop(columns="_total")

    # Prepare data
    categories = top_data.index.tolist()
    groups = top_data.columns.tolist()
    n_groups = len(groups)

    # Set colors
    if colors is None:
        colors = plt.cm.Set3(np.linspace(0, 1, n_groups))

    # Create plot
    x = np.arange(len(categories))
    width = 0.8 / n_groups

    fig, ax = plt.subplots(figsize=figsize)

    for i, group in enumerate(groups):
        values = top_data[group].fillna(0).values
        offset = (i - n_groups / 2 + 0.5) * width
        ax.bar(x + offset, values, width, label=group, color=colors[i])

    ax.set_xlabel(xlabel or "Category")
    ax.set_ylabel(ylabel or "Count")
    ax.set_title(title or f"Top {top_n} Categories by Group")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.show()
