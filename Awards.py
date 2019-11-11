import MyRanking as mr

def AWD():
	url = 'http://www.moe.gov.cn/srcsite/A10/s7058/201901/W020190102592205739382.docx'
	file_name = '2018年国家级教学成果奖获奖项目名单.docx'
	mr.saveOneFile(file_name, url)
