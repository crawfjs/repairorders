from datetime import datetime
from .repair_part import RepairPart
from .repair_details import RepairDetails

import xml.etree.ElementTree as ET

class RepairOrder:
    def __init__(self, order_id: int, date_time: datetime, status: str, cost: float, repair_details: RepairDetails):
        self.order_id = order_id
        self.date_time = date_time
        self.status = status
        self.cost = cost
        self.repair_details = repair_details

    def to_xml(self):
        return f"""
        <event>
            <order_id>{self.order_id}</order_id>
            <date_time>{self.date_time}</date_time>
            <status>{self.status}</status>
            <cost>{self.cost}</cost>
            {self.repair_details.to_xml()}
        </event>
        """

    @staticmethod
    def from_xml(self, xml_content):
        event = ET.fromstring(xml_content)
        self.order_id = event.find("order_id").int
        self.date_time = datetime(event.find("date_time")).text
        self.status = event.find("status").text
        self.cost = event.find("cost").float
        self.repair_details = RepairDetails(
            event.find("repair_details/technician").text,
            [
                RepairPart(
                    part.attrib["name"],
                    part.attrib["quantity"]
                )
                for part in event.findall("repair_details/repair_parts/part")
            ]
        )
        return self

    @staticmethod
    def from_dict(dict_content):
        response = RepairOrder(
            order_id = dict_content["order_id"],
            date_time = dict_content["date_time"],
            status = dict_content["status"],
            cost = dict_content["cost"],
            repair_details = RepairDetails(
                dict_content["technician"],
                [
                    RepairPart(
                        part["name"],
                        part["quantity"]
                    )
                    for part in dict_content["repair_parts"]
                ]
            )
        )
        
        return response