import csv
import scrapy
from re import findall
from scrapy.crawler import CrawlerProcess
import aiohttp


class MustappSpider(scrapy.Spider):
    name = "mustappspider"
    username = ''

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.create_tables()

    def start_requests(self):
        url = f'https://mustapp.com/@{self.username}/'
        yield scrapy.Request(url=url, callback=self.parse)

    async def parse(self, response):
        pattern = r'"(want|watched)":\[(.*?)]'
        found = findall(pattern, response.css(".content script::text").get())
        for movie_list in found:
            for movie_id in movie_list[1].split(','):
                if movie_list[0] == 'want':
                    movie_url = 'https://mustapp.com/p/' + f'{movie_id}'
                    yield response.follow(movie_url, callback=self.parse_want_movie_page)
                elif movie_list[0] == 'watched':
                    movie_url = f'https://mustapp.com/@{self.username}/{movie_id}/'
                    yield response.follow(movie_url, callback=self.parse_watched_movie_page)

    async def parse_want_movie_page(self, response):
        title = response.css('.productPage__title::text').get()
        year = int(response.css('.productPage__subtitle::text').get()[-4::])
        data = {'Title': title, 'Year': year}
        await self.writer_want.writerow(list(data.values()))

    async def parse_watched_movie_page(self, response):
        parsed_details = r'profile_products:.*"modified_at":"(.*)T.*"rate":(10|[0-9]|).*"reviewed":(.*"body":"(.*)"}|)'
        title = response.css('.profileProduct__product_title::text').get()
        year = int(response.css('.profileProduct__product_date::text').get()[-4::])
        details = findall(parsed_details, response.css(".content script::text").get())[0]
        date, review, rate = details[0], details[3], ''
        if details[1] != '': rate = int(details[1])
        data = {'Title': title, 'Year': year, 'Rating10': rate, 'WatchedDate': date, 'Review': review}
        await self.writer_watched.writerow(list(data.values()))

    def create_tables(self):
        self.want_file = open('want.csv', 'w', encoding='utf-8', newline='')
        self.watched_file = open('watched.csv', 'w', encoding='utf-8', newline='')
        self.writer_want = csv.writer(self.want_file)
        self.writer_watched = csv.writer(self.watched_file)
        columns_want = ['Title', 'Year']
        self.writer_want.writerow(columns_want)
        columns_watched = ['Title', 'Year', 'Rating10', 'WatchedDate', 'Review']
        self.writer_watched.writerow(columns_watched)

def main(crawler):
    process = CrawlerProcess()
    process.crawl(crawler)
    process.start()

if __name__ == "__main__":
    MySpider = MustappSpider
    MySpider.username = input('Enter your nickname: ')
    main(MySpider)
