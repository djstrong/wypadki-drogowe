import web
import json
from operator import itemgetter

urls = (
    '/', 'Index',
    '/get_data','Data'
)

db = web.database(dbn='sqlite', db='wypadki.db')
render = web.template.render('templates/')

class Index(object):
    def GET(self):
        return render.index()
    
class Data(object):
    def GET(self):
        print "GETTTTT"
        params = web.input()
        
        #wez dane z wypadkow
        accidents = db.select('wypadki',what='data,wypadki,zabici,ranni',where='miasto="%s" AND data>="%s" AND data<="%s"'%(params['selected_city'],params['date_from'],params['date_to']),order='id')
        
        
        #wez te druge dane
        table = params['selected_condition'].split(',')[0]
        param = params['selected_condition'].split(',')[1]
        conditions = db.select(table,what='data,'+param,where='miasto="%s" AND data>="%s" AND data<="%s"'%(params['selected_city'],params['date_from'],params['date_to']),order='id')
        
        
        result = {}
        
        rows = {}
        for acc in accidents:
            rows[acc['data']]={'wypadki':acc['wypadki']}
        for c in conditions:
            if rows.has_key(c['data']):
                rows[c['data']][param]=c[param]
        result['rows']=sorted(rows.items(),key=itemgetter(0))
        
        
        #specjalny przypadek - swieta - co z nim zrobic?
        
        
        #todo: obsluzyc rozne poziomy granulacji 
        
        return json.dumps(result)
        
        
        
    
    
if __name__=="__main__":
        app = web.application(urls, globals())
        app.run()
    
