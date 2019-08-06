import requests
from requests.exceptions import RequestException
import re
import json
import time
import csv

PRO = '北京大学-教授-副教授-讲师.txt'
ACA = '北京大学-院士.txt'
YANG = '北京大学-长江学者人数.txt'
REC = '北京大学-万人计划.txt'
RES = '科研获奖.txt'

def getOnePage(url):
	try:
		headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			return response.content.decode('utf-8')
		return None
	except RequestException:
		return None

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

def initCsv():
	with open('Peking_University.csv', 'w') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(['Index', 'Result'])

def writeToCsv(row):
	with open('Peking_University.csv', 'a', encoding = 'utf-8') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(row)

def writeToFile(name, content):
	with open(name, 'a', encoding = 'utf-8') as f:
		#print(type(json.dumps(content)))
		f.write(json.dumps(content, ensure_ascii = False) + '\n')

def Professor(offset):
	global count_1
	url = 'http://www.math.lb.pku.edu.cn/jsdw/js_20180628175159671361/index' + str(offset) + '.htm'
	html = getOnePage(url)
	for item in parseOnePage_Professor(html):
		print(item)
		writeToFile(PRO, item)
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
	html = getOnePage(url)
	for item in parseOnePage_Academician(html):
		print(item)
		writeToFile(ACA, item)
		count_2 += 1

def YangtzeRiverScholars():
	global count_3
	url = 'http://www.math.lb.pku.edu.cn/jsdw/rcjh/index.htm'
	html = getOnePage(url)
	for item in parseOnePage_YangtzeRiverScholars(html):
		print(item)
		writeToFile(YANG, item)
		count_3 += 1

def RecruitmentProgram():
	global count_4
	url = 'http://www.math.lb.pku.edu.cn/jsdw/rcjh/index.htm'
	html = getOnePage(url)
	for item in parseOnePage_RecruitmentProgram(html):
		print(item)
		writeToFile(REC, item)
		count_4 += 1

def ResearchAward():
	global count_5, count_6, count_7
	url = 'http://www.math.lb.pku.edu.cn/kxyj/kyjl/index.htm'
	html = getOnePage(url)
	for item in parseOnePage_ResearchAward_1(html):
		print(item)
		writeToFile(RES, item)
		count_5 += 1
	for item in parseOnePage_ResearchAward_2(html):
		print(item)
		writeToFile(RES, item)
		count_6 += 1
	for item in parseOnePage_ResearchAward_3(html):
		print(item)
		writeToFile(RES, item)
		count_7 += 1

def Library():
	global count_8
	url = 'http://www.math.lb.pku.edu.cn/kxyj/ytsg/index.htm'
	html = getOnePage(url)
	pattern = re.compile('现有纸版文献.*?"font-size:16px">(.*?)</span>.*?外文期刊.*?"font-size:16px">(.*?)</span>.*?中文期刊.*?"font-size:16px">(.*?)</span>', re.S)
	item = re.findall(pattern, html)
	count_8.append(item[0][0])
	count_8.append(item[0][1] + item[0][2])

def main():
	i = ''
	Professor(offset = i)
	for i in range(1,5):
		Professor(offset = i)
	print(count_1)
	initCsv()
	writeToCsv(['教授数量', count_1[0]])
	writeToCsv(['副教授数量', count_1[1]])
	writeToCsv(['讲师数量', count_1[2]])
	writeToFile(PRO, '=============================================================================================')
	result = {
		'教授': count_1[0],
		'副教授': count_1[1],
		'讲师': count_1[2],
		'研究员': count_1[3]
	}
	writeToFile(PRO, result)
	Academician(offset = '')
	Academician(offset = '1')
	print(count_2)
	writeToCsv(['院士数量', count_2])
	writeToFile(ACA, '=============================================================================================')
	writeToFile(ACA, '院士: ' + str(count_2))
	YangtzeRiverScholars()
	print(count_3)
	writeToCsv(['长江学者人数', count_3])
	writeToFile(YANG, '=============================================================================================')
	writeToFile(YANG, '长江学者: ' + str(count_3))
	writeToCsv(['入选青年千人计划教师数量', '无数据'])
	RecruitmentProgram()
	print(count_4)
	writeToCsv(['万人计划人数', count_4])
	writeToFile(REC, '=============================================================================================')
	writeToFile(REC, '万人计划: ' + str(count_4))
	writeToCsv(['教师博士数量', '无数据'])
	ResearchAward()
	print(count_5)
	writeToCsv(['国家奖', count_5])
	writeToFile(RES, '=============================================================================================')
	writeToFile(RES, '国家奖: ' + str(count_5))
	print(count_6)
	writeToCsv(['省部级奖', count_6])
	writeToFile(RES, '省部级奖: ' + str(count_6))
	print(count_7)
	writeToCsv(['其他科研奖', count_7])
	writeToFile(RES, '其他科研奖: ' + str(count_7))
	writeToCsv(['专利数', '无数据'])
	writeToCsv(['发表学术论文数量', '无数据'])
	writeToCsv(['学术刊物论文数', '无数据'])
	writeToCsv(['核心期刊论文数', '无数据'])
	writeToCsv(['EI、SCI论文数', '无数据'])
	writeToCsv(['论文引用量', '无数据'])
	writeToCsv(['学术专著', '无数据'])
	writeToCsv(['翻译专著', '无数据'])
	writeToCsv(['五年科研经费合计', '无数据'])
	writeToCsv(['每年科研经费', '无数据'])
	writeToCsv(['目前科研经费', '无数据'])
	writeToCsv(['目前科研项目数', '无数据'])
	writeToCsv(['国家科研项目数', '无数据'])
	writeToCsv(['省部科研项目数', '无数据'])
	writeToCsv(['企事业委托项目', '无数据'])
	writeToCsv(['国际合作项目', '无数据'])
	writeToCsv(['本科生深造率比例', '无数据'])
	writeToCsv(['平均每年授予博士学位数', '无数据'])
	writeToCsv(['五年授予硕士学位数', '无数据'])
	writeToCsv(['国家教学成果奖', '无数据'])
	writeToCsv(['省部教学成果奖', '无数据'])
	writeToCsv(['出版教材数', '无数据'])
	writeToCsv(['省部重点实验室数', '无数据'])
	writeToCsv(['国家重点实验室数', '无数据'])
	Library()
	print(count_8)
	writeToCsv(['中外文藏书合计', count_8[0]])
	writeToCsv(['五年图书经费', '无数据'])
	writeToCsv(['购买数据库数量', '无数据'])
	writeToCsv(['中外文期刊种类', count_8[1]])
	writeToCsv(['万元仪器数', '无数据'])
	writeToCsv(['仪器设备总值', '无数据'])
	writeToCsv(['五年投资仪器费', '无数据'])
	writeToCsv(['外籍讲师比例', '无数据'])
	writeToCsv(['双语课程比例', '无数据'])
	writeToCsv(['国际化科研课题比例', '无数据'])
	writeToCsv(['国际留学生比例', '无数据'])

if __name__ == '__main__':
	count_1 = [0,0,0,0]
	count_2 = 0
	count_3 = 0
	count_4 = 0
	count_5 = 0
	count_6 = 0
	count_7 = 0
	count_8 = []
	main()
