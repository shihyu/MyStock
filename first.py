#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2

def GetHtmlcode(ID):
    # Get the webpage's source html code
    source = 'http://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID='
    url = source + ID

    # Header
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Charset' : 'Big5,utf-8;q=0.7,*;q=0.3',
                #'Accept-Encoding' : 'gzip,deflate,sdch',
                'Accept-Language' : 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2' ,
                'Cache-Control' : 'max-age=0',
                'Connection' : 'keep-alive',
                'Cookie' : '427 bytes were stripped',
                'Host' : 'www.goodinfo.tw',
                'Referer' : url }

    # 連到網頁抓取資料
    req= urllib2.Request(url,"",headers)
    response = urllib2.urlopen(req)
    result = response.read().decode('utf-8')
    #print result
    return result


def main():
    fin = open('StockCode', 'r+')
    StockCodeList = [str(i)for i in fin.read().splitlines()]
    fin.close()
    #print StockCodeList
    page = GetHtmlcode('2498')
    #print type(page)
    #print page.encode('utf-8')

    regex = re.compile('<table[\s\S]*?<\/table>')
    datatable = regex.findall(page)


    #print len(datatable)

    tables = []

    for l in datatable:
        #if l.find(u"獲　利　狀　況") != -1:
        if l.find(u"\u8fd1&nbsp;10&nbsp;\u5e74&nbsp;\u80a1&nbsp;\u5229&nbsp;\u653f&nbsp;\u7b56") != -1 or \
           l.find(u'\u7372\u3000\u5229\u3000\u72c0\u3000\u6cc1') != -1:
            tables.append(l)
            #print l.encode('utf-8')

    #print len(tables)

    regex = re.compile("<tr align='center'.*</tr>")

    for t in tables:
        datarow = regex.findall(t)
        string = datarow[0].strip()
        string = string.replace("</td>"," ")
        datalist = string.split('</tr>')
        print len(datalist)
        print datalist
       # regex = re.compile("<td>(\S+)")
        #data = regex.findall(datalist)
        #print data

if __name__ == "__main__":
    main()
