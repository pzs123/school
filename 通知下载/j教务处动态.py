# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 10:37:11 2020

@author: 潘中山
"""

import requests
from lxml import etree
import pdfkit
import os
import sys


def main():
    m = -1
    Baseurl = ["https://jwc.zust.edu.cn/index/tzgg.htm"]
    Path = ["C:\\Users\\asus\\Desktop\\t通知\\j教务处动态"]
    cookie = "JSESSIONID=3ED08E07E1D2A89B5B28C45638B7313C"
    for baseurl in Baseurl:
        m = m + 1  # 获取Path
        # 1.爬取网页
        html = askURL(baseurl)
        # print(html)
        # sys.exit()
        for i in range(163, 0, -1):  # 调用获取页面信息的函数·17次（可更新）
            DATE = []
            head = []
            URL = []
            li_list = []
            lm_list = []
            ln_list = []
            url = "https://jwc.zust.edu.cn/index/tzgg/"+str(i)+".htm"
            html = askURL(url)  # 保存获取到的网页源码
            # print(html)
            # 2.逐一解析数据
            tree = etree.HTML(html)
            for j in range(1, 16):
                pro = 'section[2]/ul/li[' + str(j) + ']'
                ln_list = ln_list + tree.xpath('//' + pro + '/a/span/text()')  # 时间
                li_list = li_list + tree.xpath('//' + pro + '/a/font/text()')  # 标题
                lm_list = lm_list + tree.xpath('//' + pro + '/a/@href')  # 网址
            # print(ln_list)
            # print(li_list)
            # print(lm_list)
            # sys.exit()
            k = 0
            while k < len(li_list):  # 标题
                ln_list[k] = ln_list[k].replace("/","-")    #时间格式
                if li_list[k][0].isdigit():  # 判断标题第一个字符是否为数字
                    li_list[k] = " " + li_list[k]
                li_list[k] = li_list[k].rstrip()        #去除标题最后的空格
                data = str(ln_list[k]) + str(li_list[k])    #时间+标题
                head.append(data)   #加入列表
                k = k + 1
                # print(data)
            # print(head)
            # sys.exit()
            z = 0
            while z < len(lm_list):     #网址
                w = lm_list[z]
                w = w.replace("../../","")
                w = "https://jwc.zust.edu.cn/" + w       #
                URL.append(w)
                z = z + 1
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
                # sys.exit()
                path = Path[m]
                saveData(date, title, path, n, url)  # 保存数据
                n = n + 1


def creatpdf(path, title):
    title = title.replace("•", "·")
    path = path + "\\" + title + '.pdf'
    print(title)
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建pdf
        pdfkit.from_file("j教务处动态.html", path)
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
    li_list = tree.xpath('/html/body/section/section[6]/div/div[2]/section[2]/div/form/ul/li[1]/a/text()')  # 文件名称
    # print(li_list)
    lm_list = tree.xpath('/html/body/section/section[6]/div/div[2]/section[2]/div/form/ul/li[1]/a/@href')  # 文件地址
    # print(lm_list)
    # sys.exit()
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
        "Referer": "http://jwc.zust.edu.cn/index/zxtz.htm",

    }
    # 用户代理
    request = requests.session().get(url=url, headers=header)
    request.encoding = 'UTF-8'
    html = request.text
    # print(html)
    html = html.replace('楷体', '楷体_GB2312')
    html = html.replace('黑体', '黑体_GB2312')
    html = html.replace('仿宋', '仿宋_GB2312')
    with open('./j教务处动态.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
    return html


def askURL3(url):
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",

    }
    request = requests.session().get(url=url, headers=header)
    html = request.text
    # print(html)
    return html


def askURL4(path, name, url, urlweb):
    url = "http://jwc.zust.edu.cn/" + url
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Referer": urlweb,
    }
    request = requests.session().get(url=url, headers=header)
    date = request.content
    with open(path + "/" + name, 'wb') as fp:
        fp.write(date)


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

