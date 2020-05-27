####################################
# Author: Joy Mendonca                    
# File name: joysendsmemes.py                
# Date created : 26/05/2020
# Chrome driver url : http://chromedriver.chromium.org/downloads              
####################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException 
import urllib.request as urllib
import os 
import time
import logging as logger
import autoit
import random


class Instagram:
    def __init__(self,driverPath=None,url=None):
        self.driverPath = driverPath 
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))  # Current working Folder/Directory 
    def loadDriver(self):
        try:
            if self.driverPath is None:
                logger.error(" Please provide a driver path")
                return
            # Open chrome options pass --incognito add_argument 
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            self.driver = webdriver.Chrome(executable_path = self.driverPath , options=chrome_options)
            self.getUrl()
        except Exception as e:
            logger.error(str(e))

   

    def getUrl(self):
        try:
            if self.driver is None:
                logger.error(" Please provide an url")
                return
            # Getting to the login page and selecting the username and password elements
            self.driver.get('https://www.instagram.com/accounts/login')
            time.sleep(2)
            username = self.driver.find_element_by_name("username")
            password = self.driver.find_element_by_name("password")
            login_btn = self.driver.find_element_by_xpath('//*[@class="sqdOP  L3NKy   y3zKF     "]')
            

            # Logging in using the credentials in logininfo.txt
            loginfile = self.scriptDir.strip() + r"\logininfo.txt"
            file1 = open(loginfile, 'r') 
            Lines = file1.readlines()
            uid = Lines[0].strip()
            pswd = Lines[1].strip()
            username.send_keys(uid)
            password.send_keys(pswd)
            login_btn.click()
            time.sleep(3)
            # Skipping the annoying notification thingy that always pops up >_<
            skip_btn = self.driver.find_element_by_xpath("//*[@class='aOOlW   HoLwm ']")
            skip_btn.click()
            time.sleep(2)
            self.driver.get('https://www.instagram.com/direct/inbox/')
            time.sleep(2) 

            # Defining method check_exists_by_patch which basically returns if the element exits.
            def check_exists_by_xpath(xpath):
                try:
                    self.driver.find_element_by_xpath(xpath)
                except NoSuchElementException:
                    return False
                return True

            # Main loop which detects messages and sends meme.
            while(True):
                time.sleep(3)
                
                # Checks if there is a MESSAGE REQUEST and accepts it if there is.
                if check_exists_by_xpath("//*[@class='sqdOP yWX7d    y3zKF     ']"):
                    self.driver.find_element_by_xpath("//*[@class='sqdOP yWX7d    y3zKF     ']").click()
                    time.sleep(1)
                    self.driver.find_element_by_xpath("//*[@class='-qQT3 rOtsg']").click()
                    time.sleep(1)
                    self.driver.find_element_by_xpath("//*[@class='sqdOP yWX7d     _8A5w5    ']").click()
                    self.driver.get('https://www.instagram.com/direct/inbox/')

                # Checks if there is a new message and replies with a meme if there is.
                if check_exists_by_xpath("//*[@class='KdEwV']"):
                    time.sleep(1)
                    self.driver.find_element_by_xpath("//*[@class='                    Igw0E   rBNOH          YBx95   ybXk5    _4EzTm                      soMvl                                                                                        ']").click()
                    # I couldve skipped taking input of a meme from he txt file.
                    # As I finally went with naming the files by numbers, but I still kept it
                    # For future upgrades 
                    memelistfile = self.scriptDir.strip() + r"\memelist.txt"
                    file1 = open(memelistfile, 'r') 
                    Lines = file1.readlines()
                    # Selects a random line from memelist.txt which is basically the random meme to be sent
                    random_meme = random.choice(Lines).strip()
                    sendfile = self.scriptDir.strip() + "\memes\\" + random_meme    # Yeah. I KNOW ABOUT THE WARNING HERE I JUST DONT WANT TO DEAL WITH IT.  
                    self.driver.find_element_by_xpath("(//*[@class='wpO6b '])[2]").click()
                    # Autoit is used for the uploading of the image
                    # As chromedriver cant interact with the file explorer and I could'nt find a better way
                    # I wish to figure out a better method in the future
                    handle = "[CLASS:#32770; TITLE:Open]"
                    autoit.win_wait(handle, 100)
                    autoit.control_set_text(handle, "Edit1", sendfile)
                    time.sleep(1)
                    autoit.control_click(handle, "Button1")
                    time.sleep(2)
                    actions = ActionChains(self.driver)
                    actions.send_keys("Thanks for using. Wait for 10-15 seconds before using again.") 
                    actions.perform() 
                    time.sleep(2)
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.RETURN) 
                    actions.perform()
                    self.driver.get('https://www.instagram.com/direct/inbox/')
                    time.sleep(1)
                else:
                    time.sleep(3)
                    self.driver.refresh()

            # This is just extra code for if I ever decide to make a kill switch 
            time.sleep(3)
            print("Execution completed .....")
            self.driver.close()

            
        except Exception as e:
            logger.error( str(e))

        

# I feel like everything below is quite self explanatory.
if __name__ == "__main__":

    workinDir = os.path.dirname(os.path.realpath(__file__))  # current working Folder/Directory
    driverPath = workinDir.strip() + r"\Chromedriver\chromedriver.exe"

    
    instagram = Instagram(
        driverPath = driverPath,
        )
    instagram.loadDriver()
