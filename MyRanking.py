import xlwt, xlrd
import xlutils.copy
import requests
from requests.exceptions import RequestException
import re

def initExcel():
	f = xlwt.Workbook()
	sheet1 = f.add_sheet('sheet1', cell_overwrite_ok=True)
	row0 = ['大学', '教授数量', '副教授数量', '讲师数量', '院士数量', '长江学者人数', '入选青年千人计划教师数量', '万人计划人数', '教师博士数量', '国家奖', '省部级奖', '其他科研奖', '专利数', '发表学术论文数量', '学术刊物论文数', '核心期刊论文数', 'EI论文数', 'SCI论文数', '论文引用量', '学术专著', '翻译专著', '五年科研经费合计', '每年科研经费', '目前科研经费', '目前科研项目数', '国家科研项目数', '省部科研项目数', '企事业委托项目', '国际合作项目', '本科生深造率比例', '平均每年授予博士学位数', '五年授予硕士学位数', '国家教学成果奖', '省部教学成果奖', '出版教材数', '省部重点实验室数', '国家重点实验室数', '中外文藏书合计', '五年图书经费', '购买数据库数量', '中外文期刊种类', '万元仪器数', '仪器设备总值', '五年投资仪器费', '外籍讲师比例', '双语课程比例', '国际化科研课题比例', '国际留学生比例']
	for i in range(0,len(row0)):
		sheet1.write(0, i, row0[i])
	column0 = ['北京大学', '清华大学', '北京师范大学', '首都师范大学', '南开大学', '吉林大学', '东北师范大学', '复旦大学', '上海交通大学', '中国科学技术大学', '山东大学', '中南大学', '中山大学', '四川大学']
	for i in range(0,len(column0)):
		sheet1.write(i+1, 0, column0[i])
	f.save('result.xls')

def writeToExcel(x, y, res):
	f = xlrd.open_workbook('result.xls')
	ws = xlutils.copy.copy(f)
	table = ws.get_sheet(0)
	table.write(x, y, res)
	ws.save('result.xls')

def listAdd(a, b):
	for i in range(len(a)):
		a[i] += b[i]
	return(a)

def getOnePage(url):
	try:
		headers = {
			'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		}
		response = requests.get(url, headers = headers)
		if response.status_code == 200:
			return response.content.decode('utf-8')
		else:
			print(response)
		return None
	except RequestException:
		return None

def parse2(element, pre, aft):
	r = pre + '(.*?)' + aft
	pattern = re.compile(r, re.S)
	temp = re.findall(pattern, element)[0]
	pattern1 = re.compile('.*?(\n).*?', re.S)
	temp = re.findall(pattern1, temp)
	count = len(temp) - 1
	return count

def saveOneFile(file_name, url):
	headers = {
		'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	}
	resp = requests.get(url, headers = headers)
	with open('Files/' + file_name, 'wb') as f:
		f.write(resp.content)
		print('Already Downloaded', file_name)
