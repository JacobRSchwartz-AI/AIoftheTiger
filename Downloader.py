from __future__ import unicode_literals
import youtube_dl
from Video_Splitter_Tool import video_splitter
import cv2
import os
import string
import shutil
from Image_Score_Tool_Preprocess import image_preprocessor

def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename



ydl_opts = {}

f = open("directory.txt", "r")
path = f.read()

all_vids = ["https://www.youtube.com/watch?v=T9EDhMOhG50"
            ]

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for url in range(0,len(all_vids)):
        ydl.download([all_vids[url]])
        file_info = ydl.extract_info(all_vids[url])
        file_name = file_info['title'] + '-' + file_info['id'] + '.mp4'
        
        file_name = list(file_name)
        for char in range(0,len(file_name)):
            if file_name[char] == "|":
                file_name[char] = "_" 
        file_name = "".join(file_name)  # Change the list back to string, by using 'join' method of strings. 
        
        valid_file_name = format_filename(file_name)
        video_location = path + file_name
        valid_video_location = path + valid_file_name 
        shutil.move(video_location, valid_video_location)


        cam = cv2.VideoCapture(valid_video_location)
        #folder for output
        folder = valid_video_location[:-4] + ' Folder'
        video_splitter(cam, folder)
        folder = valid_file_name[:-4] + ' Folder'
        image_preprocessor(folder)
        print(str(int(url+1)) + " out of " + str(len(all_vids)) + " complete")


