from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import psutil
import shutil
import os

def main():
	dir =datetime.now().strftime("%Y-%m-%d")
	if  os.path.exists(dir):
		shutil.rmtree(dir)
	os.mkdir(dir)
	
	
	#readin schools sheet	
	f = open("Logins.csv","r")
	for line in f:
		splitline = line.split(",")
		print(splitline)
		if splitline[1] == "1":
			getSchoolInfo(splitline[4],splitline[3] \
				      ,splitline[2],splitline[0])

	
def getSchoolInfo(schoolURL,passCode,userName, schoolName):
	browser = webdriver.Chrome(executable_path=r'chromedriver.exe')
	browser.get(schoolURL)
	browser.set_window_position(0, 0)
	browser.set_window_size(1248, 1248)
	driverProcesses = psutil.Process(browser.service.process.pid)
	inputElems = browser.find_elements_by_tag_name("input")
	for i in inputElems:
		pureid = i.get_attribute("id")
		id = pureid.lower()
		if (id.find("username")>-1 or id.find("email")>-1):
			userElem = browser.find_element_by_id(pureid)
			print("userElem "+printElem(userElem))
		elif (id.find("password")>-1):
			passElem = browser.find_element_by_id(pureid)
			print("passElem "+printElem(passElem))
			break
		
	if userElem is None or passElem is None:
		return
		
	userElem.send_keys(userName)
	passElem.send_keys(passCode)
	passElem.send_keys(Keys.RETURN)
		
	checkAndFollowStatus("status","href",browser,schoolName)
	checkAndFollowStatus("communication","text",browser,schoolName)
	driverProcesses.children()[0].kill()
	
def printElem(elem):
	return("id: "+elem.get_attribute("id") + " name: "+ elem.get_attribute("name")+ " text: " + str(elem.get_attribute("text")))

def checkAndFollowStatus(string,attribute,browser,school):
	date = datetime.now()
	inputElems = browser.find_elements_by_tag_name("a")
	for i in inputElems:
		attributeValue = i.get_attribute(attribute)
		if attributeValue!=None:
			if attributeValue.lower().find(string)>-1:
				attrID = i.get_attribute("text")
				try:
					i.click()
				except:
					print("whoops")
				finally:
					path = date.strftime("%Y-%m-%d")+'/'+str(school)+" "+attrID+'.png'
					print("saving "+ path)
					browser.save_screenshot(path)
				return

main()
	
