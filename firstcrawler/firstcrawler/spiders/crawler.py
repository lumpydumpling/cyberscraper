from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "Jenny" #name of the crawler, use like "scrapy crawl Jenny"
    start_url = ["https://www.kali.org/tools/"]
    rules = (
        Rule(LinkExtractor(allow= "")) #only look for 
    )