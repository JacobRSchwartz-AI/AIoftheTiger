import PIL
from PIL import Image
import os

def resizeImage(basewidth, baseheight, frame_path):
    img = Image.open(frame_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
    img.save(frame_path)

f = open("directory.txt", "r")
path = f.read()

folder_name = path + "\\Test"
folder = os.listdir(folder_name)

for frame in range(0, len(folder)):
    frame_path = folder_name + "\\" + folder[frame]
    resizeImage(256, 144, frame_path)