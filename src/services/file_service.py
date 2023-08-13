from .repair_orders_logging_service import RepairOrdersLoggingService
from typing import List
import os

def read_files_from_dir(logger:RepairOrdersLoggingService, dir: str, file_prefix: str) -> List[str]:
    """
    Service method to read content from XML files and return the content from each file as a string in a list
    
    Parameters
    ----------
    logger: RepairOrdersLoggingService
        The logger to use for audit logging
    dir: str
        The directory to read the XML files from
    file_prefix: str
        The prefix of the XML files to read
        Example: "file_" will read all files that start with "file_"

    Returns
    -------
    List[str]
        Each element in the list is a string with the content of an XML file
    """

    data = []

    for root, _, files in os.walk(dir):
        for file in sorted(files):
            if file.lower().endswith('.xml') and file.startswith(file_prefix):
                xml_path = os.path.join(root, file)
                try:
                    logger.log(f"Reading {xml_path}")
                    with open(xml_path, 'r', encoding='utf-8') as xml_file:
                        content = xml_file.read()
                        content = content.rstrip('\r\n')
                        data.append(content)
                except Exception as e:
                    logger.error(f"Error reading {xml_path}: {e}")

    return data