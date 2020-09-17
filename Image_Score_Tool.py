import os
import re
import numpy as np
import cv2
import pandas as pd
import shutil
from Functions import sorted_alphanumeric, data_augmenter, resizeImage
from tkinter import filedialog
from tkinter import *


#Function that will return 1 if any directional key is pressed
def go_back(key_press):
	if key_press == 0:
		return 1
	else:
		return 0

def fun_directory_selector(request_string: str, selected_directory_list: list, search_directory):
	directory_path_string = filedialog.askdirectory(initialdir=search_directory, title=request_string)

	if len(directory_path_string) > 0:
		selected_directory_list.append(directory_path_string)
		print(directory_path_string + " added to be scored")
		fun_directory_selector('Select the next Directory or Cancel to end', selected_directory_list, os.path.dirname(directory_path_string))

	return selected_directory_list

root = Tk()
root.withdraw()
f = open("directory.txt", "r")
path = f.read()
# folder_selected = filedialog.askdirectory()
folders_selected = []
fun_directory_selector("request string", folders_selected, path + "\\\\Data\\\\Unscored Data")


for folder_selected in folders_selected:
	dst = folder_selected
	folder = os.listdir(dst)
	folder = sorted_alphanumeric(folder)

	#image is a loop counter
	image = 0
	#image_rescored tells you how many images you changed
	image_rescored = 0
	# last_frame_name is a list with all of the changed images, allows us to revert back if necessary
	last_frame_name = []

	#Goes through the images to show
	while image < len(folder):
		#Pulls the file path based on each value in the df
		file_path = dst + "\\" + folder[image]
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
				os.rename(dst + "\\" + last_frame_name[image_rescored][0], dst + "\\" + folder[image])
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
		os.rename(dst + "\\" + folder[image], dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')
		last_frame_name.append([str(image) + "_frame_" + str(img_score) + '.jpg', image])
		# print(last_frame_name)
		image_rescored += 1
		image += 1

	cv2.destroyAllWindows()
	#Removes images that were not part of the scoring procedure
	print("Removing delete images")
	folder = os.listdir(dst)
	folder = sorted_alphanumeric(folder)


	#Removes any image with a score of 9
	for scored_image in range(0,len(folder)):
		if folder[scored_image][-5] == "9":
			file_path = dst + "\\" + folder[scored_image]
			os.remove(file_path)


	data_augmenter(folder_selected)

	image_folder = os.listdir(folder_selected)

	for char in range(len(folder_selected)-1,0,-1):
		if folder_selected[char] == "/":
			char_slice = char
			break

	#Input size for our image into the neural network, Ultra HD 4k shit
	height_px = 144
	width_px = 256

	for image in image_folder:
		resizeImage(width_px, height_px, folder_selected + "////" + image)
		os.rename(folder_selected + "////" + image, folder_selected + "////" + folder_selected[char_slice:] + "_" + image)
		shutil.move(folder_selected + "\\\\" + folder_selected[char_slice:] + "_" + image, path + "Data\\\\Scored Data\\\\" + image[-5])

	shutil.rmtree(folder_selected)