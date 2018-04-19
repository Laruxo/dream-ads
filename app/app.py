from flask import Flask, g
from flask_restful import Resource, Api
import sqlite3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

DATABASE = 'ads.db'
app = Flask(__name__)
api = Api(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


class Ads(Resource):
    def get(self):
        db = sqlite3.connect(DATABASE)
        db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
        cur = db.cursor()
        try:
            cur.execute('SELECT * FROM ads WHERE active = 1 AND ignored = 0')
            result = cur.fetchall()
        except sqlite3.OperationalError:
            print('DB is empty. Try running scraper first.')
            result = []
        db.close()
        return result


api.add_resource(Ads, '/api/ads')


class Ignore(Resource):
    def get(self, ad_id):
        db = sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute('UPDATE ads SET ignored = 1 WHERE id = "%s"' % ad_id)
        db.commit()
        db.close()
        return 'ok'


api.add_resource(Ignore, '/api/ignore/<string:ad_id>')


class Scrape(Resource):
    def get(self):
        try:
            process = CrawlerProcess(get_project_settings())
            process.crawl('autoplius')
            process.crawl('autogidas')
            process.crawl('autobilis')
            process.start()
        except Exception as err:
            print('There was an error')
            process.stop()
            return 'bad'
        return 'ok'


api.add_resource(Scrape, '/api/scrape')

app.run(host='0.0.0.0')
