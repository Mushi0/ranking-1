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

### Peking_University.py

It is meant to crawl some informations on the website of Peking University. 

### papers.py

I used the database retrieval entry on my school's website. However, I found a much easier way to search the papers -- by accessing to cnki.net. So I updated this file and renamed the last one papers_1.py
