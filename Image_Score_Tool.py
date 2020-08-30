import os
import re
import numpy as np
import cv2
import pandas as pd
from Functions import sorted_alphanumeric, data_augmenter

#Function that will return 1 if any directional key is pressed
def go_back(key_press):
	if key_press == 0:
		return 1
	else:
		return 0


f = open("directory.txt", "r")
path = f.read()

#Picks a specific CSV file that has the indices of the images that we want to score
csv_file = "2008_U.S._Open_Final_Round_-_Full_Telecast-Vvi_LtvptKs" + "CSV.csv"
csv_path = path + "CSV\\\\" + csv_file

#Dataframe that reads in the csv
images_to_show = pd.read_csv(csv_path, header=None, index_col=False)
#Destination folder with a similar name to the CSV file
dst = path + "Scored Data\\\\" + csv_file[:-7] + " Folder"

#Puts all of the images in a list and sorts them
folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)

#Loop counter and list with the names of the previous frames that we have scored
image = 0
last_frame_name = []

#Goes through the images to show
while image < len(images_to_show):
	#Pulls the file path based on each value in the df
	file_path = dst + "\\" + folder[images_to_show.iloc[image,0]]
	#Reads and shows the image
	img_1 = cv2.imread(file_path)
	cv2.imshow('image',img_1)
	#Waits until the user presses a key to continue
	k = cv2.waitKey(0) & 0xFF
	mistake = go_back(k)
	#if the back arrow was pressed, go back a frame
	if mistake == 1:
		image -= 1
		#If loop counter is a whole number, revert it back to its original name
		if image >= 0:
			os.rename(dst + "\\" + last_frame_name[image],
					  dst + "\\frame" + str(images_to_show.iloc[image, 0] + 1) + '.jpg')
			continue

		else:
			image = 0
			continue

	#Conver ASCII Value to actual number we pressed
	img_score = k - 48 
	#Renames the image with the score in the 5th to last position.
	os.rename(dst + "\\frame" + str(images_to_show.iloc[image,0]+1) + '.jpg', dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')
	last_frame_name.append(str(image) + "_frame_" + str(img_score) + '.jpg')
	image += 1

#Removes images that were not part of the scoring procedure
print("Removing unscored images")
folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)
for image in range(len(images_to_show),len(folder)):
	file_path = dst + "\\" + folder[image]
	os.remove(file_path)

#Removes any image with a score of 9
for scored_image in range(0,len(images_to_show)):
	if folder[scored_image][-5] == "9":
		file_path = dst + "\\" + folder[scored_image]
		os.remove(file_path)

#Adds the word scored to the front of the folder and performs data augmentation on it. 
os.rename(path + "Scored Data\\\\" + csv_file[:-7] + " Folder", path + "Scored Data\\\\scored_" + csv_file[:-7] + " Folder")
data_augmenter(path + "Scored Data\\\\scored_" + csv_file[:-7] + " Folder")