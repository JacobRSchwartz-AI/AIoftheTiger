import os
import re
import numpy as np
import cv2
import pandas as pd


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def go_back(key_press):
	if key_press == 0:
		return 1
	else:
		return 0



f = open("directory.txt", "r")
path = f.read()

csv_file = "Justin Thomas_ Winning Highlights From The 2020 Sentry Tournament of Champions-z_lzGbUKhmYCSV" + ".csv"
csv_path = path + "\\CSV\\" + csv_file

images_to_show = pd.read_csv(csv_path, header=None, index_col=False)

# dst = path + "Scored Data\\\\scored_" + csv_file[:-7] + " Folder"
dst = r'C:\Users\HP\Documents\AI Frames\Scored Data\scored_Tiger Woods Players Championship Round 1 2018 Folder'

folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)
image = 0
last_frame_name = []

while (image < len(images_to_show)):
	file_path = dst + "\\" + folder[images_to_show.iloc[image,0]]
	print("image" + str(image))
	print("Image to show index" + str(images_to_show.iloc[image, 0]))
	img_1 = cv2.imread(file_path)
	cv2.imshow('image',img_1)
	k = cv2.waitKey(0) & 0xFF
	print(str(image))
	print("k = " + str(k))
	mistake = go_back(k)
	if mistake == 1:
		print("mistake start: " + str(image))
		image -= 1

		if image >= 0:
			os.rename(dst + "\\" + last_frame_name[image],
					  dst + "\\frame" + str(images_to_show.iloc[image, 0] + 1) + '.jpg')
			print("mistake end: " + str(image))
			continue

		else:
			image = 0
			continue

	img_score = k - 48 #Conver ASCII Value to actual number we pressed99
	os.rename(dst + "\\frame" + str(images_to_show.iloc[image,0]+1) + '.jpg', dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')
	last_frame_name.append(str(image) + "_frame_" + str(img_score) + '.jpg')
	image += 1

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