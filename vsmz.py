import urllib.request
import os
import re
import time
import socket
import multiprocessing
from bs4 import BeautifulSoup
import lxml
from urllib.error import URLError, HTTPError

#获取页码url字典
def crawerEach(url,urldir):
    #url=http://www.meizitu.com/a/more_1.html
    resp,tapp=Requestss(url)
    html=resp.read().decode('gbk')
    soup = BeautifulSoup(html,"lxml")
    items=soup.find('body').find('div',id='wrapper').find('div',id='container').find('div',id='pagecontent').find('div',id='maincontent').find(name='div',attrs={"class":"inWrap"}
    ).find('ul',attrs={'class':"wp-list clearfix"}).findAll(name="li",attrs={"class":"wp-item"})
    for item in items:
        target=item.find(name='div',attrs={"class":"con"}).find('h3').find('a')
        #if target.u ==  None and target.b == None and target.font == None:
        urldir[target.text] = ""+target.get('href')
        print("---"+target.get('href')+'----')
    resp.close();
    return urldir


#提取图片url
def getPicture(url,name):
    j=0
    resp1,tapp=Requestss(url)
    resp=resp1.read().decode('gbk')
    soup = BeautifulSoup(resp,"lxml")
    contents = soup.find('body').find('div',id='wrapper').find('div',id='container').find('div',id='pagecontent').find('div',id='maincontent').find(name='div',attrs={"class":"postContent"}
    ).find('div',id='picture').find('p').findAll('img')
    for tag in contents:    #下载图片
        fa=open("‪log.txt",'a')
        begin="正在下载:"+str(name)+'_'+str(j)
        print(begin)
        fa.write(begin+'\n')
        conn,i=Requestss(tag['src'])
        if(i!=0):
           stop="！！！未下载下载:"+str(name)+'_'+str(j)
           print(stop)
           fa.write(stop+'\n')
           fa.close()
           continue
        time.sleep(1)
        over="下载完成:"+str(name)+str(j)
        fa.write(over+'\n')
        fa.close()
        f=open(str(name)+'_'+str(j)+".jpg",'wb+')
        time.sleep(1)
        f.write(conn.read())
        f.close()
        print(over)
        j=j+1
        conn.close();
        resp1.close()
        time.sleep(1)

#页url获取 
def crawer():
    urldir={}
    for i in range(10):
        url="http://www.meizitu.com/a/more_"+str(i+1)+".html"
        print("=====================正在爬取第"+str(i+1)+"页=========")
        print("----"+url+"-------")
        urldir=crawerEach(url,urldir)#获取页码url字典
        for key,url in urldir.items():
            time.sleep(1)
            getPicture(url,key)

#获取网页 及异常处处理
def Requestss(url):
    user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    headers={'User-Agent':user_agent,}
    request=urllib.request.Request(url,None,headers)
    i=0
    while True: #一直循环，指导访问站点成功
            try:
                 request=urllib.request.Request(url,None,headers)
                 resp=urllib.request.urlopen(request,timeout=60)
                 break
            except  HTTPError as e:
                print('ConnectionError -- please wait 3 seconds')
                time.sleep(3)
            except URLError as e:
                print('ChunkedEncodingError -- please wait 3 seconds')
                time.sleep(3)
            i=i+1
            if(i>2):
                 url="http://www.meizitu.com/a/5580.html"
    return resp,i

if __name__ == "__main__":
    #print('CPU number:' + str(multiprocessing.cpu_count()))#4
    crawer()
    print("The End")

