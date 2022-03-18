#-*- codeing = utf-8 -*-


from bs4 import BeautifulSoup  # 网页解析·获取数据
import requests
from lxml import etree
import pdfkit
import sys
import os

def main():
    baseurl = "https://jwxt.zust.edu.cn/jstjkbcx.aspx?zgh=320077&xm=%E5%90%B4%E8%8C%97%E8%94%9A&gnmkdm=N122303"
    # 1.爬取网页
    getData(baseurl)




def getData(baseurl):
    # data = []
    for i in range(0, 1):  # 调用获取页面信息的函数·1次
        url = baseurl
        askURL(url)  # 保存获取到的网页源码

def askURL(url):
    header = {  # 模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Cookie": "UM_distinctid=17647d79cde142-038e9382db91a6-3b3d5203-e1000-17647d79cdf4ba; ASP.NET_SessionId=g5kpkkqpcdofrmuy4z0ut3rq; iPlanetDirectoryPro=AQIC5wM2LY4Sfcxd62i14yrRob5MzmNxUdqnfxJLkkwL7wk%3D%40AAJTSQACMDE%3D%23",
        "Referer": "https://jwxt.zust.edu.cn/js_main.aspx?xh=320077",
        "Host": "jwxt.zust.edu.cn",
    }
    # 用户代理
    cj_html_1 = requests.session().get(url, headers=header)
    html = cj_html_1.text
    # print(html)
    # sys.exit()
    soup = BeautifulSoup(cj_html_1.text, 'lxml')
    # print(soup)
    value3 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    # print(value3)
    # exit()
    data = {

        "__EVENTTARGET": "bm",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "",
        "__VIEWSTATEGENERATOR":"E6032F7F",
        "xn": "2020-2021",
        "xq": "2",
        "bm": "信息与电子工程学院",
        "TextBox1":"",
        "js": "320077",
    }

    data["__VIEWSTATE"] = value3
    html = requests.session().post(url=url, headers=header, data=data).text #陈芳妮
    html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n' + html
    html = html.replace('<table id="Table6" cellspacing="0" cellpadding="4" class="blacktab" border="0" height="132" width="100%">', '<table id="Table6" class="blacktab" rules="all" border="1" height="132" width="100%">')
    with open('./teacher.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
    name = "陈芳妮"
    name = single_get_first(name) + name
    try:
        creatpdf(name)
    except Exception:
        pass

    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    value3 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    # print(value3)
    data["__VIEWSTATE"] = value3
    data["js"] = "118072"
    data["__EVENTTARGET"] = "js"
    html = requests.session().post(url=url, headers=header, data=data).text   #陈军勇
    # print(html)
    html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'+html
    html = html.replace('<table id="Table6" cellspacing="0" cellpadding="4" class="blacktab" border="0" height="132" width="100%">', '<table id="Table6" class="blacktab" rules="all" border="1" height="132" width="100%">')
    with open('./teacher.html', 'w', encoding='utf-8') as fp:
        fp.write(html)
    name = "陈军勇"
    name = single_get_first(name) + name    #获取中文首字母
    try:
        creatpdf(name)
    except Exception:
        pass

    tree = etree.HTML(html)
    li_list = tree.xpath('//option//@value')     #工号
    li = len(li_list)
    ln_list = tree.xpath('//option//text()')  # 名字
    # print(li_list[74])
    # print(ln_list[69])

    for i in range(74,li):  #工号
        j = i - 5   #名字
        soup = BeautifulSoup(html, 'lxml')
        # print(soup)
        value3 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
        # print(value3)
        data["__VIEWSTATE"] = value3
        data["js"] = li_list[i]
        # print(li_list[i])

        html = requests.session().post(url=url, headers=header, data=data).text  # 陈寿法
        html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n' + html
        html = html.replace('<table id="Table6" cellspacing="0" cellpadding="4" class="blacktab" border="0" height="132" width="100%">', '<table id="Table6" class="blacktab" rules="all" border="1" height="132" width="100%">')

        with open('./teacher.html', 'w', encoding='utf-8') as fp:
            fp.write(html)
        name = ln_list[j]
        name = single_get_first(name) + name  # 获取中文首字母
        name = name.replace('/',' ')
        # print(ln_list[j])
        # exit()
        try:
            creatpdf(name)
        except Exception:
            pass
        z = str(i - 73)
        end = "第"+z+"条完成"
        print(end)



def creatpdf(name):
    path="C:\\Users\\admin\\Desktop\\k课表\\2020第二学期课表\\l老师课表"+"\\"+name+".pdf"
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建pdf
        pdfkit.from_file("teacher.html", path)
    else:
        pass

def single_get_first(unicode1):     #获取中文首字母
    str1 = unicode1.encode('gbk')
    try:
        ord(str1)
        return str1.decode('gbk')
    except:
        asc = str1[0] * 256 + str1[1] - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''

if __name__ == "__main__":  # 当程序执行时
    # 调用函数
    main()
    # print("爬取完毕！")