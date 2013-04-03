#-*- coding: utf-8 -*-

import urllib2
import time
from datetime import date
from datetime import timedelta
import re
import sys

class Dzien:
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
  
    self.interwencje = None
    self.osoby_zatrzymane = None
    self.osadzeni_w_izbach_wytrzezwien = None
    self.tymczasowo_aresztowani = None
    self.dozory_policyjne = None

  def __str__(self):
    return str([self.date, self.przestepstwa_rozbojnicze, self.bojki_i_pobicia, self.kradzieze_z_wlamaniem, self.kradzieze, self.wypadki, self.zabici, self.ranni, self.nietrzezwi_kierowcy, self.kolizje, self.interwencje, self.osoby_zatrzymane, self.osadzeni_w_izbach_wytrzezwien, self.tymczasowo_aresztowani, self.dozory_policyjne])

delta = timedelta(1)
date = date.today()

while True:
  date -= delta
  strdate = date.strftime("%Y_%m_%d")
  print >> sys.stderr, strdate
  link = 'http://www.podkarpacka.policja.gov.pl/zestawienia-dobowe/go:data:'+strdate+'/'
  # http://www.podkarpacka.policja.gov.pl/zestawienia-dobowe/go:data:2013_04_03/
  response = urllib2.urlopen(link)
  html = response.read()
  #print html
  
  dzien = Dzien()
  dzien.date = date # ?
  m = re.search(r'interwencje.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.interwencje = m.group(1)
  m = re.search(r'Osoby zatrzymane.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.osoby_zatrzymane = m.group(1)
  m = re.search(r'Osadzeni w izbach wytrzeźwień.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.osadzeni_w_izbach_wytrzezwien = m.group(1)
  m = re.search(r'Tymczasowo aresztowani.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.tymczasowo_aresztowani = m.group(1)
  m = re.search(r'Dozory policyjne.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.dozory_policyjne = m.group(1)  
  
  m = re.search(r'Wypadki drogowe.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.wypadki = m.group(1)
  m = re.search(r'- zabici.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.zabici = m.group(1)
  m = re.search(r'- ranni.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.ranni = m.group(1)
  m = re.search(r'Nietrzeźwi kierowcy.*?\n.*?([0-9]+)', html)
  if m is not None: dzien.nietrzezwi_kierowcy = m.group(1)

  
  print dzien
  