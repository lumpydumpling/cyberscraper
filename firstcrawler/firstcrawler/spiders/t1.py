from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "Gerona" #scrapy crawl Gerona
    # Read start URLs from file
    with open('seed_urls.txt', 'r') as file:
        start_urls = [url.strip() for url in file.readlines()]
    # Number of pages to crawl
    max_pages = 10
    # Number of levels (hops) away from the seed URLs
    max_depth = 2
    # Counter for crawled pages
    crawled_pages_counter = 0
    rules = (
        # Rule: Follow all links and parse the response using parse_item method
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )
    download_delay = 2  # Set a download delay of 2 seconds to avoid rate limiting
    
    def parse_item(self, response):
        if self.crawled_pages_counter >= self.max_pages:
            self.log("Maximum number of pages crawled reached. Stopping.")
            return
        
        # Check the depth of the current page
        depth = response.meta['depth']
        if depth > self.max_depth:
            self.log("Maximum depth reached for page {}. Stopping.".format(response.url))
            return
        
        title = response.css(".article h2::text").get()
        # Scrape the article text, excluding title and the category and tags
        paragraphs = response.css(".article > :not(.entry-categories):not(.entry-tags)::text").getall()
        article_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
        
        # Write article content to a text file
        filename = 'page_{}.txt'.format(self.crawled_pages_counter)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        self.log("Page {} crawled: {}".format(self.crawled_pages_counter, response.url))
        
        self.crawled_pages_counter += 1
