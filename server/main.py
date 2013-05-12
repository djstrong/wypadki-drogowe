#-*- coding: utf-8 -*-
import web
import json
from operator import itemgetter
import numpy

urls = (
    '/', 'Index',
    '/get_data','Data',
    '/get_regions','Regions',
)

db = web.database(dbn='sqlite', db='nowe.db')
render = web.template.render('templates/')

class Index(object):
    def GET(self):
        return render.index()
    
class Data(object):
    def GET(self):
        params = json.loads(web.input()['json'])
        print "PARAMS: ",params
        
        granularity = params['granularity']
        print "GRANULARITY",granularity
        date_str = 'data as combined_date'

        if granularity=='monthly':
            date_str = 'strftime("%Y",date(data))||"-"||strftime("%m",date(data)) as combined_date'
        elif granularity=='yearly':
            date_str = 'strftime("%Y",date(data)) as combined_date'
        elif granularity=='quarterly':
            date_str = '''strftime("%Y",date(data))||"-"||CASE 
                                                              WHEN cast(strftime('%m', date(data)) as integer) BETWEEN 1 AND 3 THEN 'q1'
                                                              WHEN cast(strftime('%m', date(data)) as integer) BETWEEN 4 and 6 THEN 'q2'
                                                              WHEN cast(strftime('%m', date(data)) as integer) BETWEEN 7 and 9 THEN 'q3'
                                                              ELSE 'q4' END as combined_date'''
        
        regions = db.select('wojewodztwa',where='id in (%s)'%",".join(params['regions']))
        
        if params['type'] in ['min_temp','max_temp']:
            return json.dumps(self.weather(params,date_str,regions))
        
        else:
            return json.dumps(self.default(params,date_str,regions))
        
        
    def default(self,params,date_str,regions):         
        rows = {}
        for region in regions:
            #dla kazdego wojewodztwa szukamy wypadkow i dodajemy
            accidents = db.select('wypadki join wojewodztwa on wypadki.wojewodztwo=wojewodztwa.id',
                                  what=date_str+',sum(wypadki) as wypadki,sum(zabici) as zabici,sum(ranni) as ranni, wojewodztwa.nazwa wojewodztwo',
                                  where='wojewodztwo="%s" AND data>="%s" AND data<="%s"'%(region['id'],params['date_from'],params['date_to']),
                                  order='data',group='combined_date')
            rows[region['nazwa']]= {}
            for acc in accidents:
                rows[region['nazwa']][acc['combined_date']]={'wypadki':acc['wypadki']}

 
        return {'rows': sorted(rows.items(),key=itemgetter(0)) }
    def weather(self,params,date_str,regions):
        rows = {}
        for region in regions:
            
            data = rows.get(region['nazwa'],{})
            weather_data = db.select('pogoda',what=date_str+', '+params['type'],
                                     where='wojewodztwo=%s AND data>="%s" AND data<="%s"'%(region['id'],params['date_from'],params['date_to']),
                                     order='data')
            accidents = db.select('wypadki join wojewodztwa on wypadki.wojewodztwo=wojewodztwa.id',
                                  what=date_str+',sum(wypadki) as wypadki,sum(zabici) as zabici,sum(ranni) as ranni, wojewodztwa.nazwa wojewodztwo',
                                  where='wojewodztwo="%s" AND data>="%s" AND data<="%s"'%(region['id'],params['date_from'],params['date_to']),
                                  order='data',group='combined_date')
            
            values = [r[params['type']] for r in weather_data]
            
            freq,bins = numpy.histogram(values)
            bins = bins.round() # mozna je zrobic troche lepsze niz domyslne z numpy
             
            pos = numpy.digitize(values,bins) # numery binow
            
            zipped = zip(pos,accidents)
            for bin_pos,acc in zipped:
                bin_str = '%s, %s'%(bins[bin_pos-2],bins[bin_pos-1]) if bin_pos>1 else '< %s'%bins[bin_pos-1]
                if data.get(bin_str,None):
                    data[bin_str]['wypadki']+=acc['wypadki']
                else: 
                    data[bin_str] = {'wypadki': acc['wypadki']}
            rows[region['nazwa']] = data 
            print rows.items()
        return {'rows': sorted(rows.items(),key=itemgetter(0))}
        
class Regions(object):
    def GET(self):
        regions = db.select('wojewodztwa')
        print "regions",regions
        results = [ {'id':r['id'],'name':r['nazwa']} for r in regions]
        print "results",results
        return json.dumps(sorted(results,key=lambda i: i['name']))
    
if __name__=="__main__":
        app = web.application(urls, globals())
        app.run()
    
