from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support.select import Select
import re
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(10, n, res)

def getEleByXpath(Xpath):
	return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, Xpath)))

def Professors():
	count = [0, 0, 0]
	url = 'http://math.ustc.edu.cn/new/teachers.php'
	global driver
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	driver = webdriver.Firefox(firefox_options = fireFoxOptions)
	# driver = webdriver.Firefox()
	driver.get(url)
	element = getEleByXpath('/html/body/table[3]/tbody/tr/td[3]/table[2]/tbody/tr[3]/td')
	element = element.text
	driver.close()
	del driver
	count[0] = mr.parse2(element, '教  授', '访问教授')
	count[1] = mr.parse2(element, '副教授', '特任副研究员')
	count[2] = mr.parse2(element, '讲师', '博士后')
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def Library():
	url = 'http://lib.ustc.edu.cn/%e6%9c%ac%e9%a6%86%e6%a6%82%e5%86%b5/%e6%9c%ac%e9%a6%86%e7%ae%80%e4%bb%8b/'
	html = mr.getOnePage(url)
	pattern = re.compile('实体馆藏中外文书刊(.*?)万册.*?中外文电子期刊近(.*?)万种', re.S)
	item = re.findall(pattern, html)[0]
	count1 = int(float(item[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(float(item[1]) * 10000)
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)

def USTC():
	Professors()
	Library()
