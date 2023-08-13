import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd

from dotenv import load_dotenv
from services.file_service import read_files_from_dir
from services.xml_service import parse_xml
from services.repair_orders_logging_service import RepairOrdersLoggingService
from typing import List

def invoke(logger:RepairOrdersLoggingService) -> pd.DataFrame:
    """
    Usecase to read content from from a directory and parse it into a DataFrame

    Uses the environment variables DATA_DIRECTORY and DATA_FILE_PREFIX to determine which files to read

    Parameters
    ----------
    logger: RepairOrdersLoggingService
        The logger to use for audit logging

    Returns
    -------
    pandas.DataFrame
    """
    # Load the environment variables from .env file or from the environment
    load_dotenv()

    default = []

    if os.getenv("DATA_DIRECTORY") is None:
        print("DATA_DIRECTORY environment variable not set")
        return default

    contents = read_files_from_dir(logger, os.getenv("DATA_DIRECTORY"), os.getenv("DATA_FILE_PREFIX") or "")
    logger.log(f"Ingested {len(contents)} files from {os.getenv('DATA_DIRECTORY')}")

    df = parse_xml(logger, contents)

    return pd.DataFrame(columns = ['order_id', 'date_time', 'status', 'cost', 'repair_details']) if df.empty else df