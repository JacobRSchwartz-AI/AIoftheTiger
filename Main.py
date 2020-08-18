from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import os
import time
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
url = "https://www.youtube.com/watch?v=KvOzw6YpOsk"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
# driver.maximize_window()
driver.fullscreen_window()

# print(driver)

fileName = "screenshot.jpg"
stop_token = True
# paused = False

while True:
    # time.sleep(5)
    driver.get_screenshot_as_file(fileName)
    try:
        result = image_analyzer(path + fileName, reconstructed_model, stop_token, creds, drive_service, doc_service, driver)
    except Exception as e:
        print(str(e))
    # os.system('cls')
    print(result[1])
    stop_token = result[2]
    if result[0]:
        playsound('glf+swng.mp3')
        paused = True
        while paused:
            paused = driver.execute_script('return document.getElementsByTagName("video")[0].paused')
        time.sleep(10)
    elif result[1] == 5:
        driver.execute_script('document.getElementsByTagName("video")[0].play()')

