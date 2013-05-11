import web
import json
from operator import itemgetter

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
        group = 'combined_date'

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
        
        #wez dane z wypadkow
        
        
        regions = db.select('wojewodztwa',where='id in (%s)'%",".join(params['regions']))
        
        #wez te druge dane
        #table = params['selected_condition'].split(',')[0]
        #param = params['selected_condition'].split(',')[1]
        #conditions = db.select(table,what=date_str+','+'avg('+param+') as '+param,where='wojewodztwo in (%s) AND data>="%s" AND data<="%s"'%(",".join(params['regions']),params['date_from'],params['date_to']),order='id',group=group)
        
        
        result = {}
        
        
        
        rows = {}
        for region in regions:
            accidents = db.select('wypadki join wojewodztwa on wypadki.wojewodztwo=wojewodztwa.id',
                                  what=date_str+',sum(wypadki) as wypadki,sum(zabici) as zabici,sum(ranni) as ranni, wojewodztwa.nazwa wojewodztwo',
                                  where='wojewodztwo="%s" AND data>="%s" AND data<="%s"'%(region['id'],params['date_from'],params['date_to']),
                                  order='data',group=group)
            rows[region['nazwa']]= {}
            for acc in accidents:
                rows[region['nazwa']][acc['combined_date']]={'wypadki':acc['wypadki']}
        #for c in conditions:
        #    if rows.has_key(c['combined_date']):
        #        rows[c['combined_date']][param]=c[param]
        result['rows']=sorted(rows.items(),key=itemgetter(0))
        
        
        #specjalny przypadek - swieta - co z nim zrobic?
        
        
        #todo: obsluzyc rozne poziomy granulacji 
        return json.dumps(result)
        
        
        
class Regions(object):
    def GET(self):
        regions = db.select('wojewodztwa')
        print "regions",regions
        results = [ {'id':r['id'],'name':r['nazwa']} for r in regions]
        print "results",results
        return json.dumps(results)
    
if __name__=="__main__":
        app = web.application(urls, globals())
        app.run()
    
