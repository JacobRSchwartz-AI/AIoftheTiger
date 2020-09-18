import cv2
import os

path = os.getcwd() + "\\"

scored_data_name = path + "\\Test Data\\"
scored_data_folder = os.listdir(scored_data_name)

#Used for widescale but consistent data renaming
#For example, when we combined Tiger with the other golfers we used this file.

#Loops through every folder in a parent folder
for folder in range(0,len(scored_data_folder)):
    #Adds a subfolder and puts it in order
    image_folder_source = scored_data_name + scored_data_folder[folder]
    image_folder = os.listdir(image_folder_source)
    print(image_folder_source)
    #Loops through the subfolder and renames if necessary
    for image in range(0,len(image_folder)):
        imageSource = image_folder_source + "\\" + image_folder[image]
        #The fifth to last position is where our score is always located because it always precedes the .jpg
        if imageSource[-5] == "6":
            os.rename(imageSource,imageSource[:-5] + "2.jpg")
        elif imageSource[-5] == "5":
            os.rename(imageSource,imageSource[:-5] + "1.jpg")
