import os
import re
import numpy as np
import cv2
import shutil
import pandas as pd
import PIL
import string
from PIL import Image

# Method to sort an entity alpha numerically
# numbers will appear first ordered from 0-9
# alphabetically chars will be ordered a-z
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)

# Method to write the data passed as a parameter
# to a file specified as the other parameter to the method
def write_to_file(filepath: str, data):
    with open(filepath, "w") as file:
        for x in range(0,len(data)):
            file.write("{}\n".format(data[x]))

# Method to format the filename with only valid characters
# that won't cause an error when reading the file names
# from the directory
def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

# Method to preprocess a folder of images by creating a CSV with the index 
# of images we want to include in our dataset as the results of their similarity score
def image_preprocessor(folder):
	f = open("directory.txt", "r")
	path = f.read()
	img_folder = path + "CSV\\\\" + folder

# Define the path that will contain the CSV of indices of the images that
# are different based on their similarity score
	csv_path = img_folder[:-7] + "CSV.csv"
	print(csv_path)
	img_folder_path = path + folder
	img_folder = os.listdir(img_folder_path)
	img_folder = sorted_alphanumeric(img_folder)

	dst = path + "Scored Data\\" + folder

# Creates copies of all of our images into another folder for some reason
	try:
		shutil.copytree(img_folder_path, dst)
	#Overwrites existing files, allows for possibility of making an additional copy
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
	
	#Loop counter
	image = 0
	sim_score = 0
	sim_score_max = [0,0]
	#Always shows the first image
	images_to_show = [0]
	flag = 0

# Define which images to score
	# print("Preprocessing images ")
	while image < len(img_folder) and flag == 0:
		file_path = img_folder_path + "\\" + img_folder[image]
		img_1 = cv2.imread(file_path)
		#Picks an image as a starting point, checks the next 50 images
		for x in range(1,51):
			if image + x < len(img_folder):
				file_path_2 = img_folder_path + "\\" + img_folder[image+x]
				img_2 = cv2.imread(file_path_2)
				sim_score = similarity_Score(img_1,img_2)
				#Keeps only the index of the image that is the most different from the first image
				if sim_score > sim_score_max[0]:
					sim_score_max[0] = sim_score
					sim_score_max[1] = image + x
			#Makes sure we keep the last image, signals that we are done
			else:
				sim_score_max[1] = len(img_folder)-1
				flag = 1
		#Pulls the index of the most dissimilar images.
		#Continues the loop with that image as the base and checking the next 50 against it.
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

# Rename files in a folder based on the input parameters
def rename_files_in_folder(folder, directory):
    for file in range(0,len(directory)):
        os.rename(folder + "\\" + directory[file], folder + "\\" + str(file) + directory[file][-12:])

# Method to fix the human error of reaction time
def reaction_time_fixer(folder, width, height):
    #Prints, pulls, and orders folder
	print(folder)
    dir = os.listdir(folder)
    dirlist = sorted_alphanumeric(dir)
    print("Resizing images in: " + folder)
	#Resizes every frame in the folder to the 256 by 144 px that the NN model uses
    for frame in range(0,len(dirlist)):
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

	#Allows this process to repeat indefinetly until it can no longer improve
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
		#Loops through the list pulling the score of the images 2 at a time
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

				#We will be comparing the ratio of the largest_diff and second_diff
				#If this ratio exceeds 3 then that indicates that there was a severe jump and that is most likely where the data scoring should have flipped.
                largest_diff = 0
                second_diff = 0
                largest_diff_index = 0
                score = 0

				#Goes backwards from the start_frame to the end_frame 30 frames before
                for frame in range(start_frame, end_frame, -1):
                    image1 = cv2.imread(folder + "\\" + dirlist[frame])
                    image2 = cv2.imread(folder + "\\" + dirlist[frame + 1])
					#Calculates similarity score between images
                    try:
                        score = similarity_Score(image1, image2)
                        #print(str(frame) + " image 1: " + str(frame + 1) + " image 2: Score: ", score)
                    except:
                        continue
                    
					#If these two are the most different stores it, moves down the previous largest diff, and stores the frame it occurred on.
                    if score > largest_diff:
                        second_diff = largest_diff
                        largest_diff = score
                        largest_diff_index = frame

					#Second most dissimalar set of images
                    elif score > second_diff:
                        second_diff = score

                
                # rename all frames between the actual flip in the dataset and the likely spot where it should have flipped
                if largest_diff >= 3 * second_diff:
                    for i in range(start_frame, largest_diff_index, - 1):
                        file = dirlist[i]
                        label = dirlist[i][-5]
                        os.rename(folder + "\\" + file,
                                folder + "\\" + str(i) + "_frame_" + str((int(label) + 1) % 2) + '.jpg')
                #delete frames if we did not find a severe jump. This indicates a smooth camera transition and data that would not be useful
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
    img.save(frame_path)

# Method to split a video clip into images and store it in the
# directory specified
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

# Method to create images that have been flipped across an imaginary
# vertical line in the middle of the image thus creating a reflection
def data_augmenter(folder):
    scored_data_folder = os.listdir(folder)

    for image in range(0,len(scored_data_folder)):
        imageSource = folder + "\\" + scored_data_folder[image]            
        img = cv2.imread(imageSource)
        vertical_img = img.copy()
        vertical_img = cv2.flip(img, 1)
        cv2.imwrite(folder + "\\flip_" + scored_data_folder[image], vertical_img)