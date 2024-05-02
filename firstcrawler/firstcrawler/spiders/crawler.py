from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "Jenny" #name of the crawler, command: "scrapy crawl Jenny"
    allowed_domains = ["schneier.com"] #restrict crawler to this website, or else it'll start scraping the whole web
    start_urls = ["https://www.schneier.com/"]  
    rules = (
        # Rule 1: Follow all links (allow=None) and parse the response using parse_item method
        Rule(LinkExtractor(allow = "news/"), callback='parse_item', follow=True),
    )
    download_delay = 2  # Set a download delay of 2 seconds so my server doesn't get rate-limited
    
    def parse_item(self, response):
        title = response.css(".article h2::text").get()
        paragraphs = response.css(".article > *:not(.entry):not(.entry-categories):not(.entry-tags)::text").getall() #scrape the article text, exclude title(.entry) and the category and tags
        article_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
        
        yield {
            "title": title,
            "article": article_content
        }
    
'''
command to run: scrapy crawl Jenny
this will run the crawler and output title and article for each link in schneier.com/news

run: scrapy crawl Jenny -o output.json
to save output in a json file

should prob cntrl c twice to stop crawler at some point
'''