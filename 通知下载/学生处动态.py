# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 19:16:51 2020

@author: admin
"""


import requests
from lxml import etree
import pdfkit
import os
import datetime
from PIL import Image
import pytesseract
import sys


def main():
    m = -1
    Baseurl = ["https://xsc.zust.edu.cn/tzgg.htm"]
    Path = ["C:\\Users\\asus\\Desktop\\t通知\\x学生处动态"]
    cookie = "UM_distinctid=17647d79cde142-038e9382db91a6-3b3d5203-e1000-17647d79cdf4ba; iPlanetDirectoryPro=AQIC5wM2LY4SfcxSUyn83uGL2j%2Ffa5YDFfY7FZxFKDcbfCc%3D%40AAJTSQACMDE%3D%23; JSESSIONID=243CB4A72E1BB68B6E47359DBF985935"
    for baseurl in Baseurl:
        m = m + 1  # 获取Path
        # 1.爬取网页
        # html = askURL(baseurl)
        # print(html)
        for i in range(5, 0, -1):  # 调用获取页面信息的函数·17次（可更新）
            DATE = []
            head = []
            URL = []
            delete = []
            # url = baseurl
            url = "https://xsc.zust.edu.cn/tzgg/" + str(i) + ".htm"
            html = askURL(url)  # 保存获取到的网页源码
            # print(html)
            # 2.逐一解析数据
            tree = etree.HTML(html)

            ln_list = tree.xpath('//tr[@class="tr0"]//span//text()')  # 时间
            li_list = tree.xpath('//tr[@class="tr0"]//a//text()')  # 标题
            lm_list = tree.xpath('//tr[@class="tr0"]//a/@href')  # 网址
            # del lm_list[0]
            # print(lm_list)
            # exit()
            for a in range(0,10):
                #print(len(lm_list[a]))
                if(len(lm_list[a])>25):
                    delete.append(a)  #记录需要删除的元素

            for x in delete:
                del ln_list[x]
                del li_list[x]
                del lm_list[x]
            # print(ln_list)
            # print(li_list)
            # print(lm_list)
            # sys.exit()
            j = 0
            k = 0
            while k < len(li_list):  # 标题
                ln_list[j] = ln_list[j].replace("/","-")
                if li_list[k][0].isdigit():  # 判断标题第一个字符是否为数字
                    li_list[k] = " " + li_list[j]
                li_list[k] = li_list[k].rstrip()    #去除标题最后的空格
                data = str(ln_list[j]) + str(li_list[k])    #时间+标题
                head.append(data)   #加入列表
                k = k + 1
                j = j + 1
                # print(data)
            # print(head)
            # sys.exit()
            z = 0
            while z < len(lm_list):     #网址
                w = lm_list[z]
                w = w.replace("..","")
                w = "https://xsc.zust.edu.cn/" + w       #
                URL.append(w)
                z = z + 1
            # sys.exit()
            DATE.append(head)
            DATE.append(URL)
            # print(DATE)
            # sys.exit()

            n = 0
            while n < len(DATE[1]):
                title = DATE[0][n]
                title = title.replace('/', ' ')
                url = DATE[1][n]
                # print(url)
                # print(title)
                html = askURL2(url, cookie)  # 保存获取到的网页源码（一则通知公告）
                date = getDate2(html)  # 其中一则通知公告的文件（列表）
                # print(date)
                path = Path[m]
                saveData(date, title, path, n, url)  # 保存数据
                n = n + 1


def creatpdf(path, title):
    title = title.replace("•", "·")
    path = path + "\\" + title + '.pdf'
    print(title)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建pdf
        pdfkit.from_file("x学生处动态.html", path)
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


def getDate2(html):  # 获取通知公告中的文件地址
    name = []
    url = []
    DATE = []
    tree = etree.HTML(html)
    # print(html)
    li_list = tree.xpath('//ul[@style="list-style-type:none;"]//li/a/text()')  # 文件名称
    # print(li_list)
    lm_list = tree.xpath('//ul[@style="list-style-type:none;"]//li/a/@href')  # 文件地址
    # print(lm_list)
    i = 0
    while i < len(li_list):
        name.append(li_list[i])
        i = i + 1
    j = 0
    while j < len(lm_list):
        url.append(lm_list[j])
        j = j + 1
    DATE.append(name)
    DATE.append(url)
    # print(DATE)
    # exit()
    return DATE


# 得到指定一个URL的网页内容
def askURL(url):
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

    }
    # 用户代理

    request = requests.get(url=url, headers=header)
    request.encoding = 'UTF-8'
    html = request.text
    return html


def askURL2(url, cookie):  # 进入通知公告
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "cookie": cookie,
        "Referer": "https://xsc.zust.edu.cn/tzgg.htm",

    }
    # 用户代理
    request = requests.session().get(url=url, headers=header)
    request.encoding = 'UTF-8'
    html = request.text
    html = html.replace('楷体', '楷体_GB2312')
    html = html.replace('黑体', '黑体_GB2312')
    html = html.replace('仿宋', '仿宋_GB2312')
    html = html.replace('<div><ul id="dropmenu1" class="dropMenu"><li><a href="../../bmjs/bmzz.htm">部门职责</a></li></ul>','')
    html = html.replace('<ul id="dropmenu2" class="dropMenu"><li><a href="../../xsjy/szjy.htm">思政教育</a></li><li><a href="../../xsjy/aqjy.htm">安全教育</a></li><li><a href="../../xsjy/jljy.htm">纪律教育</a></li><li><a href="../../xsjy/xfjy.htm">学风建设</a></li></ul>','')
    html = html.replace('<ul id="dropmenu3" class="dropMenu"><li><a href="../../pjpy/zhcp.htm">综合测评</a></li><li><a href="../../pjpy/pjpy.htm">评奖评优</a></li></ul>','')
    html = html.replace('<ul id="dropmenu5" class="dropMenu"><li><a href="../../xszz/jjzz.htm">经济资助</a></li><li><a href="../../xszz/qgzx.htm">勤工助学</a></li></ul>','')
    html = html.replace('<ul id="dropmenu6" class="dropMenu"><li><a href="../../xljk/xljkjy.htm">心理健康教育</a></li></ul>','')
    html = html.replace('<ul id="dropmenu7" class="dropMenu"><li><a href="../../gygl/wmqsjs.htm">文明寝室建设</a></li></ul>','')
    html = html.replace('<ul id="dropmenu8" class="dropMenu"><li><a href="../../dwjs/dwjs.htm">队伍建设</a></li></ul>','')
    html = html.replace('<ul id="dropmenu11" class="dropMenu"><li><a href="../../zlxz/zlxz.htm">资料下载</a></li></ul>','')
    html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'+html
    # print(html)
    # sys.exit()
    with open('./x学生处动态.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
    return html


def askURL3(url):
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

    }
    request = requests.session().get(url=url, headers=header)
    html = request.text
    # print(html)
    return html


def askURL4(path, name, url, urlweb):
    url = "http://jwc.zust.edu.cn/" + url  # 文件链接

    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Referer": url,
        "Cookie":"UM_distinctid=1754e1c5a0b2e9-05f42278cc4a65-c781f38-144000-1754e1c5a0c95e; JSESSIONID=238A5E059FBEBBFC783E21997C566696"
    }
    request = requests.session().get(url=url, headers=header)
    with open(path+"\\"+name, 'wb') as fp:
        fp.write(request.content)

def saveData(date, title, path, i, url):
    j = 0
    if len(date[0]) == 0:
        try:
            i = i + 1
            result = "第" + str(i) + "份下载完成"
            print(result)
            creatpdf(path, title)  # 打印pdf输出
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
        while j < len(date[0]):
            askURL4(path, date[0][j], date[1][j], url)
            j = j + 1


if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    print("爬取完毕！")
