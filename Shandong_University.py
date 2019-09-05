import re
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(11, n, res)

def parseOnePage_Scholars(pos):
	url = 'http://www.math.sdu.edu.cn/szdw/jcrc/' + pos + '.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('</a></dd>', re.S)
	items = re.findall(pattern, html)
	return len(items)

def Scholars():
	count = [0, 0]
	positions = ['zkyys', 'zjxzjljh_tpjs']
	for i, pos in enumerate(positions):
		count[i] = parseOnePage_Scholars(pos)
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 4, item)

def Library():
	url = 'http://www.lib.sdu.edu.cn/page/about.html'
	html = mr.getOnePage(url)
	pattern = re.compile('馆藏纸质文献(.*?)万余册', re.S)
	item = re.findall(pattern, html)[0]
	count1 = int(float(item) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)

def SDU():
	Scholars()
	Library()
