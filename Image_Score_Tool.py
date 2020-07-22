import os
import re
import numpy as np
import cv2
import pandas as pd


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


f = open("directory.txt", "r")
path = f.read()

csv_file = "Rory McIlroy HighlightsCSV" + ".csv"
csv_path = path + csv_file

images_to_show = pd.read_csv(csv_path, header=None, index_col=False)

dst = path + "Scored Data\\scored_" + csv_file[:-7] + " Folder"

folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)

for image in range(0,len(images_to_show)):
	file_path = dst + "\\" + folder[images_to_show.iloc[image,0]]
	img_1 = cv2.imread(file_path)
	cv2.imshow('image',img_1)
	k = cv2.waitKey(0) & 0xFF
	img_score = k - 48 #Conver ASCII Value to actual number we pressed
	os.rename(dst + "\\frame" + str(images_to_show.iloc[image,0]+1) + '.jpg', dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')

print("Removing unscored images")
folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)
for image in range(len(images_to_show),len(folder)):
	file_path = dst + "\\" + folder[image]
	os.remove(file_path)

for scored_image in range(0,len(images_to_show)):
	if folder[scored_image][-5] == "9":
		file_path = dst + "\\" + folder[scored_image]
		os.remove(file_path)