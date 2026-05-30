<div align="center">

<!-- PROJECT LOGO -->
<br />
<h1>Correlation Plot</h1>

  <p align="center">
    Publication-quality correlation visualization for scientific research
    <br />
    <a href="#demo">View Demo</a>
    ·
    <a href="#quick-start">Quick Start</a>
    ·
    <a href="#configuration">Configuration</a>
  </p>

<!-- BADGES -->
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.8+-blue?logo=python&logoColor=white" alt="Python 3.8+">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License MIT">
    <img src="https://img.shields.io/badge/dependencies-5-lightgrey" alt="Dependencies">
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details open>
  <summary><b>Table of Contents</b></summary>
  <ol>
    <li><a href="#demo">Demo</a></li>
    <li><a href="#quick-start">Quick Start</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#configuration">Configuration</a></li>
    <li><a href="#dependencies">Dependencies</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

---

## Demo

<div align="center">
  <img src="figures/correlation_bubble_plot_preview.png" width="48%" alt="Correlation Bubble Plot">
  &nbsp;
  <img src="figures/pairwise_relationship_matrix_preview.png" width="48%" alt="Pairwise Relationship Matrix">

  *Left: Correlation bubble plot — square size ∝ |r|, color encodes sign & strength. Right: Pairwise relationship matrix — histogram (diagonal), scatter + linear fit (lower), r-value + significance (upper).*
</div>

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/tang200312/Correlation-Plot.git
cd Correlation-Plot

# 2. Install
pip install -r requirements.txt

# 3. Run
python src/plot_correlation.py
```

Three files are written to `figures/`:

| Output | Description |
|---|---|
| `correlation_matrix.csv` | Full pairwise correlation table |
| `correlation_bubble_plot.png` | Bubble matrix (300 DPI) |
| `pairwise_relationship_matrix.png` | Multi-panel matrix (300 DPI) |

**To use your own data:** replace `data/example_data.csv` with any numeric CSV and rerun.

---

## Features

- **Bubble plot** — color-coded grid squares, size proportional to |r|, clean journal style
- **Pairwise matrix** — everything in one figure: distribution, scatter, regression, r-values, significance
- **Significance stars** — \*\*\*(p<0.001), \*\*(p<0.01), \*(p<0.05) as you'd expect in a paper
- **Times New Roman** throughout — matches the typography most journals require
- **Configurable** — swap method (Pearson/Spearman/Kendall), colors, DPI from constants at the top
- **Data-agnostic** — feed it any numeric CSV, it auto-selects numeric columns only

---

## Project Structure

```
.
├── src/
│   └── plot_correlation.py    # main script
├── data/
│   └── example_data.csv       # sample dataset (11 features, 200 samples)
├── figures/                   # output (auto-created on first run)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Configuration

Open `src/plot_correlation.py` and tweak the constants near the top:

| Constant | Default | What it does |
|---|---|---|
| `CORR_METHOD` | `"pearson"` | Correlation method — also `"spearman"`, `"kendall"` |
| `FIG_DPI` | `300` | Output resolution (300 = journal-ready) |
| `PALETTE` | `["#eaf3e2", …, "#0868a6"]` | Colormap for the bubble plot |
| `GREEN` | `"#7aa06a"` | Color for positive correlation / histograms |
| `PINK` | `"#d65a7f"` | Color for negative correlation / scatter points |

---

## Dependencies

| Package | Tested |
|---|---|
| Python | ≥ 3.8 |
| matplotlib | ≥ 3.5 |
| numpy | ≥ 1.21 |
| pandas | ≥ 1.3 |
| scipy | ≥ 1.7 |
| seaborn | ≥ 0.11 |

```bash
pip install -r requirements.txt
```

---

## License

Distributed under the MIT License. Use freely in your research or project.
