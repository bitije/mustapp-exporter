import csv
import asyncio
import scrapy
from re import findall
from scrapy.crawler import CrawlerProcess

class MustappSpider(scrapy.Spider):
    name = "mustappspider"
    username = ''

    def __init__(self, *args, **kwargs):
        """
        Create empty csv tables while instance is
        created
        """
        self.create_tables()
        super().__init__(*args, **kwargs)

    def start_requests(self):
        """
        Define entry point for crawling
        """
        url = f'https://mustapp.com/@{self.username}/'
        yield scrapy.Request(url=url, callback=self.parse)

    async def parse(self, response):
        """
        Parse data using regex pattern
        Pattern is searching for want and
        watched list if id's in html content
        """
        pattern = r'"(want|watched)":\[(.*?)]'
        found = findall(pattern, response.css(".content script::text").get())
        return self.fetch_movie(response, found)

    async def fetch_movie(self, response, found):
        """
        Fetching found movies and passing them
        for parsing movie info
        """
        for movie_list in found:
            for movie_id in movie_list[1].split(','):
                if movie_list[0] == 'want':
                    movie_url = 'https://mustapp.com/p/' + f'{movie_id}'
                    yield response.follow(movie_url, callback=self.parse_want_movie_page)
                elif movie_list[0] == 'watched':
                    movie_url = f'https://mustapp.com/@{self.username}/{movie_id}/'
                    yield response.follow(movie_url, callback=self.parse_watched_movie_page)

    async def parse_want_movie_page(self, response):
        """
        Crawling wanted movie for title, year.
        Then write it to CSV table.
        """
        title = response.css('.productPage__title::text').get()
        year = int(response.css('.productPage__subtitle::text').get()[-4::])
        data = {'Title': title, 'Year': year}
        self.writer_want.writerow(list(data.values()))

    async def parse_watched_movie_page(self, response):
        """
        Crawling watched movie for title, year,
        review data, time when it was watched.
        Then write it to CSV table.
        """
        parsed_details = r'profile_products:.*"modified_at":"(.*)T.*"rate":(10|[0-9]|).*"reviewed":(.*"body":"(.*)"}|)'
        title = response.css('.profileProduct__product_title::text').get()
        year = int(response.css('.profileProduct__product_date::text').get()[-4::])
        details = findall(parsed_details, response.css(".content script::text").get())[0]
        date, review, rate = details[0], details[3], ''
        if details[1] != '': rate = int(details[1])
        data = {'Title': title, 'Year': year, 'Rating10': rate, 'WatchedDate': date, 'Review': review}
        self.writer_watched.writerow(list(data.values()))

    def create_tables(self):
        """
        Creating empty tables for movies
        """
        self.want_file = open('want.csv', 'w', encoding='utf-8', newline='')
        self.watched_file = open('watched.csv', 'w', encoding='utf-8', newline='')
        self.writer_want = csv.writer(self.want_file)
        self.writer_watched = csv.writer(self.watched_file)
        columns_want = ['Title', 'Year']
        self.writer_want.writerow(columns_want)
        columns_watched = ['Title', 'Year', 'Rating10', 'WatchedDate', 'Review']
        self.writer_watched.writerow(columns_watched)

async def main():
    """
    Start crawler instance of MustappSpider with username
    from user input
    """
    MySpider = MustappSpider
    MySpider.username = input('Enter your nickname: ')
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()

if __name__ == "__main__":
    asyncio.run(main())
