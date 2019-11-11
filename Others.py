import MyRanking as mr

def OTH():
	url = 'http://www.moe.gov.cn/s78/A16/A16_tjdc/201805/W020180522573775990138.pdf'
	file_name = '2017 年高等学校科技统计资料汇编.pdf'
	mr.saveOneFile(file_name, url)
