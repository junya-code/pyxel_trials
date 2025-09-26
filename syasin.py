from PIL import Image

img = Image.open("resized.png")
img = img.resize((160, 120))
img.save("resized.png")
