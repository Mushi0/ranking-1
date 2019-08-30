from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support.select import Select
import re
import xlwt, xlrd
import xlutils.copy

def writeToExcel(n, res):
	f = xlrd.open_workbook('result.xls')
	ws = xlutils.copy.copy(f)
	table = ws.get_sheet(0)
	table.write(8, n, res)
	ws.save('result.xls')

def getEleByXpath(Xpath):
	return WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, Xpath)))

def Professor():
	T = '院士'
	count = [0,0,0,0]
	url = 'http://math.fudan.edu.cn/Pictrueleft.aspx?info_lb=548&flag=526'
	global browser
	browser = webdriver.Chrome()
	browser.get(url)
	while(1):
		pages = getEleByXpath('//*[@id="ContentPlaceHolder1_Pager22"]/div[1]')
		pattern = re.compile('共\s(\d+)\s页,当前第\s(\d+)\s页.*?', re.S)
		pages = re.findall(pattern, pages.text)[0]
		print('第' + pages[1] + '页')
		if pages[0] == pages[1]:
			break
		elements = browser.find_elements_by_class_name('people_text')
		for item in elements:
			item = item.text
			pattern = re.compile('职称：(.*?)\n.*?', re.S)
			result = re.findall(pattern, item)[0]
			print(result)
			if T in item:
				count[3] += 1
			result = re.sub(u'（.*?）', '', result)
			if result == '教授':
				count[0] += 1
			elif result == '副教授':
				count[1] += 1
			elif result == '讲师':
				count[2] += 1
		onclick = getEleByXpath('//*[@id="ContentPlaceHolder1_Pager22"]/div[2]/a[11]')
		onclick.click()
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)
	browser.close()

def FU():
	Professor()

FU()
