#-*- codeing = utf-8 -*-

import pdfkit
import requests
import os
import re

def main():
    pdfkit.from_file("j教务处动态.html", "C:\\Users\\asus\\Desktop\\a.pdf")


if __name__ == "__main__" :  #当程序执行时
#调用函数
    main()