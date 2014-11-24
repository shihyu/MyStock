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

    regex = re.compile('<td[\S\s]*?>(\w+|[0-9]+\.[0-9]+]*|[0-9]+\,[0-9]*|\-[0-9]+\.[0-9]+]*|\-\d+|\-)<\/td>')
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

    print '\n'
    print dict_['股票名稱']
    print '\n'

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

    #print sum / float(Dividends_year)
    return sum


def TWSE(dict_):
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

    dict_['歷年股價資訊'] = reversed_list

def PBR(data_dict):
    StockAssetsStatus_list = data_dict['資產負債狀況']
    TWSE_list = data_dict['歷年股價資訊']

    # BPS（每股凈值產=凈資產/股票數）
    # 如果BPS>股票價格，那么這個股票就可以買，相反就不能買。
    print '股價淨值比(PBR) = 股價 / BSP(每股淨值)\n'

    tmp_list = []
    for row in StockAssetsStatus_list:
        if re.match(r'\d{4}', str(row[0])):
            tmp_list.append(row)

    for row in tmp_list:
        print row

    if len(tmp_list) >= 10 and len(TWSE_list) >= 10:
        year = 10
    else:
        if len(tmp_list) > len(TWSE_list):
            year = len(TWSE_list)
        else:
            year = len(tmp_list)


    print year

    print '\n'
    for row in TWSE_list:
        print row
    
    #for row in StockAssetsStatus_list:
        #print row[7]

    print '\n'
    sum = 0
    for i in range(0, year):
        print('%s / %s = %f' % (TWSE_list[i][6], tmp_list[i][7],float(TWSE_list[i][6]) / float(tmp_list[i][7]) ))
        sum += float(TWSE_list[i][6]) / float(tmp_list[i][7])

    print '\n'
    print "股價淨值比%f" % (sum / float(year))

def PER(data_dict):
    print "\nPER"
    Profit_list = data_dict['績效']
    TWSE_list = data_dict['歷年股價資訊']

    tmp_list = []
    for row in Profit_list:
        if re.match(r'\d{4}', str(row[0])):
            tmp_list.append(row)

    for row in tmp_list:
        print row

    if len(tmp_list) >= 10 and len(TWSE_list) >= 10:
        year = 10
    else:
        if len(tmp_list) > len(TWSE_list):
            year = len(TWSE_list)
        else:
            year = len(tmp_list)

    print year 

    cheap_sum = 0
    expensive_sum = 0
    nominal_sum = 0
    eps_sum = 0

    for i in range(0, year):
        #print TWSE_list[i][6] + " / " + tmp_list[i][6] 
        print('%s / %s = %f' % (TWSE_list[i][6], tmp_list[i][6], float(TWSE_list[i][6]) / float(tmp_list[i][6])))
        #print('%s / %s +' % (TWSE_list[i][6], tmp_list[i][6]))
        #print ('%f +' % (float(tmp_list[i][6])))
        eps_sum += float(tmp_list[i][6])
        #print float(TWSE_list[i][6]) / float(tmp_list[i][6])
        cheap_sum += float(TWSE_list[i][6]) / float(tmp_list[i][6]) # 便宜價
        expensive_sum += float(TWSE_list[i][4]) / float(tmp_list[i][6]) # 昂貴價
        nominal_sum += float(TWSE_list[i][8]) / float(tmp_list[i][6]) # 平均價

    print '\n'
    print eps_sum
    print cheap_sum / float(year)
    print expensive_sum / float(year)
    print nominal_sum / float(year)


def historical_prices(data_dict):
    TWSE_list = data_dict['歷年股價資訊']

    if len(TWSE_list) >= 10:
        year = 10
    else:
        year = len(TWSE_list)

    cheap_sum = 0
    expensive_sum = 0
    nominal_sum = 0

    for i in range(0, year):
        cheap_sum += float(TWSE_list[i][6]) # 便宜價
        expensive_sum += float(TWSE_list[i][4]) # 昂貴價
        nominal_sum += float(TWSE_list[i][8]) # 平均價

    print '\n'
    print cheap_sum/ float(year)
    print expensive_sum / float(year)
    print nominal_sum / float(year)


def main():
    fin = open('StockCode', 'r+')
    StockCodeList = [str(i)for i in fin.read().splitlines()]
    fin.close()

    page = GetHtmlcode('2103')
    dict_ = parse_stock(page)
    TWSE(dict_)

    pasre_stock_value(dict_)
    PBR(dict_)
    PER(dict_)
    historical_prices(dict_)

if __name__ == "__main__":
    main()
