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

os.chdir(r"C:\Users\manag\Documents\GitHub\AIoftheTiger")

f = open("directory.txt", "r")
path = f.read()

folder_name = "Tiger_Woods_Extended_Highlights_From_Round_1_At_The_Northern_Trust_2020-gfna-rhpdJI Folder"
dst = path + "Test Data\\\\" + folder_name
folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)

initial_score = int(input("Enter 1 to score initially, enter anything else to rescore: "))

if initial_score == 1:
	csv_file = folder_name[:-7] + "CSV.csv"
	csv_path = path + "CSV\\\\" + csv_file

	#Dataframe that reads in the csv
	images_to_show = pd.read_csv(csv_path, header=None, index_col=False)
	#Destination folder with a similar name to the CSV file
	
	#image is a loop counter
	image = 0
	#image_rescored tells you how many images you changed
	image_rescored = 0
	# last_frame_name is a list with all of the changed images, allows us to revert back if necessary
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
			#Reduce the number of images that have been rescored
			image_rescored -= 1
			#Ensures we don't encounter an index error
			if image >= 0 and image_rescored >= 0:
				#Make image equal to its previous value
				image = last_frame_name[image_rescored][1]
				#Rever the name of the image and its flip back to its original, pop it out of list
				os.rename(dst + "\\" + last_frame_name[image_rescored][0], dst + "\\" + folder[images_to_show.iloc[image,0]])
				last_frame_name.pop()
				continue
			#Essentially, when we try to go back from the very first image we are unable to go negative and just stay there
			else:
				image = 0
				image_rescored = 0
				continue

		#Conver ASCII Value to actual number we pressed
		img_score = k - 48 
		#Renames the image with the score in the 5th to last position.
		# os.rename(dst + "\\frame" + str(images_to_show.iloc[image,0]+1) + '.jpg', dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')
		os.rename(dst + "\\" + folder[images_to_show.iloc[image,0]], dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')
		last_frame_name.append([str(image) + "_frame_" + str(img_score) + '.jpg', image])
		# print(last_frame_name)
		image_rescored += 1
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
	os.rename(path + "Test Data\\\\" + csv_file[:-7] + " Folder", path + "Test Data\\\\scored_" + csv_file[:-7] + " Folder")
	data_augmenter(path + "Test Data\\\\scored_" + csv_file[:-7] + " Folder")

else:
	#image is a loop counter
	image = 0
	#image_rescored tells you how many images you changed
	image_rescored = 0
	# last_frame_name is a list with all of the changed images, allows us to revert back if necessary
	last_frame_name = []

	#Our data is augmented with vertical flips so we only need to loop through the first half and we will automatically update the flipped copy
	while image < len(folder)/2:
		file_path = dst + "\\" + folder[image]	
		#Reads in rgb values of the file
		img_1 = cv2.imread(file_path)
		#Displays the image to the user
		cv2.imshow('image',img_1)
		#Waits until the user  presses a key to continue, goes back if they hit any key on the directional pad
		k = cv2.waitKey(0) & 0xFF
		mistake = go_back(k)
		#If a mistake is made and we need to go back
		if mistake == 1:
			#Reduce the number of images that have been rescored
			image_rescored -= 1
			#Ensures we don't encounter an index error
			if image >= 0 and image_rescored >= 0:
				#Make image equal to its previous value
				image = last_frame_name[image_rescored][1]
				#Rever the name of the image and its flip back to its original, pop it out of list
				os.rename(dst + "\\" + last_frame_name[image_rescored][0], dst + "\\" + folder[image])
				os.rename(dst + "\\flip_" + last_frame_name[image_rescored][0], dst + "\\flip_" + folder[image])
				last_frame_name.pop()
				continue
			#Essentially, when we try to go back from the very first image we are unable to go negative and just stay there
			else:
				image = 0
				image_rescored = 0
				continue

		#Conver ASCII Value to actual number we pressed99
		img_score = k - 48 
		#Renames according to the new score pressed.
		os.rename(dst + "\\" + folder[image], dst + "\\" + folder[image][:-5] + str(img_score) + '.jpg')
		os.rename(dst + "\\flip_" + folder[image], dst + "\\flip_" + folder[image][:-5] + str(img_score) + '.jpg')
		#Appends the name of the new image at position 0 and the index in our folder at position 1
		last_frame_name.append([folder[image][:-5] + str(img_score) + '.jpg', image])
		# print(last_frame_name)
		image_rescored += 1
		image += 1


	print("Done rescoring, deleting files if necessary")
	folder = os.listdir(dst)
	folder = sorted_alphanumeric(folder)

	#Removes any image that has been given the score of 9
	for scored_image in range(0,len(folder)):
		if folder[scored_image][-5] == "9":
			file_path = dst + "\\" + folder[scored_image]
			os.remove(file_path)

	#Renames folder itself to have a RE in front of it.
	os.rename(dst, path + "Test Data\\\\RE_" + folder_name)