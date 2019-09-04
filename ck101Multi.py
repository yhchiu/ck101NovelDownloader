import requests
from bs4 import BeautifulSoup
from requests_html import HTML
import re
import multiprocessing 
import time
import os
from multiprocessing import Pool
from functools import partial

def getHtml(url): #分析HTML裡面源碼回傳
	headers={'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
	
	return requests.get(url,headers = headers).text

def multiTa(tid,temp): #用來multiprocess，接受tid來定位書本、temp來計算頁數
	pageText=getHtml(f'https://ck101.com/forum.php?mod=viewthread&tid={tid}&extra=page%3D3&page='+str(temp)) #運用tid跟頁數來生成url，然後用getHTML function得到源碼
	soup = BeautifulSoup(pageText, 'html.parser') #利用bs4解析
	mydivs = soup.findAll("td", {"class": "t_f"}) #找出所有內文
	fileB=open('temp/'+str(temp)+".txt","w",encoding="utf-8") #生成頁數檔名暫存
	
	for a in mydivs:	#將所有內文寫入到暫存檔裡面
		fileB.write(a.get_text())
	
	fileB.close() #檔案關閉
		


if __name__ == '__main__':
	starttime = time.time() #計算時間，時間開始
	
	tid=3803713	#小說tid，可以從網址看到，範例為極道天魔，滾開作品
	
	fpg=1	#開始頁數
	lpg=122	#結束頁數
	#上面兩參數可依照需求調整
	
	pageText=getHtml(f'https://ck101.com/forum.php?mod=viewthread&tid={tid}&extra=page%3D3')	
	soup = BeautifulSoup(pageText, 'html.parser')
	#先找第一頁，取得標題資訊
	
	title = re.sub(r"\s+","",soup.title.string)
	title = title.split("作者")[0]
	#從標題資訊中split出完整標題
	
	print(f'準備下載{title}')
	
	try:	#確認目錄down存在與否，不存在則建立down
		fileV=open('down/'+title+".txt","a",encoding="utf-8")
		print('在目錄down建立檔案')	
	except:
		print('目錄down不存在')
		print('生成目錄down')
		os.mkdir('down')
		print('在目錄down建立檔案')
		fileV=open('down/'+title+".txt","a",encoding="utf-8")
	

	try:	#確認目錄temp存在與否，不存在則建立temp
		fileA=open('temp/temp.txt','a',encoding='utf-8')
		print('在目錄temp建立檔案')
	except:
		print('目錄temp不存在')
		print('生成目錄temp')
		os.mkdir('temp')
		print('在目錄temp建立檔案')
		fileA=open('temp/temp.txt','a',encoding='utf-8')
	
	print('開始下載')
	
	#運用multiprocess來加速下載
	pool = multiprocessing.Pool()
	pool.map(partial(multiTa,tid), range(fpg,lpg+1))
	pool.close()
	
	print('檔案製作')
	
	#將所有temp檔案合併，移除
	for num in range(fpg,lpg+1):
		fileB=open('temp/'+str(num)+".txt","r",encoding="utf-8")
		fileA.write(fileB.read())
		fileB.close()
		os.remove('temp/'+str(num)+".txt")
		
	fileA.close()
	fileA=open('temp/temp.txt',"r",encoding="utf-8")
	
	print('簡易排版')
	
	#簡易排版然後寫入最終檔案
	for lines in fileA.read().splitlines():
		if(lines != '\n' and lines != '	'):
			lines=re.sub("\n+","", lines)
			fileV.write('	'+lines+'\n')
	fileA.close()
	os.remove('temp/temp.txt')
	print('一共花費{}秒'.format(time.time() - starttime),end=' ')
	print(f'下載{lpg-fpg+1}頁')