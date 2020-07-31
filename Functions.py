import os
import re
import numpy as np
import cv2
import shutil
import pandas as pd
import PIL
import string
from PIL import Image

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0,len(data)):
            file.write("{}\n".format(data[x]))

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def image_preprocessor(folder):
	f = open("directory.txt", "r")
	path = f.read()
	img_folder = path + "CSV\\\\" + folder

	csv_path = img_folder[:-7] + "CSV.csv"
	print(csv_path)
	img_folder_path = path + folder
	img_folder = os.listdir(img_folder_path)
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
		print(str(sim_score_max[1]) + " out of " + str(len(img_folder)-1) + " complete")
		sim_score_max = [0,0]

	write_to_file(csv_path, images_to_show)
	shutil.rmtree(img_folder_path)

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


def resizeImage(basewidth, baseheight, frame_path):
    img = Image.open(frame_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, baseheight), PIL.Image.ANTIALIAS)
    img.save(frame_path)

def video_splitter(cam, folder):
    try:

        # creating a folder named folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0

    while True:

        # reading from frame
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = folder + "\\" + "frame" + str(int(1+currentframe/3)) + ".jpg"

            if currentframe % 3 == 0:
                if currentframe % 300 == 0:
                    os.system('cls')
                    print('Creating...' + name)
                # writing the extracted images
                cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1

        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

def data_augmenter(folder):
    scored_data_folder = os.listdir(folder)

    for image in range(0,len(scored_data_folder)):
        imageSource = folder + "\\" + scored_data_folder[image]            
        img = cv2.imread(imageSource)
        vertical_img = img.copy()
        vertical_img = cv2.flip(img, 1)
        cv2.imwrite(folder + "\\flip_" + scored_data_folder[image], vertical_img)