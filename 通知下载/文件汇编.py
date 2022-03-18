#-*- codeing = utf-8 -*-
#@Time :  15:06
#@Author : 潘中山
#@File : 通知.py
#@Software : PyCharm


import requests
from lxml import etree
import os
import re

def main():
    j = -1
    Baseurl = ["http://oa2list.zust.edu.cn/XZWJ.aspx","http://oa2list.zust.edu.cn/DWWJ.aspx","http://oa2list.zust.edu.cn/BGSWJ.aspx","http://oa2list.zust.edu.cn/XQTBWJ.aspx","https://oa2list.zust.edu.cn/XQTBWJ.aspx"]
    Path = ["C:\\Users\\C1-515\\Desktop\\t通知\\x学校通知\\w文件汇编\\x行政文件","C:\\Users\\C1-515\\Desktop\\t通知\\x学校通知\\w文件汇编\\d党委文件","C:\\Users\\C1-515\\Desktop\\t通知\\x学校通知\\w文件汇编\\b办公室文件","C:\\Users\\C1-515\\Desktop\\t通知\\x学校通知\\t通知简报\\x校情简报"]
    for baseurl in Baseurl:
        j = j + 1   #获取Path
        cookie = "iPlanetDirectoryPro=AQIC5wM2LY4SfcyrH0DTr6JhUW6Mpg5BwWZp6dh5qWTlV98%3D%40AAJTSQACMDE%3D%23; MOD_AUTH_CAS=MOD_AUTH_ST-6632-QyQ6Zq3e9b9jWtKcWIgt1605269302715-sqQq-cas; JSESSIONID=0000_BQBvbEGjUSEGpPegeggCBl:19vn53d81; iPlanetDirectoryPro=AQIC5wM2LY4SfcyrH0DTr6JhUW6Mpg5BwWZp6dh5qWTlV98%3D%40AAJTSQACMDE%3D%23"
        #1.爬取网页
        # html = askURL(baseurl)
        # print(html)
        DATE = getDate(baseurl,cookie)     #获取标题和网址超链接
        # print(DATE)
        # exit()
        i = 0
        while i < len(DATE[1]):
            title = DATE[0][i]
            title = title.replace('/',' ')
            url = DATE[1][i]
            # print(url)
            # print(title)
            url2 = getDate2(url,cookie)     #获取文件网址
            # print(date)
            path= Path[j]
            saveData(url2, title, path,i,cookie,url)  # 保存数据
            i = i + 1


def getDate(baseurl,cookie):
    DATE = []
    head = []
    URL = []
    for i in range(0,1):       #调用获取页面信息的函数·1次
        url = baseurl
        html = askURL(url,cookie)      #保存获取到的网页源码
        #2.逐一解析数据
        tree = etree.HTML(html)
        li_list = tree.xpath('//div/table/tr/td//text()')    #标题/时间
        # print(li_list)
        lm_list = tree.xpath('//div//tr//a/@href')  #网址
        # print(lm_list)
        j = 1
        while j < len(li_list):     #标题
            data = str(li_list[j+1]) + str(li_list[j])
            head.append(data)
            j = j + 3
        for w in lm_list:
            w = str(w)
            URL.append(w)
        DATE.append(head)
        DATE.append(URL)
    return DATE

def getDate2(url,cookie):         #获取通知公告中的文件地址
    for i in range(0, 1):  # 调用获取页面信息的函数·1次
        html = askURL2(url,cookie)
        tree = etree.HTML(html)
        li_list = tree.xpath('//div/input/@onclick')  # 文件地址
        s = li_list[0]
        list = re.findall("\d+", s)
        num = list[0]+"_"+list[1]
        url2 = "http://oa2.zust.edu.cn/fileReleasePub/downloadFileReleasePub.do?type=html&content="+num+"&title=%E6%B5%99%E6%B1%9F%E7%A7%91%E6%8A%80%E5%AD%A6%E9%99%A2%E5%85%B3%E4%BA%8E%E7%BB%99%E4%BA%88%E4%B8%9B%E7%90%B3%E6%A1%90%E7%AD%8975%E5%90%8D%E5%90%8C%E5%AD%A6%E6%94%BE%E5%BC%83%E5%85%A5%E5%AD%A6%E8%B5%84%E6%A0%BC%E5%A4%84%E7%90%86%E7%9A%84%E5%86%B3%E5%AE%9A&moduleId="
        # print(DATE)
        return url2


#得到指定一个URL的网页内容
def askURL(url,cookie):
    header = {                #模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Host": "oa2list.zust.edu.cn",
        "cookie": cookie,
    }
                     #用户代理
    request = requests.session().get(url=url,headers=header)
    #request.encoding='UTF-8'
    html = request.text
    # print(html)
    return html

def askURL2(url,cookie):          #进入通知公告
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Cookie": cookie,
        "Referer": "http://oa2list.zust.edu.cn/TZGG.aspx",
        "Host": "oa2.zust.edu.cn",

    }
    # 用户代理
    request = requests.session().get(url=url, headers=header)
    html = request.text
    # print(html)
    return html

def askURL4(path,url2,name,cookie,urlweb):
    path = path + "/"+name + ".pdf"
    folder = os.path.exists(path)
    print(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建pdf
        header = {  # 模拟浏览器头部信息·向服务器发送信息
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "Cookie": cookie,
            "Host": "oa2.zust.edu.cn",
            "Referer": urlweb,
        }
        request = requests.session().get(url=url2, headers=header)
        date = request.content
        with open(path, 'wb') as fp:
            fp.write(date)
        print("新增")
    else:
        pass


def saveData(url2,title,path,i,cookie,url):
    i = i + 1
    askURL4(path, url2, title, cookie,url)
    result = "第" + str(i) + "份下载完成"
    print(result)


if __name__ == "__main__" :  #当程序执行时
#调用函数
    main()
    print("爬取完毕！")

