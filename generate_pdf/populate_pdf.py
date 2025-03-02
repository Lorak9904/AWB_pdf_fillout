import json
import fitz
from text_positions import TextPositions
from format import Formatter

# TODO:
# unit tests

class PDFPopulator:
    def __init__(self, template_path: str, output_pdf_path: str, awb_data_path: str, shipment_table_path: str) -> None:
        self.template_path: str = template_path
        self.output_pdf_path: str = output_pdf_path
        self.awb_data: str = awb_data_path
        self.shipment_table: str = shipment_table_path
        self.text_positions = TextPositions().text_positions
        self.formatter = None # initialized in fill_pdf() method
        self.fontsize = 6
        self.color = (0, 0, 0)
    
    # json_to_open: path to json file (awb data or shipment table)
    def load_data(self, json_to_open: str) -> dict:
        with open(json_to_open, "r") as f:
            return json.load(f)

    def fill_pdf(self) -> None:
        awb_data = self.load_data(self.awb_data)
        self.formatter = Formatter(awb_data, self.fontsize, self.color)
        doc = fitz.open(self.template_path)
        page = doc[0]

        page.insert_text(self.text_positions["AWB_Number"], awb_data["AWB_Number"], fontsize=self.fontsize, color=self.color)

        # formatable data insertion
        self.formatter.format_data(awb_data, page, "Shipper")
        self.formatter.format_data(awb_data, page, "Consignee")
        self.formatter.format_data(awb_data, page, "Issuing_Carrier")
        self.formatter.format_text_block(awb_data, page, "Accounting_Information")
        self.formatter.format_text_block(awb_data, page, "Handling_Information", 170, 4)

        # additional formatting not required
        page.insert_text(self.text_positions["Agent_IATA_Code"], awb_data["Agent_IATA_Code"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Agent_Account_No"], awb_data["Agent_Account_No"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Airport_Departure"], awb_data["Airport_Departure"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Routing_Destination_TO"], awb_data["ROUTING_DESTINATION"]["TO"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Routing_Destination_By_First_Carrier"], awb_data["ROUTING_DESTINATION"]["By_First_Carrier"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Routing_Destination_to"], awb_data["ROUTING_DESTINATION"]["to"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Routing_Destination_by"], awb_data["ROUTING_DESTINATION"]["by"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Routing_Destination_to_2"], awb_data["ROUTING_DESTINATION"]["to_2"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Routing_Destination_by_2"], awb_data["ROUTING_DESTINATION"]["by_2"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Airport_Destination"], awb_data["Airport_Destination"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Flight_Data"], awb_data["Flight_Data"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Currency"], awb_data["Currency"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["WT/VAL/PPD"], awb_data["WT/VAL"]["PPD"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["WT/VAL/COLL"], awb_data["WT/VAL"]["COLL"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["OTHER/PPD"], awb_data["OTHER"]["PPD"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["OTHER/COLL"], awb_data["OTHER"]["COLL"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["CHGS"], awb_data["CHGS"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Reference_Number"], awb_data["Reference_Number"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Declared_Value_For_Carriage"], awb_data["Declared_Value_For_Carriage"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Declared_Value_For_Customs"], awb_data["Declared_Value_For_Customs"], fontsize=self.fontsize, color=self.color)

        self.fill_shipment_table(doc[0])

        doc.save(self.output_pdf_path)
        doc.close()
    
    def fill_shipment_table(self, doc):
        shipment_data = self.load_data(self.shipment_table)
        # doc = fitz.open(self.template_path)
        page = doc

        # Define starting position (adjust based on PDF template)
        base_x = self.text_positions["Shipment_Table_Start_X"]
        base_y = self.text_positions["Shipment_Table_Start_Y"]
        row_height = 10  # Adjust based on PDF row spacing

        for index, item in enumerate(shipment_data["shipmentTable"]):
            y_offset = base_y + (index * row_height)

            page.insert_text((base_x, y_offset), str(item["noOfPieces"]), fontsize=self.fontsize, color=self.color)

            # dynamic measurement unit select todo
            page.insert_text((base_x + 30, y_offset), f'{item["grossWeight"]} kg', fontsize=self.fontsize, color=self.color)
            page.insert_text((base_x + 74, y_offset), item["k/lb"], fontsize=self.fontsize, color=self.color)

            page.insert_text((base_x + 88, y_offset), item["rateClass"], fontsize=self.fontsize, color=self.color)
            page.insert_text((base_x + 96, y_offset), item["commodity"], fontsize=self.fontsize, color=self.color)
            page.insert_text((base_x + 160, y_offset), str(item["chargeableWeight"]), fontsize=self.fontsize, color=self.color)
            page.insert_text((base_x + 215, y_offset), f'{item["rate/charge"]}', fontsize=self.fontsize, color=self.color)
            page.insert_text((base_x + 275, y_offset), f'{item["total"]}', fontsize=self.fontsize, color=self.color)

            # for now, the text is truncated if exceeds 57 chars
            nature_goods = item["natureAndQuantityOfGoods"]
            if len(nature_goods) > 57:
                nature_goods = nature_goods[:54] + "..."

            page.insert_text((base_x + 370, y_offset), nature_goods, fontsize=self.fontsize, color=self.color)



# example usage
template_path = "../awb_templates/awb_template.pdf"
output_pdf_path = "filled_awb.pdf"
json_path = "../awb_templates/awb_example.json"
shipment_table_path = "../awb_templates/shipment_table_example.json"
filler = PDFPopulator(template_path, output_pdf_path, json_path, shipment_table_path)
filler.fill_pdf()
