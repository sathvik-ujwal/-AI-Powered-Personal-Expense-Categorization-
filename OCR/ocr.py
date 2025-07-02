from PIL import Image
import pytesseract

image_path = "/home/sathvik/Documents/image_data/shop_bill_1.jpg"
text = pytesseract.image_to_string(Image.open(image_path))

print("Extracted Text:")
print(text)
