from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "Lia" #name of the crawler, command: "scrapy crawl Jenny"
    with open('seed_urls.txt', 'r') as file:
        start_urls = [url.strip() for url in file.readlines()]
    # start_urls = ["https://www.schneier.com/"]  
    max_pages = 10  # Number of pages to crawl
    max_depth = 2   # Number of levels (hops) away from the seed URLs
    crawled_pages_counter = 0
    rules = (
        # Rule 1: Follow all links (allow=None) and parse the response using parse_item method
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
    download_delay = 2  # Set a download delay of 2 seconds so my server doesn't get rate-limited
    
    def parse_item(self, response):
        if self.crawled_pages >= self.max_pages:
            self.log("Maximum number of pages crawled reached. Stopping.")
            return
        
        # Check the depth of the current page
        depth = response.meta['depth']
        if depth > self.max_depth:
            self.log("Maximum depth reached for page {}. Stopping.".format(response.url))
            return
        
        title = response.css(".article h2::text").get()
        paragraphs = response.css(".article > :not(.entry-categories):not(.entry-tags)::text").getall() #scrape the article text, exclude title(.entry) and the category and tags
        article_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
        
        # yield {
        #     "title": title,
        #     "article": article_content
        # }
        filename = 'page_{}.txt'.format(self.crawled_pages_counter)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        self.log("Page {} crawled: {}".format(self.crawled_pages, response.url))
        
        self.crawled_pages_counter += 1
