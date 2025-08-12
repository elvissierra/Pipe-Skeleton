
ETL Skeleton pipeline to iterate upon


pip install -e .

# ETL Skeleton: Modular, DRY ETL Pipeline Framework

## Overview

This repository provides a modular, DRY (Don't Repeat Yourself) ETL (Extract, Transform, Load) pipeline skeleton. Designed for rapid integration into new data projects, it enables you to quickly build robust, configurable ETL workflows with minimal boilerplate. The structure supports easy extension, testability, and clear separation of concerns.

---

## Project Structure

```text
ETL_Skeleton/
├── extract.py         # Data extraction logic (e.g., from CSV, API, etc.)
├── transform.py       # Data transformation and cleaning utilities
├── validate.py        # Schema and data validation routines
├── load.py            # Data loading logic (e.g., to SQLite, DB)
├── utils.py           # Utility functions (config loading, retry, timing, etc.)
├── logger.py          # Centralized logging setup (file + console)
├── main.py            # Pipeline entry point with CLI
├── config/
│   ├── config.py      # Loads YAML + .env; exposes all config as constants
│   ├── dev.yaml       # Example YAML config (dev environment)
│   ├── prod.yaml      # Example YAML config (prod environment)
│   └── .env           # Secrets/overrides (not committed)
├── __init__.py        # Package marker
├── README.md          # This file
└── pyproject.toml     # Package metadata and dependencies
```

**Descriptions:**
- **extract.py**: Functions to extract/load raw data from files, APIs, etc.
- **transform.py**: Functions to clean, filter, and manipulate data frames.
- **validate.py**: Ensures data/schema meets requirements before loading.
- **load.py**: Loads processed data into a database or other destination.
- **utils.py**: Helpers for config, I/O, retry, timers, DB context, etc.
- **logger.py**: Sets up a logger for file and console output.
- **main.py**: Orchestrates the ETL process; provides a CLI interface.
- **config/**: Contains environment-based YAML configs and `.env` for secrets.
- **pyproject.toml**: Declares dependencies; allows editable installs.

---

## Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/etl-core.git
   cd ETL_Skeleton
   ```
2. **Install in editable/development mode (recommended):**
   ```bash
   pip install -e .
   ```
3. **Install dependencies (if not using pip editable):**
   ```bash
   pip install -r requirements.txt
   ```
   Or rely on `pyproject.toml` for dependency management.

---

## Configuration

The pipeline supports flexible configuration via:

- **YAML files in `config/`**: Environment-specific settings (e.g., `dev.yaml`, `prod.yaml`) define paths, DB info, columns, filters, etc.
- **`.env` file in `config/`**: For secrets or environment variable overrides (e.g., DB passwords, API keys). Uses [python-dotenv](https://pypi.org/project/python-dotenv/).

**How it works:**
1. `.env` is loaded first to set environment variables.
2. The `PIPELINE_ENV` variable (from `.env` or CLI) selects which YAML config to load (`dev.yaml` by default).
3. `config/config.py` exposes all relevant settings as Python constants for use throughout the pipeline.

**Typical config options:**
- `extract.data_path`: Path to source data (CSV, etc.)
- `load.db_path`: SQLite or DB destination path
- `logging.log_file`: Path for log file output
- `transform.required_columns`: List of columns to require/filter
- `transform.filter_col`/`filter_val`: Filtering logic
- `load.table_name`/`table_schema`: DB table and schema definition

---

## Usage

Run the pipeline via the CLI:
```bash
python main.py \
    --env dev \
    --data-path ./data/input.csv \
    --db-path ./output/etl.sqlite \
    --table-name my_table \
    --filter-col status \
    --filter-val inactive
```

**Arguments:**
- `--env`: Which config environment to use (`dev` or `prod`). Defaults to `dev`.
- `--data-path`: Path to input data file (overrides config).
- `--db-path`: Output database path (overrides config).
- `--table-name`: Destination table name.
- `--filter-col`, `--filter-val`: Filter logic for transformation step.
- `--required-columns`: List of columns to require (space-separated).
- `--table-schema`: JSON string to override the schema from config.

**Defaults:** All arguments default to values loaded from the selected YAML config. Any CLI argument will override its config value.

---

## Extending the Pipeline

- **To add new extract, transform, or load logic:**
  - Create modular functions in the respective module (e.g., `extract.py`).
  - Use utility decorators (e.g., `@timeit`, `@retry`) from `utils.py` for DRY error handling and logging.
  - Expose new config variables in the YAML and access them via `config/config.py`.
  - Register new steps in `main.py` as needed.

- **Keep DRY:**
  - Use utility functions for repeated logic (I/O, DB, validation).
  - Leverage shared logging and configuration patterns.

---

## Logging

Logging is handled centrally via `logger.py`:
- Logs are written both to a file (path set in YAML config) and to the console.
- All pipeline steps use the same logger, ensuring consistent, timestamped logs.
- Log level is set to INFO by default; you can adjust as needed in the config.

---

## License

MIT License. See [LICENSE](LICENSE) for details.