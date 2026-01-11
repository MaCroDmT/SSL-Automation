# Example code for generating a Code128 barcode
import barcode
from barcode.writer import ImageWriter

# Define data and format
data = '01745547578'
Code128 = barcode.get_barcode_class('code128')

# Create and save the barcode as a PNG
Code128(data, writer=ImageWriter()).save('my_barcode')
