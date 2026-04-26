# whca-graphic

Fast-launch template for data journalism and analysis projects using modern Python tools.

## Quick Start

### Option 1: Global command (recommended)

```bash
# Run once to install the command
./install-global.sh

# Then from anywhere:
new-ds-project my-story-name
cd my-story-name
uv run jupyter lab
```

### Option 2: Manual copy

```bash
cp -r datascience-template my-story-name
cd my-story-name
uv sync
uv run jupyter lab
```

Add extras when a project needs them: `uv sync --extra viz` (or `geo`, `data`, `scraping`, etc.).

## Project Structure

```
├── data/
│   ├── raw/            # Original, immutable data — never modify these files
│   ├── processed/      # Cleaned and export-ready data
│   └── external/       # External reference data
├── notebooks/
│   ├── 01_analysis.ipynb       # Start your work here
│   └── templates/              # Reference notebooks (copy cells as needed)
│       ├── 90_exploratory_data_analysis.ipynb
│       └── 91_memory_monitoring.ipynb
├── utils/              # Shared helper functions
├── config.py           # Paths, plot defaults, runtime settings
├── .env.example        # Environment variable template
└── pyproject.toml      # Dependencies and extras
```

## Environment Setup

```bash
cp .env.example .env
# Edit .env with API keys, custom paths, etc.
```

The `.env` file is git-ignored. Never commit secrets.

## Default Packages

The base install is intentionally minimal:

| Package | Purpose |
|---|---|
| `pandas` | Tabular data wrangling |
| `numpy` | Numerical backbone |
| `requests` | HTTP / data fetching |
| `python-dotenv` | `.env` loading |
| `jupyterlab` | Notebook interface |

## Optional Extras

Pull in only what a project actually needs:

```bash
uv sync --extra viz          # charts and interactive viz
uv sync --extra geo          # mapping and spatial joins
uv sync --extra data         # polars, pyarrow, duckdb — high-performance tables and SQL
uv sync --extra scraping     # web scraping (run `playwright install` after)
uv sync --extra datawrapper  # Datawrapper API client
uv sync --extra io           # Excel and YAML file support
uv sync --extra databases    # PostgreSQL via SQLAlchemy + psycopg
uv sync --extra notebooks    # nbconvert and classic notebook interface
uv sync --extra diagnostics  # memory profiling
```

Combine as needed: `uv sync --extra viz,datawrapper`

**Contents by extra:**
- **viz**: matplotlib, seaborn, plotly, ipywidgets, altair
- **geo**: geopandas, folium, censusdis
- **data**: polars, pyarrow, duckdb
- **scraping**: beautifulsoup4, httpx, lxml, selenium, playwright
- **datawrapper**: datawrapper
- **io**: openpyxl, pyyaml
- **databases**: sqlalchemy, psycopg
- **notebooks**: nbconvert, notebook
- **diagnostics**: psutil, memory-profiler

### Removing an extra

1. Delete the extra name from `[project.optional-dependencies]` in `pyproject.toml`
2. Run `uv sync` — uv removes packages that are no longer in the spec

## Utility Functions

### `utils/data_utils.py`

```python
from utils import quick_info, clean_column_names, detect_outliers

quick_info(df)                         # shape, dtypes, missing values, stats
clean_column_names(df)                 # lowercase, underscored column names
detect_outliers(df, method='iqr')      # returns dict of {col: [outlier indices]}
create_date_features(df, 'date_col')   # extracts year/month/day/weekday/quarter
memory_optimization(df)                # downcast int/float dtypes to save RAM

# Require viz extra:
plot_distributions(df)
correlation_analysis(df)
categorical_analysis(df)
```

### `utils/journalism_utils.py`

```python
from utils import (
    quick_export_for_web,
    data_fact_check,
    quick_summary_table,
    compare_periods,
    create_story_charts,  # requires viz extra
)

quick_export_for_web(df, 'filename', format_type='csv')   # csv, json, html, excel → data/processed/
data_fact_check(df)                                        # nulls, dupes, ranges — full df
data_fact_check(df, column='amount')                       # drill into a specific column
quick_summary_table(df, group_by='state', aggregate_cols=['count'], agg_func='sum')
compare_periods(df, 'date', 'value', '2023-01-01', '2024-01-01')
```

## Configuration

`config.py` exposes commonly used paths and defaults. Import what you need:

```python
from config import PROCESSED_DATA_DIR, FIGURES_DIR, RANDOM_SEED, DPI
```

Override anything via `.env`:

```
OUTPUT_DIR=data/processed
FIGURE_DIR=notebooks/figures
FIGURE_DPI=300
RANDOM_SEED=42
```

## GitHub Actions

Two workflow templates are included:

**`analysis.yml`** — executes numbered notebooks (`notebooks/[0-9]*.ipynb`) and uploads rendered HTML plus `data/processed/` as build artifacts. Runs on push to `main` and can be triggered manually. `--allow-errors` is set so a missing-data cell won't abort the run.

**`fetch.yml`** — scheduled data fetch template. Disabled by default (manual trigger only). To activate, uncomment the `schedule:` block and set your cron expression. The workflow runs your fetch script, then commits any new files in `data/raw/` back to the repo. Add API keys as GitHub Actions secrets (repo → Settings → Secrets and variables → Actions) and map them in the `env:` block.

## VS Code

Opening the project folder will:
- Auto-detect the `.venv` created by `uv`
- Suggest recommended extensions (Jupyter, Pylance, GitHub Actions, Copilot)
- Enable format-on-save and import organization

No extra configuration needed.

## uv Reference

```bash
uv run jupyter lab              # launch Jupyter
uv run python script.py         # run a script in the project env
uv sync --extra viz             # add an extra
uv add package-name             # add a one-off package
uv lock --upgrade               # refresh lockfile to latest allowed versions
uv export --format requirements-txt > requirements.txt
```

## Preflight (before creating new projects from this template)

Run these occasionally — monthly if the template is actively changing, quarterly otherwise:

```bash
# Refresh locked versions
uv lock --upgrade
uv sync --force

# Validate the template creates a working project
./run-smoke-test.sh
```

After upgrading, commit the updated `uv.lock` so new projects inherit tested pins.

**Playwright note:** After `uv sync --extra scraping`, browser binaries need a one-time install per machine:

```bash
playwright install
```

## Best Practices

- Keep `data/raw/` immutable — load it, never overwrite it
- Commit notebooks with outputs cleared
- Use `data_fact_check()` before publishing numbers
- Set `RANDOM_SEED` in `.env` for reproducibility

## Troubleshooting

| Problem | Fix |
|---|---|
| VS Code doesn't see the venv | Restart VS Code; select interpreter via Command Palette → *Python: Select Interpreter* |
| Package conflicts after updating | `uv sync --force` to rebuild from scratch |
| Wrong Python version | Check `.python-version`; ensure `uv python install 3.13` has run |
| Playwright browsers missing | `playwright install` after syncing the `scraping` extra |
