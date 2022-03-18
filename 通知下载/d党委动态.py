# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 10:37:11 2020

@author: admin
"""
import requests
from lxml import etree
import pdfkit
import os
import sys


def main():
    m = -1
    Baseurl = ["https://zzb.zust.edu.cn/tzgg.htm"]
    Path = ["C:\\Users\\admin\\Desktop\\t通知\\d党委动态"]
    cookie = "iPlanetDirectoryPro=AQIC5wM2LY4Sfcx0DYWCL82wxz3QLumDy0GmdxB9Dyxotn0%3D%40AAJTSQACMDI%3D%23; JSESSIONID=104B3F85DAB80EEA155141AF6CD15CDC"
    for baseurl in Baseurl:
        m = m + 1  # 获取Path
        # 1.爬取网页
        # html = askURL(baseurl)
        # print(html)
        for i in range(17, -1, -1):  # 调用获取页面信息的函数·17次（可更新）
            DATE = []
            head = []
            URL = []
            li_list = []
            lm_list = []
            ln_list = []
            url = "https://zzb.zust.edu.cn/tzgg/" + str(i) + ".htm"  # （可更新）
            html = askURL(url)  # 保存获取到的网页源码
            # print(html)
            # 2.逐一解析数据
            tree = etree.HTML(html)
            for j in range(0, 12):
                pro = 'li[@id="line_u5_' + str(j) + '"]'
                ln_list = ln_list + tree.xpath('//' + pro + '//text()')  # 时间
                li_list = li_list + tree.xpath('//' + pro + '//a/@title')  # 标题
                lm_list = lm_list + tree.xpath('//' + pro + '//a/@href')  # 网址
            # print(ln_list)
            # print(li_list)
            # print(lm_list)
            j = 0
            k = 0
            while k < len(li_list):  # 标题
                data = str(ln_list[j]) + str(li_list[k])
                head.append(data)
                k = k + 1
                j = j + 2
            # print(head)
            # sys.exit()
            z = 0
            while z < len(lm_list):
                w = lm_list[z]
                w = "http://zzb.zust.edu.cn/" + w
                URL.append(w)
                z = z + 1
            # sys.exit()
            DATE.append(head)
            DATE.append(URL)
            # print(DATE)

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
        pdfkit.from_file("党委动态.html", path)
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
        "Referer": "http://zzb.zust.edu.cn/tzgg.htm",
        "Host": "zzb.zust.edu.cn",

    }
    # 用户代理
    request = requests.session().get(url=url, headers=header)
    request.encoding = 'UTF-8'
    html = request.text
    # print(html)
    html = html.replace('楷体', '楷体_GB2312')
    html = html.replace('黑体', '黑体_GB2312')
    html = html.replace('仿宋', '仿宋_GB2312')
    with open('./党委动态.html', 'w', encoding='utf-8') as fp:
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
    url = "http://zzb.zust.edu.cn/" + url
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

