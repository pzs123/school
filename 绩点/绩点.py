#-*- codeing = utf-8 -*-
#@Time :  19:11
#@Author : 潘中山
#@File : 绩点.py
#@Software : PyCharm


from bs4 import BeautifulSoup      #网页解析·获取数据
import xlwt     #进行excel操作
import requests
import lxml
from lxml import etree

def main():
    baseurl = "http://jwxt.zust.edu.cn.ez.zust.edu.cn/xscjcx.aspx?xh=1180220014&xm=%E6%BD%98%E4%B8%AD%E5%B1%B1&gnmkdm=N121605"
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "绩点.xls"
    #3.保存数据
    saveData(datalist,savepath)
    #askURL("http://jwxt.zust.edu.cn.ez.zust.edu.cn/xscjcx.aspx?xh=1180220014&xm=%E6%BD%98%E4%B8%AD%E5%B1%B1&gnmkdm=N121605")



#爬取网页
def getData(baseurl):
    data = []
    for i in range(0,1):       #调用获取页面信息的函数·1次
        url = baseurl
        html = askURL(url)      #保存获取到的网页源码

        #2.逐一解析数据
        tree = etree.HTML(html)
        li_list = tree.xpath('//tr/td/text()')
        #print(li_list)
        for item in li_list[10:]:     #查找符合要求的字符串，形成列表
            # item = str(item)
            #print(item)    #测试
            data.append(item)                       #添加
            #datalist = datalist.append(data)
    #print(data)

    return data

#得到指定一个URL的网页内容
def askURL(url):
    header = {                #模拟浏览器头部信息·向服务器发送信息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "Cookie":"UM_distinctid=17433a3cde1172-0f5d4e594ae996-3323766-144000-17433a3cde27b5; iPlanetDirectoryPro=AQIC5wM2LY4Sfcw9iMCb1F63MLtBfFczeTVQnXAYf3xjaT0%3D%40AAJTSQACMDE%3D%23; ezproxy=F0h6ocGlQY9Jyb5; ezproxyl=F0h6ocGlQY9Jyb5; cookies=44785.4931.7938.0000; ASP.NET_SessionId=asauvx2rb5vgjk45hc2njr55",
        "Referer": "http://jwxt.zust.edu.cn.ez.zust.edu.cn/xs_main.aspx?xh=1180220014",
        # "Host": "jwxt.zust.edu.cn.ez.zust.edu.cn",
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "Accept-Encoding":"gzip, deflate",
        # "Accept-Language":"zh-CN,zh;q=0.9",
        # "Cache-Control":"max-age=0",
        # "Upgrade-Insecure-Requests":"1"

    }
                     #用户代理
    S = requests.session()
    cj_html_1 = S.get(url,headers=header)
    soup = BeautifulSoup(cj_html_1.text,'lxml')
    #print(soup)
    value3 = soup.find('input',attrs={'name':'__VIEWSTATE'})['value']
    #print(value3)
    data = {

        "__EVENTTARGET":"",
        "__EVENTARGUMENT":"",
        "__VIEWSTATE":"",
        "hidLanguage": "",
        "ddlXN":"",
        "ddlXQ":"",
        "ddl_kcxz":"",
        "btn_zcj": "%E5%8E%86%E5%B9%B4%E6%88%90%E7%BB%A9"

    }
    data["__VIEWSTATE"] = value3
    request = requests.session().post(url=url,headers=header,data=data)
    html = request.text
    #print(html)
    return html


def saveData(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建working对象
    sheet = book.add_sheet('绩点',cell_overwrite_ok=True)    #创建工作表
    col = ("课程名称","绩点")
    for i in range(0,2):
        sheet.write(0,i,col[i]) #列名
    k = 3
    for i in range(0,50):
        print("第%d条"%(i+1))
        for j in range(0,2):
            if j == 0:
                sheet.write(i+1,j,datalist[k])      #数据
                k = k + 4
            if j == 1:
                sheet.write(i + 1, j, datalist[k])  # 数据
                k = k + 9

    book.save(savepath)       #保存
if __name__ == "__main__" :  #当程序执行时
#调用函数
    main()
    #print("爬取完毕！")