
from tkinter import *
from turtle import pd

from PIL import Image, ImageTk

#
# an image viewer
import pandas as pd
from pandas import np


# class UI(Label):
#     def __init__(self, master, im):
#         if im.mode == "1":
#             # bitmap image
#             self.image = ImageTk.BitmapImage(im, foreground="white")
#             Label.__init__(self, master, image=self.image, bg="black", bd=0)
#         else:
#             # photo image
#             self.image = ImageTk.PhotoImage(im)
#             Label.__init__(self, master, image=self.image, bd=0)
#
# script interface
import sys
if not sys.argv[1:]:
##    print "Syntax: python pilview.py imagefile"
##    sys.exit(1)
    filename = "C:\\Users\\HP\\Documents\\AI Frames\\Tiger Woods Bridgestone Round 2 2018 Folder\\frame15.jpg"
else:
    filename = sys.argv[1]
root = Tk()
root.title(filename)
#im = Image.open(filename)  #<--- !!! works!

colourImg = Image.open(filename)
colourPixels = colourImg.convert("RGB")
colourArray = np.array(colourPixels.getdata()).reshape(colourImg.size + (3,))
indicesArray = np.moveaxis(np.indices(colourImg.size), 0, 2)
allArray = np.dstack((indicesArray, colourArray)).reshape((-1, 5))


df = pd.DataFrame(allArray, columns=["y", "x", "red","green","blue"])
print(df)
#UI(root, im).pack()
#root.mainloop()