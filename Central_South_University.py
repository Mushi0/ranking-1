import re
import xlwt, xlrd
import xlutils.copy
import requests

def writeToExcel(n, res):
	f = xlrd.open_workbook('result.xls')
	ws = xlutils.copy.copy(f)
	table = ws.get_sheet(0)
	table.write(12, n, res)
	ws.save('result.xls')

def listAdd(a, b):
	for i in range(len(a)):
		a[i] += b[i]
	return(a)

def parseOnePage_Professor(dep):
	positions = ['js', 'fjs', 'js1']
	count = [0, 0, 0]
	for i, pos in enumerate(positions):
		url = 'http://math.csu.edu.cn/szdw/' + dep + '/' + pos + '.htm'
		response = requests.get(url)
		html = response.content.decode('utf-8')
		pattern = re.compile('font-size:9pt', re.S)
		items = re.findall(pattern, html)
		count[i] = int(len(items)/2)
	return count

def Professor():
	count = [0, 0, 0]
	departments = ['sxyyysxx', 'xxyjskxx', 'glytjxx', 'gdsxjxyyjzx']
	for dep in departments:
		c = parseOnePage_Professor(dep)
		print(c)
		count = listAdd(count, c)
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def Library():
	url = 'http://lib.csu.edu.cn/bgjs.jhtml'
	response = requests.get(url)
	html = response.content.decode('utf-8')
	pattern = re.compile('纸质文献总量(.*?)万余册', re.S)
	item = re.findall(pattern, html)[0]
	count1 = int(float(item) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)

def CSU():
	Professor()
	Library()
