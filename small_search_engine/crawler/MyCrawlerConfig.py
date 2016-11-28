

import re
import os.path


try:
    # For python 2
    from urlparse import urlparse, parse_qs
except ImportError:
    # For python 3
    from urllib.parse import urlparse, parse_qs

from Crawler4py.Config import Config

class MyCrawlerConfig(Config):
    def __init__(self):
        Config.__init__(self)
        
        self.UserAgentString = "UCI Inf141-CS121 crawler 24427400 59359881 33062456 62838370"
        if os.path.exists('count.txt'):
		with open('count.txt','r') as file:
			self.count = int(file.readline())
	else:
		self.count = 0
        self.PolitenessDelay = 1200

    def GetSeeds(self):

        '''Returns the first set of urls to start crawling from'''
        return ["http://www.ics.uci.edu"]

    def HandleData(self, parsedData):
        '''Function to handle url data. Guaranteed to be Thread safe.
        parsedData = {"url" : "url", "text" : "text data from html", "html" : "raw html data"}
        Advisable to make this function light. Data can be massaged later. Storing data probably is more important'''

        url = parsedData["url"].encode("utf8")
        text =parsedData["text"].encode("utf8")
        
	
        with open('data/'+ str(self.count)+ '.txt', 'w') as file1:
            file1.write( text )


        with open('url.txt', 'a') as file2:
            file2.write( str(self.count) + "," + url + "\n")

        self.count += 1

        with open('count.txt','w') as file3:
            file3.write( str(self.count))


        return

    def ValidUrl(self, url):
        '''Function to determine if the url is a valid url that should be fetched or not.'''
        parsed = urlparse(url)
        try:
            return ".ics.uci.edu" in parsed.hostname \
                and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
			    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
			    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
			    + "|thmx|mso|arff|rtf|jar|csv"\
			    + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path)

        except TypeError:
            print ("TypeError for ", parsed)


