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
import sqlite3

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
  
    conn = sqlite3.connect('nowe.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS biomet  (
      wojewodztwo INTEGER,
      data DATE, 
      wartosc INTEGER,
      PRIMARY KEY (wojewodztwo, data),
      FOREIGN KEY(wojewodztwo) REFERENCES wojewodztwa(id))''')
  
    wojewodztwa = {'WOJ. DOLNOŚLĄSKIE':'dolnośląskie', 'WOJ. KUJAWSKO-POMORSKIE':'kujawsko-pomorskie', 'WOJ. LUBELSKIE':'lubelskie', 'WOJ. LUBUSKIE':'lubuskie', 'WOJ. ŁÓDZKIE':'łódzkie', 'WOJ. MAŁOPOLSKIE':'małopolskie', 'WOJ. MAZOWIECKIE':'mazowieckie', 'WOJ. OPOLSKIE':'opolskie', 'WOJ. PODKARPACKIE':'podkarpackie', 'WOJ. PODLASKIE':'podlaskie', 'WOJ. POMORSKIE':'pomorskie', 'WOJ. ŚLĄSKIE':'śląskie', 'WOJ. ŚWIĘTOKRZYSKIE':'świętokrzyskie', 'WOJ. WARMIŃSKO-MAZURSKIE':'warmińsko-mazurskie', 'WOJ. WIELKOPOLSKIE':'wielkopolskie', 'WOJ. ZACHODNIOPOMORSKIE':'zachodniopomorskie'}
  
    lista_wojewodztw = wojewodztwa.values()
  
    miasta = {'Białystok':'podlaskie', 'Bydgoszcz':'kujawsko-pomorskie', 'Gdańsk':'pomorskie', 'Gorzów Wlkp.':'lubuskie', 'Katowice':'śląskie', 'Kielce':'świętokrzyskie', 'Kraków':'małopolskie', 'Lublin':'lubelskie', 'Łódź':'łódzkie', 'Olsztyn':'warmińsko-mazurskie', 'Opole':'opolskie', 'Poznań':'wielkopolskie', 'Rzeszów':'podkarpackie', 'Szczecin':'zachodniopomorskie', 'Warszawa':'mazowieckie', 'Wrocław':'dolnośląskie'}
  
    delta = timedelta(1)
    dateX = date.today()
    dateX = dateX.replace(day = 1)

    dane = collections.defaultdict(list)
    
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
      
      for miasto, woj in miasta.iteritems():
        woj_id = lista_wojewodztw.index(woj)
        values = {'data1'      : strdate+' 06:00',
            'data2'   : enddate,
            'pora'         : '1', 'poz':'', 'oboj':'', 'nieg':'', 'bnieg':'', 'wyn':'', 'miastas':miasto}

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
            dane[(date2, woj_id)].append(int(biomet))
            
      
      dateX = dateX - relativedelta(months=1)

    for k,v in dane.iteritems():
      data, woj_id = k
      biomet = sorted(v)[len(v)/2]      
      c.execute('INSERT OR IGNORE INTO biomet VALUES(?, ?, ?)', (woj_id, data, biomet))
      
    conn.commit()
      #break

    for k, v in katowice.iteritems():
      katowice[k] = sorted(v)[len(v)/2]

    f = open('katowice_biometeo.json','w')
    import json
    x = json.dumps(katowice,sort_keys=True,indent=4, separators=(',', ': '))
    f.write(x.encode('utf-8'))
    f.close()