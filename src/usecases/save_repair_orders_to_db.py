import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd

from dotenv import load_dotenv
from models.repair_order import RepairOrder
from services.database_service import create_database, insert_repair_order
from services.repair_orders_logging_service import RepairOrdersLoggingService
from typing import List

def invoke(logger:RepairOrdersLoggingService, run_id: str, data: List[RepairOrder]):
    """
    Usecase to convert repair orders into records in a new database

    Parameters
    ----------
    logger: RepairOrdersLoggingService
        The logger to use for audit logging
    run_id: str
        The identifier for the current run
    data: List[RepairOrder]
        The repair orders to save to the database

    Returns
    -------
    None
    """
    # Load the environment variables from .env file or from the environment
    load_dotenv()

    if os.getenv("DATABASE_PATH") is None:
        print("DATABASE_PATH environment variable not set")
        return

    if os.getenv("DATABASE_PATH") != ":memory:":
        os.makedirs(os.getenv("DATABASE_PATH"), exist_ok=True)
        database = f"{os.getenv('DATABASE_PATH')}/{run_id}.sqlite"
    else:
        database = os.getenv('DATABASE_PATH')
    
    create_database(logger, database)

    logger.log(f"Saving {len(data)} repair orders to database {database}")
    for repair_order in data:
        insert_repair_order(logger, database, repair_order)

    logger.log(f"Save for run {run_id} complete.")