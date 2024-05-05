from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

#must be in correct folder, /spiders to access seed_urls
class CrawlingSpider(CrawlSpider):
    name = "Gerona" #scrapy crawl Gerona
    with open('seed_urls.txt', 'r') as file:
        start_urls = [url.strip() for url in file.readlines()] # Read start URLs from file
    # Number of pages to crawl
    max_pages = 100
    # Number of levels (hops) away from the seed URLs
    max_depth = 6
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
        
        # for wikipedia pages
        title = response.xpath('//span[has-class("mw-page-title-main")]/text()').get() 
        if not title:
            title = response.css('h1::text').get()  
        if not title:
            title = response.css('header::text').get()  
        if not title:
            title = response.css('h2::text').get()  
        if not title:
            title = response.css('h3::text').get()  
        if not title:
            last_part = (response.url).rsplit('/', 1)[-1]
            # Split the last part by "-" and get the title
            title = last_part.split('-')
            # Join the title parts with spaces
            title = ' '.join(title)
        
        # text_content = ' '.join(response.css('.article .content p::text').getall())  # Example: Search for text within <p> tags with class "content" and "article", etc
        paragraphs = response.css(":not(.entry-categories):not(.entry-tags) p::text").getall() #.article > 
        text_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
        if not text_content:
            text_content = ' '.join(response.css('div.article ::text').getall()) 
        
        cybersecurity_keywords = ['cyber', 'security', 'hacker', 'threat', 'vulnerability']
        if any(keyword in text_content.lower() for keyword in cybersecurity_keywords):
            
        output_folder = 'scraped_pages'
        os.makedirs(output_folder, exist_ok=True)

        # Write scraped data to a text file
        filename = os.path.join(output_folder, 'page_{}.txt'.format(self.crawled_pages_counter))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'URL: {response.url}\n')
            f.write(f'Title: {title.lstrip()}\n')
            f.write(f'Text Content: {text_content}\n')
        
        self.log("Page {} crawled: {}".format(self.crawled_pages_counter, response.url))
        
        self.crawled_pages_counter += 1
