# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup  # 网页解析·获取数据
import requests
from lxml import etree
import pdfkit
import os
import sys

requests.packages.urllib3.disable_warnings()

def main():
    baseurl = "https://jwxt-zust-edu-cn.ez.zust.edu.cn/tjkbcx.aspx?xh=1180220014&xm=%E6%BD%98%E4%B8%AD%E5%B1%B1&gnmkdm=N121601"
    # 1.爬取网页
    getData(baseurl)

def creatpdf(title):
    path = "C:\\Users\\asus\\Desktop\\k课表\\2020第二学期课表\\z专业课表" + "\\" + title + '.pdf'
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建pdf
        pdfkit.from_file("专业课表.html",path)
    else:
        pass

def getData(baseurl):
    # data = []
    for i in range(0, 1):  # 调用获取页面信息的函数·1次
        url = baseurl
        askURL(url)  # 保存获取到的网页源码


def askURL(url):
    count = 0
    header={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'Cookie': 'UM_distinctid=177d706fc83ac1-05d89ec4f7becd-73e356b-144000-177d706fc84147; iPlanetDirectoryPro=AQIC5wM2LY4Sfczi04wrxPwbkNiBMmMDhLlhSwTQTkH25fw%3D%40AAJTSQACMDI%3D%23; ezproxy=Zd2AOI8OzGkj8kZ; ezproxyl=Zd2AOI8OzGkj8kZ; ezproxyn=Zd2AOI8OzGkj8kZ; ASP.NET_SessionId=qgmq4l55ncm3fmyuor2lwy3q',
        'Referer': 'https://jwxt-zust-edu-cn.ez.zust.edu.cn/xs_main.aspx?xh=1180220014',
        # 'Host': "jwxt-zust-edu-cn.ez.zust.edu.cn",
        # "Origin": "https://jwxt-zust-edu-cn.ez.zust.edu.cn",
    }
    # 用户代理
    cj_html_1 = requests.session().get(url=url, headers=header,verify=False)
    html = cj_html_1.text
    # print(html)
    # sys.exit()

    tree = etree.HTML(html)
    li_list = tree.xpath('//*[@id="zy"]/option/@value')  # 专业（号码）
    # print(li_list)
    # sys.exit()
    ln_list = ["2020", "2019", "2018", "2017"]  # 年级
    # print(ln_list)
    # sys.exit()

    soup = BeautifulSoup(cj_html_1.text, 'lxml')
    # print(soup)
    value3 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']  # 获取view
    # print(value3)
    # sys.exit()

    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": "",
        "xn": "2020-2021",
        "xq": "2",
        "nj": "2018",
        "xy": "02",
        "zy": "",
        "kb": "",
    }

    for z in range(0, len(li_list)):
        data["__VIEWSTATE"] = value3
        data["__EVENTTARGET"] = "zy"
        data["zy"] = li_list[z]
        # print(data)
        # sys.exit()

        html = requests.session().post(url=url, headers=header, data=data,verify=False).text  # 填写专业
        html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n' + html
        # print(html)
        # sys.exit()

        for m in range(0, 4):
            soup = BeautifulSoup(html, 'lxml')
            # print(soup)
            value3 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
            # print(value3)
            data["__VIEWSTATE"] = value3
            data["__EVENTTARGET"] = "nj"
            data["nj"] = ln_list[m]
            # print(ln_list[i])
            html = requests.session().post(url=url, headers=header, data=data,verify=False).text  # 年级
            html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n' + html
            # print(html)
            # sys.exit()

            tree = etree.HTML(html)
            lz_list = tree.xpath('//*[@id="kb"]/option/@value')  # 推荐课表(号码)
            # print(li_list)
            lm_list = tree.xpath('//*[@id="kb"]/option/text()')  # 推荐课表（专业班级名称）
            # print(lm_list)
            # sys.exit()
            i = -1
            classnum = []
            classname = []
            while lz_list[i]:
                classnum.append(lz_list[i])
                classname.append(lm_list[i])
                i = i - 1
            # print(classnum)
            # print(classname)
            # sys.exit()
            j = 0
            while len(classnum) > j:
                soup = BeautifulSoup(html, 'lxml')
                # print(soup)
                value3 = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
                # print(value3)
                data["__VIEWSTATE"] = value3
                data["__EVENTTARGET"] = "kb"
                data["kb"] = classnum[j]
                # print(li_list[i])
                html = requests.session().post(url=url, headers=header, data=data,verify=False).text  # 181班
                html = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n' + html
                # print(html)
                # sys.exit()
                with open('./专业课表.html', 'w', encoding='utf-8') as fp:
                    fp.write(html)

                title = classname[j]
                title = single_get_first(title) + title  # 获取中文首字母
                try:
                    creatpdf(title)
                except Exception:
                    pass
                count = count + 1
                end = "第" + str(count) + "条完成"
                print(end)
                j = j + 1

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
    print("爬取完毕！")