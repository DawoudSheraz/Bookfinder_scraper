# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import CsvItemExporter


class BookfinderPipeline(object):

    """
    Item pipeline to export extracted data
    """

    def __init__(self):
        """
        Initialize file where data would be saved
        """

        self.csv_exporter = CsvItemExporter(open('data.csv', 'wb'))
        self.csv_exporter.encoding = 'utf-8'
        self.csv_exporter.fields_to_export = [
            'url', 'title', 'isbn', 'authors', 'publisher', 'prices'
        ]
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        """
        Export current item.

        :param item: Current item
        :param spider: Spider that extracted data
        :return: item itself
        """
        self.csv_exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.csv_exporter.finish_exporting()
