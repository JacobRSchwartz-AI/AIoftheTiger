from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import os
import time
import threading
from OCR import prepare_ocr
from Neural_Network_Predict import image_analyzer
import tensorflow as tf
from Golfer_List import get_active_golfer_list
import keyboard
from tensorflow.keras import datasets, layers, models, optimizers, callbacks

# Method to monitor keyboard presses so that we can add functionality to
# pause, play, fastfoward, and rewind the video
def keyboard_monitoring(driver):
    while True:
        try:
            #Checks to see if video is paused
            paused = driver.execute_script('return document.getElementsByTagName("video")[0].paused')
            # want to play video at regular speed?
            if keyboard.is_pressed("P") and paused:
                driver.execute_script('document.getElementsByTagName("video")[0].play()')
                driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=1')
            # want to pause video?
            elif keyboard.is_pressed("P") and not paused:
                driver.execute_script('document.getElementsByTagName("video")[0].pause()')
            # want to fastforward video?
            elif keyboard.is_pressed("S"):
                driver.execute_script('document.getElementsByTagName("video")[0].play()')
                driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=5')
            # want to rewind video?
            elif keyboard.is_pressed("R"):
                driver.execute_script('document.getElementsByTagName("video")[0].play()')
                driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=-1')
        except:
            continue

# change directory 
os.chdir(r"C:\Users\HP\Documents\AIoftheTiger New")
f = open("directory.txt", "r")
path = f.read()

# defines the model we use for our Neural Network
my_model = path + "3_RE-test-model-034.h5"
reconstructed_model = tf.keras.models.load_model(my_model)

# gets all our tools to run the OCR
creds, drive_service, doc_service = prepare_ocr()

url = input("What url do you want me to watch? ")

done = False
golfer_list = []

# get a list of golfers that are active in today's golf world
active_golfers = get_active_golfer_list(path + "default_golfer_list.txt")

# loop to get us the list of golfers they want to get see
while done == False:
    golfer = input("Input the last name of a golfer you would like to watch. "
                   "Input '0' when you have listed all golfers you want to watch: ")
    # if not done entering golfers...
    if golfer != '0':
        golfer = golfer.upper()
        #is golfer they want to see in active golfer list?
        if golfer in active_golfers:
            golfer_list.append(golfer[:-1])
        # the golfer they want to see is not in active golfer list
        else:
            overwrite = input("WARNING! The golfer you entered doesn't exist in our list. Do you still want"
                              "to continue? Enter 'y' to use your golfer.")
            overwrite = overwrite.upper()
            if overwrite == 'Y':
                golfer_list.append(golfer)
            else:
                continue
    # you need at least one golfer to use our tool
    elif len(golfer_list) == 0:
        print("Please enter the name of at least one golfer.")
        continue
    else:
        done = True

# url = "https://www.youtube.com/watch?v=-dlgPrBYcuY"

# Create a driver for Google Chrome Browser and open a webpage with the provided url 
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
driver.fullscreen_window()

# Have a thread to constantly look for keys to be pressed
# control_thread = threading.Thread(target=keyboard_monitoring, args=([driver]))
# control_thread.start()
# # print(driver)
# print(control_thread.is_alive())

fileName = "screenshot.jpg"
stop_token = True
lag_time = 0

# Does the magic of finding the golfer we are looking for
while True:
    # get a screenshot of the video on the screen
    driver.get_screenshot_as_file(fileName)
    try:
        # determine if the user wants to see this image or not
        result = image_analyzer(path + fileName, reconstructed_model, stop_token, creds, golfer_list, drive_service,
                                doc_service, driver)
    except Exception as e:
        print(str(e))
    # for testing purposes to monitor lag time and the score
    # result[0] = boolean data type telling us whether it is a golfer we want to see or not
    # result[1] = score our Neural Netowrk gave the screenshot
    # result[2] = stop token to tell us whether the video is paused or not
    # result[3] = the start time of the lag
    print(result[1], lag_time)
    stop_token = result[2]
    start_time = result[3]
    # is this is a golfer we want to see?
    if result[0]:
        playsound('glf+swng.mp3')
        paused = True
        lag_addition = 0
        while paused:
            # is the video paused?
            paused = driver.execute_script('return document.getElementsByTagName("video")[0].paused')
            # want to play the video?
            if keyboard.is_pressed("P") and lag_addition == 0:
                driver.execute_script('document.getElementsByTagName("video")[0].play()')
                end_time = time.time()
                lag_time = end_time - start_time
                lag_addition = 1
        # done watching the golfer I want return to automatically notifying me when 
        # a golfer I want returns to the screen
        while keyboard.is_pressed("D") != True:
            continue
    # not a golfer we want to see, but OCR gave screenshot a 5
    elif result[1] == 5:
        driver.execute_script('document.getElementsByTagName("video")[0].play()')
        end_time = time.time()
        lag_time += end_time - start_time

    # is the video paused?
    paused = driver.execute_script('return document.getElementsByTagName("video")[0].paused')
    # get rid of lag time by speeding up the video until we 
    # are caught back up to a reasonable point in the broadcast
    if lag_time >= 0.5 and not paused:
        current_time = time.time()
        end_time = time.time() + 0.5
        # speed up the video
        driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=2')
        while current_time <= end_time:
            current_time = time.time()
        # return video to normal speed
        driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=1')
        lag_time -= 0.5