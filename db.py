import sqlite3
import json
import os.path
import os

conn = None


def create_db():
    c = conn.cursor()
#    return str([self.date, self.przestepstwa_rozbojnicze, self.bojki_i_pobicia, self.kradzieze_z_wlamaniem, self.kradzieze, self.wypadki, self.zabici, self.ranni, self.nietrzezwi_kierowcy, self.kolizje])

    c.execute('''CREATE TABLE wypadki (
                                       id integer primary key,
                                       data text,  
                                       wypadki integer, 
                                       zabici integer, 
                                       ranni integer,
                                       nietrzezwi_kierowcy integer, 
                                       miasto text )''')
    
    c.execute('''CREATE TABLE pogoda (
                                      id integer primary key,
                                      data text,
                                      max_temp integer,
                                      min_temp integer,
                                      wiatr real,
                                      cisnienie real,
                                      deszcz text,
                                      snieg text,
                                      wschod text,
                                      zachod text,
                                      miasto text
    )''')
    
    c.execute('''CREATE TABLE swieta (
                                      id integer primary key,
                                      data text,
                                      opis text
                                    )''')
    
def fill_db():
    load_data('pogoda_Katowice.log',columns = ['max_temp','min_temp','wiatr','cisnienie','deszcz','snieg','wschod','zachod'],city='katowice',table='pogoda')
    load_data('pogoda_Rzeszow.log',columns = ['max_temp','min_temp','wiatr','cisnienie','deszcz','snieg','wschod','zachod'],city='rzeszow',table='pogoda')
    
    load_data('rzeszow.json',columns= ['wypadki','zabici','ranni','nietrzezwi_kierowcy'],city='rzeszow',table='wypadki')
    load_data('katowice.json',columns= ['wypadki','zabici','ranni','nietrzezwi_kierowcy'],city='katowice',table='wypadki')
    
    load_data('swieta.log',columns=['opis'],city=None,table='swieta')
    
def load_data(filename,columns,city,table):
    f = open(filename,'r')
    data = json.load(f,encoding='utf-8')
    c = conn.cursor()
    to_inserts = []
    print ",".join(['data']+columns+['miasto'])
    for k,v in data.iteritems():
        x = [k]+[v.get(column,None) for column in columns]
        if city:
            x += [city]
        to_inserts.append(x)
    c.executemany("INSERT INTO %s (%s) values (%s)"%(table,",".join(['data']+columns+['miasto'] if city else ['data']+columns),",".join(['?' for i in range(len(['data']+columns+['miasto'] if city else ['data']+columns))])),to_inserts)
    conn.commit()
    
def load_wypadki(city):
    f = open(city+".log",'r')
    data = json.load(f,encoding='utf-8')
    c = conn.cursor()
    to_inserts = []
    columns = ['wypadki','zabici','ranni','nietrzezwi_kierowcy']

if __name__=="__main__":
    if os.path.exists('wypadki.db'):
        os.remove('wypadki.db')
    conn = sqlite3.connect('wypadki.db')
    try:
        c = conn.cursor()
        create_db()
        fill_db()
    except Exception,e:
        print "exception",e
        
    
    