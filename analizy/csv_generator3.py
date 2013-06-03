import sqlite3
import csv
import numpy
import sys
from operator import itemgetter

if __name__=="__main__":
    conn = sqlite3.connect('../server/nowe.db')
    
    #czy duzo, czy malo wypadkow na podstawie pogody
    c = conn.cursor()


        
    pogoda = c.execute("""SELECT max_temp,min_temp,cisnienie,zachod-wschod as godzin_dnia,phase,wartosc,strftime('%w',pogoda.data) as dzien_tygodnia,strftime('%m',pogoda.data) as miesiac,wypadki,zabici,ranni,kolizje,wojewodztwa.nazwa
                            FROM pogoda JOIN wypadki ON wypadki.data=pogoda.data
                            JOIN moon_phase ON moon_phase.data=pogoda.data
                            JOIN biomet ON biomet.data=pogoda.data AND biomet.wojewodztwo=pogoda.wojewodztwo
                            JOIN wojewodztwa ON wojewodztwa.id=pogoda.wojewodztwo
                        WHERE pogoda.data>'2009-01-01' AND pogoda.wojewodztwo=wypadki.wojewodztwo""").fetchall()


    with open('zbiorcze/zbiorcze2.csv','w') as file:
        writer = csv.DictWriter(file, ['max_temp','min_temp','cisnienie','godzin_dnia','faza_ksiezyca','biomet','dzien_tygodnia','miesiac','wypadki','zabici','ranni','kolizje','wojewodztwo'])
        writer.writeheader()
        for row in pogoda:
            writer.writerow({'max_temp':row[0],
                              'min_temp':row[1],
                              'cisnienie':row[2],
                              'godzin_dnia':row[3],
                              'faza_ksiezyca':row[4],
                              'biomet':row[5],
                              'dzien_tygodnia':row[6],
                              'miesiac':row[7],
                              'wypadki':row[8],'zabici':row[9],'ranni':row[10],'kolizje':row[11],'wojewodztwo':row[12].encode('utf-8')})
                              #'wypadki':bin_names[pos-1]})
                              #wypadki:'%s, %s'%(bins[pos-2],bins[pos-1]) if pos>1 else '< %s'%bins[pos-1]})
    
                
    
    