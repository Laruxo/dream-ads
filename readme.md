# Dream Ads

Introducing:
* Scrapy as Web Scraper
* Flask as API
* VueJs as Frontend

### Try it out
```
$ git submodule update --init --remote
$ docker-compose run --rm node npm install
$ docker-compose up
```

First run may take a while because it runs `npm install`.

Then visit `localhost:8080` for frontend or `localhost:5000/api` for API.

### Want to see your favorite motorcycles?

* Open `./scraper/spiders/*_spider.py`
* At the top of the file there are 4 links to different model searches on each scraped site.
* Here you can add your models and links to their searches.
* After making the changes simply run scraper again (from Frontend/API/CLI).
* Happy riding!
