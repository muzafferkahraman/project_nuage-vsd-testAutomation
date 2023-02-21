####################################################
'''
VSD Performance Checker 
GUI Enterprise Checker with Selenium
@author Muzaffer Kahraman 2022
'''
####################################################

#!/usr/bin/env python3
from property_parser import Credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
from datetime import date
import logging
import time

def web():

 global driver

 op = webdriver.ChromeOptions()
 op.add_argument('--ignore-certificate-errors')
 op.add_argument("--start-maximized")

 op.add_argument('--headless')
 op.add_argument('--disable-gpu')
 op.add_argument("--no-sandbox")
 op.add_argument("--disable-dev-shm-usage")
 display = Display(visible=0, size=(1920, 1080))
 display.start()
 driver = webdriver.Chrome("/usr/bin/chromedriver",options=op)




if __name__=="__main__":
    
    today = date.today()
    logfile = "/var/log/{}_vsd_performance_checker.log".format(str(today))
    logging.basicConfig(filename=logfile,level=logging.INFO,format='%(asctime)s %(levelname)s  %(message)s')
    logging.info("GUI Enterprise Checker Started")

    # Let's parse the config file using the credentials class
    creds=Credentials("credential.properties")

    web()
    driver.get(creds.get_url())
    logging.info('URL '+creds.get_url()+' requested')
    WebDriverWait(driver,5060).until(ec.element_to_be_clickable((By.XPATH,"//span[normalize-space()='Username']")))

    inputElement = driver.find_element_by_xpath("//input[@id='username']")
    inputElement.send_keys(creds.get_user())

    inputElement = driver.find_element_by_xpath("//input[@id='password']")
    inputElement.send_keys(creds.get_passwd())

    inputElement = driver.find_element_by_xpath("//input[@id='organization']")
    inputElement.send_keys(creds.get_org())

    WebDriverWait(driver,60).until(ec.element_to_be_clickable((By.XPATH,"//img[@alt='submit']")))
  
    inputElement = driver.find_element_by_xpath("//img[@alt='submit']")
    inputElement.click()

    WebDriverWait(driver,60).until(ec.visibility_of_element_located((By.XPATH,"//button[@id='OK']")))
    inputElement = driver.find_element_by_xpath("//button[@id='OK']")
    inputElement.click()
    logging.info('GUI Logged in')

    inputElement = driver.find_element_by_id("enterprises")
    
    A=inputElement.text.split("\n")
    logging.info('GUI Enterprise List Fetched')
    B=[]
    for s in A:
        if s.find("TestEnterprise") >= 0: 
            B.append(s)
    
    if len(B) == 10:
        logging.info('BINGO! ** GUI Enterprises are Verifed to be Created Correctly in Number **')

    inputElement = driver.find_element_by_xpath("//img[@alt='logout']")
    inputElement.click()    
    
    logging.info('GUI Logged Out')
    driver.close()   
