import sqlite3
import csv
import numpy
import sys
from operator import itemgetter

if __name__=="__main__":
    conn = sqlite3.connect('../server/nowe.db')
    
    #czy duzo, czy malo wypadkow na podstawie pogody
    c = conn.cursor()
    for wypadki in ['wypadki','zabici','ranni','kolizje']:
        wojewodztwa = c.execute("SELECT * from wojewodztwa").fetchall() 
        for w in wojewodztwa:
            print "WOJEWODZTWO",w
            print c.execute("SELECT * from moon_phase").fetchone()
            
            pogoda = c.execute("""SELECT max_temp,min_temp,cisnienie,zachod-wschod as godzin_dnia,phase,%s
                                    FROM pogoda JOIN wypadki ON wypadki.data=pogoda.data
                                    JOIN moon_phase ON moon_phase.data=pogoda.data
                                WHERE pogoda.data>'2009-01-01' AND pogoda.wojewodztwo=wypadki.wojewodztwo and pogoda.wojewodztwo=%d"""%(wypadki,w[0])).fetchall()
            print len(pogoda)
            acc = map(itemgetter(5),pogoda)
            freq,bins = numpy.histogram(acc)
            print freq
            print bins
            
    
            positions = numpy.digitize(acc,bins) # numery binow
            print max(positions)
            print min(positions)
        
            with open(wypadki+'/pogoda_%s.csv'%w[1],'w') as file:
                writer = csv.DictWriter(file, ['max_temp','min_temp','cisnienie','godzin_dnia','faza_ksiezyca',wypadki])
                writer.writeheader()
                for row,pos in zip(pogoda,positions):
                    writer.writerow({'max_temp':row[0],
                                     'min_temp':row[1],
                                     'cisnienie':row[2],
                                     'godzin_dnia':row[3],
                                     'faza_ksiezyca':row[4],
                                     #'wypadki':bin_names[pos-1]})
                                     wypadki:'%s, %s'%(bins[pos-2],bins[pos-1]) if pos>1 else '< %s'%bins[pos-1]})
    
                
    
    