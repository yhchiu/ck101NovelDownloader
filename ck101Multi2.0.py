import requests
from bs4 import BeautifulSoup
from requests_html import HTML
import re
import multiprocessing 
import time
import os
from multiprocessing import Pool
from functools import partial
import datetime
from time import sleep

def fetch(url):
	headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

	resp=requests.get(url,headers = headers).text
	
	return resp

def findContent(url):

	soup=BeautifulSoup(fetch(url),'html.parser')
	content= soup.find_all('td','t_f')
	
	return content
	
def findLast(url):
	soup=BeautifulSoup(fetch(url),'html.parser')
	last=soup.find('div','pg',).text.split(' ')[1].split('下')[0]
	return int(last)

def findTitle(url):
	soup=BeautifulSoup(fetch(url),'html.parser')
	title=soup.find('h1').text.split('作者')[0].split(']')[1].strip()
	return title
	
def mkFile(title,last):
	fileA=open(f"src/{title}.txt","w",encoding="utf-8")
	
	for i in range(1,last+1):
		fileT=open(f"temp/temp{i}.txt","r",encoding="utf-8")
		fileA.write(fileT.read())
		fileT.close()
		os.remove(f'temp/temp{i}.txt')

def multiTa(tid,temp):

	url=f"https://ck101.com/forum.php?mod=viewthread&tid={tid}&extra=page%3D1&page={temp}"
	fileT=open(f"temp/temp{temp}.txt","w",encoding="utf-8")
	while True:
		contents=findContent(url)
		if(len(contents)==0):
			sleep(0.5)
		else:
			break
	for content in contents:
		lines=content.text.splitlines()
		temp=0
		for line in lines:
			if line != '':
				if(temp==0):
					fileT.write(line.strip()+'\n\n\n\n')
					temp+=1
				else:
					line=re.sub('本帖最後由.*編輯','',line)
					fileT.write('       '+line.strip()+'\n\n')
		temp=0
		fileT.write('\n\n\n\n\n\n')
	fileT.close()
	
if __name__ == '__main__':

	if(not os.path.exists('src')):	
		os.mkdir('src')
	if(not os.path.exists('temp')):	
		os.mkdir('temp')

	tid=2995922
	url=f"https://ck101.com/thread-{tid}-1-1.html"
	
	last=findLast(url)
	
	pool = multiprocessing.Pool()
	pool.map(partial(multiTa,tid), range(1,last+1))
	pool.close()
	mkFile(findTitle(url),last)
	