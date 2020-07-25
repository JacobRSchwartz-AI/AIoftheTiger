import cv2
import os

f = open("directory.txt", "r")
path = f.read()

scored_data_name = path + "\\Scored Data\\"
scored_data_folder = os.listdir(scored_data_name)

for folder in range(0,len(scored_data_folder)):
    image_folder_source = scored_data_name + scored_data_folder[folder]
    image_folder = os.listdir(image_folder_source)
    print(image_folder_source)
    for image in range(0,len(image_folder)):
        imageSource = image_folder_source + "\\" + image_folder[image]
        if imageSource[-5] == "6":
            os.rename(imageSource,imageSource[:-5] + "3.jpg")
        elif imageSource[-5] == "5":
            os.rename(imageSource,imageSource[:-5] + "4.jpg")
        elif imageSource[-5] == "7":
            os.rename(imageSource,imageSource[:-5] + "5.jpg")
        elif imageSource[-5] == "8":
            os.rename(imageSource,imageSource[:-5] + "6.jpg")
        # img = cv2.imread(imageSource)
        # vertical_img = img.copy()
        # vertical_img = cv2.flip(img, 1)
        # cv2.imwrite(image_folder_source + "\\flip_" + image_folder[image], vertical_img)


 
 

