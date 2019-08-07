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

LIST = ['Peking University', 'Tsinghua University', 'Beijing Normal University', 'Capital Normal University', 'Nankai University', 'Jilin University', 'Northeast Normal University', 'Fudan University', 'Shanghai Jiao Tong University', 'University of Science and Technology of China', 'Shandong University', 'Central South University', 'Sun Yat-sen University, SYSU', 'Sichuan University']

NUMBER = ''
PASS = ''

def writeToExcel(n, res):
	f = xlrd.open_workbook('result.xls')
	ws = xlutils.copy.copy(f)
	table = ws.get_sheet(0)
	table.write(n + 1, 16, res)
	ws.save('result.xls')

def MyClickClass(classname):
	onclick = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
	onclick.click()

def MyClickID(idname):
	onclick = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, idname)))
	onclick.click()

def MySel(selname, selection):
	onsel = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, selname)))
	sel = Select(onsel)
	sel.select_by_value(selection)

def MyInpute(name, inputs):
	input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, name)))
	input.clear()
	input.send_keys(inputs)

def papers():
	global browser
	browser = webdriver.Chrome()
	browser.get('http://125.70.226.88:8888/login')
	input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
	# input = browser.find_element_by_name('username')
	input.send_keys(NUMBER)
	input = browser.find_element_by_name('password')
	input.send_keys(PASS)
	input.send_keys(Keys.ENTER)
	try:
		MyClickClass('layui-layer-btn0')
	except:
		print('')
	onclick = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div[1]')))
	# onclick = browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]')
	onclick.click()
	time.sleep(2)
	handle1 = browser.current_window_handle
	handles = browser.window_handles
	for newhandle in handles:
		if newhandle != handle1:
			browser.switch_to_window(newhandle)
	onclick = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'EI Compendex')))
	# onclick = browser.find_element_by_xpath('//*[@id="result_list"]/table/tbody/tr[6]/td[2]')
	onclick.click()
	time.sleep(2)
	handle2 = browser.current_window_handle
	handles = browser.window_handles
	for newhandle in handles:
		if newhandle != handle1:
			if newhandle != handle2:
				browser.switch_to_window(newhandle)
	MyClickClass('button')
	MyClickID('add-searchfield-link')
	MySel('sect1', 'AF')
	MySel('field_c330', 'KY')
	MyInpute('search-word-c330', 'Mathematics')
	for i, uni in enumerate(LIST):
		MyInpute('search-word-1', uni)
		MyClickID('searchBtn')
		result = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'results-count')))
		result = re.findall(r'(.*?) records', result.text)
		print(result[0])
		writeToExcel(i, result[0])
