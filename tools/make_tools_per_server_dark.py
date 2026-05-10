"""Render the 'tools per MCP server' bar chart in a dark-theme palette
that matches the M3-Bench blog (cyan/magenta/lime on deep navy).

Reads the catalog from the sibling code repo and writes a PNG + SVG into
blog/assets/img/ that the website embeds without the white card wrapper.

Usage:
    cd Open-M3-Bench/blog
    python tools/make_tools_per_server_dark.py
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyBboxPatch

BLOG = Path(__file__).resolve().parent.parent
CATALOG = (
    BLOG.parent / "code" / "save" / "mcp_tools_with_desc.json"
)
OUT_PNG = BLOG / "assets" / "img" / "mcp_tools_per_server.png"
OUT_SVG = BLOG / "assets" / "img" / "mcp_tools_per_server.svg"

# Blog palette (mirrors assets/css/style.css)
BG        = "#0f1422"   # --bg-soft
PANEL     = "#11182b"   # --bg-card
LINE      = "#1f2a44"   # --line
FG        = "#e8ecf5"   # --fg
FG_DIM    = "#9aa5c0"   # --fg-dim
FG_MUTED  = "#6b7794"   # --fg-muted
CYAN      = "#5ef1ff"
MAG       = "#ff6bd6"
LIME      = "#b6f36a"
AMBER     = "#ffc857"

CATEGORY_COLOR = {
    "Academic & Knowledge":  "#7cc4ff",
    "Office Automation":     "#ff9ec8",
    "Geography & Travel":    "#b6f36a",
    "Science & Space":       "#c084fc",
    "Computer Vision":       "#5ef1ff",
    "E-commerce & Finance":  "#ffc857",
    "Health":                "#ff7b7b",
    "Weather & Air Quality": "#82f0c4",
}

# Map each server to its dominant category (resolved from catalog)
def server_category(tools: dict) -> str:
    cats = Counter()
    for _, info in tools.items():
        if not isinstance(info, dict):
            continue
        cat = info.get("catalogry") or info.get("category") or info.get("catalog") or info.get("catalogue")
        if cat:
            cats[cat] += 1
    return cats.most_common(1)[0][0] if cats else "Uncategorized"


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))

    # counts & category per server
    rows = []
    cat_totals = Counter()
    for server, tools in data.items():
        if not isinstance(tools, dict):
            continue
        n = sum(1 for _, info in tools.items() if isinstance(info, dict))
        if n <= 0:
            continue
        cat = server_category(tools)
        cat_totals[cat] += n
        rows.append((server, n, cat))
    rows.sort(key=lambda r: (-r[1], r[0]))

    labels  = [r[0].replace("_", " ") for r in rows]
    counts  = [r[1] for r in rows]
    colors  = [CATEGORY_COLOR.get(r[2], CYAN) for r in rows]

    # ---- Plot ---------------------------------------------------------
    mpl.rcParams.update({
        "font.family": ["DejaVu Sans Mono", "monospace"],
        "axes.edgecolor": LINE,
        "axes.linewidth": 1.0,
        "axes.labelcolor": FG_DIM,
        "xtick.color": FG_DIM,
        "ytick.color": FG_DIM,
        "savefig.facecolor": BG,
        "figure.facecolor": BG,
    })

    fig, ax = plt.subplots(figsize=(12, 5.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)

    x = list(range(len(rows)))
    bars = ax.bar(
        x, counts,
        width=0.72,
        color=colors,
        edgecolor=LINE,
        linewidth=0.6,
    )

    # Value labels above each bar
    for bar, v in zip(bars, counts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(counts) * 0.015,
            str(v),
            ha="center", va="bottom",
            color=FG, fontsize=9, fontweight="bold",
        )

    # Axis & ticks
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=9.5, color=FG_DIM)
    ax.set_xlabel("MCP server", color=FG_DIM, fontsize=11, labelpad=8)
    ax.set_ylabel("number of tools", color=FG_DIM, fontsize=11, labelpad=8)
    ax.set_ylim(0, max(counts) * 1.18)

    # grid
    ax.yaxis.grid(True, linestyle=":", linewidth=0.8, color=LINE, alpha=0.9)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(LINE)

    # Legend (one swatch per category, ordered by total tools desc)
    from matplotlib.patches import Patch
    legend_items = [
        Patch(facecolor=CATEGORY_COLOR[c], edgecolor=LINE, label=f"{c}  ·  {cat_totals[c]}")
        for c, _ in cat_totals.most_common()
    ]
    leg = ax.legend(
        handles=legend_items,
        loc="upper right",
        frameon=True,
        facecolor=PANEL,
        edgecolor=LINE,
        fontsize=9,
        labelcolor=FG_DIM,
        ncol=2,
        columnspacing=1.2,
        handlelength=1.2,
        handleheight=1.0,
        handletextpad=0.6,
        borderpad=0.8,
    )
    leg.get_frame().set_linewidth(1)

    # Corner title like a terminal panel
    ax.set_title(
        "// tools_per_server :: mcp_servers.json",
        color=CYAN, fontsize=10, loc="left",
        pad=10, fontweight="bold", fontfamily="monospace",
    )

    plt.tight_layout()
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PNG, dpi=220, facecolor=BG, bbox_inches="tight")
    fig.savefig(OUT_SVG, facecolor=BG, bbox_inches="tight")
    print(f"wrote  {OUT_PNG}  ({OUT_PNG.stat().st_size/1024:.1f} KB)")
    print(f"wrote  {OUT_SVG}  ({OUT_SVG.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
