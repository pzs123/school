#-*- codeing = utf-8 -*-
#!Time : 2021/5/3 18:53
#@File : spider.py
#@Software : PyCharm



from bs4 import BeautifulSoup      #网页解析·获取数据
import xlwt     #进行excel操作
import requests
from lxml import etree
from requests.packages import urllib3
urllib3.disable_warnings()

def main():

    #输入点击“成绩查询”后的信息（url,cookie,referer）
    #修改（1）
    baseurl = "https://jwxt-zust-edu-cn.ez.zust.edu.cn/xscjcx.aspx?xh=1180220014&xm=%E6%BD%98%E4%B8%AD%E5%B1%B1&gnmkdm=N121605"

    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "历年成绩.xls"
    #3.保存数据
    saveData(datalist,savepath)


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

        #修改（2）
        "Cookie":"UM_distinctid=1793166fa3a78-0f93a1699455de-d7e1739-144000-1793166fa3baa8; iPlanetDirectoryPro=AQIC5wM2LY4Sfcx7MatvuR%2FDJoig%2B7jDscyn25JJ5ssYSjU%3D%40AAJTSQACMDI%3D%23; ezproxy=AIcAzpjpPBeYfou; ezproxyl=AIcAzpjpPBeYfou; ezproxyn=AIcAzpjpPBeYfou; ASP.NET_SessionId=2okjzn3ljh45zb555ef5qfar",
        "Referer": "https://jwxt-zust-edu-cn.ez.zust.edu.cn/xs_main_zzjk1.aspx?xh=1180220014&type=1",
    }
                     #用户代理
    S = requests.session()
    cj_html_1 = S.get(url,headers=header,verify=False)
    # print(cj_html_1.text)
    soup = BeautifulSoup(cj_html_1.text,'lxml')
    #print(soup)
    value3 = soup.find('input',attrs={'name':'__VIEWSTATE'})['value']
    # print(value3)
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
    request = requests.session().post(url=url,headers=header,data=data,verify=False)
    html = request.text
    #print(html)

    return html


def saveData(datalist,savepath):
    print("save...")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建working对象
    sheet = book.add_sheet('历年成绩',cell_overwrite_ok=True)    #创建工作表
    col = ("学年","学期","课程代码","课程名称","课程性质","课程归属","学分","绩点","成绩","辅修标记","补考成绩","重修成绩","开课学院","重修标记")
    for i in range(0,14):
        sheet.write(0,i,col[i]) #列名
    k=0
    for i in range(0,int(len(datalist)/13)):
        print("第%d条"%(i+1))
        for j in range(0,13):
            sheet.write(i+1,j,datalist[k])      #数据
            k = k + 1
    book.save(savepath)       #保存
if __name__ == "__main__" :  #当程序执行时
#调用函数
    main()
    print("爬取完毕！")