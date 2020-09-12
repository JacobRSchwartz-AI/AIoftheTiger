import os
import re
import numpy as np
import cv2
import shutil
import math
import time
import pandas as pd
import PIL
import string
from PIL import Image


# Method to sort an entity alpha numerically
# numbers will appear first ordered from 0-9
# alphabetically chars will be ordered a-z
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


# Method to write the data passed as a parameter
# to a file specified as the other parameter to the method
def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0, len(data)):
            file.write("{}\n".format(data[x]))


# Method to format the filename with only valid characters
# that won't cause an error when reading the file names
# from the directory
def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
    return filename


# Rename files in a folder based on the input parameters
def rename_files_in_folder(folder, directory):
    for file in range(0, len(directory)):
        os.rename(folder + "\\" + directory[file], folder + "\\" + str(file) + directory[file][-12:])


# Method to fix the human error of reaction time
def reaction_time_fixer(folder, width, height):
    # Prints, pulls, and orders folder
    print(folder)


    dir = os.listdir(folder)
    dirlist = sorted_alphanumeric(dir)
    print("Resizing images in: " + folder)
    # Resizes every frame in the folder to the 256 by 144 px that the NN model uses
    for frame in range(0, len(dirlist)):
        frame_path = folder + "\\" + dirlist[frame]
        resizeImage(width, height, frame_path)

    rename_files_in_folder(folder, dirlist)

    # loop through folder and determine flip from 0 to 1
    # choose the frame before the flip and go back 30 using loop down below
    # if largest difference is 3x the second largest diff we need to rename frames
    # so that they reflect the flip
    # else delete all 30 we checked in the loop
    # continue looping through the folder
    # reset largest diff and second largest diff

    # Allows this process to repeat indefinetly until it can no longer improve
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
        # Loops through the list pulling the score of the images 2 at a time
        for image in range(len(dirlist) - 1):
            image1_score = str(dirlist[image][-5])
            image2_score = str(dirlist[image + 1][-5])

            # % done
            if image % round(len(dirlist) / 100) == 0:
                print(str(int(image / round(len(dirlist) / 100))) + "% done")

            # flip occurs here, we will look back at the previous 30 frames
            if image1_score != image2_score:
                start_frame = image
                end_frame = start_frame - 30

                if end_frame < 0:
                    end_frame = 0

                # We will be comparing the ratio of the largest_diff and second_diff
                # If this ratio exceeds 3 then that indicates that there was a severe jump and that is most likely where the data scoring should have flipped.
                largest_diff = 0
                second_diff = 0
                largest_diff_index = 0
                score = 0

                # Goes backwards from the start_frame to the end_frame 30 frames before
                for frame in range(start_frame, end_frame, -1):
                    image1 = cv2.imread(folder + "\\" + dirlist[frame])
                    image2 = cv2.imread(folder + "\\" + dirlist[frame + 1])
                    # Calculates similarity score between images
                    try:
                        score = similarity_Score(image1, image2)
                        # print(str(frame) + " image 1: " + str(frame + 1) + " image 2: Score: ", score)
                    except:
                        continue

                    # If these two are the most different stores it, moves down the previous largest diff, and stores the frame it occurred on.
                    if score > largest_diff:
                        second_diff = largest_diff
                        largest_diff = score
                        largest_diff_index = frame

                    # Second most dissimalar set of images
                    elif score > second_diff:
                        second_diff = score

                # rename all frames between the actual flip in the dataset and the likely spot where it should have flipped
                if largest_diff >= 3 * second_diff:
                    for i in range(start_frame, largest_diff_index, - 1):
                        file = dirlist[i]
                        label = dirlist[i][-5]
                        os.rename(folder + "\\" + file,
                                folder + "\\" + str(i) + "_frame_" + str((int(label) + 1) % 2) + '.jpg')
                # delete frames if we did not find a severe jump. This indicates a smooth camera transition and data that would not be useful
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


# Method to resize an image to the size specified by the parameters
def resizeImage(basewidth, baseheight, frame_path):
    img = Image.open(frame_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
    img = img.convert('RGB')
    img.save(frame_path)


# Method to split a video clip into images and store it in the
# directory specified
def video_splitter(valid_video_location, folder, start_prop):
    try:

        # creating a folder named folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    cam = cv2.VideoCapture(valid_video_location)
    total_frames = cam.get(cv2.CAP_PROP_FRAME_COUNT)
    # frame
    # currentframe = 0
    starting_frame = math.floor(start_prop*total_frames)
    ending_frame = math.floor((start_prop+0.1)*total_frames)

    cam.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)

    while True:

        # reading from frame
        ret, frame = cam.read()

        if ret: 
            if starting_frame < ending_frame:
                # if video is still left continue creating images
                name = folder + "\\" + "frame" + str(int(starting_frame / 3)) + ".jpg"

                if starting_frame % 150 == 0:
                    # os.system('cls')
                    print('Creating...' + name)
                    # writing the extracted images
                    cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
                starting_frame += 1

            else:
                break
        else:
            break

    
    cam.release()
    cv2.destroyAllWindows()


# Method to create images that have been flipped across an imaginary
# vertical line in the middle of the image thus creating a reflection
def data_augmenter(folder):
    scored_data_folder = os.listdir(folder)
    for image in range(0, len(scored_data_folder)):
        imageSource = folder + "\\" + scored_data_folder[image]
        img = cv2.imread(imageSource)
        vertical_img = img.copy()
        vertical_img = cv2.flip(img, 1)
        cv2.imwrite(folder + "\\flip_" + scored_data_folder[image], vertical_img)