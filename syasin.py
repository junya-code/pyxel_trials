from PIL import Image

img = Image.open("original.png")
img = img.resize((256, 256))
img.save("resized.png")
