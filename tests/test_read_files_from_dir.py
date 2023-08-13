import sys
sys.path.append('../')

import unittest
import os
import uuid
from src.services.file_service import read_files_from_dir
from src.services.repair_orders_logging_service import RepairOrdersLoggingService

# Unit tests
class TestReadFilesFromDir(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and XML files for testing
        self.temp_dir = 'tmp/test_read_files_from_dir'
        os.makedirs(self.temp_dir, exist_ok=True)

        self.logger = RepairOrdersLoggingService(run_key=f"unittest-{uuid.uuid4()}")
        
        # Generate some XML content
        for i in range(1, 4):    
            with open(os.path.join(self.temp_dir, f"file-{i}.xml"), 'w') as file:
                xml_content = self.__generate_content__(i)
                file.write(xml_content)

    def tearDown(self):
        # Clean up the temporary directory and files
        for file in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file)
            os.remove(file_path)
        os.rmdir(self.temp_dir)

    def __generate_content__(self, index: int):
        return f"<data>Content of XML file {index}</data>"

    def test_read_files_from_dir(self):
        xml_contents = read_files_from_dir(self.logger, self.temp_dir, "file-")
        expected_contents = [self.__generate_content__(i) for i in range(1, 4)]
        self.assertEqual(xml_contents, expected_contents)

# Run the unit tests
if __name__ == '__main__':
    unittest.main()