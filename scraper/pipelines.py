from scrapy.exceptions import DropItem
import os
import json
import sqlite3
import logging
import datetime


def current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def find_item_index(items, item_id):
    for index, item in enumerate(items):
        if item['id'] == item_id:
            return index
    return None


class DeduplicationPipeline(object):
    def open_spider(self, spider):
        self.db = sqlite3.connect(spider.name + '.db')
        cur = self.db.cursor()
        cur.execute(
            'CREATE TABLE IF NOT EXISTS ads ('
            'id VARCHAR,'
            'link VARCHAR,'
            'model VARCHAR,'
            'title VARCHAR,'
            'price INTEGER,'
            'mileage INTEGER,'
            'cubic INTEGER,'
            'power INTEGER,'
            'year INTEGER,'
            'color VARCHAR,'
            'description TEXT,'
            'location VARCHAR,'
            'created_at DATETIME,'
            'active BOOLEAN,'
            'images BLOB'
            ')')
        self.items = []
        filename = spider.name + '.json'
        try:
            if os.path.isfile(filename) and os.stat(filename).st_size != 0:
                file = open(filename, 'r', encoding='utf-8')
                self.items = json.loads(file.read())
                file.close()
        except IOError:
            spider.log('Failed to read file %s' % filename, logging.ERROR)
        for item in self.items:
            item['active'] = False

    def close_spider(self, spider):
        filename = spider.name + '.json'
        file = open(filename, 'w')
        file.write(json.dumps(self.items, ensure_ascii=False))
        file.close()
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        index = find_item_index(self.items, item['id'])
        if index is not None:
            diff = {
                key: (item[key], self.items[index][key])
                for key in item if key in self.items[index] and item[key] != self.items[index][key]
            }
            # ignore date diff
            if len(diff) > 1:
                print('Updating item %s' % item['id'])
                self.items[index] = dict(item)
            self.items[index]['active'] = True
            raise DropItem('Item %s already exists' % item['id'])

        print('Adding item %s' % item['id'])
        item['active'] = True
        item['date'] = current_date()
        self.items.append(dict(item))
        cur = self.db.cursor()
        cur.execute('')
        return item
