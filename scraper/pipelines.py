import datetime
import sqlite3
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


def current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


class JsonDeduplicationPipeline(object):
    def open_spider(self, spider):
        self.db = TinyDB('ads.json', default_table='ads', storage=CachingMiddleware(JSONStorage))
        Ads = Query()
        self.db.update({'active': False}, Ads.id.search(spider.name + '-'))

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        Ads = Query()
        result = self.db.get(Ads.id == item['id'])
        if result is not None:
            # check if ignored
            if result['ignored']:
                return

            print('Updating item %s' % item['id'])
            self.db.update({
                'price': item.get('price'),
                'mileage': item.get('mileage'),
                'description': item.get('description'),
                'active': True
            }, Ads.id == item['id'])

            return item

        print('Adding item %s' % item['id'])
        item['active'] = True
        item['ignored'] = False
        item['created_at'] = current_date()
        self.db.insert(dict(item))

        return item


class SqlDeduplicationPipeline(object):
    def open_spider(self, spider):
        self.db = sqlite3.connect('ads.db')
        cur = self.db.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS ads ('
            'id VARCHAR PRIMARY KEY NOT NULL,'
            'link VARCHAR NOT NULL,'
            'model VARCHAR NOT NULL,'
            'title VARCHAR NOT NULL,'
            'price INTEGER NOT NULL,'
            'mileage INTEGER,'
            'cubic INTEGER NOT NULL,'
            'power INTEGER,'
            'year INTEGER NOT NULL,'
            'color VARCHAR,'
            'description TEXT,'
            'location VARCHAR NOT NULL,'
            'images VARCHAR,'
            'created_at DATETIME NOT NULL,'
            'active BOOLEAN NOT NULL,'
            'ignored BOOLEAN NOT NULL DEFAULT 0'
            ')')
        cur.execute('UPDATE ads SET active = 0 WHERE id LIKE "%s"' % (spider.name + '-%'))

    def close_spider(self, spider):
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        cur = self.db.cursor()

        cur.execute('SELECT id, ignored FROM ads WHERE id = "%s"' % item['id'])
        result = cur.fetchone()

        # update if exists
        if result is not None:
            # check if ignored
            if result[1] == 1:
                return

            print('Updating item %s' % item['id'])
            cur.execute(
                'UPDATE ads SET '
                'price = :price, active = 1 '
                'WHERE id = :id',
                dict(item)
            )

            return item

        # otherwise, add new item
        print('Adding item %s' % item['id'])
        item['active'] = True
        item['created_at'] = current_date()
        keys = item.keys()
        columns = ', '.join(keys)
        placeholders = ':' + ', :'.join(keys)
        cur.execute('INSERT INTO ads (%s) VALUES (%s)' % (columns, placeholders), dict(item))

        return item
