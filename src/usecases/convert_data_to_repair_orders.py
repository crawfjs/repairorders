import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.repair_order import RepairOrder, RepairPart
from services.repair_orders_logging_service import RepairOrdersLoggingService
from typing import Dict, List
import pandas as pd

def process_to_repair_order(logger: RepairOrdersLoggingService, data: Dict[str, pd.DataFrame]) -> List[RepairOrder]:
    """
    Usecase to convert a DataFrame into a list of RepairOrder objects

    Parameters
    ----------
    logger: RepairOrdersLoggingService
        The logger to use for audit logging
    data: Dict[str, pd.DataFrame]
        The data to convert

    Returns
    -------
    List[RepairOrder]
    """
    logger.log("Processing data to repair orders")
    repair_orders = []
    for window_start, window_data in data.items():
        for index, row in window_data.iterrows():
            row_dict = row.to_dict()
            row_dict['date_time'] = index.to_pydatetime()
            repair_order = RepairOrder.from_dict(row_dict)
            repair_orders.append(repair_order)

    return repair_orders
