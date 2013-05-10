#-*- coding: utf-8 -*-

import csv
import sqlite3
import sys
import datetime
reload(sys)
sys.setdefaultencoding("utf-8")

conn = sqlite3.connect('nowe.db')
c = conn.cursor()

c.execute('''CREATE TABLE wojewodztwa (
  id INTEGER PRIMARY KEY,
  nazwa TEXT NOT NULL)''')

c.execute('''CREATE TABLE wypadki (
  wojewodztwo INTEGER,
  data DATE,
  wypadki INTEGER,
  zabici INTEGER,
  ranni INTEGER,
  kolizje INTEGER,
  PRIMARY KEY (wojewodztwo, data),
  FOREIGN KEY(wojewodztwo) REFERENCES wojewodztwa(id))''')

wojewodztwa = {'WOJ. DOLNOŚLĄSKIE':'dolnośląskie', 'WOJ. KUJAWSKO-POMORSKIE':'kujawsko-pomorskie', 'WOJ. LUBELSKIE':'lubelskie', 'WOJ. LUBUSKIE':'lubuskie', 'WOJ. ŁÓDZKIE':'łódzkie', 'WOJ. MAŁOPOLSKIE':'małopolskie', 'WOJ. MAZOWIECKIE':'mazowieckie', 'WOJ. OPOLSKIE':'opolskie', 'WOJ. PODKARPACKIE':'podkarpackie', 'WOJ. PODLASKIE':'podlaskie', 'WOJ. POMORSKIE':'pomorskie', 'WOJ. ŚLĄSKIE':'śląskie', 'WOJ. ŚWIĘTOKRZYSKIE':'świętokrzyskie', 'WOJ. WARMIŃSKO-MAZURSKIE':'warmińsko-mazurskie', 'WOJ. WIELKOPOLSKIE':'wielkopolskie', 'WOJ. ZACHODNIOPOMORSKIE':'zachodniopomorskie'}

lista_wojewodztw = wojewodztwa.values()

for i,woj in enumerate(lista_wojewodztw):
  c.execute('INSERT INTO wojewodztwa VALUES(?, ?)', (i, unicode(woj)))
  
conn.commit()

def parsuj(plik):
  global c, conn
  wojewodztwo = None
  f = open(plik)
  reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
  for row in reader:
    if row[1] in wojewodztwa:
      wojewodztwo = wojewodztwa[row[1]]
      continue
    if wojewodztwo:
  #    print row
      data = row[2]
      rok, miesiac, dzien = map(int, data.split('/'))
      wypadki = row[3]
      zabici = row[4]
      ranni = row[5]
      kolizje = row[6]
      print data, wypadki, zabici, ranni, kolizje
      woj_id = lista_wojewodztw.index(wojewodztwo)
      c.execute('INSERT INTO wypadki VALUES(?, ?, ?, ?, ?, ?)', (woj_id, datetime.date(rok, miesiac, dzien), wypadki, zabici, ranni, kolizje))
      
  conn.commit()
  
  
import glob
for plik in glob.glob("policja/*.csv"):
    parsuj(plik)