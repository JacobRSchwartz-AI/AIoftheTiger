from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import os
import time
import keyboard
from OCR import prepare_ocr
from Neural_Network_Predict import image_analyzer
import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks

os.chdir("C:\\Users\\manag\\Documents\\GitHub\\AIoftheTiger")
f = open("directory.txt", "r")
path = f.read()

# defines the model we use for our Neural Network
my_model = path + "RE-test-model-030.h5"
reconstructed_model = tf.keras.models.load_model(my_model)

# gets all our tools to run the OCR
creds, drive_service, doc_service = prepare_ocr()

# url = input("What url do you want me to watch? ")
url = "https://www.youtube.com/watch?v=oqYbG8Zhoag"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
# driver.maximize_window()
driver.fullscreen_window()
# time.sleep(10)
# driver.minimize_window()
# print(driver)

fileName = "screenshot.jpg"
stop_token = True
lag_time = 0
# paused = False

while True:
    # if keyboard.is_pressed("W"):
    #     driver.set_window_position(0,0)
    #     driver.fullscreen_window()
    # # time.sleep(5)
    driver.get_screenshot_as_file(fileName)
    try:
        result = image_analyzer(path + fileName, reconstructed_model, stop_token, creds, drive_service, doc_service, driver)
    except Exception as e:
        print(str(e))
    # os.system('cls')
    print(lag_time)
    stop_token = result[2]
    start_time = result[3]
    if result[0]:
        playsound('glf+swng.mp3')
        # driver.set_window_position(0,0)
        # driver.maximize_window()
        # driver.fullscreen_window()
        paused = True
        lag_addition = 0
        while paused:
            paused = driver.execute_script('return document.getElementsByTagName("video")[0].paused')
            if keyboard.is_pressed("P") and lag_addition == 0:
                driver.execute_script('document.getElementsByTagName("video")[0].play()')
                end_time = time.time()
                lag_time += (end_time - start_time)
                lag_addition = 1
        while keyboard.is_pressed("D") != True:
            continue
        # driver.set_window_position(-2000,0)
        # time.sleep(10)
    elif result[1] == 5:
        driver.execute_script('document.getElementsByTagName("video")[0].play()')
        end_time = time.time()
        lag_time += (end_time - start_time)
    if lag_time >= 1:
        current_time = time.time()
        end_time = time.time() + 1
        driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=2')
        while current_time <= end_time:
            current_time = time.time()
        driver.execute_script('document.getElementsByTagName("video")[0].playbackRate=1')
        lag_time -= 1
