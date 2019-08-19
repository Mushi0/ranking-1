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
import urllib.request
import tesserocr
from PIL import Image

LIST = ['北京大学', '清华大学', '北京师范大学', '首都师范大学', '南开大学', '吉林大学', '东北师范大学', '复旦大学', '上海交通大学', '中国科学技术大学', '山东大学', '中南大学', '中山大学', '四川大学']

def writeToExcel(x, y, res):
	f = xlrd.open_workbook('result.xls')
	ws = xlutils.copy.copy(f)
	table = ws.get_sheet(0)
	table.write(x + 1, y, res)
	ws.save('result.xls')

def getEleById(Id):
	return WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, Id)))

def getResult(i, n):
	browser.switch_to.frame('iframeResult')
	time.sleep(2)
	result = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pagerTitleCell')))
	result = re.findall(r' 找到 (.*?) 条结果 ', result.text)
	print(result[0])
	writeToExcel(i, n, result[0])

def clickOnSearch(onclick2):
	browser.execute_script("arguments[0].scrollIntoView()", onclick2)
	onclick2.click()

def reference(i):
	sum = 0
	t = 1
	while(1):
		onclick = getEleById('Page_next')
		table = browser.find_element_by_class_name('GridTableContent')
		results = browser.find_elements_by_xpath('//span[@class = "KnowledgeNetcont"]/a')
		if results == []:
			break
		for result in results:
			sum += int(result.text)
		# time.sleep(3)
		onclick.click()
		if t%15 == 0:
			'''# 验证码真可恶
			element = getEleById('CheckCodeImg')
			img_url = element.get_attribute('src')
			image = urllib.request.urlopen(img_url).read()
			f = open('code.jpg', 'wb')
			f.write(image)
			f.close()
			image = Image.open('code.jpg')
			# image.convert('1')
			code = tesserocr.image_to_text(image)
			print(code)
			input = getEleById('CheckCode')
			input.send_keys(code)
			onclick = browser.find_elements_by_xpath('/html/body/p[1]/input[2]')
			browser.execute_script("arguments[0].scrollIntoView()", onclick)
			onclick.click()'''
			time.sleep(5)
		if not getEleById('Page_next'):
			break
		t += 1
		print(t, sum)
	writeToExcel(i, 18, sum)
	print(sum)

def papers():
	global browser
	browser = webdriver.Chrome()
	browser.get('https://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ')
	input = getEleById('au_1_value2')
	onclick0 = getEleById('AllmediaBox')
	onclick1 = getEleById('mediaBox2')
	onclick2 = getEleById('btnSearch')
	onclick3 = getEleById('mediaBox1')
	onclick4 = getEleById('mediaBox3')
	for i, uni in enumerate(LIST):
		onclick0.click()
		input.clear()
		input.send_keys(uni + '数学')
		input.send_keys(Keys.ENTER)
		getResult(i, 14)
		onclick = browser.find_element_by_xpath('//div[@id="id_grid_display_num"]/a[3]')
		onclick.click()
		onclick = browser.find_element_by_xpath('//*[@id="J_ORDER"]/tbody/tr[1]/td/table/tbody/tr/td[1]/span[4]/a')
		onclick.click()
		reference(i)
		browser.switch_to.parent_frame()
		onclick1.click()
		clickOnSearch(onclick2)
		getResult(i, 16)
		browser.switch_to.parent_frame()
		onclick1.click()
		onclick3.click()
		clickOnSearch(onclick2)
		getResult(i, 17)
		browser.switch_to.parent_frame()
		onclick3.click()
		onclick4.click()
		clickOnSearch(onclick2)
		getResult(i, 15)
		browser.switch_to.parent_frame()
	browser.close()

papers()
