import MyRanking as mr

def TD():
	url = 'http://www.moe.gov.cn/s78/A08/A08_gggs/s8468/201601/W020160112518426906333.xls'
	file_name = '2015年国家级实验教学示范中心入选名单.xls'
	mr.saveOneFile(file_name, url)
