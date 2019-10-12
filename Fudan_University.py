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
	mr.writeToExcel(8, n, res)

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
	del browser

def Academician():
	url = 'http://math.fudan.edu.cn/content.aspx?info_lb=574&flag=526'
	browser = webdriver.Chrome()
	browser.get(url)
	page = browser.find_elements_by_xpath('//*[@id="size"]/div[1]/div/strong')
	count = len(page)
	browser.close()
	print('院士：　' + str(count))
	writeToExcel(4, count)

def monographPatent(urln, x, name):
	url = 'http://math.fudan.edu.cn/content.aspx?info_lb=' + urln + '&flag=527'
	global browser
	browser = webdriver.Chrome()
	browser.get(url)
	table = getEleByXpath('//*[@id="size"]/table/tbody')
	table = table.find_elements_by_xpath('//tr')
	count = len(table) - 1
	print(name + str(count))
	writeToExcel(x, count)
	browser.close()
	del browser

def Projects_1():
	url = 'http://math.fudan.edu.cn/content.aspx?info_lb=786&flag=554'
	global browser
	browser = webdriver.Chrome()
	browser.get(url)
	table = getEleByXpath('//*[@id="size"]/table/tbody')
	table = table.text
	pattern = re.compile('.*?(\n).*?', re.S)
	t = re.findall(pattern, table)
	count = len(t)
	print('企事业委托项目: ' + str(count))
	writeToExcel(27, count)
	browser.close()
	del browser
	return count

def Projects_2(count):
	url = 'http://math.fudan.edu.cn/content.aspx?info_lb=787&flag=554'
	global browser
	browser = webdriver.Chrome()
	browser.get(url)
	table = getEleByXpath('//*[@id="size"]/table/tbody')
	table = table.text
	pattern1 = re.compile('.*?(国家).*?', re.S)
	t1 = re.findall(pattern1, table)
	count1 = len(t1)
	pattern2 = re.compile('.*?(上海市).*?', re.S)
	t2 = re.findall(pattern2, table)
	count2 = len(t2)
	pattern3 = re.compile('.*?(国际).*?', re.S)
	t3 = re.findall(pattern3, table)
	count3 = len(t3)
	print('国家科研项目数: ' + str(count1))
	writeToExcel(25, count1)
	print('省部科研项目数: ' + str(count2))
	writeToExcel(26, count2)
	print('国际合作项目: ' + str(count3))
	writeToExcel(28, count3)
	count = count + count1 + count2 + count3
	print('目前科研项目数: ' + str(count))
	writeToExcel(24, count)
	browser.close()
	del browser

def Library():
	url = 'http://www.library.fudan.edu.cn/60/list.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('馆藏纸本文献资源约</span><span lang="EN-US" style="color:#333333;">(.*?)</span>.*?中文报刊</span><span lang="EN-US" style="color:#333333;">(.*?)</span>.*?外文报刊</span><span lang="EN-US" style="color:#333333;">(.*?)</span>', re.S)
	items = re.findall(pattern, html)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(items[1]) + int(items[2])
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)

def FU():
	Professor()
	monographPatent('555', 19, '近年学术专著: ')
	monographPatent('586', 12, '近年专利数: ')
	count = Projects_1()
	Projects_2(count)
	Library()

Academician()
