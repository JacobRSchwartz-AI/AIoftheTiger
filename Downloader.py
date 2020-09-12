from __future__ import unicode_literals
import youtube_dl
import cv2
import os
import string
import shutil
import math
import time
import concurrent.futures
from Functions import format_filename, video_splitter, image_preprocessor, write_to_file
from moviepy.editor import VideoFileClip


ydl_opts = {}

# os.chdir(r"C:\Users\manag\Documents\GitHub\AIoftheTiger")
f = open("directory.txt", "r")
path = f.read()

#List of all videos to download from the internet
all_vids = [
           
            "https://www.youtube.com/watch?v=UtbO01lyZTw&frags=wn&ab_channel=PGATOUR",
			
            ]

# index of all_vids we are currently in
url_index = 0
#Not sure what this does, but its using the youtube_dl library the way the tutorial did
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	#Loops through every url in the list
	for url in all_vids:
		Downloads the video
		ydl.download([url])

		#Extracts file info so that we can know the name of the file and can do stuff with it immediately.
		file_info = ydl.extract_info(url)
		file_name = file_info['title'] + '-' + file_info['id'] + '.mkv'

		#Converts the file name from the file_info into a list
		file_name = list(file_name)
		#Loops through every character in the list and copies the changes that the library makes to the filename
		index = 0
		for char in file_name:
			if char == "|" or char == "/":
				file_name[index] = "_"			
			elif char == ":":
				file_name[index] = " -"
			
			index += 1

		# Change the list back to string, by using 'join' method of strings. 
		file_name = "".join(file_name)

		#Uses another function to convert the filename into a valid filename.
		# This is important because sometimes cv2 has difficulty turning a video into images if it doesn't like the name  
		valid_file_name = format_filename(file_name)
		video_location = path + file_name
		valid_video_location = path + valid_file_name
		try:
			shutil.move(video_location, valid_video_location)
		except FileNotFoundError:
			file_name = file_name[:-4] + '.mp4'
			valid_file_name = format_filename(file_name)
			video_location = path + file_name
			valid_video_location = path + valid_file_name
			shutil.move(video_location, valid_video_location)

		#Read in the video into cam using cv2
		
		#creates folder for output with split out images
		folder = valid_video_location[:-4] + ' Folder'
		# clip = VideoFileClip(valid_video_location)
		# length = clip.duration
		# print(length)
		# fps = cam.get(cv2.CAP_PROP_FPS)
		# print(fps)
		# total_frames = math.floor(fps*length)
		
		cam = cv2.VideoCapture(valid_video_location)
		total_frames = cam.get(cv2.CAP_PROP_FRAME_COUNT)	
		cam.release()
		cv2.destroyAllWindows()
		
		start_time = time.time()
		splitter_threads = [[valid_video_location, folder, 0],
							[valid_video_location, folder, 0.1],
							[valid_video_location, folder, 0.2],
							[valid_video_location, folder, 0.3],
							[valid_video_location, folder, 0.4],
							[valid_video_location, folder, 0.5],
							[valid_video_location, folder, 0.6],
							[valid_video_location, folder, 0.7],
							[valid_video_location, folder, 0.8],
							[valid_video_location, folder, 0.9]]
		

		# video_splitter(valid_video_location, folder, starting_proportions[8])
		# video_splitter(valid_video_location, folder, starting_proportions[9])

		try:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				for result in executor.map(lambda p: video_splitter(*p), splitter_threads):
					continue
					# print(test_folder_model[0])
		except Exception as e:
			print(str(e))

		
		folder = valid_file_name[:-4] + ' Folder'
		#Initializes a new name of a folder that does not contain the entire path because the entire path is added in the function itself.
		try:
			shutil.move(path + folder, path + "Test Data\\")
		except:
			shutil.rmtree(path + "Test Data\\" + folder)
			shutil.move(path + folder, path + "Test Data\\")
		


		preprocess_threads = [[folder, 0],
							[folder, 0.1],
							[folder, 0.2],
							[folder, 0.3],
							[folder, 0.4],
							[folder, 0.5],
							[folder, 0.6],
							[folder, 0.7],
							[folder, 0.8],
							[folder, 0.9]]
		images_to_show = []

		try:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				for result in executor.map(lambda p: image_preprocessor(*p), preprocess_threads):
					# print(result)
					images_to_show.append(result)
					# print(test_folder_model[0])
		except Exception as e:
			print(str(e))

		flattened_list = []

		#flatten the lis
		for x in images_to_show:
			for y in x:
				flattened_list.append(y)

		# For the love of storage space, we remove the video file after splitting it into frames.
		os.remove(valid_video_location)
		print(str(int(url_index + 1)) + " out of " + str(len(all_vids)) + " complete")
		url_index += 1


