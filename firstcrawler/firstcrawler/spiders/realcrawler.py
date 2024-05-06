from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os
from scrapy.exceptions import CloseSpider


class CrawlingSpider(CrawlSpider):
    name = "Lia" #name of the crawler, command: "scrapy crawl Lia"
    total_data_size = 0  # Track cumulative size of crawled data
    max_data_size = 500 * 1024 * 1024

    start_urls = ["https://www.linux.com", "https://www.kali.org/tools/",
     "https://www.redhat.com/en/topics", "https://medium.com/cybersecurity-science",
    "https://docs.metasploit.com/", "https://cplusplus.com/doc/tutorial/", "https://www.ibm.com/topics", 
   "https://www.computernetworkingnotes.com/ccna-study-guide/", 
    "https://www.tutorialspoint.com/powershell/", "https://www.techtarget.com/searchwindowsserver/definition/PowerShell",
    "https://www.esecurityplanet.com/networks/how-to-set-up-a-firewall/" 
    #  "https://www.schneier.com/", "https://www.geeksforgeeks.org/basics-computer-networking/", "https://ubuntuforums.org/", "https://www.cisco.com/c/en/us/td/docs/routers/access/cisco_router_and_security_device_manager/24/software/user/guide/Fwall.html",
    # "https://www.cisco.com/c/en/us/support/all-products.html", "https://www.cisco.com/c/en/us/tech/index.html", 
]
    
    # start_urls = ["https://www.schneier.com/", "https://www.redhat.com/en/topics", "https://medium.com/cybersecurity-science"]    
    # start_urls = ["https://docs.metasploit.com/", "https://cplusplus.com/doc/tutorial/", "https://www.ibm.com/topics", "https://www.geeksforgeeks.org/basics-computer-networking/", "https://www.computernetworkingnotes.com/ccna-study-guide/", "https://www.tutorialspoint.com/powershell/", "https://www.techtarget.com/searchwindowsserver/definition/PowerShell"]    
    #     start_urls = ["https://www.esecurityplanet.com/networks/how-to-set-up-a-firewall/", "https://www.cisco.com/c/en/us/td/docs/routers/access/cisco_router_and_security_device_manager/24/software/user/guide/Fwall.html", "https://www.cisco.com/c/en/us/support/all-products.html", "https://www.cisco.com/c/en/us/tech/index.html", "https://docs.paloaltonetworks.com/", "https://docs.paloaltonetworks.com/ngfw"]    
    max_pages = 100  # Number of pages to crawl
    max_depth = 6   # Number of levels (hops) away from the seed URLs
    crawled_pages_counter = 0
    rules = (
        # Rule 1: Follow all links (allow=None) and parse the response using parse_item method
        Rule(LinkExtractor(), callback='parse_item', follow=False),
    )
    download_delay = 2  # Set a download delay of 2 seconds so my server doesn't get rate-limited
    
    def parse_item(self, response):
        if self.crawled_pages_counter >= self.max_pages:
            self.log("Maximum number of pages crawled reached. Stopping.")
            return
        
        # Check the depth of the current page
        depth = response.meta['depth']
        if depth > self.max_depth:
            self.log("Maximum depth reached for page {}. Stopping.".format(response.url))
            return
        
        paragraphs = response.css(":not(.entry-categories):not(.entry-tags) ::text").getall() 

        # Original method
        text_content = ' '.join([p for p in paragraphs if p.strip()])
        if not text_content:
            text_content = ''.join(response.css('div.article p::text').getall()) 
        
        # Method which supports links and bold text in content
        text_content = ''
        for p in paragraphs:
            selector = Selector(text=p)
            text_content = text_content + ''.join(response.css("p::text,b::text,a::text").getall())
        
        # Removes newlines and tab characters in text_content
        text_content = text_content.replace('\n', '').replace('\t', '')

        with open('handle.txt', 'r') as file:
            keywords = [keyword.strip() for keyword in file.readlines()]
            
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
        yield {
            "title": title,
            "article": text_content,
        }
        data_size = len(text_content.encode('utf-8'))  # Convert to bytes; returns the number of bytes required to encode the string in UTF-8
        self.total_data_size += data_size
        if self.total_data_size >= self.max_data_size or self.crawled_pages_counter >= self.max_pages: #explicitly accessing the max_data_size attribute of the current instance of the class CrawlingSpider as opposed to local variables
                self.log(f"Maximum data size reached. Crawling stopped.")
                raise CloseSpider("Maximum data size reached")
            
        filename = 'attempt5.txt'  # Specify the filename for the combined text file
        with open(filename, 'a', encoding='utf-8') as f:  # Use 'a' mode to append to the file
            f.write(f'URL: {response.url}\n')
            f.write(f'Title: {title}\n')
            f.write(f'Text Content: {text_content}\n')  
            f.write(f'Data: {data_size} Bytes \n')
            f.write(f'total data: {self.total_data_size} Bytes \n\n') 
        
        self.log("Page {} crawled: {}".format(self.crawled_pages_counter, response.url))
        
        self.crawled_pages_counter += 1
