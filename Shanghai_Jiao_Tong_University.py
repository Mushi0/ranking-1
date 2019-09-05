import re
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(9, n, res)

def parseOnePage_Professor(order):
	url = 'http://www.math.sjtu.edu.cn/faculty/duty.php?duty=' + str(order)
	html = mr.getOnePage(url)
	pattern = re.compile('desc-zh', re.S)
	items = re.findall(pattern, html)
	return len(items)

def Professor():
	count = [0, 0, 0]
	order = [1, 2, 4]
	for i, o in enumerate(order):
		count[i] = parseOnePage_Professor(o)
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def SJTU():
	Professor()
