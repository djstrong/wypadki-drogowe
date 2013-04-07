#-*- coding: utf-8 -*-

import urllib2
import sys
import datetime
import re
import HTMLParser
import csv

opady = {
         }

if __name__=="__main__":
    if len(sys.argv)<4:
        print "Usage: ",sys.argv[0],"city date_from date_to"
        sys.exit(1)
    date = datetime.datetime.strptime(sys.argv[2],"%Y-%m-%d")
    date_to = datetime.datetime.strptime(sys.argv[3],"%Y-%m-%d")
    city_url = "http://www.pogoda.ekologia.pl/Archiwum/Archiwum_pogody/"+sys.argv[1]+","
    

    weather = {}
    
    parser = HTMLParser.HTMLParser() 
    while date<=date_to:
        date_str = date.strftime("%Y-%m-%d")
        print date_str
        url = city_url+date_str
        
        resp = urllib2.urlopen(url)
        html = resp.read().decode('utf-8')
        html = parser.unescape(html) 
        weather[date_str] = {}
        w = weather[date_str]
        
        #wschod/zachod
        match = re.search(date_str+r',.*?([0-9]{2}:[0-9]{2}:[0-9]{2}).*?([0-9]{2}:[0-9]{2}:[0-9]{2})',html,re.MULTILINE | re.U)
        if match:
            w['wschod']=match.group(1)
            w['zachod']=match.group(2)
            
        
        #temperatura

        match = re.search(r'<td class="temperatura">(.*?)</td>',html,re.MULTILINE | re.U)
        if match:
            temp_range = match.group(1).split(u'÷')
            w['min_temp']=int(temp_range[0].strip())
            w['max_temp']=int(temp_range[1].strip())
            
        #cisnienie
        match = re.search(r'<td.*?class="cisnienie".*?>(.*?)</td>',html,re.MULTILINE | re.U)
        if match:
            w['cisnienie']=float(match.group(1).strip())
        
        match = re.search(r'<td.*?class="kierunek".*?>(.*?)<',html,re.MULTILINE | re.U)
        if match:
            w['wiatr[km/h]'] = float(match.group(1).strip())
            
        match = re.search(r'<td.*?class="opady".*?>(.*?)</td>',html,re.MULTILINE | re.U)
        if match:
            print "opady",match.groups()
            t = None
            val = None
            # czy sa podwojne:
            multiple =  re.findall(u'deszcz|śnieg',match.group(1),re.MULTILINE | re.U)
            if len(multiple)>1:
                splitted = [x.strip() for x in match.group(1).split('<br />') if x.strip()]
                for s in splitted:
                    print s
                    m = re.search(r'(\w+)\W+(.*)',s,re.MULTILINE | re.U)
                    if m:
                        t = m.group(1)
                        val = m.group(2)
                        val = re.search(r'[0-9]+(\.[0-9]+)?',val).group(0)
                        print "type,val",t,val
                        #w[t] = val
            else:
                if '<br' in match.group(1):
                    splitted = [x.strip() for x in match.group(1).split('<br />') if x.strip()]
                    if len(splitted)==2:
                        t = splitted[0]
                        val = re.search(r'[0-9]+-[0-9]+',splitted[1]).group(0)
                        #w[t] = v
                    elif len(splitted)==1:
                        m = re.search(r'(\w+)\W+(.*)',splitted[0],re.MULTILINE | re.U)
                        if m:
                            t = m.group(1)
                            val = m.group(2)
                            val = re.search(r'[0-9]+(\.[0-9]+)?',val).group(0)
                            print t,type(t)
                            #w[t]=val
            if t==u'śnieg':
                t = 'snieg'
            if t and val:
                w[t]=val
                        
            #type = match.group(1)
            #num_in_type = re.search(r'[0-9]+',type,re.MULTILINE | re.U)
            #if num_in_type:
                
            #if match.group(2):
            #    range = re.search(r'[0-9]+-[0-9]+',match.group(2),re.MULTILINE | re.U)
            #    if range:
            #    w['ilosc_opadow[mm/12h]'] =  range.group(0)
            #else:
            #    w['ilosc_opadow[mm/12h]'] = ''
    
        date = date+datetime.timedelta(days=1)
    
    print "\n".join(map(str,weather.iteritems()))
    
    f = open('pogoda.log','w')
    import json
    x = json.dumps(weather,sort_keys=True,indent=4, separators=(',', ': '))
    print x
    print type(x)
    f.write(x.encode('utf-8'))
    f.close()
        