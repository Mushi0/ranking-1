# ranking-1

## Introduction

This is a small project about using python(scrapy) to crawl some informations about universities in China. Things like the number of professors, the number of books collected in the library etc. 

### main.py

### papers_1.py

It is used to crawl the number of papers published by the university. Since I am a student from Sichuan University, I used the remote access to the website of our library. Just add the student ID and the password in this file and you can use it: 

```python
NUMBER = '123456'
PASS = '123456'
```

### papers.py

I used the database retrieval entry on my school's website. However, I found a much easier way to search the papers -- by accessing to cnki.net. So I updated this file and renamed the last one papers_1.py. The check codes problem is not solved yet, you should enter some check codes on the web driver while it asks you to. 

### Peking_University.py

It is meant to crawl some informations on the website of Peking University. 

### Sichuan_University.py

It is meant to crawl some informations on the website of Sichuan University. 

### Fudan_University.py

It is meant to crawl some informations on the website of Fudan University. 

### Central_South_University.py

It is meant to crawl some informations on the website of Central South University. 

### Sun_Yat-sen_University.py

It is meant to crawl some informations on the website of Sun Yat-sen University.

### Shandong_University.py

It is meant to crawl some informations on the website of Sun Shandong University. 

### University_of_Science_and_Technology_of_China.py

It is meant to crawl some informations on the website of Sun University of Science and Technology of China. 

### Shanghai_Jiao_Tong_University.py

It is meant to crawl some informations on the website of Shanghai Jiao Tong University. 

### Northest_Normal_University.py

It is meant to crawl some informations on the website of Northest Normal University. 

### Jilin_University.py

It is meant to crawl some informations on the website of Northest Jilin University. 

### Nankai_University.py

It is meant to crawl some informations on the website of Northest Nankai University. 

### Capital_Normal_University.py

It is meant to crawl some informations on the website of Northest Capital Normal University. 

### Beijing_Normal_University.py

It is meant to crawl some informations on the website of Beijing Normal University. 

### Tsinghua_University.py

It is meant to crawl some informations on the website of Tsinghua University. 

### Awards.py

It is meant to crawl the file: 2018年国家级教学成果奖获奖项目名单.docx

### Teaching_Demonstration.py

It is meant to crawl the file: 2015年国家级实验教学示范中心入选名单.xls

### Others.py

It is meant to crawl the file: 2017 年高等学校科技统计资料汇编.pdf

### Projects.py

It is meant to crawl the file: 结题项目统计.xlsx
