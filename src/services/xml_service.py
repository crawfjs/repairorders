import logging
import pandas as pd
import xml.etree.ElementTree as ET

from typing import List
from services.repair_orders_logging_service import RepairOrdersLoggingService

def parse_xml(logger:RepairOrdersLoggingService, file_contents: List[str]) -> pd.DataFrame:
    """
    Service method to parse event XML content and store it into a Pandas DataFrame
    
    Parameters
    ----------
    logger: RepairOrdersLoggingService
        The logger to use for audit logging
    file_contents: List[str]
        Each string is the content from an xml file and represents a complete xml structure

    Example content record:
    <event>
        <order_id>123</order_id>
        <date_time>2023-08-10T12:34:56</date_time>
        <status>Completed</status>
        <cost>100.50</cost>
        <repair_details>
            <technician>John Doe</technician>
            <repair_parts>
                <part name="Brake Pad" quantity="2"/>
                <part name="Oil Filter" quantity="1"/>
            </repair_parts>
        </repair_details>
    </event>

    Returns
    -------
    pandas.DataFrame
    """
    data = []

    for xml_content in file_contents:
        try:
            event = ET.fromstring(xml_content)
            data.append({
                "order_id": event.find("order_id").text,
                "date_time": event.find("date_time").text,
                "status": event.find("status").text,
                "cost": event.find("cost").text,
                "technician": event.find("repair_details/technician").text,
                "repair_parts": [
                    {
                        "name": part.attrib["name"],
                        "quantity": part.attrib["quantity"]
                    }
                    for part in event.findall("repair_details/repair_parts/part")
                ]
            })
        except ET.ParseError as e:
            logger.error(f"Error parsing XML: {e} {xml_content}")

    df = pd.DataFrame(data)
    return df