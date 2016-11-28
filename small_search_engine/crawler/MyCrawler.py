

from Crawler4py.Crawler import Crawler
from MyCrawlerConfig import MyCrawlerConfig


crawler = Crawler(MyCrawlerConfig())


print (crawler.StartCrawling())

exit(0)
