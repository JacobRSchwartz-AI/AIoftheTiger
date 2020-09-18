# AIoftheTiger
A program to take in frames of a golf broadcast as input and output an alert when a designated golfer(s) is about to play a shot.

# Install
1. Make sure you have Python downloaded. If you haven't yet downloaded Python you can download [here](https://www.python.org/downloads/).
2. Make sure you have an IDE that supports Python. Download our favorite Integrated Development Environment (IDE), Visual Studio Code, [here](https://code.visualstudio.com/download). 
3. Setup your virtual environment interpreter [here](https://code.visualstudio.com/docs/python/environments).
4. Clone this repository
5. Replace the contents of "directory.txt" so that it only contains the directory where your project resides. (Make sure to get rid of <>)
6. See setup OCR below

# Setup OCR
1. Go [here](https://developers.google.com/drive/api/v3/quickstart/python) and perform step 1: Enable the Drive API.
2. Name your project anything you want.
3. Make sure the configure your OAuth client dropdown says 'Desktop app' and click create
4. Click the 'Download Client Configuration' which will download 'credentials.json' to your downloads folder.
5. Move 'credentials.json' to your working directory
6. Follow this link [here](https://console.developers.google.com) and click 'ENABLE APIS AND SERVICES'.
7. Enter 'doc' into the search bar and click on 'Google Docs API'.
8. Click Enable API.
9. Open the project in your IDE of choice and run 'Main.py'.
10. Once running the program will display 'please use url' message. Control click the link.
11. Once the website is up click on 'Advanced'.
12. Click on 'Quickstart (unsafe)' DON'T WORRY IT'S VERY SAFE : )
13. Click Allow.
14. Click Allow again.
15. Copy and paste the code into IDE terminal and press enter.
16. See usage below for tips and tricks.


# Usage
1. Enter the last name of every golfer that you want to see.
2. You can enter the word "Leader" if you want to see every shot of whoever is currently winning the tournament.
3. Enter 0 once finished creating your list of golfers and launch the Selenium Browswer.
4. When the Selenium web browser pops up, wait until it automatically fullscreens.
5. Once one of your golfers is found by the program, it'll pause the video and play an audio alert.
6. To start the broadcast, hit the "P" character on the keyboard.
7. After you hit play, the Neural Network will NOT continue to run so that you can watch the broadcast normally.
8. To resume the Neural Network, hit the letter "D" on your keyboard. 
9. You'll know the Neural Network has been resumed if the video appears to speed up is a bit choppy. This is to make back the time that the live video was on pause and get back to live.
