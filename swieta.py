#-*- coding: utf-8 -*-

import urllib2
import sys
import datetime
import HTMLParser
from BeautifulSoup import BeautifulSoup
import StringIO
import gzip
opady = {
         }

if __name__=="__main__":
    if len(sys.argv)<3:
        print "Usage: ",sys.argv[0],"year_from year_to"
        sys.exit(1)
    year_from = int(sys.argv[1])
    year_to = int(sys.argv[2])
    url = "http://www.kalendarzswiat.pl/swieta/wolne_od_pracy/"
    

    holidays = {}
    parser = HTMLParser.HTMLParser() 
    for y in range(year_to-year_from+1):
        u = url+str(year_from+y)
        resp = urllib2.urlopen(u)
        if resp.info().get('Content-Encoding')=='gzip':
            
            buf = StringIO.StringIO( resp.read())
            r = gzip.GzipFile(fileobj=buf).read()
        else:
            r = resp.read()
        html = r.decode('utf-8')
        html = parser.unescape(html)
        
        page = BeautifulSoup(html)
        
        table = page.findAll('table', {'class':'tab_easy'})[0]
        rows = table.findAll('tr')
        
        for row in rows:
            tds = row.findAll('td')
            if tds:
                try:
                    date = datetime.datetime.strptime(tds[0].div.a['data-date'],'%b. %d, %Y')
                except:
                    date = datetime.datetime.strptime(tds[0].div.a['data-date'],'%B %d, %Y')
                name = tds[1].text
                holidays[date.strftime('%Y-%m-%d')] = name.encode('utf-8')
                
    
    print holidays
    
    f = open('swieta.log','w')
    import json
    x = json.dumps(holidays,sort_keys=True,indent=4, separators=(',', ': '))
    print x
    print type(x)
    f.write(x.encode('utf-8'))
    f.close()
                
                
        
        