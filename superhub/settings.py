# -*- coding: utf-8 -*-

# Scrapy settings for superhub project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'superhub'

SPIDER_MODULES = ['superhub.spiders']
NEWSPIDER_MODULE = 'superhub.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'superhub (+https://github.com/sneakypete81/superhub)'
