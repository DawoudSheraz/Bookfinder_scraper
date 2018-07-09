import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import FormRequest
from bookfinderSpider.items import BookfinderItem, BookfinderItemLoader


class BookfinderSpider(CrawlSpider):

    name = "Bookfinder"
    start_urls = [
        'https://www.bookfinder.com/',
    ]

    def parse(self, response):

        input_data = open('isbn.txt', 'r')
        out = [isbn for isbn in input_data]

        for every_entry in out:
            yield FormRequest.from_response(
                response, formname="search_form",
                formdata={
                    'isbn': every_entry
                },
                callback=self.save_book_data
            )

    def save_book_data(self, response):

        # open('temp.html', 'w').write(response.body)

        book_finder_item_loader = BookfinderItemLoader(BookfinderItem())

        book_finder_item_loader.add_value('url', response.url)
        book_finder_item_loader.add_value('authors', self.get_authors_names(response))
        book_finder_item_loader.add_value('prices', self.get_prices_list(response))
        book_finder_item_loader.add_value('title', self.get_book_title(response))
        book_finder_item_loader.add_value('publisher', self.get_publisher_name(response))
        book_finder_item_loader.add_value('isbn', self.get_isbn(response))

        yield book_finder_item_loader.load_item()

    def get_prices_list(self, response):
        """
        Returns all available prices for a book.

        :param response: Fetched Page
        :return: list of prices
        """

        data_table = response.css('.results-table-LogoRow.has-data')
        return [temp.xpath('td[4]/div/span/a/text()').extract_first(default='') for temp in data_table]

    def get_book_title(self, response):
        """
        Returns book title
        """
        return response.css("#describe-isbn-title::text").extract_first(default='')

    def get_authors_names(self, response):
        """
        Returns author names for a given book.

        :param response: fetched page
        :return: comma separated string of author names
        """
        return response.xpath('//*[@id="bd-isbn"]/div/div[2]/div[2]/p/strong/a/span/text()').extract_first(default='')

    def get_publisher_name(self, response):
        """
        Returns the book publisher name and year.

        :param response: fetched page
        :return: publisher info
        """
        return response.css('.describe-isbn::text').extract_first(default='')

    def get_isbn(self, response):
        return response.xpath('//*[@id="bd-isbn"]/div/div[2]/div[1]/h1/text()').extract_first(default='')
