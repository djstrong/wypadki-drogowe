#-*- coding: utf-8 -*-
import sqlite3
import json
import os.path
import os

conn = None


def create_db():
    c = conn.cursor()
#    return str([self.date, self.przestepstwa_rozbojnicze, self.bojki_i_pobicia, self.kradzieze_z_wlamaniem, self.kradzieze, self.wypadki, self.zabici, self.ranni, self.nietrzezwi_kierowcy, self.kolizje])

#    c.execute('''CREATE TABLE wypadki (
#                                       id integer primary key,
#                                       data text,  
#                                       wypadki integer, 
#                                       zabici integer, 
#                                       ranni integer,
#                                       nietrzezwi_kierowcy integer, 
#                                       miasto text )''')


  
    c.execute('''CREATE TABLE pogoda (
                                      data DATE,
                                      wojewodztwo INTEGER,
                                      max_temp integer,
                                      min_temp integer,
                                      wiatr real,
                                      cisnienie real,
                                      deszcz text,
                                      snieg text,
                                      wschod text,
                                      zachod text,
                                      PRIMARY KEY (wojewodztwo, data),
                                      FOREIGN KEY(wojewodztwo) REFERENCES wojewodztwa(id))
    ''')
    
    c.execute('''CREATE TABLE swieta (
                                      id integer primary key,
                                      data text,
                                      opis text
                                    )''')
    c.execute('CREATE UNIQUE INDEX "data_miasto" on pogoda (data ASC, miasto ASC)')
    
def fill_db():
    load_data('pogoda_Katowice.log',columns = ['max_temp','min_temp','wiatr','cisnienie','deszcz','snieg','wschod','zachod'],city='katowice',table='pogoda')
    load_data('pogoda_Rzeszow.log',columns = ['max_temp','min_temp','wiatr','cisnienie','deszcz','snieg','wschod','zachod'],city='rzeszow',table='pogoda')
    
    load_data('rzeszow.json',columns= ['wypadki','zabici','ranni','nietrzezwi_kierowcy'],city='rzeszow',table='wypadki')
    load_data('katowice.json',columns= ['wypadki','zabici','ranni','nietrzezwi_kierowcy'],city='katowice',table='wypadki')
    
    load_data('swieta.log',columns=['opis'],city=None,table='swieta')
    
def load_data(filename,columns,region,table):
    f = open(filename,'r')
    data = json.load(f,encoding='utf-8')
    c = conn.cursor()
    to_inserts = []
    print ",".join(['data']+columns+['miasto'])
    for k,v in data.iteritems():
        x = [k]+[v.get(column,None) for column in columns]
        if region:
            x += [region]
        to_inserts.append(x)
    c.executemany("INSERT INTO %s (%s) values (%s)"%(table,",".join(['data']+columns+['wojewodztwo'] if region else ['data']+columns),",".join(['?' for i in range(len(['data']+columns+['wojewodztwa'] if region else ['data']+columns))])),to_inserts)
    conn.commit()
    
def load_wypadki(city):
    f = open(city+".log",'r')
    data = json.load(f,encoding='utf-8')
    c = conn.cursor()
    to_inserts = []
    columns = ['wypadki','zabici','ranni','nietrzezwi_kierowcy']

if __name__=="__main__":
    #if os.path.exists('wypadki.db'):
    #    os.remove('wypadki.db')
        conn = sqlite3.connect('nowe.db')
    #try:
        c = conn.cursor()
        c.execute('drop table pogoda')
        c.execute('''CREATE TABLE pogoda (
                                      data DATE,
                                      wojewodztwo INTEGER,
                                      max_temp integer,
                                      min_temp integer,
                                      wiatr real,
                                      cisnienie real,
                                      deszcz text,
                                      snieg text,
                                      wschod text,
                                      zachod text,
                                      PRIMARY KEY (wojewodztwo, data),
                                      FOREIGN KEY(wojewodztwo) REFERENCES wojewodztwa(id))
    ''')
        
        #create_db()
        #fill_db()
        region_capital = {
                          u'dolnośląskie':'Wroclaw',
                          u'podlaskie':'Bialystok',
                          u'kujawsko-pomorskie':'Bydgoszcz',
                          u'pomorskie':'Gdansk',
                          u'śląskie':'Katowice',
                          u'świętokrzyskie':'Kielce',
                          u'małopolskie':'Krakow',
                          u'lubelskie':'Lublin',
                          u'warmińsko-mazurskie':'Olsztyn',
                          u'opolskie':'Opole',
                          u'wielkopolskie':'Poznan',
                          u'podkarpackie':'Rzeszow',
                          u'zachodniopomorskie':'Szczecin',
                          u'mazowieckie':'Warszawa',
                          u'lubuskie':'Zielona-Gora',
                          u'łódzkie':'Lodz'
                          }
        regions = c.execute('SELECT id,nazwa from wojewodztwa').fetchall()
        print regions
        for region in regions:
            load_data('pogoda_%s.log'%region_capital[region[1]],columns = ['max_temp','min_temp','wiatr','cisnienie','deszcz','snieg','wschod','zachod'],region=region[0],table='pogoda')
        
    #except Exception,e:
    #    raise e
        
    
    