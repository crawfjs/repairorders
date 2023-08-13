import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pandas._libs.tslibs.timestamps import Timestamp
import unittest
import uuid
import pandas as pd
from src.services.repair_orders_logging_service import RepairOrdersLoggingService
from src.usecases.window_by_datetime_to_get_latest_event import window_by_datetime

# Unit tests
class TestWindowByDateTimeToGetLatestEvent(unittest.TestCase):
    def setUp(self):
        # Data for testing
        data = [
            {'id': 1, 'date_time': '2023-08-01T13:00:00', 'cost': 'In Progress'},
            {'id': 2, 'date_time': '2023-08-02T08:00:01', 'cost': 'Not Started'},
            {'id': 3, 'date_time': '2023-08-02T12:00:02', 'cost': 'In Progress'},
            {'id': 4, 'date_time': '2023-08-03T10:00:03', 'cost': 'Completed'},
            {'id': 5, 'date_time': '2023-08-03T11:10:04', 'cost': 'In Progress'},
            {'id': 6, 'date_time': '2023-08-03T13:24:05', 'cost': 'Not Started'},
            {'id': 7, 'date_time': '2023-08-04T09:10:06', 'cost': 'In Progress'},
            {'id': 8, 'date_time': '2023-08-04T11:11:07', 'cost': 'Reopened'},
            {'id': 9, 'date_time': '2023-08-04T12:34:08', 'cost': 'Completed'},
            {'id': 10, 'date_time': '2023-08-04T14:01:09', 'cost': 'In Progress'},
        ]
        self.logger = RepairOrdersLoggingService(run_key=f"unittest-{uuid.uuid4()}")
        self.logger.log("Setting up TestWindowByDateTimeToGetLatestEvent")

        self.data = pd.DataFrame(data)        

    def tearDown(self):
        self.logger.log("Tear down complete for TestWindowByDateTimeToGetLatestEvent")
        self.data = None

    def test_window_of_1_day(self):
        self.logger.log("Testing window of 1 day")
        # Arrange
        expected_keys = [Timestamp('2023-08-01 00:00:00'), Timestamp('2023-08-02 00:00:00'), Timestamp('2023-08-03 00:00:00'), Timestamp('2023-08-04 00:00:00')]
        
        # Act
        result = window_by_datetime(self.logger, self.data, "1D")

        # Assert
        self.assertEqual(list(result.keys()), expected_keys)
    
    def test_window_of_2_days(self):
        # Arrange
        expected_keys = [Timestamp('2023-08-01 00:00:00'), Timestamp('2023-08-03 00:00:00')]
        
        # Act
        result = window_by_datetime(self.logger, self.data, "2D")

        # Assert
        self.assertEqual(list(result.keys()), expected_keys)

# Run the unit tests
if __name__ == '__main__':
    unittest.main()