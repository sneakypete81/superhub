# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ConnectedDeviceItem(scrapy.Item):
    device_name = scrapy.Field()
    ip_address = scrapy.Field()
    mac_address = scrapy.Field()
    time_connected = scrapy.Field()
    is_wired = scrapy.Field()