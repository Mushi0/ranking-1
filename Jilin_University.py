import re
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(6, n, res)

def parse1(pos):
	url = 'http://math.jlu.edu.cn/szdw/' + pos + '.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('</a></td>', re.S)
	items = re.findall(pattern, html)
	return len(items)

def Professor():
	count = [0, 0, 0]
	positions = ['js', 'fjs', 'js1']
	for i, pos in enumerate(positions):
		count[i] = parse1(pos)
	print(count)
	for i, item in enumerate(count):
		writeToExcel(i + 1, item)

def Scholars():
	url = 'http://math.jlu.edu.cn/szdw/spys.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('中国科学院院士', re.S)
	items = re.findall(pattern, html)
	count = len(items)
	print('院士数量: ' + str(count))
	writeToExcel(4, count)

def Library():
	url = 'http://lib.jlu.edu.cn/portal/about/about.aspx'
	html = mr.getOnePage(url)
	pattern = re.compile('各类纸质书刊(\d+)万册，其中.*?订购中文期刊(\d+)种，外文期刊(\d+)种，报.*?西文文献数据库(\d+)种，中文数据库(\d+)种，中', re.S)
	items = re.findall(pattern, html)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(items[1]) + int(items[2])
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)
	count3 = int(items[3]) + int(items[4])
	print('购买数据库数量: ' + str(count3))
	writeToExcel(39, count3)

def JLU():
	Professor()
	Scholars()
	Library()
