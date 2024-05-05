from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

#must be in correct folder, /spiders to access seed_urls
class CrawlingSpider(CrawlSpider):
    name = "Gerona" #scrapy crawl Gerona
    total_data_size = 0  # Track cumulative size of crawled data
    max_data_size = 500 * 1024 * 1024  # Maximum data size in bytes (500 MB)
    
    if os.path.exists('scraped_pages'):
        os.system('rm -rf scraped_pages') # Remove the folder and its contents
    
    with open('seed_urls.txt', 'r') as file:
        start_urls = [url.strip() for url in file.readlines()] # Read start URLs from file
    max_pages = 10000    # Number of pages to crawl
    max_depth = 60     # Number of levels (hops) away from the seed URLs
    crawled_pages_counter = 0     # Counter for crawled pages
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),         # Rule: Follow all links and parse the response using parse_item method
    )
    download_delay = 2  # Set a download delay of 2 seconds to avoid rate limiting
    
    def parse_item(self, response):
        if self.crawled_pages_counter >= self.max_pages:
            self.log("Maximum number of pages crawled reached. Stopping.")
            return
        
        # Check the depth of the current page
        depth = response.meta['depth'] #When the crawler follows a link and sends a new request to fetch another page, it includes the curr depth as part of the request metadata
        if depth > self.max_depth:
            self.log("Maximum depth reached for page {}. Stopping.".format(response.url))
            return
        
        # text_content = ' '.join(response.css('.article .content p::text').getall())  # Example: Search for text within <p> tags with class "content" and "article", etc
        paragraphs = response.css(":not(.entry-categories):not(.entry-tags) p::text").getall() #.article > 
        text_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
        if not text_content:
            text_content = ' '.join(response.css('div.article ::text').getall()) 
        
        # print(text_content)
        # print("")
        
        with open('keywords.txt', 'r') as file:
            keywords = [keyword.strip() for keyword in file.readlines()]
        if any(keyword in text_content.lower() for keyword in keywords):
            # for wikipedia pages
            title = response.xpath('//title/text()').get()
            if not title:
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
            
            # removes leading whitespace
            title = title.lstrip()

            # removes newlines
            title = title.replace("\n","")

            #removes domain name from title
            title = title.split(" |")[0]
            title = title.split(" -")[0]
            #alternatively, title = re.sub(r' \|.*| -.*', '', title)  # Remove domain names from title
            # print(title)
            
            data_size = len(text_content.encode('utf-8'))  # Convert to bytes; returns the number of bytes required to encode the string in UTF-8
            self.total_data_size += data_size #accessing the instance variable within the class
            if self.total_data_size >= self.max_data_size: #explicitly accessing the max_data_size attribute of the current instance of the class CrawlingSpider as opposed to local variables
                self.log(f"Maximum data size reached. Crawling stopped.")
                raise CloseSpider("Maximum data size reached")
        
            output_folder = 'scraped_pages'
            os.makedirs(output_folder, exist_ok=True)

            # Write scraped data to a text file
            filename = os.path.join(output_folder, 'page_{}.txt'.format(self.crawled_pages_counter))
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'URL: {response.url}\n')
                f.write(f'Title: {title}\n')
                f.write(f'Text Content: {text_content}\n')
                f.write(f'Data: {data_size} Bytes \n')
                f.write(f'total data: {self.total_data_size} Bytes \n')
            
            self.log("Page {} crawled: {}".format(self.crawled_pages_counter, response.url))
            
            self.crawled_pages_counter += 1
