import PIL
from PIL import Image

basewidth = 256
baseheight = 144
img = Image.open("C:\\Users\\HP\\Documents\\AI Frames\\Tiger Woods Bridgestone Round 2 2018 Folder\\frame15.jpg")
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
img.save("C:\\Users\\HP\\Documents\\AI Frames\\Tiger Woods Bridgestone Round 2 2018 Folder\\frame15.jpg")
