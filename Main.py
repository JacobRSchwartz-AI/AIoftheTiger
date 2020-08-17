from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import os
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
# print(driver)

fileName = "screenshot.jpg"

while True:
    # time.sleep(5)
    driver.get_screenshot_as_file(fileName)
    try:
        result = image_analyzer(path + fileName, reconstructed_model, creds, drive_service, doc_service)
    except Exception as e:
        print(str(e))
    if result[0]:
        playsound('glf+swng.mp3')

