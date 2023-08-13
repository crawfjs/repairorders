import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
import uuid
import pandas as pd
import sqlite3
from src.usecases import save_repair_orders_to_db
from src.models.repair_order import RepairOrder
from src.services.repair_orders_logging_service import RepairOrdersLoggingService

# Unit tests
class TestRepairOrdersToDB(unittest.TestCase):
    def setUp(self):
        # Let's use the in-memory database for testing
        os.environ["DATABASE_PATH"] = "data/test"
        self.run_key = f"unittest-{uuid.uuid4()}"
        self.database_file_path = f"{os.getenv('DATABASE_PATH')}/{self.run_key}.sqlite"

        # Data for testing
        self.data = [
            RepairOrder.from_dict({'order_id': 101, 'date_time': '2023-08-10T10:00:00', 'status': 'In Progress', 'cost': 50.25, 'technician': 'Jane Smith', 'repair_parts': [{'name': 'Air Filter', 'quantity': '1'}]}),
            RepairOrder.from_dict({'order_id': 101, 'date_time': '2023-08-10T12:30:00', 'status': 'Completed', 'cost': 60.00, 'technician': 'Jane Smith', 'repair_parts': [{'name': 'Air Filter', 'quantity': '1'}, {'name': 'Oil Filter', 'quantity': '1'}]}),
            RepairOrder.from_dict({'order_id': 102, 'date_time': '2023-08-11T09:00:00', 'status': 'In Progress', 'cost': 85.00, 'technician': 'James Brown', 'repair_parts': [{'name': 'Fuel Filter', 'quantity': '1'}, {'name': 'Air Filter', 'quantity': '1'}]})
        ]

        self.logger = RepairOrdersLoggingService(self.run_key)
        self.logger.log("Setting up TestRepairOrdersToDB")

    def tearDown(self):
        # Remove the database file
        os.remove(self.database_file_path)
        self.logger.log("Tear down complete for TestRepairOrdersToDB")
        self.data = None

    def test_save_repair_orders_to_db(self):
        # Arrange
        self.logger.log("Testing save_repair_orders_to_db")
        
        # Act
        save_repair_orders_to_db.invoke(self.logger, self.run_key, self.data)

        # Assert
        db = sqlite3.connect(self.database_file_path)
        cursor = db.execute("SELECT order_id FROM repair_orders order by order_id asc")
        
        results = cursor.fetchall()
        self.assertEqual(results[0][0], 101)
        self.assertEqual(results[1][0], 102)
        
        db.close()

    def test_save_repair_orders_events_in_db(self):
        # Arrange
        self.logger.log("Testing test_save_repair_orders_events_in_db")
        
        # Act
        save_repair_orders_to_db.invoke(self.logger, self.run_key, self.data)

        # Assert
        db = sqlite3.connect(self.database_file_path)
        cursor = db.execute("SELECT cost FROM repair_orders_events order by date_time asc")
        
        results = cursor.fetchall()
        self.assertEqual(results[0][0], 50.25)
        self.assertEqual(results[1][0], 60.00)
        self.assertEqual(results[2][0], 85.00)
        
        db.close()

    def test_save_repair_orders_events_parts_in_db(self):
        # Arrange
        self.logger.log("Testing test_save_repair_orders_events_parts_in_db")
        
        # Act
        save_repair_orders_to_db.invoke(self.logger, self.run_key, self.data)

        # Assert
        db = sqlite3.connect(self.database_file_path)
        cursor = db.execute("SELECT name FROM repair_parts order by repair_order_date_time asc, name asc")
        
        results = cursor.fetchall()
        self.assertEqual(results[0][0], 'Air Filter')
        self.assertEqual(results[1][0], 'Air Filter')
        self.assertEqual(results[2][0], 'Oil Filter')
        self.assertEqual(results[3][0], 'Air Filter')
        self.assertEqual(results[4][0], 'Fuel Filter')
        
        db.close()

# Run the unit tests
if __name__ == '__main__':
    unittest.main()