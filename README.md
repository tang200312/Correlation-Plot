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
    <a href="#usage">Usage</a>
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
    <li><a href="#usage">Usage</a></li>
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

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run with example data
python src/plot_correlation.py
```

Three files appear in `figures/`:

| Output | Description |
|---|---|
| `correlation_bubble_plot.png` | Bubble matrix (300 DPI) |
| `pairwise_relationship_matrix.png` | Multi-panel matrix (300 DPI) |
| `correlation_matrix.csv` | Full pairwise correlation table |

---

## Usage

### Use your own CSV

```bash
python src/plot_correlation.py --data /path/to/your_data.csv
```

Your CSV can have **any number of rows and columns**. The script automatically picks all numeric columns — non-numeric columns (text, dates, etc.) are skipped. First row must be column headers.

Example of a valid CSV:

| NDVI | EVI | Chlorophyll | Biomass |
|------|-----|-------------|---------|
| 0.36 | 0.26 | 2.1 | 134.5 |
| 0.42 | 0.31 | 2.5 | 156.2 |
| ... | ... | ... | ... |

### Change correlation method

```bash
python src/plot_correlation.py --data your_data.csv --method spearman
python src/plot_correlation.py --data your_data.csv --method kendall
```

### Custom output directory

```bash
python src/plot_correlation.py --data your_data.csv --out ./results
```

### See all options

```bash
python src/plot_correlation.py --help
```

```
usage: plot_correlation.py [-h] [--data DATA] [--out OUT] [--method {pearson,spearman,kendall}]

optional arguments:
  -h, --help            show this help message and exit
  --data DATA, -d DATA  Path to input CSV (default: data/example_data.csv)
  --out OUT, -o OUT     Output directory (default: figures/)
  --method METHOD, -m METHOD
                        Correlation method (default: pearson)
```

---

## Features

- **Bubble plot** — color-coded grid squares, size proportional to |r|, clean journal style
- **Pairwise matrix** — everything in one figure: distribution, scatter, regression, r-values, significance
- **Significance stars** — \*\*\*(p<0.001), \*\*(p<0.01), \*(p<0.05)
- **Times New Roman** typography — matches most journal requirements
- **Configurable** — swap method (Pearson/Spearman/Kendall), colors, DPI from constants at the top
- **Any numeric CSV** — auto-detects columns, ignores non-numeric data

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
├── LICENSE
├── .gitignore
└── README.md
```

---

## Configuration

### Command-line (recommended)

| Flag | Default | Description |
|---|---|---|
| `--data` / `-d` | `data/example_data.csv` | Input CSV path |
| `--out` / `-o` | `figures/` | Output directory |
| `--method` / `-m` | `pearson` | Correlation method |

### Edit `src/plot_correlation.py` for deeper customization

| Constant | Default | What it does |
|---|---|---|
| `FIG_DPI` | `300` | Output resolution (300 = journal-ready) |
| `PALETTE` | 5-color blue-green gradient | Bubble plot colormap |
| `GREEN` | `#7aa06a` | Color for positive correlation / histograms |
| `PINK` | `#d65a7f` | Color for negative correlation / scatter points |

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

MIT — see [LICENSE](LICENSE). Use freely in your research or project.
