import os
import cv2

# opens file specific to your individual directory
f = open("directory.txt", "r")
path = f.read()

import re
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


folder = path + "Scored Data\\scored_TW Memorial Round 3 2018 Folder"
dir = os.listdir(folder)

# determines similarity score between two images
def similarity_Score(image1, image2):
    error = 0
    normalizer = len(image1) * len(image1[0]) * len(image1[0][0])
    for x in range(0, len(image1)):
        for y in range(0, len(image1[0])):
            for z in range(0, len(image1[0][0])):
                error += ((image1[x][y][z] / 255) - (image2[x][y][z] / 255)) ** 2

    error /= normalizer
    return error


# image1 = cv2.imread(folder + "\\" + "204_frame_0.jpg")
# image2 = cv2.imread(folder + "\\" + "203_frame_0.jpg")
# print(similarity_Score(image1, image2))


# loop through folder and determine flip from 0 to 1
# choose the frame before the flip and go back 30 using loop down below
# if largest difference is 3x the second largest diff we need to rename frames
# so that they reflect the flip
# else delete all 30 we checked in the loop
# continue looping through the folder
# reset largest diff and second largest diff


dirlist = sorted_alphanumeric(dir)

image1_score = 0
image2_score = 0
for image in range(len(dirlist) - 1):
    image1_score = str(dirlist[image][-5])
    image2_score = str(dirlist[image + 1][-5])

    # % done
    if image % round(len(dirlist) / 100) == 0:
        print(str(int(image / round(len(dirlist) / 100))) + "% done")

    # flip occurs here?
    if image1_score != image2_score:
        start_frame = image
        end_frame = start_frame - 30

        if end_frame < 0:
            end_frame = 0

        largest_diff = 0
        second_diff = 0
        largest_diff_index = 0
        score = 0

        for frame in range(start_frame, end_frame, -1):
            image1 = cv2.imread(folder + "\\" + dirlist[frame])
            image2 = cv2.imread(folder + "\\" + dirlist[frame + 1])
            score = similarity_Score(image1, image2) * 100
            #print(str(frame) + " image 1: " + str(frame + 1) + " image 2: Score: ", score)

            if score > largest_diff:
                second_diff = largest_diff
                largest_diff = score
                largest_diff_index = frame

            elif score > second_diff:
                second_diff = score

        print("Largest Diff: " + str(largest_diff) + "\nSecond Diff: " + str(second_diff))

        # rename all frames within
        if largest_diff >= 3 * second_diff:
            for i in range(start_frame, largest_diff_index, - 1):
                file = dirlist[i]
                label = dirlist[i][-5]
                os.rename(folder + "\\" + file,
                          folder + "\\" + str(i) + "_frame_" + str((int(label) + 1) % 2) + '.jpg')
        #delete
        else:
            for i in range(end_frame, start_frame + 1):
                file = dirlist[i]
                os.remove(folder + "\\" + file)



