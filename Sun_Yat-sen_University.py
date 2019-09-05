from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import json
import time
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(13, n, res)

def getEleByXpath(Xpath):
	return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xpath)))

def parse1(pos):
	count = 0
	url = 'http://math.sysu.edu.cn/' + pos
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	driver = webdriver.Firefox(firefox_options = fireFoxOptions)
	# driver = webdriver.Firefox()
	t = 0
	while(1):
		url1 = url + '?page=' + str(t)
		driver.get(url1)
		if t == 0:
			time.sleep(5)
		# last = driver.find_elements_by_class_name('pager-item pager-item-last')
		elements = driver.find_elements_by_class_name('col-sm-12')
		c = len(elements) - 2
		count = count + c
		if c < 10:
			break
		t += 1
	driver.close()
	del driver
	return count

def Professors():
	count = [0, 0, 0]
	count[0] = parse1('professors')
	print('教授： ' + str(count[0]))
	count[1] = parse1('associate-professors')
	print('副教授： ' + str(count[1]))
	count[2] = parse1('instructors')
	count[2] += parse1('seniorlecturer')
	print('讲师： ' + str(count[2]))
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def Scholars():
	count = [0, 0, 0]
	url = 'http://math.sysu.edu.cn/talent'
	global driver
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	driver = webdriver.Firefox(firefox_options = fireFoxOptions)
	# driver = webdriver.Firefox()
	driver.get(url)
	element = getEleByXpath('//*[@id="content"]/article/div/div/div[2]/div[2]/div/div[2]/div')
	element = element.text
	driver.close()
	del driver
	count[0] = mr.parse2(element, '特聘教授', '（六）')
	count[1] = mr.parse2(element, '（十四）', '（十五）')
	count[2] = mr.parse2(element, '（十五）', '（十六）')
	count[2] += mr.parse2(element, '（十六）', '（十七）')
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 5, item)

def Library():
	url = 'http://library.sysu.edu.cn/about'
	global driver
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	driver = webdriver.Firefox(firefox_options = fireFoxOptions)
	# driver = webdriver.Firefox()
	driver.get(url)
	element = getEleByXpath('//*[@id="content"]/article/div/div/div[2]/div[2]/div/div[2]/div')
	element = element.text
	driver.close()
	del driver
	pattern = re.compile('纸质馆藏总量达(.*?)万册.*?中文电子期刊(.*?)种；外文电子期刊(.*?)种', re.S)
	items = re.findall(pattern, element)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(items[1]) + int(items[2])
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)

def SYSU():
	Professors()
	Scholars()
	Library()
