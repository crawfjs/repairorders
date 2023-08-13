import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlite3.dbapi2 import Cursor
import sqlite3
from models.repair_order import RepairOrder
from services.repair_orders_logging_service import RepairOrdersLoggingService

def create_database(logger: RepairOrdersLoggingService, database_file_path: str):
    """
    Create a new database.

    Parameters
    ----------
    database_file_path: str
        The path to the database file

    Returns
    -------
    None
    """

    logger.log(f"Creating database {database_file_path}")
    db = sqlite3.connect(database_file_path)

    # Create the tables
    cursor = db.cursor()

    logger.log("Creating table repair_orders")
    cursor.execute('''
        CREATE TABLE repair_orders (
            order_id INTEGER NOT NULL PRIMARY KEY
        );
    ''')

    cursor.execute('''
        CREATE TABLE repair_orders_events (
            order_id INTEGER NOT NULL,
            date_time DATETIME NOT NULL,
            status TEXT NOT NULL,
            cost REAL NOT NULL,
            technician TEXT NOT NULL,
            primary key (order_id, date_time),
            FOREIGN KEY(order_id) REFERENCES repair_orders(order_id)
        );
    ''')

    logger.log("Creating table repair_parts")
    cursor.execute('''
        CREATE TABLE repair_parts (
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            repair_order_id INTEGER NOT NULL,
            repair_order_date_time DATETIME NOT NULL,
            FOREIGN KEY(repair_order_id, repair_order_date_time) REFERENCES repair_orders_events(order_id, date_time)
        );
    ''')
    db.commit()
    db.close()
    logger.log("Finished creating database.")

def __insert_repair_order__(logger: RepairOrdersLoggingService, cursor: Cursor, repair_order: RepairOrder):
    logger.log(f"Inserting repair order {repair_order.order_id} into database")

    cursor.execute("""
        INSERT OR IGNORE INTO repair_orders (order_id)
        VALUES (?)
    """, (
        repair_order.order_id,
    ))

def __insert_repair_order_events__(logger: RepairOrdersLoggingService, cursor: Cursor, repair_order: RepairOrder):
    logger.log(f"Inserting repair order events for {repair_order.order_id} into database")

    cursor.execute("""
        INSERT INTO repair_orders_events (order_id, date_time, status, cost, technician)
        VALUES (?, ?, ?, ?, ?)
    """, (
        repair_order.order_id,
        repair_order.date_time,
        repair_order.status,
        repair_order.cost,
        repair_order.repair_details.technician
    ))

def __insert_repair_order_parts__(logger: RepairOrdersLoggingService, cursor: Cursor, repair_order: RepairOrder):
    logger.log(f"Inserting repair order parts for {repair_order.order_id} into database")

    for repair_part in repair_order.repair_details.repair_parts:
        cursor.execute("""
            INSERT INTO repair_parts (name, quantity, repair_order_id, repair_order_date_time)
            VALUES (?, ?, ?, ?)
        """, (
            repair_part.name,
            repair_part.quantity,
            repair_order.order_id,
            repair_order.date_time
        ))


def insert_repair_order(logger: RepairOrdersLoggingService, database_file_path: str, repair_order: RepairOrder):
    """
    Insert a new repair order into the database.
    
    Parameters
    ----------
    database_file_path: str
        The path to the database file
    repair_order: RepairOrder
        The repair order to insert

    Returns
    -------
    None
    """
    db = sqlite3.connect(database_file_path)
    cursor = db.cursor()

    __insert_repair_order__(logger, cursor, repair_order)

    __insert_repair_order_events__(logger, cursor, repair_order)

    __insert_repair_order_parts__(logger, cursor, repair_order)

    db.commit()
    db.close()