import re
import json
import time
import MyRanking as mr

PRO = '北京大学-教授-副教授-讲师.txt'
ACA = '北京大学-院士.txt'
YANG = '北京大学-长江学者人数.txt'
REC = '北京大学-万人计划.txt'
RES = '科研获奖.txt'

count_1 = [0,0,0,0]
count_2 = 0
count_3 = 0
count_4 = 0
count_5 = 0
count_6 = 0
count_7 = 0
count_8 = []

def parseOnePage_Professor(html):
	pattern = re.compile('<div class="left_info">.*?<h3>(.*?)</h3>.*?职  称：.*?<i>(.*?)</i></p>.*?研究方向：.*?<i>(.*?)</i></p>', re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield{
			'name': item[0],
			'position': item[1].lstrip() if '\t' in item[1] else item[1],
			'fields': item[2]
		}

def parseOnePage_Academician(html):
	pattern = re.compile('<div class="subAcademician_info">.*?<h3>(.*?)</h3>', re.S)
	items = re.findall(pattern, html)
	for item in items:
		yield{
			'name': item
		}

def parseOnePage_YangtzeRiverScholars(html):
	pattern_1 = re.compile('教育部青年长江学者(.*?)<div class="subLateBox">', re.S)
	pattern = re.compile('<a href="#">(.*?)((.*?))</a>', re.S)
	temp = re.findall(pattern_1, html)
	items = re.findall(pattern, temp[0])
	for item in items:
		yield{
			'name': item[0],
			'year': item[1]
		}

def parseOnePage_RecruitmentProgram(html):
	pattern_1 = re.compile('中组部“万人计划”百千万工程领军人才(.*?)<div class="subLateBox">', re.S)
	pattern = re.compile('<a href="#">(.*?)((.*?))</a>', re.S)
	temp = re.findall(pattern_1, html)
	items = re.findall(pattern, temp[0])
	for item in items:
		yield{
			'name': item[0],
			'year': item[1]
		}

def parseOnePage_ResearchAward_1(html):
	pattern_1 = re.compile('国家奖(.*?)省部级奖励', re.S)
	pattern = re.compile('<td class="et.*?width="192" x:str="">(.*?)</td>.*?width="432" x:str="">(.*?)</td>.*?width="214" x:str="">(.*?)</td>.*?width="120" x:str="">(.*?)</td>', re.S)
	temp = re.findall(pattern_1, html)
	items = re.findall(pattern, temp[0])
	for item in items:
		yield{
			'award': item[0],
			'project': item[1],
			'name': item[2],
			'time': item[3]
		}

def parseOnePage_ResearchAward_2(html):
	pattern_1 = re.compile('省部级奖励(.*?)社会科技奖励', re.S)
	pattern = re.compile('<td class="et.*?width="302" x:str="">(.*?)</td>.*?width="360" x:str="">(.*?)</td>.*?width="231" x:str="">(.*?)</td>.*?width="122" x:str="">(.*?)</td>', re.S)
	temp = re.findall(pattern_1, html)
	items = re.findall(pattern, temp[0])
	for item in items:
		yield{
			'award': item[0],
			'project': item[1],
			'name': item[2],
			'time': item[3]
		}

def parseOnePage_ResearchAward_3(html):
	pattern_1 = re.compile('社会科技奖励(.*?)<p style="text-align: center;">&nbsp;</p>', re.S)
	pattern = re.compile('<td class="et.*?width="311" x:str="">(.*?)</td>.*?width="594" x:str="">(.*?)</td>', re.S)
	temp = re.findall(pattern_1, html)
	items = re.findall(pattern, temp[0])
	for item in items:
		yield{
			'award': item[0],
			'name': item[1]
		}

def writeToExcel(n, res):
	mr.writeToExcel(1, n, res)

'''def writeToFile(name, content):
	with open(name, 'a', encoding = 'utf-8') as f:
		#print(type(json.dumps(content)))
		f.write(json.dumps(content, ensure_ascii = False) + '\n')'''

def Professor(offset):
	global count_1
	url = 'http://www.math.lb.pku.edu.cn/jsdw/js_20180628175159671361/index' + str(offset) + '.htm'
	html = mr.getOnePage(url)
	for item in parseOnePage_Professor(html):
		print(item)
		# writeToFile(PRO, item)
		if item['position'] == '教授':
			count_1[0] += 1
		elif item['position'] == '副教授':
			count_1[1] += 1
		elif item['position'] == '讲师':
			count_1[2] += 1
		else:
			count_1[3] += 1

def Academician(offset):
	global count_2
	url = 'http://www.math.lb.pku.edu.cn/jsdw/zgkxyys/index' + offset + '.htm'
	html = mr.getOnePage(url)
	for item in parseOnePage_Academician(html):
		print(item)
		# writeToFile(ACA, item)
		count_2 += 1

def YangtzeRiverScholars():
	global count_3
	url = 'http://www.math.lb.pku.edu.cn/jsdw/rcjh/index.htm'
	html = mr.getOnePage(url)
	for item in parseOnePage_YangtzeRiverScholars(html):
		print(item)
		# writeToFile(YANG, item)
		count_3 += 1

def RecruitmentProgram():
	global count_4
	url = 'http://www.math.lb.pku.edu.cn/jsdw/rcjh/index.htm'
	html = mr.getOnePage(url)
	for item in parseOnePage_RecruitmentProgram(html):
		print(item)
		# writeToFile(REC, item)
		count_4 += 1

def ResearchAward():
	global count_5, count_6, count_7
	url = 'http://www.math.lb.pku.edu.cn/kxyj/kyjl/index.htm'
	html = mr.getOnePage(url)
	for item in parseOnePage_ResearchAward_1(html):
		print(item)
		# writeToFile(RES, item)
		count_5 += 1
	for item in parseOnePage_ResearchAward_2(html):
		print(item)
		# writeToFile(RES, item)
		count_6 += 1
	for item in parseOnePage_ResearchAward_3(html):
		print(item)
		# writeToFile(RES, item)
		count_7 += 1

def Library():
	global count_8
	url = 'http://www.math.lb.pku.edu.cn/kxyj/ytsg/index.htm'
	html = mr.getOnePage(url)
	pattern = re.compile('现有纸版文献.*?"font-size:16px">(.*?)</span>.*?外文期刊.*?"font-size:16px">(.*?)</span>.*?中文期刊.*?"font-size:16px">(.*?)</span>', re.S)
	item = re.findall(pattern, html)[0]
	count_8.append(item[0])
	count_8.append(item[1] + item[2])

def PKU():
	Professor(offset = '')
	for i in range(1,5):
		Professor(offset = i)
	print(count_1)
	writeToExcel(1, count_1[0])
	writeToExcel(2, count_1[1])
	writeToExcel(3, count_1[2])
	'''writeToFile(PRO, '=============================================================================================')
	result = {
		'教授': count_1[0],
		'副教授': count_1[1],
		'讲师': count_1[2],
		'研究员': count_1[3]
	}
	writeToFile(PRO, result)'''
	Academician(offset = '')
	Academician(offset = '1')
	print(count_2)
	writeToExcel(4, count_2)
	'''writeToFile(ACA, '=============================================================================================')
	writeToFile(ACA, '院士: ' + str(count_2))'''
	YangtzeRiverScholars()
	print(count_3)
	writeToExcel(5, count_3)
	'''writeToFile(YANG, '=============================================================================================')
	writeToFile(YANG, '长江学者: ' + str(count_3))'''
	RecruitmentProgram()
	print(count_4)
	writeToExcel(7, count_4)
	'''writeToFile(REC, '=============================================================================================')
	writeToFile(REC, '万人计划: ' + str(count_4))'''
	ResearchAward()
	print(count_5)
	writeToExcel(9, count_5)
	print(count_6)
	writeToExcel(10, count_6)
	print(count_7)
	writeToExcel(11, count_7)
	'''writeToFile(RES, '=============================================================================================')
	writeToFile(RES, '国家奖: ' + str(count_5))
	writeToFile(RES, '省部级奖: ' + str(count_6))
	writeToFile(RES, '其他科研奖: ' + str(count_7))'''
	Library()
	print(count_8)
	writeToExcel(37, count_8[0])
	writeToExcel(40, count_8[1])
