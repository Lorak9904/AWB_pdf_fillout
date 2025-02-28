from dataclasses import dataclass

# text positions hardcoded to according to the template (awb_templates/awb_template.py)
@dataclass
class TextPositions:
    text_positions = {
    "AWB_Number": (70, 20),
    "Shipper_Name": (65, 60),
    # split into multiple lines
    "Shipper_Address": (65, 70),
    "Shipper_Phone": (65, 80),
    "Shipper_Account_Number": (225, 50),
    "Consignee_Name": (65, 130),
    "Consignee_Address": (65, 140),
    "Consignee_Phone": (65, 150),
    "Issuing_Carrier_Name": (65, 195),
    "Issuing_Carrier_Address": (65, 205),
    "Issuing_Carrier_Phone": (65, 215),
    "Agent_IATA_Code": (65, 240),
    "Agent_Account_No": (200, 240),
    "Airport_Departure": (65, 265),
    "Routing_Destination_TO": (65, 285),
    "Routing_Destination_By_First_Carrier": (90, 285),
    "Routing_Destination_to": (217, 285),
    "Routing_Destination_by": (247, 285),
    "Routing_Destination_to_2": (270, 285),
    "Routing_Destination_by_2": (297, 285),
    "Airport_Destination": (65, 310),
    "Flight_Data": (200, 310),
    "Reference_Number": (320, 265),
    "Currency": (320, 285),
    "CHGS": (350, 290),
    "WT/VAL/PPD": (365, 290),
    "WT/VAL/COLL": (380, 290),
    "OTHER/PPD": (395, 290),
    "OTHER/COLL": (410, 290),
    "Accounting_Information": (350, 200),
    "Declared_Value_For_Carriage": (425, 290),
    "Declared_Value_For_Customs": (510, 290),
    "Handling_Information": (60, 335),
    # TODO: shipment data?
}