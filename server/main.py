import web



urls = (
    '/', 'Index'
)

db = web.database(dbn='sqlite', db='wypadki.db')
render = web.template.render('templates/')

class Index(object):
    def GET(self):
        w = db.select('wypadki',what='wypadki,zabici,ranni',where='miasto="katowice"',order='id')
        daty = db.select('wypadki',what='data',where='miasto="katowice"',order='id')
        return render.index(name='ble',wypadki=w.list()[:5],daty=daty.list()[:5])
    
    
if __name__=="__main__":
        app = web.application(urls, globals())
        app.run()
    
