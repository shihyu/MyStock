#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import csv

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

def split_html_tags(tables, list_):
    #print tables.encode('utf-8')
    #print tables
    regex = re.compile("<tr align='center'[\s\S]*?<\/tr>")
    datarow = regex.findall(tables)
    #print datarow
    #print len(datarow)
    datarow = datarow[1:]
    str_convert = ''.join(datarow)

    string = str_convert.strip()
    #print string

    regex = re.compile('<td[\S\s]*?>(\w+|[0-9]+\.[0-9]+]*|[0-9]+\,[0-9]*)<\/td>')
    data = regex.findall(string)

    #print data

    for i in data:
        list_.append(i)


def group_list(l,block):
    size = len(l)
    return [l[i:i+block] for i in range(0,size,block)]

def parse_stock(page):
    regex = re.compile("\<title\>(.*)\<\/title\>")
    title = regex.findall(page)[0]
    title = title[:title.find('-')].strip()
    #print title

    regex = re.compile('<table[\s\S]*?<\/table>')
    #print page
    datatable = regex.findall(page)
    #print datatable
    #print len(datatable)

    data_dict = {}
    Profit_list = []
    Dividends_list = []
    StockAssetsStatus_list = []
    list_ = []

    for l in datatable:
        if l.find(u"\u5408&nbsp;\u4f75&nbsp;\u7372&nbsp;\u5229&nbsp;\u72c0&nbsp;\u6cc1") != -1:
            split_html_tags(l, Profit_list)
        elif l.find(u'\u8fd1&nbsp;10&nbsp;\u5e74&nbsp;\u80a1&nbsp;\u5229&nbsp;\u653f&nbsp;\u7b56') != -1:
            #print l
            split_html_tags(l, Dividends_list)
        elif l.find(u'\u5408\u4f75\u8cc7\u7522\u8ca0\u50b5\u72c0\u6cc1') != -1:
            #print l
            split_html_tags(l, StockAssetsStatus_list)

    #print StockAssetsStatus_list

    Dividends_list = group_list(Dividends_list, 4)
    Profit_list = group_list(Profit_list, 7)
    StockAssetsStatus_list = group_list(StockAssetsStatus_list, 8)

    for i in Dividends_list:
        print i

    print '\n'

    for i in Profit_list:
        print i
    print '\n'
        
    for i in StockAssetsStatus_list:
        print i
    print '\n'
    
    data_dict['股票名稱'] = title
    data_dict['股利'] = Dividends_list
    data_dict['績效'] = Profit_list
    data_dict['資產負債狀況'] = StockAssetsStatus_list

    #print data_dict['績效']

    #list_.append(Dividends_list)
    #list_.append(Profit_list)
        
    return data_dict

# 計算出股票價值 五年的現金值利率 每股淨值 ROE 毛利率
def pasre_stock_value(dict_):

    print dict_['股票名稱']
    Dividends_list = []

    Dividends_list = dict_['股利']
    
    if len(Dividends_list) >= 5:
        Dividends_year = 5
    else:
        Dividends_year = len(Dividends_list)

    #print Dividends_list
    sum = 0.0
    # 計算五年股利平均
    for i in range(0, Dividends_year):
        #print float(Dividends_list[i][3])
        sum += float(Dividends_list[i][3])  

    print sum / float(Dividends_year)
    print '\n'

    return sum


def TWSE():
    TWSEURL = 'http://www.twse.com.tw/ch/trading/exchange/FMNPTK/FMNPTK2.php?STK_NO=2103&myear=2014&mmon=09&type=csv'
    tmp_list = []
    reversed_list = []

    for line in urllib2.urlopen(TWSEURL).readlines():
        if re.match(r'^\d+\,\".*"\,.*\,"', line.strip()):
            tmp_list.append(line)

    for i in csv.reader(tmp_list):
        reversed_list.append(i)

    reversed_list = reversed_list[::-1]
    for i in reversed_list:
        print i

    return reversed_list

def PBR(TWSE_list, data_dict):
    StockAssetsStatus_list = data_dict['資產負債狀況']

    print '\n'

    for row in StockAssetsStatus_list:
        if re.match(r'\d{4}', str(row[0])):
            print row

    #for row in TWSE_list:
        #print row[6] 
    
    #for row in StockAssetsStatus_list:
        #print row[7]


def main():
    fin = open('StockCode', 'r+')
    StockCodeList = [str(i)for i in fin.read().splitlines()]
    fin.close()

    page = GetHtmlcode('2103')
    dict_ = parse_stock(page)
    pasre_stock_value(dict_)
    list_ = TWSE()
    PBR(list_, dict_)

if __name__ == "__main__":
    main()
