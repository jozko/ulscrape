# -*- coding: utf-8 -*-
import httplib2
from bs4 import BeautifulSoup
import re
import sys
import os
import shutil
import urllib2
import argparse

UL_BASE_URL = 'http://www.uradni-list.si/uradni-list?year='
UL_YEAR_URL = 'http://www.uradni-list.si/1?year=%s&edition=%s'
DLPATH = '/tmp'
OPTIONS = []
DLPDFS = []

# Get UL page, decide based on number of params.
# Also returns response code, you can get it as
# get_html(UL_BASE_URL, YEAR)[1]['status'] if i
# you need it. Will always get you 200 methinks.
def get_html(*args):
    html = httplib2.Http()
    if len(args) == 2:
        status, response = html.request(args[0] + args[1])
    if len(args) == 3:
        status, response = html.request(args[0] % (args[1], args[2]))
    return response, status

def fetch_file(url, basepath):
    fname = url.split('/')[-1]
    fpath = os.path.join(basepath, fname)
    print "Downloading %s to %s " % (url, fpath)
    req = urllib2.urlopen(url)
    with open(fpath, 'wb') as fp:
        shutil.copyfileobj(req, fp)

# Get base html for year, to parse option values for all publications
# for that particular year. If you use 0000 as year, you'll get ALL
# ever published documents, from year 1991 to lastest. Weird stuff.
# After some parsing of base html docs, it will start downloading PDF files.

def parse_ul(*args):
    YEAR = str(args[0])
    ulhtml = get_html(UL_BASE_URL, YEAR)[0]
    soup = BeautifulSoup(ulhtml)

    # Get all UL publication codes into one list
    for option in soup.find_all('option'):
        if re.match('\d+', option.get('value')):
            OPTIONS.append(option.get('value'))

    # Then request each release sub page, scrape
    # _pdf URLs from it and put it into one list.
    for item in OPTIONS:
            print 'Will fetch pdfs from ' + UL_YEAR_URL % ( YEAR, item )
            raw = get_html( UL_YEAR_URL, YEAR, item )
            ulpdfs = raw[0]
            a = BeautifulSoup(ulpdfs)
            # Use BS4 to extract all links, check for ones containing _pdf
            # and append everything to one big, happy list.
            for link in a.find_all('a'):
                if link.get('href') and '_pdf' in link.get('href'):
                    DLPDFS.append(link.get('href'))
    # Now get rid of duplicates using set over big, happy list
    # And show some numbers, so people are not bored while waiting for files
    uniqpdfs = set(DLPDFS)
    print 'Number of UL publications in year %s is: %s' % ( YEAR, str(len(OPTIONS)) )
    print 'Number of PDF files to download: %s' % ( str(len(uniqpdfs)) ) 

    # And one last for loop over set list, to actually download PDF files
    for pdf in uniqpdfs:
        url = 'http://www.uradni-list.si%s' % (pdf)
        filedir = os.path.join(DLPATH, YEAR)
        fetch_file(url, filedir)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Enter year of UL publications you wish to download')
    parser.add_argument('--year', '-y', type=int, help='Year of UL publication, starting with 1991 (oldest) and ending with current year. You can also get all published documents using 0 as a year argument')
    args = parser.parse_args()
    ayear = str(args.year)

    if re.match('\d{4}', ayear):
        print UL_BASE_URL + ayear
        parse_ul(ayear)
    elif re.match('0', ayear):
        print UL_BASE_URL + '0000'
        parse_ul('0000')
    else:
        print '''%s is not a valid year, is it? 
        Use -h to get some help...''' % ayear

