from lxml import html
from lxml.html.clean import Cleaner
from math import log
import os
import re
import json
import time

class Indexer(object):
    def __init__(self):
        self.term2termID = {}               #{'apple':0, 'zoo': 3}
        self.docID2doc = {}                 #{0:'an article about apple', 1:'an article about cat'}
        self.docID2termIDs = {}             #{docID1:[termID1,termID2], docID2:[termID5,termID9]}
        self.termId2docFre = {}             #{termID1: 10, termID2: 15} #term1 shows up in 10 documents
        self.termCount = 0 
        self.docCount = 0
        self.postingLists = {}              #{termID1:{docID1:5.4553,docID5:0.324},termID2:{docID9:2.023,docID15:1.998}}

    def get_content(self, pathName):
        try:
            file = open(pathName, "r")
            html_text = file.read()
            file.close()
        except:
            print("Fail to open the file located in {}".format(pathName))
            return None
        try:
            cleaner = Cleaner()
            cleaner.javascript = True
            cleaner.style = True
            htmlData = cleaner.clean_html(html_text)
        except:
            print("Could not remove style and js code from the file located in {}".format(pathName))
            return None
        return html.fromstring(htmlData).text_content()

    def parse(self,raw_content):
        raw_content.encode("utf-8")
        terms = re.split("[^a-zA-Z0-9]+",raw_content)
        self.docID2termIDs[self.docCount] = []
        for term in terms:
            if(len(term) != 0):
                term = term.lower()
                if term not in self.term2termID:
                    self.term2termID[term] = self.termCount
                    self.termCount += 1
                self.docID2termIDs[self.docCount].append(self.term2termID[term])
        self.docCount += 1

    def load_data(self, pathname):
        jsonFile = open(pathname)
        data = json.load(jsonFile)
        jsonFile.close()
        dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Html")
        for i in range(len(data)):
            self.docID2doc[self.docCount] = data[str(i)]["url"].encode("utf-8")
            filepath = os.path.join(dirpath, data[str(i)]["file"].encode("utf-8"))
            content = self.get_content(filepath)
            if content != None:
                self.parse(content)

    def build_postingLists(self):
        for termID in range(self.termCount):
        	self.postingLists[termID] = {}
        for docID in range(self.docCount):
            for termID in self.docID2termIDs[docID] :
                if docID not in self.postingLists[termID]:
                    self.postingLists[termID][docID] = 0
                self.postingLists[termID][docID] += 1    

    def build_termId2docFre(self):
        for termID in range(self.termCount):
            self.termId2docFre[termID] = len(self.postingLists[termID])

    #we only call WTF when term_frequency != 0
    def WTF(self, term_frequency):
        # if term_frequency == 0:
        #     return 0
        return 1 + log(term_frequency,10)

    def IDF(self, doc_frequency):
        return log((self.docCount / doc_frequency), 10)

    def compute_TF_IDF(self):
        for termID in range(self.termCount):
            for docID in self.postingLists[termID]:
                term_frequency = self.postingLists[termID][docID]
                doc_frequency = self.termId2docFre[termID]
                self.postingLists[termID][docID] = self.WTF(term_frequency) * self.IDF(doc_frequency)

    def write_postingLists(self):
        with open('postingLists.json', 'w') as f:
            json.dump(self.postingLists, f)
        
        
#        with open('postingLists.txt', 'w') as file:
#        	for termID in self.postingLists:
#        		file.write(str(termID)+":{")
#        		for docID in self.postingLists[termID]:
#        			file.write(str(docID)+":"+str(self.postingLists[termID][docID])+",")
#        		file.write("}\n")

    def write_term2termID(self):
        with open('term2termID.json', 'w') as f:
            json.dump(self.term2termID, f)
        
#        with open('term2termID.txt', 'w') as file:
#        	for term in self.term2termID:
#        		file.write(str(term)+":"+str(self.term2termID[term])+"\n")

    def write_docID2doc(self):
        with open('docID2doc.json', 'w') as f:
            json.dump(self.docID2doc, f)

#        with open('docID2doc.txt', 'w') as file:
#        	for doc in self.docID2doc:
#        		file.write(str(doc)+":"+str(self.docID2doc[doc])+"\n")

    def write_docID2termIDs(self):
        with open('docID2termIDs.json', 'w') as f:
            json.dump(self.docID2termIDs, f)
                
#        with open('docID2termIDs.txt', 'w') as file:
#        	for docID in self.docID2termIDs:
#        		file.write(str(docID)+":[")
#        		for termID in self.docID2termIDs[docID]:
#        			file.write(str(termID)+",")
#        		file.write("]\n")

    def write_termId2docFre(self):
        with open('termId2docFre.json', 'w') as f:
            json.dump(self.termId2docFre, f)
        
#        with open('termId2docFre.txt', 'w') as file:
#        	for termID in self.termId2docFre:
#        		file.write(str(termID)+":"+str(self.termId2docFre[termID])+"\n")

    def write_indices_to_disk(self):
    	self.write_postingLists()
    	self.write_term2termID()
    	self.write_docID2doc()
    	self.write_docID2termIDs()
    	self.write_termId2docFre()


if __name__ == "__main__":
    #start_time = time.time()
    myIndexer = Indexer()
    myIndexer.load_data("html_files.json")
    myIndexer.build_postingLists()
    myIndexer.build_termId2docFre()
    myIndexer.compute_TF_IDF()
    myIndexer.write_indices_to_disk()
    #print("--- %s seconds ---" % (time.time() - start_time))




