import re
import MyRanking as mr

def writeToExcel(n, res):
	mr.writeToExcel(5, n, res)

def Professor():
	url = 'http://sms.nankai.edu.cn/5542/list.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('数学学科现有教师(\d+)人，教授(\d+)人、博士.*?博士学位的(\d+)人。其中，中国科学院院士(\d+)人、第三', re.S)
	items = re.findall(pattern, html)[0]
	count1 = items[1]
	print('教授数量: ' + str(count1))
	writeToExcel(1, count1)
	count2 = int(items[2])/int(items[0])
	count2 = '%.2f%%' % (count2 * 100)
	print('教师博士数量: ' + str(count2))
	writeToExcel(8, count2)
	count3 = items[3]
	print('院士数量: ' + str(count3))
	writeToExcel(4, count3)

def NKU():
	Professor()
