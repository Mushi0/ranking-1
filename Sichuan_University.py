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
	mr.writeToExcel(14, n, res)

def getEleById(Id):
	return WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, Id)))

def Professor():
	url = 'http://math.scu.edu.cn/info/1013/2721.htm'
	global browser
	browser = webdriver.Firefox()
	browser.get(url)
	element = getEleById('vsb_content').text
	pattern = re.compile('院士(.*?)：.*?教授(.*?)：.*?副教授(.*?)：.*?讲师(.*?)：', re.S)
	professors = re.findall(pattern, element)
	order = [4, 1, 2, 3]
	name = ['院士', '教授', '副教授', '讲师']
	for i, item in enumerate(professors[0]):
		if item == '':
			writeToExcel(order[i], '1')
			print(name[i] + ': ' + '1')
		else:
			pattern = re.compile('.*?(\d+).*?', re.S)
			result = re.findall(pattern, item)
			writeToExcel(order[i], result)
			print(name[i] + ': ' + result[0])
	browser.close()
	del browser

def Scholars():
	url = 'http://math.scu.edu.cn/szdw/gdrc.htm'
	global browser
	browser = webdriver.Firefox()
	browser.get(url)
	element = getEleById('vsb_content_4').text
	pattern = re.compile('国家青年千人计划入选者\n(\d+).*?教育部青年长江学者\n(\d+).*?“万人计划“科技创新领军人才\n(\d+).*?', re.S)
	scholars = re.findall(pattern, element)
	order = [6, 5, 7]
	name = ['入选青年千人计划教师数量', '长江学者人数', '万人计划人数']
	for i, item in enumerate(scholars[0]):
		writeToExcel(order[i], item)
		print(name[i] + ': ' + item)
	browser.close()

def SCU():
	Professor()
	Scholars()
