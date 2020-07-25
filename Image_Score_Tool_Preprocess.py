import os
import re
import numpy as np
import cv2
import shutil
from Fix_Reaction_Time import similarity_Score
from Fix_Reaction_Time import rename_files_in_folder
import pandas as pd

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0,len(data)):
            file.write("{}\n".format(data[x]))



# parent_folder = os.listdir(path)

def image_preprocessor(folder):
	f = open("directory.txt", "r")
	path = f.read()
	img_folder = path + folder

	csv_path = img_folder[:-7] + "CSV.csv"
	img_folder_path = img_folder
	img_folder = os.listdir(img_folder)
	img_folder = sorted_alphanumeric(img_folder)

	dst = path + "Scored Data\\" + folder

	try:
		shutil.copytree(img_folder_path, dst)
	except FileExistsError:
		print("Folder " + dst + " already exists")
		decision = 0
		# decision = int(input("Enter 0 to overwrite and 1 to keep additional scored copies: "))
		if decision == 0:
			shutil.rmtree(dst)
			shutil.copytree(img_folder_path, dst)
			# print("Overwriting Data")
		else:
			dst += str(2)
			shutil.copytree(img_folder_path, dst)
			print("Copying Data")

	image = 0
	sim_score = 0
	sim_score_max = [0,0]
	images_to_show = [0]
	flag = 0

	# print("Preprocessing images ")
	while image < len(img_folder) and flag == 0:
		file_path = img_folder_path + "\\" + img_folder[image]
		img_1 = cv2.imread(file_path)
		for x in range(1,51):
			if image + x < len(img_folder):
				file_path_2 = img_folder_path + "\\" + img_folder[image+x]
				img_2 = cv2.imread(file_path_2)
				sim_score = similarity_Score(img_1,img_2)
				if sim_score > sim_score_max[0]:
					sim_score_max[0] = sim_score
					sim_score_max[1] = image + x
			else:
				sim_score_max[1] = len(img_folder)-1
				flag = 1
		image = sim_score_max[1]
		images_to_show.append(image)
		print(str(sim_score_max[1]) + " out of " + str(len(folder)-1) + " complete")
		sim_score_max = [0,0]

	write_to_file(csv_path, images_to_show)


# images_to_show = pd.read_csv(csv_path, header=None, index_col=False)

# print(images_to_show)


# print("Done preprocessing, ready to score")

# for image in range(0,len(images_to_show)):
# 	file_path = unscored_data_name + "\\" + folder[images_to_show[image]]
# 	img_1 = cv2.imread(file_path)
# 	cv2.imshow('image',img_1)
# 	k = cv2.waitKey(0) & 0xFF
# 	img_score = k - 48 #Conver ASCII Value to actual number we pressed
# 	os.rename(dst + "\\frame" + str(images_to_show[image]+1) + '.jpg', dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')

# print("Removing unscored images")
# folder = os.listdir(dst)
# folder = sorted_alphanumeric(folder)
# for image in range(len(images_to_show),len(folder)):
# 	file_path = dst + "\\" + folder[image]
# 	os.remove(file_path)

# for scored_image in range(0,len(images_to_show)):
# 	if folder[scored_image][-5] == "9":
# 		file_path = dst + "\\" + folder[scored_image]
# 		os.remove(file_path)