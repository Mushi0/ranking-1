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
	mr.writeToExcel(7, n, res)

def getEleById(Id):
	return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, Id)))

def parse1(x):
	xpath = '//*[@id="right_nav"]/div[2]/div[3]/div[2]/table/tbody/tr/td[2]/table[' + x + ']/tbody/tr'
	elements = driver.find_elements_by_xpath(xpath)
	count = 6*(len(elements) - 2)
	element = elements[len(elements) - 1].text
	element = element.replace('  ', '')
	pattern = re.compile(' ', re.S)
	items = re.findall(pattern, element)
	count = count + len(items) + 1
	return count

def parse3(element, pre, aft):
	r = pre + '(.*?)' + aft
	pattern = re.compile(r, re.S)
	temp = re.findall(pattern, element)[0]
	for i in range(4):
		temp = temp.replace(' '*(4 - i), '　')
	pattern = re.compile('([\u4E00-\u9FA5][\u4e00-\u9fa5\\s][\u4e00-\u9fa5])', re.S)
	items = re.findall(pattern, temp)
	count = len(items)
	return count

def parse4(element, pre, aft):
	r = pre + '(.*)' + aft
	pattern = re.compile(r, re.S)
	temp = re.findall(pattern, element)[0]
	pattern = re.compile('(◆)', re.S)
	items = re.findall(pattern, temp)
	count = len(items)
	return count

def Professor():
	count = [0, 0, 0]
	url = 'http://math35.nenu.edu.cn/hsystem/bin/aspdu/list_jslbother.asp?sortindex=%B8%DA%CE%BB'
	global driver
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	driver = webdriver.Firefox(firefox_options = fireFoxOptions)
	# driver = webdriver.Firefox()
	driver.get(url)
	for i in range(3):
		count[i] = parse1(str(i + 1))
	driver.close()
	del driver
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def Scholars():
	count = [0, 0, 0]
	url = 'http://www.nenu.edu.cn/576/list.htm'
	global driver# global driver
	fireFoxOptions = webdriver.FirefoxOptions()
	fireFoxOptions.set_headless()
	driver = webdriver.Firefox(firefox_options = fireFoxOptions)
	# driver = webdriver.Firefox()
	driver.get(url)
	elements = getEleById('wp_content_w8_0')
	elements = elements.text
	driver.close()
	del driver
	count[0] = mr.parse2(elements, '院士', '荣誉教授')
	count[1] += parse3(elements, '教育部“长江学者奖励计划”特聘教授', '教育部“长江学者奖励计划”青年学者')
	count[1] += parse3(elements, '教育部“长江学者奖励计划”青年学者', '教育部“长江学者和创新团队发展计划”带头人')
	count[1] += parse3(elements, '教育部“长江学者和创新团队发展计划”带头人', '中国科学院“百人计划”')
	count[2] += parse3(elements, '国家“万人计划”哲学社会科学领军人才', '国家“万人计划”科技创新领军人才')
	count[2] += parse3(elements, '国家“万人计划”科技创新领军人才', '国家“万人计划”教学名师')
	count[2] += parse3(elements, '国家“万人计划”教学名师', '国家杰出青年科学基金获得者')
	count[2] += parse3(elements, '国家“万人计划”青年拔尖人才', '国家优秀青年科学基金获得者')
	print(count)
	writeToExcel(4, count[0])
	writeToExcel(5, count[1])
	writeToExcel(7, count[2])

def ResearchAward():
	count = [0, 0, 0]
	url = 'http://www.nenu.edu.cn/275/list.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('学术专著(\d+)部，获得省部级科研奖励(\d+)项。6部著.*?文库》；(\d+)项成果获得全国高等.*?奖2项）；(\d+)项成果获全国教育', re.S)
	items = re.findall(pattern, html)[0]
	count[0] = int(items[2]) + int(items[3])
	count[1] = int(items[1])
	count[2] = int(items[0])
	print('国家奖', count[0])
	writeToExcel(9, count[0])
	print('省部级奖', count[1])
	writeToExcel(10, count[1])
	print('学术专著', count[2])
	writeToExcel(19, count[2])

def Projects():
	count = [0, 0]
	url = 'http://www.nenu.edu.cn/273/list.htm'
	html = mr.getOnePage(url)
	count[0] += parse4(html, '由国家社科基金资助设立的重大项目：', '由教育部社科司资助设立的重大课题：')
	count[0] += parse4(html, '由国家自然科学基金资助的、面向世界科学前沿的重大基础研究项目，如：', '由科技部资助的以国家重大需求为导向的重大科学问题研究项目（含课题），如：')
	count[1] += parse4(html, '由教育部社科司资助设立的重大课题：', '科技项目')
	count[1] += parse4(html, '由科技部资助的以国家重大需求为导向的重大科学问题研究项目（含课题），如：', '')
	print('国家科研项目数', count[0])
	writeToExcel(25, count[0])
	print('省部科研项目数', count[1])
	writeToExcel(26, count[1])

def Library():
	url = 'http://www.library.nenu.edu.cn/Menu/AboutUs/BGGK/TSGJJ.aspx'
	html = mr.getOnePage(url)
	pattern = re.compile('藏书总量约.*?(\d+\.\d+).*?万册。图书.*?电子期刊.*?>(\d+)</span>.*?种，订购', re.S)
	items = re.findall(pattern, html)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	print('中外文期刊种类: ' + items[1])
	writeToExcel(40, int(items[1]))

def NENU():
	Professor()
	Scholars()
	ResearchAward()
	Projects()
	Library()
