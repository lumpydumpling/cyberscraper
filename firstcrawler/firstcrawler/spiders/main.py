import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from t1 import CrawlingSpider as Gerona
from realcrawler import CrawlingSpider as Lia
import sys

if(len(sys.argv) > 1):
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    pages = int(sys.argv[1])
    depth = int(sys.argv[2])
    process.crawl(Lia, max_pages=pages, max_depth=depth)
    # process.crawl(tyla, max_pages=pages, max_depth=depth)
    process.start()
else:
    print("Enter max pages and max depth")