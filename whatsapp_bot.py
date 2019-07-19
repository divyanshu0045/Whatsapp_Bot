#!/usr/bin/env python

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import sys
import time
import os 


def main():
        os.environ['PATH'] = os.environ['PATH'] + ':' + os.getcwd()
	browser = login()
	while True:
            #name = raw_input("Enter recipient's name:")
            #msg = raw_input("Enter message to send:")
            #count=1
            name = None
            msg = None
            count = None
            with (open('msg','r')) as m:
                for line in m:
                    line = line.strip()
                    if (line[0]=='#'):
                        continue
                    try:
                        name = line.split()[0]
                    except:
                        print "Invalid line in config file [%s]" % (line)
                        continue
                    try:
                        msg = line.split()[1]
                    except:
                        print "Invalid line in config file [%s]" % (line)
                        continue
                    try:
                        count = line.split[2]
                    except:
                        count = 1
                    for i in range(count):
                        send_msg(browser, name, msg)
            time.sleep(1)

def login(browser_name="chrome"):
	browser = None
	options = Options()
	options.add_argument("--disable-dev-shm-usage"); # overcome limited resource problems
        options.add_argument("--no-sandbox"); # Bypass OS security model
        options.headless = True
        options.nogui = True
        print "Starting %s..." %(browser_name)
	if (browser_name == "chrome"):
		browser = webdriver.Chrome(options=options)
	if (browser_name == "firefox"):
		browser = webdriver.Firefox()
        print "Getting Page..."
	browser.get('https://web.whatsapp.com/')
	while True:
		try:
			browser.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div/div[2]/div/img') #QR Code
			print "Waiting for login"
			time.sleep(5)
		except:
			print "Logging in..."
			break

	try:
		wait = WebDriverWait(browser, 30)       
		wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/label/input'))) #search bar
	except TimeoutException:
		print "It took too long to login...Please try again...Exiting!!!"
		sys.exit()
	return browser

def send_msg(browser,name,msg):
	if (len(name) == 0 or len(msg) == 0):
		print "Invalid User Input"
		return
	search = browser.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/input') #search bar
	search.clear()
	search.send_keys(name + u'\ue007')
	
	try:
			wait = WebDriverWait(browser, 3)
			wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'))) #message field
	except TimeoutException:
			print "No results found..."
			return

	#getText = browser.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div[2]/div')	
	#if not (getText.text.lower() == "messages"):
	#	print "No results found..."
	#	return
	
	#result = browser.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div[3]/div/div/div[1]/div/img') #first search result
	#result.click()
	message = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]') #message field
	message.send_keys(msg)
        message.send_keys(Keys.RETURN)
	#send = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button') #send button
	#send.click()

if __name__ == '__main__':
  main()
