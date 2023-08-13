import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from typing import Dict
from services.repair_orders_logging_service import RepairOrdersLoggingService

def window_by_datetime(logger: RepairOrdersLoggingService, data: pd.DataFrame, window: str) -> Dict[str, pd.DataFrame]:
    """
    Usecase to window data by datetime

    Parameters
    ----------
    logger: RepairOrdersLoggingService
        The logger to use for audit logging
    data: pd.DataFrame
        The data to window
    window: str
        The window to use
        Example: "1D" will window the data by 1 day

    Returns
    -------
    Dict[str, pd.DataFrame]
    """

    logger.log(f"Windowing data by {window}")

    data['date_time'] = pd.to_datetime(data['date_time'])
    data.set_index('date_time', inplace=True)
    
    windows = data.resample(window)

    result = {}
    for window_start, window_data in windows:
        result[window_start] = window_data
    
    return result
