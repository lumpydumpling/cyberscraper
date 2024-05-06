from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import os

class CrawlingSpider(CrawlSpider):
    name = "Lia" #name of the crawler, command: "scrapy crawl Lia"
    # with open('seed_urls.txt', 'r') as file:
    #     start_urls = [url.strip() for url in file.readlines()]
    if os.path.exists('scraped_pages'):
        os.system('rm -rf scraped_pages') # Remove the folder and its contents
    start_urls = ["https://www.schneier.com/"]  
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
        
        #title is text content of span with certain class
#         text = []
#         links = []
#         #title = response.xpath('//span[has-class("mw-page-title-main")]/text()').get()
#         paragraphs = """<p><b>Unix</b> (<span class="rt-commentedText nowrap"><span class="IPA nopopups noexcerpt" lang="en-fonipa"><a href="/wiki/Help:IPA/English" title="Help:IPA/English">/<span style="border-bottom:1px dotted"><span title="/ˈ/: primary stress follows">ˈ</span><span title="/j/: 'y' in 'yes'">j</span><span title="/uː/: 'oo' in 'goose'">uː</span><span title="'n' in 'nigh'">n</span><span title="/ɪ/: 'i' in 'kit'">ɪ</span><span title="'k' in 'kind'">k</span><span title="'s' in 'sigh'">s</span></span>/</a></span> <span class="ext-phonos skin-invert"><span data-nosnippet="" id="ooui-php-1" class="ext-phonos-PhonosButton noexcerpt ext-phonos-PhonosButton-emptylabel oo-ui-widget oo-ui-widget-enabled oo-ui-buttonElement oo-ui-buttonElement-frameless oo-ui-iconElement oo-ui-buttonWidget" data-ooui="{&quot;_&quot;:&quot;mw.Phonos.PhonosButton&quot;,&quot;href&quot;:&quot;\/\/upload.wikimedia.org\/wikipedia\/commons\/transcoded\/c\/c8\/En-us-Unix.oga\/En-us-Unix.oga.mp3&quot;,&quot;rel&quot;:[&quot;nofollow&quot;],&quot;framed&quot;:false,&quot;icon&quot;:&quot;volumeUp&quot;,&quot;data&quot;:{&quot;ipa&quot;:&quot;&quot;,&quot;text&quot;:&quot;&quot;,&quot;lang&quot;:&quot;en&quot;,&quot;wikibase&quot;:&quot;&quot;,&quot;file&quot;:&quot;En-us-Unix.oga&quot;},&quot;classes&quot;:[&quot;ext-phonos-PhonosButton&quot;,&quot;noexcerpt&quot;,&quot;ext-phonos-PhonosButton-emptylabel&quot;]}"><a role="button" tabindex="0" href="//upload.wikimedia.org/wikipedia/commons/transcoded/c/c8/En-us-Unix.oga/En-us-Unix.oga.mp3" rel="nofollow" aria-label="Play audio" title="Play audio" class="oo-ui-buttonElement-button"><span class="oo-ui-iconElement-icon oo-ui-icon-volumeUp"></span><span class="oo-ui-labelElement-label"></span><span class="oo-ui-indicatorElement-indicator oo-ui-indicatorElement-noIndicator"></span></a></span><sup class="ext-phonos-attribution noexcerpt navigation-not-searchable"><a href="/wiki/File:En-us-Unix.oga" title="File:En-us-Unix.oga">ⓘ</a></sup></span></span>, <a href="/wiki/Help:Pronunciation_respelling_key" title="Help:Pronunciation respelling key"><i title="English pronunciation respelling"><span style="font-size:90%">YOO</span>-niks</i></a>; trademarked as <b>UNIX</b>) is a family of <a href="/wiki/Computer_multitasking" title="Computer multitasking">multitasking</a>, <a href="/wiki/Multi-user_software" title="Multi-user software">multi-user</a> computer <a href="/wiki/Operating_system" title="Operating system">operating systems</a> that derive from the original <a href="/wiki/AT%26T_Corporation" title="AT&amp;T Corporation">AT&amp;T</a> Unix, whose development started in 1969<sup id="cite_ref-reader_1-1" class="reference"><a href="#cite_note-reader-1">[1]</a></sup> at the <a href="/wiki/Bell_Labs" title="Bell Labs">Bell Labs</a> research center by <a href="/wiki/Ken_Thompson" title="Ken Thompson">Ken Thompson</a>, <a href="/wiki/Dennis_Ritchie" title="Dennis Ritchie">Dennis Ritchie</a>, and others.<sup id="cite_ref-Ritchie_4-0" class="reference"><a href="#cite_note-Ritchie-4">[4]</a></sup>
# </p>""" #scrape the article text, exclude title(.entry) and the category and tags
#         print(paragraphs)
#         article_content = ''.join(word for word in Selector(text=paragraphs).css("b::text,p::text,a::text").getall() if not word.startswith('['))
#         #article_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
#         #print(title)
#         print(article_content)
        meta_description = response.xpath('//meta[@name="description"]/@content').get()

        title = response.css('h1::text').get()  
        paragraphs = response.css(":not(.entry-categories):not(.entry-tags) p::text").getall() #.article > 
        text_content = ' '.join([p.strip() for p in paragraphs if p.strip()])
        if not text_content:
            text_content = ' '.join(response.css('div.article ::text').getall()) 
        yield {
            "title": title,
            "article": text_content,
            "meta": meta_description
        }
        # filename = 'page_{}.txt'.format(self.crawled_pages_counter)
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(article_content)
        
        self.log("Page {} crawled: {}".format(self.crawled_pages_counter, response.url))
        
        self.crawled_pages_counter += 1
