import fitz
import json

def load_json(json_path: str) -> dict:
    with open(json_path, "r") as f:
        return json.load(f)

template_path = "../awb_templates/awb_template.pdf"
output_pdf_path = "filled_awb.pdf"

doc = fitz.open(template_path)

text_positions = {
    "AWB_Number": (70, 20),
    "Shipper_Name": (65, 60),
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
    # cant be hardcoded, in form of a list
    # "Shipment_No_of_Pieces": (100, 460),
    # "Shipment_Weight": (300, 460),
    # "Shipment_Charge": (100, 440),
    # "Total_Prepaid": (100, 420),
    # "Total_Collect": (300, 420),
    # "Executed_On_Date": (100, 400),
    # "Executed_On_Place": (300, 400),
    # "Shipper_Certification": (100, 380),
    # "Signatures_Shipper": (100, 360),
    # "Signatures_Issuer": (300, 360),
    # "Original_Copy": (100, 340)
}



page = doc[0]
awb_data = load_json("../awb_templates/awb_example.json")

# insert text at specified positions
page.insert_text(text_positions["AWB_Number"], awb_data["AWB_Number"], fontsize=8, color=(0, 0, 0))
page.insert_text(text_positions["Shipper_Name"], awb_data["Shipper"]["Name"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Shipper_Address"], awb_data["Shipper"]["Address"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Shipper_Phone"], awb_data["Shipper"]["Phone"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Shipper_Account_Number"], awb_data["Shipper"]["Account_Number"], fontsize=8, color=(0, 0, 0))

page.insert_text(text_positions["Consignee_Name"], awb_data["Consignee"]["Name"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Consignee_Address"], awb_data["Consignee"]["Address"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Consignee_Phone"], awb_data["Consignee"]["Phone"], fontsize=6, color=(0, 0, 0))

page.insert_text(text_positions["Issuing_Carrier_Name"], awb_data["Issuing_Carrier"]["Name"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Issuing_Carrier_Address"], awb_data["Issuing_Carrier"]["Address"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Issuing_Carrier_Phone"], awb_data["Issuing_Carrier"]["Phone"], fontsize=6, color=(0, 0, 0))

page.insert_text(text_positions["Agent_IATA_Code"], awb_data["Agent_IATA_Code"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Agent_Account_No"], awb_data["Agent_Account_No"], fontsize=6, color=(0, 0, 0))

page.insert_text(text_positions["Accounting_Information"], awb_data["Accounting_Information"], fontsize=6, color=(0, 0, 0))

page.insert_text(text_positions["Airport_Departure"], awb_data["Airport_Departure"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Airport_Destination"], awb_data["Airport_Destination"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Flight_Data"], awb_data["Flight_Data"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Currency"], awb_data["Currency"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["WT/VAL/PPD"], awb_data["WT/VAL"]["PPD"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["WT/VAL/COLL"], awb_data["WT/VAL"]["COLL"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["OTHER/PPD"], awb_data["OTHER"]["PPD"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["OTHER/COLL"], awb_data["OTHER"]["COLL"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["CHGS"], awb_data["CHGS"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Reference_Number"], awb_data["Reference_Number"], fontsize=6, color=(0, 0, 0))

# carriage
page.insert_text(text_positions["Declared_Value_For_Carriage"], awb_data["Declared_Value_For_Carriage"], fontsize=6, color=(0, 0, 0))
page.insert_text(text_positions["Declared_Value_For_Customs"], awb_data["Declared_Value_For_Customs"], fontsize=6, color=(0, 0, 0))

page.insert_text(text_positions["Handling_Information"], awb_data["Handling_Information"], fontsize=6, color=(0, 0, 0))
# shipment details
# shipment = awb_data["Shipment"][0]
# page.insert_text(text_positions["Shipment_No_of_Pieces"], str(shipment["No_of_Pieces"]), fontsize=10, color=(0, 0, 0))
# page.insert_text(text_positions["Shipment_Weight"], str(shipment["Weight"]), fontsize=10, color=(0, 0, 0))
# page.insert_text(text_positions["Shipment_Charge"], str(shipment["Charge"]), fontsize=10, color=(0, 0, 0))

# page.insert_text(text_positions["Executed_On_Date"], awb_data["Executed_On"]["Date"], fontsize=10, color=(0, 0, 0))
# page.insert_text(text_positions["Executed_On_Place"], awb_data["Executed_On"]["Place"], fontsize=10, color=(0, 0, 0))

# Save the filled PDF
doc.save(output_pdf_path)
doc.close()

print(f"Filled AWB saved as: {output_pdf_path}")
