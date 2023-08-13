import os
import uuid
from services.repair_orders_logging_service import RepairOrdersLoggingService
from usecases import convert_data_to_repair_orders, read_content_from_all_sources, save_repair_orders_to_db, window_by_datetime_to_get_latest_event

def process():
    run_key = uuid.uuid4()

    logger = RepairOrdersLoggingService(run_key)
    logger.log("Starting process")

    # Collect all content and store it into a DataFrame
    df = read_content_from_all_sources.invoke(logger)

    # Window the data by datetime and get the latest event
    latest_events = window_by_datetime_to_get_latest_event.window_by_datetime(logger, df, "1D")

    # Convert the data into RepairOrder objects
    repair_orders = convert_data_to_repair_orders.process_to_repair_order(logger, latest_events)

    # Save the repair orders to a database
    save_repair_orders_to_db.invoke(logger, run_key, repair_orders)

    logger.log("Finished process")


if __name__ == "__main__":
    process()
