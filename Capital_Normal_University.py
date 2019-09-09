import re
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(4, n, res)

def parse1(page):
	url = 'http://math.cnu.edu.cn/szdw/qtjs/index' + page + '.htm'
	html = mr.getOnePage(url)
	html = html.replace('学位：', '学  位：')
	pattern = re.compile('职  称：(.*?)<br>学  位：(.*?)<br>毕业', re.S)
	result = re.findall(pattern, html)
	return result

def count1(result):
	count = [0, 0, 0, 0, 0]
	for item in result:
		if '副教授' in item[0]:
			count[1] += 1
		elif '教授' in item[0]:
			count[0] += 1
		elif '讲师' in item[0]:
			count[2] += 1
		if '博士' in item[1]:
			count[3] += 1
		count[4] += 1
	return count

def Professor():
	count = [0, 0, 0, 0, 0]
	for i in range(5):
		if i == 0:
			result = parse1('')
		else:
			result = parse1(str(i))
		count = mr.listAdd(count, count1(result))
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

def Scholars():
	url = 'http://math.cnu.edu.cn/szdw/lyys/index.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('<strong>', re.S)
	result = re.findall(pattern, html)
	count = len(result)
	print('院士数量: ' + str(count))
	writeToExcel(4, count)

def Library():
	url = 'http://lib.cnu.edu.cn/library/95.html'
	html = mr.getOnePage(url)
	pattern = re.compile('印刷型文献(\d+)万余册，电子图书.*?电子期刊(\d+)万余种。购买非书刊类数据库(\d+)个，自', re.S)
	items = re.findall(pattern, html)[0]
	count1 = int(float(items[0]) * 10000)
	print('中外文藏书合计: ' + str(count1))
	writeToExcel(37, count1)
	count2 = int(float(items[1]) * 10000)
	print('中外文期刊种类: ' + str(count2))
	writeToExcel(40, count2)
	print('购买数据库数量: ' + items[2])
	writeToExcel(39, int(items[2]))

def CNU():
	Professor()
	Scholars()
	Library()
