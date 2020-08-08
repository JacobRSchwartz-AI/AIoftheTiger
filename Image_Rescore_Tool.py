import os
import re
import numpy as np
import cv2
import pandas as pd
from Functions import sorted_alphanumeric, data_augmenter


def go_back(key_press):
	if key_press == 0:
		return 1
	else:
		return 0


f = open("directory.txt", "r")
path = f.read()
# data_augmenter(path + "Test Data\\\\scored_TW BMW Round 1 2018 Folder")
parent_folder = path + "Test Data\\\\"
parent_folder = os.listdir(parent_folder)

for sub_folder in range(0,len(parent_folder)):
	if parent_folder[sub_folder][0] != "R":
		folder_name = parent_folder[sub_folder]
		dst = path + "Test Data\\\\" + folder_name


		folder = os.listdir(dst)
		folder = sorted_alphanumeric(folder)
		image = 0
		image_rescored = 0
		last_frame_name = []

		while image < len(folder)/2:
			file_path = dst + "\\" + folder[image]
			if folder[image][-5] == "2":
				img_1 = cv2.imread(file_path)
				# print(img_1)
				# print(file_path)
				cv2.imshow('image',img_1)
				k = cv2.waitKey(0) & 0xFF
				mistake = go_back(k)
				if mistake == 1:
					image_rescored -= 1
					if image >= 0 and image_rescored >= 0:
						image = last_frame_name[image_rescored][1]
						os.rename(dst + "\\" + last_frame_name[image_rescored][0], dst + "\\" + folder[image])
						os.rename(dst + "\\flip_" + last_frame_name[image_rescored][0], dst + "\\flip_" + folder[image])
						last_frame_name.pop()
						continue

					else:
						image = 0
						image_rescored = 0
						continue

				img_score = k - 48 #Conver ASCII Value to actual number we pressed99
				os.rename(dst + "\\" + folder[image], dst + "\\" + folder[image][:-5] + str(img_score) + '.jpg')
				os.rename(dst + "\\flip_" + folder[image], dst + "\\flip_" + folder[image][:-5] + str(img_score) + '.jpg')
				last_frame_name.append([folder[image][:-5] + str(img_score) + '.jpg', image])
				# print(last_frame_name)
				image_rescored += 1
			image += 1

		print("Removing unscored images")
		folder = os.listdir(dst)
		folder = sorted_alphanumeric(folder)

		for scored_image in range(0,len(folder)):
			if folder[scored_image][-5] == "9":
				file_path = dst + "\\" + folder[scored_image]
				os.remove(file_path)


		os.rename(dst, path + "Test Data\\\\RE" + folder_name)