#-*- coding: utf-8 -*-

import urllib2
import time
from datetime import date,datetime
from datetime import timedelta
import re
import sys
import urllib
from dateutil.relativedelta import relativedelta
import collections

class Dzien(object):
  def __init__(self):
    self.date = None
    self.przestepstwa_rozbojnicze = None
    self.bojki_i_pobicia = None
    self.kradzieze_z_wlamaniem = None
    self.kradzieze = None
    self.wypadki = None
    self.zabici = None
    self.ranni = None
    self.nietrzezwi_kierowcy = None
    self.kolizje = None

  def __str__(self):
    return str([self.date, self.przestepstwa_rozbojnicze, self.bojki_i_pobicia, self.kradzieze_z_wlamaniem, self.kradzieze, self.wypadki, self.zabici, self.ranni, self.nietrzezwi_kierowcy, self.kolizje])


if __name__=="__main__":
    delta = timedelta(1)
    dateX = date.today()
    dateX = dateX.replace(day = 1)

    
    if len(sys.argv)<2:
        print "usage: ",sys.argv[0],"date_from"
        sys.exit(1)
    date_from = datetime.strptime(sys.argv[1],'%Y-%m-%d').date()
    
    katowice = collections.defaultdict(list)
    while dateX>date_from:
      #date -= delta
      strdate = dateX.strftime("%Y-%m-%d")
      enddate = (dateX+relativedelta(months=1)).strftime("%Y-%m-%d")
      print strdate
      link = 'https://www.biometeo.pl/ajax/w83iz5a2ytTgmu3N6brT2tjVl-yVp87K2M7a19Dc4qjcl-rg/'
      
      values = {'data1'      : strdate+' 06:00',
          'data2'   : enddate,
          'pora'         : '1', 'poz':'', 'oboj':'', 'nieg':'', 'bnieg':'', 'wyn':'', 'miastas':'Katowice'}

      data = urllib.urlencode(values)
      request = urllib2.Request(link, data)
      
      response = urllib2.urlopen(request)
      html = response.read()
      print html
      
      m = re.search(r'<wyn>(.*?)</wyn>', html)
      if m is not None: 
        wyn = m.group(1)
        days = wyn.split(';')
        for day in days:
          m, d, y, biomet = map(int, day.split(','))
          date2 = date(y, m, d)
          katowice[date2.strftime('%Y-%m-%d')].append(int(biomet))
      
      dateX = dateX - relativedelta(months=1)
      #break

    for k, v in katowice.iteritems():
      katowice[k] = float(sum(v))/len(v)

    f = open('katowice_biometeo.json','w')
    import json
    x = json.dumps(katowice,sort_keys=True,indent=4, separators=(',', ': '))
    f.write(x.encode('utf-8'))
    f.close()