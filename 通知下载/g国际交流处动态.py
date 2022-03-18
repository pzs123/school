# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 19:37:46 2021

@author: admin
"""

import requests
from lxml import etree
import pdfkit
import os
import sys


# 修改输入验证码后的cookie
def main():
    m = -1
    Baseurl = ["https://io.zust.edu.cn/tzgg.htm"]
    Path = ["C:\\Users\\asus\\Desktop\\t通知\\g国际交流处动态"]
    cookie = "UM_distinctid=17647d79cde142-038e9382db91a6-3b3d5203-e1000-17647d79cdf4ba; iPlanetDirectoryPro=AQIC5wM2LY4SfcxSUyn83uGL2j%2Ffa5YDFfY7FZxFKDcbfCc%3D%40AAJTSQACMDE%3D%23; JSESSIONID=243CB4A72E1BB68B6E47359DBF985935"
    for baseurl in Baseurl:
        m = m + 1  # 获取Path
        # 1.爬取网页
        # print(html)
        # for i in range(5, 0, -1):  # 调用获取页面信息的函数·5次（可更新）
        DATE = []
        head = []
        URL = []
        li_list = []
        lm_list = []
        ln_list = []
        delete = []

        url = baseurl
        # url = "https://xsc.zust.edu.cn/tzgg/"+str(i)+".htm"
        html = askURL(url)  # 保存获取到的网页源码
        # print(html)
        # 2.逐一解析数据
        tree = etree.HTML(html)
        for z in range(0, 10):
            xpathtime = '//*[@id="line_u4_' + str(z) + '"]/span/text()'
            xpathtitle = '//*[@id="line_u4_' + str(z) + '"]/a/div//text()'
            xpathurl = '//*[@id="line_u4_' + str(z) + '"]/a/@href'
            ln_list.append(tree.xpath(xpathtime)[0])  # 时间
            li_list.append(tree.xpath(xpathtitle)[0])  # 标题
            lm_list.append(tree.xpath(xpathurl)[0])  # 网址
        # print(lm_list)
        # sys.exit()

        for a in range(0, len(lm_list)):
            if (len(lm_list[a]) > 30):
                delete.append(a)  # 记录需要删除的元素

        for x in delete:  # 删除
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
            ln_list[j] = ln_list[j].replace("/", "-")
            if li_list[k][0].isdigit():  # 判断标题第一个字符是否为数字
                li_list[k] = " " + li_list[j]
            li_list[k] = li_list[k].rstrip()  # 去除标题最后的空格
            data = str(ln_list[j]) + str(li_list[k])  # 时间+标题
            head.append(data)  # 加入列表
            k = k + 1
            j = j + 1
            # print(data)
        # print(head)
        # sys.exit()
        z = 0
        while z < len(lm_list):  # 网址
            w = lm_list[z]
            w = w.replace("..", "")
            w = "https://io.zust.edu.cn/" + w  #
            URL.append(w)
            z = z + 1

        DATE.append(head)
        DATE.append(URL)
        # print(DATE)
        # sys.exit()

        n = 0
        while n < len(DATE[1]):
            title = DATE[0][n]
            title = title.replace('/', ' ')  # 标题中"/"换成空格
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
        pdfkit.from_file("g国际交流处动态.html", path)
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
    # sys.exit()
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
    html = html.replace('''    								<li><a class="go" href="../../index.htm" title="网站首页">网站首页</a>

			  </li>
				<li class="s">|</li>
				<li><a class="go" href="../../gywm/gzzz.htm" title="关于我们">关于我们</a>
				<blockquote><div class="ChildNavIn">
<a class="First " href="../../gywm/gzzz.htm">工作职责</a>
<a class="First " href="../../gywm/jgsz.htm">机构设置</a>
</div></blockquote>
			  </li>
				<li class="s">|</li>
				<li><a class="go" href="../../tzgg.htm" title="通知公告">通知公告</a>

			  </li>
				<li class="s">|</li>
				<li><a class="go" href="../../gzdt.htm" title="工作动态">工作动态</a>

			  </li>
				<li class="s">|</li>
				<li><a class="go" href="../../bszn/jzgygcg.htm" title="办事指南">办事指南</a>
				<blockquote><div class="ChildNavIn">
<a class="First " href="../../bszn/jzgygcg.htm">教职工因公出国</a>
<a class="First " href="../../bszn/pqwzwj.htm">聘请外专外教</a>
<a class="First " href="../../bszn/xscg_j_.htm">学生出国（境）</a>
<a class="First " href="../../bszn/gjxshy.htm">国际学术会议</a>
</div></blockquote>
			  </li>
				<li class="s">|</li>
				<li><a class="go" href="../../gjhz/hzgk.htm" title="国际合作">国际合作</a>
				<blockquote><div class="ChildNavIn">
<a class="First " href="../../gjhz/hzgk.htm">合作概况</a>
<a class="First " href="../../gjhz/hzyx/oz.htm">合作院校</a>
<a class="First " href="../../gjhz/hzxm/xsjl.htm">合作项目</a>
<a class="First " href="../../gjhz/zwhzbx/zdgcsxy.htm">中外合作办学</a>
<a class="First " href="../../gjhz/gjhzy.htm">国际化专业</a>
</div></blockquote>
			  </li>
				<li class="s">|</li>
				<li><a class="go" href="../../gathz/hzgk.htm" title="港澳台合作">港澳台合作</a>
				<blockquote><div class="ChildNavIn">
<a class="First " href="../../gathz/hzgk.htm">合作概况</a>
<a class="First " href="../../gathz/hzyx.htm">合作院校</a>
<a class="First " href="../../gathz/hzxm.htm">合作项目</a>''',''' ''')
    # print(html)
    # sys.exit()
    with open('g国际交流处动态.html', 'w', encoding='utf-8') as fp:
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
        "Cookie": "UM_distinctid=1754e1c5a0b2e9-05f42278cc4a65-c781f38-144000-1754e1c5a0c95e; JSESSIONID=150C9A493A52C49B1D2B8CF49CEAC07C"
    }
    request = requests.session().get(url=url, headers=header)
    with open(path + "\\" + name, 'wb') as fp:
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
