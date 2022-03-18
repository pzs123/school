#-*- codeing = utf-8 -*-
#@Time :  15:06
#@Author : 潘中山
#@File : 通知.py
#@Software : PyCharm


import requests
from lxml import etree
import pdfkit
import os
import re
import base64

def main():
    j = -1
    cookie = "iPlanetDirectoryPro=AQIC5wM2LY4SfcyW8lLccIo3CPqoybuMSmU6fJ7FDp%2Fng7E%3D%40AAJTSQACMDE%3D%23; MOD_AUTH_CAS=MOD_AUTH_ST-29914-LxtekEEjH3pPbDg9OEeo1607338379708-sqQq-cas; JSESSIONID=0000S1rGAT6WTrF2p4ScExQ0F5T:19vn53d81; iPlanetDirectoryPro=AQIC5wM2LY4SfcyW8lLccIo3CPqoybuMSmU6fJ7FDp%2Fng7E%3D%40AAJTSQACMDE%3D%23"
    Baseurl = ["http://oa2list.zust.edu.cn/TZGG.aspx","http://oa2list.zust.edu.cn/GGGS.aspx"]
    Path = ["C:\\Users\\C1-515\\Desktop\\t通知\\x学校通知\\t通知简报\\x通知公告（原名学校通知）","C:\\Users\\C1-515\\Desktop\\t通知\\x学校通知\\g公示公告"]
    for baseurl in Baseurl:
        j = j + 1   #获取Path
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

            askURL2(url,cookie)  # 保存获取到的网页源码（一则通知公告）
            date = getDate2(url,cookie)     #其中一则通知公告的文件（列表）
            # print(date)
            path= Path[j]
            saveData(date, title, path,i,cookie,url)  # 保存数据
            i = i + 1

def creatpdf(path,title):
    title = title.replace("•","·")
    path = path + "\\" + title + '.pdf'
    print(title)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建pdf
        pdfkit.from_file("web.html",path)
    else:
        pass

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        pass

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
            if li_list[j][0].isdigit():     #判断标题第一个字符是否为数字
                li_list[j]=" "+li_list[j]
            data = li_list[j+1] + li_list[j]
            head.append(data)
            j = j + 3
        for w in lm_list:
            w = str(w)
            URL.append(w)
        DATE.append(head)
        DATE.append(URL)
    return DATE

def getDate2(url,cookie):         #获取通知公告中的文件地址
    DATE = []
    for i in range(0, 1):  # 调用获取页面信息的函数·1次
        s = str(re.findall("\d+", url)[1])
        # print(s)
        url2 = "http://oa2.zust.edu.cn/forum/attachments.do?resourceId="+s+"&resourceType=321"
        date = askURL3(url2,cookie)             #获取文件下载链接
        # 2.逐一解析数据

        user_dict_1 = eval(date)        #转换为字典
        list = user_dict_1['files']        #得到列表
        j = 0
        while j < len(list):
            date = str(list[j])
            user_dict_2 = eval(date)
            date = user_dict_2['downLoadUrl']
            name = user_dict_2['name']
            DATE.append(date)
            DATE.append(name)
            j = j + 1
        # print(DATE)
        return DATE


#得到指定一个URL的网页内容
def askURL(url,cookie):
    header = {                #模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Referer": "http://oa2list.zust.edu.cn/XQTBWJ.aspx",
        "Host": "oa2list.zust.edu.cn",
        "cookie": cookie,
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection": "keep - alive",
        "Upgrade - Insecure - Requests": "1",
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
    html = html.replace('楷体', '楷体_GB2312')
    html = html.replace('黑体', '黑体_GB2312')
    html = html.replace('仿宋', '仿宋_GB2312')
    tree = etree.HTML(html)
    li_list = tree.xpath('//p//span//img/@src')
    try:
        picture = li_list[0]
        picture2 = "http://oa2.zust.edu.cn/"+picture
        askURL5(picture2,cookie,url)        #爬取图片
        with open("图片1.jpg", 'rb') as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')       #将图片base64编码
        coding = "data:image/jpg;base64,"+image_base64
        html = html.replace(picture, coding)          #调用图片编码
    except Exception:
        pass
    with open('./web.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
    return html


def askURL3(url,cookie):
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Cookie": cookie,
    }
    request = requests.session().get(url=url, headers=header)
    html = request.text
    # print(html)
    return html

def askURL4(path,url,name,cookie,urlweb):
    s = str(re.findall("\d+", url)[0])
    url = "http://oa2.zust.edu.cn/forum/download.do?attachId="+s+"&media=0&iPlanetDirectoryPro=AQIC5wM2LY4Sfcy7PPt0P9VyArbzJYsIpmoEcPLe3eZlTlA%3D%40AAJTSQACMDI%3D%23"
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Cookie": cookie,
        "Host": "oa2.zust.edu.cn",
        "Referer": urlweb,
    }
    request = requests.session().get(url=url, headers=header)
    date = request.content
    with open(path+"/"+name,'wb') as fp:
        fp.write(date)

def askURL5(picture,cookie,urlweb):

    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Cookie": cookie,
        "Host": "oa2.zust.edu.cn",
        "Referer": urlweb,
    }
    request = requests.session().get(url=picture, headers=header)
    date = request.content
    with open('图片1.jpg', 'wb') as fp:
        fp.write(date)

def saveData(date,title,path,i,cookie,url):
    j = 0
    if len(date) == 0:
        try:
            i = i + 1
            result = "第" + str(i) + "份下载完成"
            print(result)
            creatpdf(path,title)  # 打印pdf输出
        except Exception:
            pass
    else:
        try:
            i = i + 1
            path = path + "\\" + title
            mkdir(path)
            result = "第" + str(i) + "份下载完成"
            print(result)
            creatpdf(path, title)  # 打印pdf输出
        except Exception:
            pass
        while j < len(date):
            askURL4(path,date[j],date[j+1],cookie,url)
            j = j + 2

if __name__ == "__main__" :  #当程序执行时
#调用函数
    main()
    print("爬取完毕！")

