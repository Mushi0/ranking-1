import MyRanking as mr
import papers
import Peking_University
import Sichuan_University
import Fudan_University
import Central_South_University
import Sun_Yat-sen_University
import Shandong_University
import University_of_Science_and_Technology_of_China
import Shanghai_Jiao_Tong_University
import Northest_Normal_University
import Jilin_University
import Nankai_University
import Capital_Normal_University

def main():
	mr.initExcel()
	papers.papers()
	Peking_University.PKU()
	Sichuan_University.SCU()
	Fudan_University.FU()
	Central_South_University.CSU()
	Sun_Yat-sen_University.SYSU()
	Shandong_University.SDU()
	University_of_Science_and_Technology_of_China.USTC()
	Shanghai_Jiao_Tong_University.SJTU()
	Northest_Normal_University.NENU()
	Jilin_University.JLU()
	Nankai_University.NKU()
	Capital_Normal_University.CNU()

if __name__ == '__main__':
	main()
