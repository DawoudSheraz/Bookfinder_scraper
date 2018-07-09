# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


class BookfinderItem(scrapy.Item):

    """
    Data Model to save extracted Items
    """

    url = Field()
    title = Field()
    prices = Field()
    authors = Field()
    publisher = Field()
    isbn = Field()


def remove_commas(x):
    """
    To remove , and ; from a string

    :param x: string
    :return: string without , and ;
    """
    out_val = x
    try:
        out_val = x.replace(',', '').replace(';', '')
    except:
        pass
    return out_val


def replace_commas(x):
    """
    To replace , and ; from a string with |

    :param x: string
    :return: string without , and ;
    """
    out_val = x
    try:
        out_val = x.replace(',', '|').replace(';', '|')
    except:
        pass
    return out_val


def remove_slashes(x):
    """
    To remove / from string

    :param x: string
    :return: string without /
    """
    out_val = x
    try:
        out_val = x.replace('/', '')
    except:
        pass
    return out_val


class BookfinderItemLoader(ItemLoader):

    """
    ItemLoader class to filter individual fields.

    """

    default_input_processor = MapCompose(remove_tags)
    default_output_processor = Join()

    prices_in = MapCompose(remove_tags, remove_commas)
    prices_out = Join(';')

    authors_in = MapCompose(remove_tags, replace_commas)

    isbn_in = MapCompose(remove_slashes)




