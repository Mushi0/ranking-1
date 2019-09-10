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
	mr.writeToExcel(3, n, res)

def count1(result):
	count = [0, 0, 0, 0]
	for item in result:
		if '副教授' in item:
			count[1] += 1
		elif '教授' in item:
			count[0] += 1
		elif '讲师' in item:
			count[2] += 1
		elif '院士' in item:
			count[3] += 1
	return count

def Professor():
	url = 'http://math.bnu.edu.cn/jzg/szdw/index.htm'
	result = []
	global browser
	browser = webdriver.Chrome()
	browser.get(url)
	tables = browser.find_elements_by_class_name('subNameList')
	for table in tables:
		items = table.find_elements_by_tag_name('li')
		for item in items:
			item = item.find_element_by_tag_name('a')
			urli = item.get_attribute('href')
			browser.execute_script('window.open()')
			browser.switch_to_window(browser.window_handles[1])
			browser.get(urli)
			try:
				info = browser.find_element_by_class_name('subPeople_info').text
				info = info.replace('职称 Title：', '职称：')
				pattern = re.compile('职称：(.*?)\n', re.S)
				result.append(re.findall(pattern, info)[0])
			except:
				print('Failed')
			browser.close()
			browser.switch_to_window(browser.window_handles[0])
	browser.close()
	del browser
	count = count1(result)
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def Scholars():
	url = 'http://math.bnu.edu.cn/jzg/rcjh/index.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('长江学者特聘教授：(.*?)<br />', re.S)
	items = re.findall(pattern, html)[0]
	pattern = re.compile('([\u4E00-\u9FA5][\u4e00-\u9fa5\\s][\u4e00-\u9fa5])', re.S)
	count = len(re.findall(pattern, items))
	print('长江学者人数: ' + str(count))
	writeToExcel(5, count)

def Library():
	url = 'http://www.lib.bnu.edu.cn/content/guan-chang-ji-yu'
	html = mr.getOnePage(url)
	pattern = re.compile('纸本文献总量达(.*?)万余册，中外文全文电子期刊(\d+)万余种，中外文.*?引进中外文数据库(\d+)个，自', re.S)
	items = re.findall(pattern, html)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(float(items[1]) * 10000)
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)
	print('购买数据库数量: ' + items[2])
	writeToExcel(39, int(items[2]))

def BNU():
	Professor()
	Scholars()
	Library()
