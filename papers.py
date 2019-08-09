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

LIST = ['北京大学', '清华大学', '北京师范大学', '首都师范大学', '南开大学', '吉林大学', '东北师范大学', '复旦大学', '上海交通大学', '中国科学技术大学', '山东大学', '中南大学', '中山大学', '四川大学']

def writeToExcel(x, y, res):
	f = xlrd.open_workbook('result.xls')
	ws = xlutils.copy.copy(f)
	table = ws.get_sheet(0)
	table.write(x + 1, y, res)
	ws.save('result.xls')

def getEleById(Id):
	return WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, Id)))

def papers():
	global browser
	browser = webdriver.Chrome()
	browser.get('https://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ')
	input = getEleById('au_1_value2')
	onclick0 = getEleById('AllmediaBox')
	onclick1 = getEleById('mediaBox2')
	onclick2 = getEleById('btnSearch')
	onclick3 = getEleById('mediaBox1')
	for i, uni in enumerate(LIST):
		onclick0.click()
		input.clear()
		input.send_keys(uni + '数学')
		input.send_keys(Keys.ENTER)
		browser.switch_to.frame('iframeResult')
		time.sleep(2)
		result = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagerTitleCell')))
		result = re.findall(r' 找到 (.*?) 条结果 ', result.text)
		print(result[0])
		writeToExcel(i, 14, result[0])
		browser.switch_to.parent_frame()
		onclick1.click()
		browser.execute_script("arguments[0].scrollIntoView()", onclick2)
		onclick2.click()
		browser.switch_to.frame('iframeResult')
		time.sleep(2)
		result = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagerTitleCell')))
		result = re.findall(r' 找到 (.*?) 条结果 ', result.text)
		print(result[0])
		writeToExcel(i, 16, result[0])
		browser.switch_to.parent_frame()
		onclick3.click()
		browser.execute_script("arguments[0].scrollIntoView()", onclick2)
		onclick2.click()
		browser.switch_to.frame('iframeResult')
		time.sleep(2)
		result = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagerTitleCell')))
		result = re.findall(r' 找到 (.*?) 条结果 ', result.text)
		print(result[0])
		writeToExcel(i, 17, result[0])
		browser.switch_to.parent_frame()
	browser.close()
