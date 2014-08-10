#!/usr/bin/env python
"""
Lists the devices currently connected to a Virgin SuperHub 2
"""
import argparse
import getpass

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals

from superhub.spiders.connected_device_spider import ConnectedDeviceSpider

class ItemCollector:
    def __init__(self):        
        self.items = []

    def add_item(self, item):
        self.items.append(item)

def get_connected_devices(ip_address, password, loglevel="WARNING"):
    spider = ConnectedDeviceSpider(ip_address, password)
    collector = ItemCollector()
    crawler = Crawler(Settings())
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.signals.connect(collector.add_item, signals.item_passed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start(loglevel=loglevel, logstdout=False)
    reactor.run() # the script will block here
    return collector.items

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ip-address", default="192.168.0.1", help="IP address of the SuperHub [DEFAULT: 192.168.0.1]")
    parser.add_argument("--password", help="SuperHub password (will prompt if not specified)")
    parser.add_argument("--debug", action="store_true", help="Turn on Scrapy debugging")
    args = parser.parse_args()

    if args.password is None:
        args.password = getpass.getpass("SuperHub Password >")

    if args.debug:
        loglevel = "DEBUG"
    else:
        loglevel = "WARNING"

    items = get_connected_devices(args.ip_address, args.password, loglevel)

    for item in items:
        print "%s : %s" % (item["ip_address"], item["device_name"])

if __name__ == "__main__":
    main()
