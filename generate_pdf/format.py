import textwrap
import fitz
from text_positions import TextPositions

# TODO: remove redundancy
class AdressFormatter():
    def __init__(self, awb_data: dict, fontsize: int, color: tuple) -> None:
        self.text_positions = TextPositions().text_positions
        self.awb_data = awb_data
        self.page = fitz.Page
        self.line_spacing = 10
        self.fontsize = fontsize
        self.color = color
    
    def wrap_text(self, text, max_width=70, max_lines=3):
        wrapped_lines = textwrap.wrap(text, width=max_width)

        if len(wrapped_lines) > max_lines:
            wrapped_lines = wrapped_lines[:max_lines]
            wrapped_lines[-1] = wrapped_lines[-1][:max_width - 3] + "..."

        return wrapped_lines
    
    def format_shipper_data(self, awb_data: dict, page: fitz.Page) -> None:
        # wrap shipper address into multiple lines if needed (line exceeds maxlen)
        shipper_address_lines = self.wrap_text(awb_data["Shipper"]["Address"])
        base_x, base_y = self.text_positions["Shipper_Address"]
        base_y -= 5 # 5 pixels higher for padding

        for i, line in enumerate(shipper_address_lines):
            page.insert_text((base_x, base_y + (i * self.line_spacing)), line, fontsize=self.fontsize, color=self.color)
        # calc new-y according to no. lines used
        last_address_y = base_y + (len(shipper_address_lines) * self.line_spacing)  # Last used Y position
        # adjusted pos for shipper phone
        shipper_phone_position = (self.text_positions["Shipper_Phone"][0], last_address_y)
        page.insert_text(shipper_phone_position, awb_data["Shipper"]["Phone"], fontsize=self.fontsize, color=self.color)
        page.insert_text(self.text_positions["Shipper_Account_Number"], awb_data["Shipper"]["Account_Number"], fontsize=self.fontsize, color=self.color)

    def format_consignee_data(self, awb_data: dict, page: fitz.Page) -> None:
        consignee_name_position = (self.text_positions["Consignee_Name"][0], self.text_positions["Consignee_Name"][1] - 5)
        page.insert_text(consignee_name_position, awb_data["Consignee"]["Name"], fontsize=self.fontsize, color=self.color)

        consignee_address_lines = self.wrap_text(awb_data["Consignee"]["Address"])

        base_x, base_y = self.text_positions["Consignee_Address"]
        base_y -= 5  # 5 pixels higher for padding

        for i, line in enumerate(consignee_address_lines):
            page.insert_text((base_x, base_y + (i * self.line_spacing)), line, fontsize=self.fontsize, color=self.color)

        # new y pos based on no. of lines
        last_address_y = base_y + (len(consignee_address_lines) * self.line_spacing)
        consignee_phone_position = (self.text_positions["Consignee_Phone"][0], last_address_y)
        page.insert_text(consignee_phone_position, awb_data["Consignee"]["Phone"], fontsize=self.fontsize, color=self.color)

    def format_carrier_data(self, awb_data: dict, page: fitz.Page) -> None:
        issuing_carrier_name_position = (self.text_positions["Issuing_Carrier_Name"][0], self.text_positions["Issuing_Carrier_Name"][1] - 5)
        page.insert_text(issuing_carrier_name_position, awb_data["Issuing_Carrier"]["Name"], fontsize=self.fontsize, color=self.color)

        issuing_carrier_address_lines = self.wrap_text(awb_data["Issuing_Carrier"]["Address"])

        base_x, base_y = self.text_positions["Issuing_Carrier_Address"]
        base_y -= 5  # Move everything 5 pixels higher

        for i, line in enumerate(issuing_carrier_address_lines):
            page.insert_text((base_x, base_y + (i * self.line_spacing)), line, fontsize=self.fontsize, color=self.color)

        # new y pos based on no. of lines
        last_address_y = base_y + (len(issuing_carrier_address_lines) * self.line_spacing)

        # --- Adjusted Position for Issuing Carrier Phone ---
        issuing_carrier_phone_position = (self.text_positions["Issuing_Carrier_Phone"][0], last_address_y - 1)
        page.insert_text(issuing_carrier_phone_position, awb_data["Issuing_Carrier"]["Phone"], fontsize=self.fontsize, color=self.color)