import cv2
import os

f = open("directory.txt", "r")
path = f.read()

scored_data_name = path + "\\Test Data\\"
scored_data_folder = os.listdir(scored_data_name)

for folder in range(0,len(scored_data_folder)):
    image_folder_source = scored_data_name + scored_data_folder[folder]
    image_folder = os.listdir(image_folder_source)
    print(image_folder_source)
    for image in range(0,len(image_folder)):
        imageSource = image_folder_source + "\\" + image_folder[image]
        if imageSource[-5] == "6":
            os.rename(imageSource,imageSource[:-5] + "2.jpg")
        elif imageSource[-5] == "5":
            os.rename(imageSource,imageSource[:-5] + "1.jpg")
