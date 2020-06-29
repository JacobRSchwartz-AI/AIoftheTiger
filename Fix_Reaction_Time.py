import os
import cv2
import numpy as np
import re
from ResizeImages import resizeImage


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


# determines similarity score between two images
def similarity_Score(image1, image2):
    error = 0
    normalizer = len(image1) * len(image1[0]) * len(image1[0][0])
    image1_array = np.asarray(image1) / 255
    image2_array = np.asarray(image2) /255
    score_array = image1_array - image2_array
    score_array = np.square(score_array)
    error = 100*score_array.sum() / normalizer
    return error

def rename_files_in_folder(folder, directory):
    for file in range(0,len(directory)):
        os.rename(folder + "\\" + directory[file], folder + "\\" + str(file) + directory[file][-12:])

def reaction_time_fixer(folder, width, height):
    print(folder)
    dir = os.listdir(folder)
    dirlist = sorted_alphanumeric(dir)
    print("Resizing images in: " + folder)
    for frame in range(0,len(dirlist)):
        frame_path = folder + "\\" + dirlist[frame]
        resizeImage(width, height, frame_path)

    rename_files_in_folder(folder, dirlist)

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

    end_dir_len = 0
    start_dir_len = len(dirlist)
    pass_num = 1

    while end_dir_len != start_dir_len:
        print("Pass Number: " + str(pass_num))
        dir = os.listdir(folder)
        dirlist = sorted_alphanumeric(dir)
        start_dir_len = len(dirlist) 
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
                    #print(str(dirlist[frame]))
                    try:
                        score = similarity_Score(image1, image2)
                        #print(str(frame) + " image 1: " + str(frame + 1) + " image 2: Score: ", score)
                    except:
                        continue
                    
                    if score > largest_diff:
                        second_diff = largest_diff
                        largest_diff = score
                        largest_diff_index = frame

                    elif score > second_diff:
                        second_diff = score

                #print("Largest Diff: " + str(largest_diff) + "\nSecond Diff: " + str(second_diff))

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
                        try:
                            os.remove(folder + "\\" + file)
                        except:
                            continue

        dir = os.listdir(folder)
        dirlist = sorted_alphanumeric(dir)
        rename_files_in_folder(folder, dirlist)
        end_dir_len = len(dirlist)
        print(len(dirlist))
        pass_num += 1

# opens file specific to your individual directory
# f = open("directory.txt", "r")
# path = f.read()
# scored_data = os.listdir(path + "Scored Data")
# width = 256
# height = 144

# print(scored_data)

# for folder_file in range(0,len(scored_data)):
#     folder = path + "Scored Data\\" + scored_data[folder_file]
#     reaction_time_fixer(folder)