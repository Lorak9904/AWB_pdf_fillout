import json
import fitz
from text_positions import TextPositions
from utils import AdressFormatter

# TODO:
# refactor, scaling/formatting
# unit tests

class PDFPopulator:
    def __init__(self, template_path: str, output_pdf_path: str, json_path: str) -> None:
        self.template_path: str = template_path
        self.output_pdf_path: str = output_pdf_path
        self.json_path: str = json_path
        self.text_positions = TextPositions().text_positions
        self.address_formatter = None # initialized in fill_pdf() method
        self.fontsize = 6
        self.color = (0, 0, 0)
    
    def load_data(self) -> dict:
        with open(self.json_path, "r") as f:
            return json.load(f)

    def fill_pdf(self) -> None:
        awb_data = self.load_data()
        self.address_formatter = AdressFormatter(awb_data, self.fontsize, self.color)
        doc = fitz.open(self.template_path)
        page = doc[0]

        page.insert_text(self.text_positions["AWB_Number"], awb_data["AWB_Number"], fontsize=self.fontsize, color=self.color)

        # shipper data formatting        
        self.address_formatter.format_shipper_data(awb_data, page)
        # consignee data
        self.address_formatter.format_consignee_data(awb_data, page)
        # issuing carrier data
        self.address_formatter.format_carrier_data(awb_data, page)

        # misc
        page.insert_text(self.text_positions["Agent_IATA_Code"], awb_data["Agent_IATA_Code"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Agent_Account_No"], awb_data["Agent_Account_No"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Accounting_Information"], awb_data["Accounting_Information"], fontsize=self.fontsize, color=self.color)
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
        # carriage
        page.insert_text(self.text_positions["Declared_Value_For_Carriage"], awb_data["Declared_Value_For_Carriage"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Declared_Value_For_Customs"], awb_data["Declared_Value_For_Customs"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Handling_Information"], awb_data["Handling_Information"], fontsize=self.fontsize, color=self.color)
        # save
        doc.save(output_pdf_path)
        doc.close()

# example usage
template_path = "../awb_templates/awb_template.pdf"
output_pdf_path = "filled_awb.pdf"
json_path = "../awb_templates/awb_example.json"
filler = PDFPopulator(template_path, output_pdf_path, json_path)
filler.fill_pdf()