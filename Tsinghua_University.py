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
	mr.writeToExcel(2, n, res)

def count1(result):
	count = [0, 0, 0, 0, 0]
	for item in result:
		if '副教授' in item:
			count[1] += 1
		elif '教授' in item:
			count[0] += 1
		elif '讲师' in item:
			count[2] += 1
		if '博士' in item:
			count[3] += 1
		count[4] += 1
	return count

def Professor():
	url = 'http://math.tsinghua.edu.cn/publish/math/9383/index.html'
	result = []
	global browser
	browser = webdriver.Chrome()
	browser.get(url)
	table = browser.find_elements_by_xpath('/html/body/div/div[13]/table/tbody/tr/td[2]/div[2]/table/tbody/tr')
	for line in table:
		items = line.find_elements_by_tag_name('td')
		for item in items:
			try:
				item = item.find_element_by_tag_name('a')
				urli = item.get_attribute('href')
				browser.execute_script('window.open()')
				browser.switch_to_window(browser.window_handles[1])
				browser.get(urli)
				try:
					info = browser.find_element_by_id('s2_right_con').text
					# info = info.replace('职称 Title：', '职称：')
					pattern = re.compile('教育背景\n(.*?)\n', re.S)
					result.append(re.findall(pattern, info)[0])
				except:
					print('Failed')
				browser.close()
				browser.switch_to_window(browser.window_handles[0])
			except:
				print('Failed')
	browser.close()
	del browser
	count = count1(result)
	print('教授数量: ' + str(count[0]))
	writeToExcel(1, count[0])
	print('副教授数量: ' + str(count[1]))
	writeToExcel(2, count[1])
	print('讲师数量: ' + str(count[2]))
	writeToExcel(3, count[2])
	count2 = count[3]/count[4]
	count2 = '%.2f%%' % (count2 * 100)
	print('教师博士数量: ' + str(count2))
	writeToExcel(8, count2)

def Library():
	url = 'http://lib.tsinghua.edu.cn/about/collection.html'
	html = mr.getOnePage(url)
	pattern = re.compile('实体馆藏总量约(.*?)万册（件）.*?各类数据库(\d+)个；电子期刊(.*?)万种', re.S)
	items = re.findall(pattern, html)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(float(items[2]) * 10000)
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)
	print('购买数据库数量: ' + items[1])
	writeToExcel(39, int(items[1]))

def THU():
	Professor()
	Library()
