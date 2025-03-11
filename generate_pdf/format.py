import textwrap
import fitz
from text_positions import TextPositions

class Formatter():
    def __init__(self, awb_data: dict, fontsize: int, color: tuple) -> None:
        self.text_positions = TextPositions().text_positions
        self.awb_data = awb_data
        self.page = fitz.Page
        self.line_spacing = 10
        self.fontsize = fontsize
        self.color = color
    
    # formatting utility, wraps text into max_lines of max_width
    # if the text is to long it ends it with "..."
    def wrap_text(self, text, max_width=70, max_lines=3):
        wrapped_lines = textwrap.wrap(text, width=max_width, break_long_words=True, break_on_hyphens=True)

        if len(wrapped_lines) > max_lines:
            wrapped_lines = wrapped_lines[:max_lines]
            wrapped_lines[-1] = wrapped_lines[-1][:max_width - 3] + "..."

        return wrapped_lines
    
    # method used to format all the data that require multiple lines and eventual wrapping
    # used to format: Shipper, Consignee, Issuing_Carrier
    def format_data(self, awb_data: dict, page: fitz.Page, category: str) -> None:
        # wrap the address into multiple lines if needed (line exceeds maxlen)
        address_lines = self.wrap_text(awb_data[category]["Address"])
        base_x, base_y = self.text_positions[f"{category}_Address"]
        base_y -= 5

        for i, line in enumerate(address_lines):
            page.insert_text((base_x, base_y + (i * self.line_spacing)), line, fontsize=self.fontsize, color=self.color)
        last_address_y = base_y + (len(address_lines) * self.line_spacing)
        phone_position = (self.text_positions[f"{category}_Phone"][0], last_address_y)
        page.insert_text(phone_position, awb_data["Shipper"]["Phone"], fontsize=self.fontsize, color=self.color)
        if category == "Shipper":
            page.insert_text(self.text_positions[f"{category}_Account_Number"], awb_data[category]["Account_Number"], fontsize=self.fontsize, color=self.color)


    # used to format unstandarized text blocks: Accounting Information & Handling Information
    def format_text_block(self, awb_data: dict, page: fitz.Page, category: str, max_width=100, max_lines=6): 
        text_lines = self.wrap_text(awb_data[category], max_width, max_lines)
        base_x, base_y = self.text_positions[category]

        for i, line in enumerate(text_lines):
            page.insert_text((base_x, base_y + (i * self.line_spacing)), line, fontsize=self.fontsize, color=self.color)