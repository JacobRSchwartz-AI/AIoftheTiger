from __future__ import unicode_literals
import youtube_dl
import cv2
import os
import string
import shutil
from Functions import format_filename, video_splitter, image_preprocessor

ydl_opts = {}

f = open("directory.txt", "r")
path = f.read()

#List of all videos to download from the internet
all_vids = [
           
            "https://www.youtube.com/watch?v=pQBwjPL6RIk"
            ]

#Not sure what this does, but its using the youtube_dl library the way the tutorial did
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	#Loops through every url in the list
    for url in range(0,len(all_vids)):
		#Downloads the video
        ydl.download([all_vids[url]])

		#Extracts file info so that we can know the name of the file and can do stuff with it immediately.
        file_info = ydl.extract_info(all_vids[url])
        file_name = file_info['title'] + '-' + file_info['id'] + '.mp4'

		#Converts the file name from the file_info into a list
        file_name = list(file_name)
		#Loops through every character in the list and copies the changes that the library makes to the filename
        for char in range(0,len(file_name)):
            if file_name[char] == "|" or file_name[char] == "/":
                file_name[char] = "_" 

		# Change the list back to string, by using 'join' method of strings. 
        file_name = "".join(file_name)

		#Uses another function to convert the filename into a valid filename.
		# This is important because sometimes cv2 has difficulty turning a video into images if it doesn't like the name  
        valid_file_name = format_filename(file_name)
        video_location = path + file_name
        valid_video_location = path + valid_file_namef 
        shutil.move(video_location, valid_video_location)

		#Read in the video into cam using cv2
        cam = cv2.VideoCapture(valid_video_location)
        #creates folder for output with split out images
        folder = valid_video_location[:-4] + ' Folder'
        video_splitter(cam, folder)

		#Initializes a new name of a folder that does not contain the entire path because the entire path is added in the function itself.
        folder = valid_file_name[:-4] + ' Folder'
		#Creates a CSV file with the index of the most relevant frames that we want to include in our dataset
        image_preprocessor(folder)
		#For the love of storage space, we remove the video file after splitting it into frames.
        os.remove(valid_video_location)
        print(str(int(url+1)) + " out of " + str(len(all_vids)) + " complete")


