from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import time

# driver = webdriver.Chrome(ChromeDriverManager().install())
# url = "https://www.youtube.com/watch?v=oqYbG8Zhoag"
# driver.get(url)



def screenshot_from_url(driver, filename):
    driver.get_screenshot_as_file(filename)
    


# for x in range(0,6):
#     time.sleep(3)
#     screenshot_from_url(driver, filename + str(x) + ".jpg")

# driver.quit()

# driver.quit()
# print("end...")