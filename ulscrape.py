import httplib2
from bs4 import BeautifulSoup
import re
import sys
import os
import shutil

UL_BASE_URL = 'http://www.uradni-list.si/uradni-list?year='
UL_YEAR_URL = 'http://www.uradni-list.si/1?year=%s&edition=%s'
YEAR = sys.argv[1]
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
        print args[0] + args[1]
    if len(args) == 3:
        status, response = html.request(args[0] % (args[1], args[2]))
        print args[0] % (args[1], args[2])
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
# Note to self - this to __main__
ulhtml = get_html(UL_BASE_URL, YEAR)[0]
soup = BeautifulSoup(ulhtml)

# Get all UL publication codes into one list
for option in soup.find_all('option'):
    if re.match('\d+', option.get('value')):
        OPTIONS.append(option.get('value'))

# Then request each release sub page, scrape
# _pdf URLs from it and put it into one list.
for item in OPTIONS:
        print 'Downloading pdfs from ' + UL_YEAR_URL % ( YEAR, item )
        raw = get_html( UL_YEAR_URL, YEAR, item )
        ulpdfs = raw[0]
        #print ulpdfs
        print item
        print 'Response status code is ' + raw[1]['status']
        a = BeautifulSoup(ulpdfs)
        for link in a.find_all('a'):
            if link.get('href') and '_pdf' in link.get('href'):
                print (link.get('href'))
                DLPDFS.append(link.get('href'))
        #    print 'Stevilo PDF datotek za download je: ' + str(len(DLPDFS))
        #    print DLPDFS
#        pdf = 'http://www.uradni-list.si%s' % b[0]
#        print pdf
#        urlgrab(pdf)
print 'Stevilo zadetkov je: ' + str(len(OPTIONS))
print 'Stevilo PDF datotek za download je: ' + str(len(DLPDFS))

def get_pdfs(pdflist):
    uniqpdfs = set(pdflist)
    for pdf in uniqpdfs:
        url = 'http://www.uradni-list.si%s' % (pdf)
        filedir = os.path.join(DLPATH, YEAR)
        fetch_file(url, filedir)
        
d = set(DLPDFS)
print (len(d))
#print DLPDFS
for i in d:
    print i
#sys.exit()
