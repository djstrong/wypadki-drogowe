#-*- coding: utf-8 -*-

import urllib2
import time
from datetime import date,datetime
from datetime import timedelta
import re
import sys


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
    date = date.today()
    
    if len(sys.argv)<2:
        print "usage: ",sys.argv[0],"date_from"
        sys.exit(1)
    date_from = datetime.strptime(sys.argv[1],'%Y-%m-%d').date()
    
    katowice = {}
    while date>date_from:
      date -= delta
      strdate = date.strftime("%Y_%m_%d")
      print strdate
      link = 'http://www.slaska.policja.gov.pl/staystyka-zdarzen/go:data:'+strdate+'/'
      response = urllib2.urlopen(link)
      html = response.read()
      #print html
      
      dzien = Dzien()
      dzien.date = date.strftime('%Y-%m-%d') # ?
      m = re.search(r'przestępstwa rozbójnicze.*?>([0-9]+)<', html)
      if m is not None: dzien.przestepstwa_rozbojnicze = m.group(1)
      m = re.search(r'bójki i pobicia.*?>([0-9]+)<', html)
      if m is not None: dzien.bojki_i_pobicia = m.group(1)
      m = re.search(r'kradzieże z włamaniem.*?>([0-9]+)<', html)
      if m is not None: dzien.kradzieze_z_wlamaniem = m.group(1)
      m = re.search(r'kradzieże.*?>([0-9]+)<', html)
      if m is not None: dzien.kradzieze = m.group(1)
      m = re.search(r'wypadki.*?>([0-9]+)<', html)
      if m is not None: dzien.wypadki = m.group(1)
      m = re.search(r'zabici.*?>([0-9]+)<', html)
      if m is not None: dzien.zabici = m.group(1)
      m = re.search(r'ranni.*?>([0-9]+)<', html)
      if m is not None: dzien.ranni = m.group(1)
      m = re.search(r'nietrzeźwi kierowcy.*?>([0-9]+)<', html)
      if m is not None: dzien.nietrzezwi_kierowcy = m.group(1)
      m = re.search(r'kolizje.*?>([0-9]+)<', html)
      if m is not None: dzien.kolizje = m.group(1)
      
      katowice[date.strftime('%Y-%m-%d')] = dzien.__dict__
      
    f = open('katowice.json','w')
    import json
    x = json.dumps(katowice,sort_keys=True,indent=4, separators=(',', ': '))
    f.write(x.encode('utf-8'))
    f.close()
  