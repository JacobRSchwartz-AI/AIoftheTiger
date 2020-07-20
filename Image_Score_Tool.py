import os
import re
import numpy as np
import cv2
import shutil
from Fix_Reaction_Time import similarity_Score
from Fix_Reaction_Time import rename_files_in_folder

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


f = open("C:\\Users\\manag\\PycharmProjects\\AIoftheTiger\\directory.txt", "r")
path = f.read()

img_folder = "KetoPizza Folder"
unscored_data_name = path + "\\" + img_folder
folder = os.listdir(unscored_data_name)
folder = sorted_alphanumeric(folder)

dst = path + "Scored Data\\scored_" + img_folder

try:
    shutil.copytree(unscored_data_name, dst)
except FileExistsError:
    print("Folder " + dst + " already exists")
    decision = int(input("Enter 0 to overwrite and 1 to keep additional scored copies: "))
    if decision == 0:
        shutil.rmtree(dst)
        shutil.copytree(unscored_data_name, dst)
        print("Overwriting Data")
    else:
        dst += str(2)
        shutil.copytree(unscored_data_name, dst)
        print("Copying Data")

image = 0
sim_score = 0
sim_score_max = [0,0]
images_to_show = [0]
flag = 0

print("Preprocessing images ")
while image < len(folder) and flag == 0:
	file_path = unscored_data_name + "\\" + folder[image]
	img_1 = cv2.imread(file_path)
	for x in range(1,51):
		if image + x < len(folder):
			file_path_2 = unscored_data_name + "\\" + folder[image+x]
			img_2 = cv2.imread(file_path_2)
			sim_score = similarity_Score(img_1,img_2)
			if sim_score > sim_score_max[0]:
				sim_score_max[0] = sim_score
				sim_score_max[1] = image + x
		else:
			sim_score_max[1] = len(folder)-1
			flag = 1
	image = sim_score_max[1]
	images_to_show.append(image)
	print(str(sim_score_max[1]) + " out of " + str(len(folder)-1) + " complete")
	sim_score_max = [0,0]


print("Done preprocessing, ready to score")

for image in range(0,len(images_to_show)):
	file_path = unscored_data_name + "\\" + folder[images_to_show[image]]
	img_1 = cv2.imread(file_path)
	cv2.imshow('image',img_1)
	k = cv2.waitKey(0) & 0xFF
	img_score = k - 48 #Conver ASCII Value to actual number we pressed
	os.rename(dst + "\\frame" + str(images_to_show[image]+1) + '.jpg', dst + "\\" + str(image) + "_frame_" + str(img_score) + '.jpg')

print("Removing unscored images")
folder = os.listdir(dst)
folder = sorted_alphanumeric(folder)
for image in range(len(images_to_show),len(folder)):
	file_path = dst + "\\" + folder[image]
	os.remove(file_path)
