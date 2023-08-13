from .repair_part import RepairPart
from typing import List
import pandas as pd

class RepairDetails:
    def __init__(self, technician, repair_parts: List[RepairPart]):
        self.technician = technician
        self.repair_parts = repair_parts

    def to_xml(self):
        return f"""
        <repair_details>
            <technician>{self.technician}</technician>
            <repair_parts>
                {self.repair_parts.to_xml()}
            </repair_parts>
        </repair_details>
        """