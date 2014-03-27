#! /usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import datetime
from datetime import date, timedelta as td
from pprint import pprint
import operator

TotalStockInfoList = []

def GetHtmlcode(ID):
    # Get the webpage's source html code
    source = 'http://www.goodinfo.tw/stockinfo/StockDividendSchedule.asp?STOCK_ID='
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
    result = response.read().decode("utf8")
    #print result
    return result

def GetStockCurrentInfo(page):
    infolist =['股票名稱',
               '資料日期',
               '成交價',
               '漲跌價',
               '漲跌幅',
               '昨收',
               '開盤價',
               '最高價',
               '最低價']

    # Print Out the result
    data_dict = {}

    regex = re.compile("\<title\>(.*)\<\/title\>")
    datatable = regex.findall(page)[0]
    #print type(datatable)
    data_dict[infolist[0]] = datatable 
    #print datatable

    regex = re.compile(":\s+([0-9][0-9]\/[0-9][0-9])\<")
    datatable = regex.findall(page)[0]
    #print type(datatable)
    data_dict[infolist[1]] = datatable 

    # Get the data <table></table>
    regex = re.compile("(<table class='std_tbl' border='0'.+\s+.*\s+.*\s+.*<\/table>)")
    datatable = regex.findall(page)[0]
    #print datatable
    #raw_input()

    # Get the data row <tr></tr>
    regex = re.compile("<tr align='center'.*</tr>")
    datarow = regex.findall(datatable)
    string = datarow[0].strip()

    # Special operation on empty data cell
    string = string.replace("</td>"," ")
    #print string

    # Get each data <td></td>
    datalist = string.split('</tr>')
    #print datalist[1]

    regex = re.compile(">(\S+)")
    datatable = regex.findall(datalist[1])
    #print datatable

    for num, item in enumerate(datatable):
        #print item
        data_dict[infolist[num+2]] = item.strip()

    return data_dict

def GetStockHistoryInfo(page):
    infolist =['盈餘所屬年度',
               '股利發放年度',
               '股東會日期',
               '除息交易日',
               '除息參考價（元）',
               '除權交易日',
               '除權參考價（元）',
               '股利發放年度之股價統計：最高',
               '股利發放年度之股價統計：最低',
               '股利發放年度之股價統計：年均',
               '現金股利：盈餘',
               '現金股利：公積',
               '現金股利：合計',
               '股票股利：盈餘',
               '股票股利：公積',
               '股票股利：合計',
               '股利合計',
               '年均殖利率（%）']

    # Get the data <table></table>
    regex = re.compile("<table class='std_tbl' width='100%'.*<\/table>")
    datatable = regex.findall(page)[0]
    #print type(datatable)

    # Get the data row <tr></tr>
    regex = re.compile("<tr bgcolor=.*</tr>")
    datarow = regex.findall(datatable)
    string = datarow[0].strip()

    # Clean data row
    cleanlist = ["<nobr>", " align='right'", "</nobr>"]
    for target in cleanlist:
        string = string.replace(target,'').strip(' ')

    # Special operation on empty data cell
    string = string.replace("</td>"," ")
        
    # Get each data <td></td>
    datalist = string.split('</tr>')

    # Print Out the result
    data_dict = {}

    for item in datalist[:-1]:
        #print item
        if u'股' in item or u'權' in item:
            continue
        
        rowlist = item.split('<td>')[1:]
        #print rowlist
        newrowlist = {}
        for num,item in enumerate(rowlist):
            newrowlist[infolist[num]] = item.strip()
            #print infolist[0]
            #print newrowlist[infolist[0]]
            #raw_input()
            data_dict[rowlist[1].strip()] = newrowlist
    return data_dict

def OutputToHtml():
    '''
    for item in TotalStockInfoList:
        print type(item[0])
        print type(item[1])
        print type(item[2])
        print type(item[3])
        print type(item[4])
        print type(item[5])
        print type(item[6])
    '''
    with open('myStockpage.html', 'w') as myFile:
        myFile.write('<html>')
        myFile.write('<head>')
        myFile.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8">')
        myFile.write('<title>MyStock</title>')
        myFile.write('</head>')
        myFile.write('<body>')
        myFile.write('<table style="text-align: left; height: 30px; width: 876px;" border="1" cellpadding="2" cellspacing="2">')
        myFile.write('<tbody>')
        myFile.write('<tr>')
        myFile.write('<td style="background-color: rgb(102, 255, 255); text-align: center; width: 117px;">名 稱</td>')
        myFile.write('<td style="background-color: rgb(102, 255, 255); text-align: center; width: 117px;">日 期</td>')
        myFile.write('<td style="background-color: rgb(102, 255, 255); text-align: center; width: 117px;">成 交價</td>')
        myFile.write('<td style="background-color: rgb(102, 255, 255); text-align: center; width: 117px;">合 理價</td>')
        myFile.write('<td style="background-color: rgb(51, 255, 51); text-align: center; width: 117px;">低 價</td>')
        myFile.write('<td style="background-color: rgb(255, 0, 0); text-align: center; width: 117px;">高 價</td>')
        myFile.write('<td style="background-color: rgb(255, 153, 255); text-align: center; width: 117px;">五 年平均股利</td>')
        myFile.write('<td style="background-color: rgb(255, 102, 0); text-align: center; width: 117px;">殖利率</td>')
        myFile.write('</tr>')

        for item in TotalStockInfoList:
            myFile.write('<tr>')
            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % item[0].encode('utf8'))
            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % item[1].encode('utf8'))
            if float(item[2].encode('utf8')) >= float(item[5]):
                myFile.write('<td style="width: 117px; text-align: center;color: rgb(255, 0, 0);">%s</td>' % item[2].encode('utf8'))
            elif float(item[2].encode('utf8')) <= float(item[4]):
                myFile.write('<td style="width: 117px; text-align: center;color: rgb(0, 255, 0);">%s</td>' % item[2].encode('utf8'))
            else:
                myFile.write('<td style="width: 117px; text-align: center;color: rgb(0, 0, 0);">%s</td>' % item[2].encode('utf8'))

            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % str(item[3]))
            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % str(item[4]))
            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % str(item[5]))
            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % str(item[6]))
            myFile.write('<td style="width: 117px; text-align: center;">%s</td>' % str(item[7]))
            myFile.write('</tr>')

        myFile.write('</tbody>')
        myFile.write('</table>')
        myFile.write('</body>')
        myFile.write('</html>')

def StatisticsStockInfo(StockHistory_dict, StocCurrent_dict):
    StockInfoList = []
    keylist = StockHistory_dict.keys()
    keylist = sorted(keylist,reverse = True)

    sum = 0
    for  num, year in  enumerate(keylist):
        if (num < 5):
            sum += float((StockHistory_dict[str(year)])['股利合計'])
            #print (StockHistory_dict[str(year)])['股利合計']
        else:
            break

    five_price = sum / 5.0
    StockName = StocCurrent_dict['股票名稱'] 
    
    StockInfoList.append(StockName[:len(StockName)-29])
    StockInfoList.append(StocCurrent_dict['資料日期'])
    StockInfoList.append(StocCurrent_dict['成交價'])
    StockInfoList.append(five_price * 20)
    StockInfoList.append(five_price / 0.0625)
    StockInfoList.append(five_price / 0.03125)
    StockInfoList.append(five_price)
    #print type(five_price)
    #print type(float(StocCurrent_dict['成交價'].encode('utf8')))
    #raw_input()
    StockInfoList.append(round((five_price / float(StocCurrent_dict['成交價'].encode('utf8'))) * 100.0, 2))

    TotalStockInfoList.append(StockInfoList)

    '''
    print " 代碼   名稱    資料日期  成交價   合理價     低價      高價        五年平均股利"
    print StockName[:len(StockName)-29] , "  "\
          , StocCurrent_dict['資料日期'] , "   "\
          , StocCurrent_dict['成交價'] , "   "  \
          , five_price * 20  , "   "            \
          , five_price / 0.0625 , "   "         \
          , five_price / 0.03125, "   " \
          , five_price
    '''

def main():
    fin = open('StockCode', 'r+')
    StockCodeList = [str(i)for i in fin.read().splitlines()]
    fin.close()
    #print StockCodeList

    for ID in StockCodeList:
        #print ID
        # ID setting
        # ID = '2412'
        page = GetHtmlcode(ID)
        StockHistory_dict = GetStockHistoryInfo(page)
        StocCurrent_dict = GetStockCurrentInfo(page)
        #pprint(StockHistory_dict)
        StatisticsStockInfo(StockHistory_dict, StocCurrent_dict)

    #print TotalStockInfoList
    TotalStockInfoList.sort(key=operator.itemgetter(7), reverse=True)

    OutputToHtml()

if __name__ == "__main__":
    main()

