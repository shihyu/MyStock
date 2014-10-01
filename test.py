# -*- coding: utf-8 -*-
import urllib2
import csv
import re

TWSEURL = 'http://www.twse.com.tw/ch/trading/exchange/FMNPTK/FMNPTK2.php?STK_NO=2103&myear=2014&mmon=09&type=csv'

for row in csv.reader(urllib2.urlopen(TWSEURL).readlines()):
    print row
