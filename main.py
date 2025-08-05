import sys
import argparse
from etl.extract import extract_data
from etl.validate import validate_schema
from etl.transform import transform_data
from etl.load import load_data
from etl.logger import setup_logger
from etl.config.config import (
    DATA_PATH, REQUIRED_COLUMNS,
    FILTER_COLUMN, FILTER_VALUE,
    DB_PATH, TABLE_NAME, TABLE_SCHEMA,
)

def run_pipeline(args=None):
    logger = setup_logger(__name__)
    logger.info("=== Pipeline starting (env=%s) ===", args.env)
    try:
        df = extract_data(args.data_path)
        validate_schema(df, args.required_columns)
        df = transform_data(df, filter_col=args.filter_col, filter_value=args.filter_val)
        load_data(df, args.db_path, args.table_name, args.table_schema)
        logger.info("=== Pipeline completed successfully ===")
        return 0
    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        return 1

def parse_args():
    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument("--env", default=None, help="Config environment (dev|prod)")
    parser.add_argument("--data-path", default=DATA_PATH, help="Input CSV path")
    parser.add_argument("--required-columns", nargs="+", default=REQUIRED_COLUMNS)
    parser.add_argument("--filter-col", default=FILTER_COLUMN)
    parser.add_argument("--filter-val", default=FILTER_VALUE)
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--table-name", default=TABLE_NAME)
    parser.add_argument("--table-schema", type=str, default=None,
                        help="JSON string of table schema; overrides config")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # allow overriding table_schema via JSON on CLI
    if args.table_schema:
        import json
        args.table_schema = json.loads(args.table_schema)
    else:
        args.table_schema = TABLE_SCHEMA
    sys.exit(run_pipeline(args))