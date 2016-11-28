#Tianya Chen 59359881, Lewis Liu 24427400, Kaiyi Ma 62838370, Jianyu Zheng 33062456
#Please run this Python script using Python 2.7
import re
import json
import operator
import os
from math import log, sqrt
import time

class SearchEng(object):
    def __init__(self):
        self.termIDs = []
        self.term2tfidf = {}
        self.docID2doc = {}
        self.termId2docFre = {}
        self.docID2score = {}
        self.postingLists = {}
        self.magnitude = {}
        self.docCount = 0

    def load_data(self):
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docID2doc.json')
        with open(fileName, 'r') as file:       
            self.docID2doc = json.load(file)
        self.docCount = len(self.docID2doc)
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'termId2docFre.json')
        with open(fileName, 'r') as file:       
            self.termId2docFre = json.load(file)
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postingLists.json')
        with open(fileName, 'r') as file:
            self.postingLists = json.load(file)
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'magnitude.json')
        with open(fileName, 'r') as file:
            self.magnitude = json.load(file)

    def get_termIDs(self, input):
        listOfTerms = re.split("[^a-zA-Z0-9]+",input.lower())
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'term2termID.json')
        with open(fileName, 'r') as file:
            temp = json.load(file)
        for term in listOfTerms:
            if term in temp.keys():
                self.termIDs.append(temp[term])

    def calculate_term_tfidf(self):
        for termID in self.termIDs:
            if termID not in self.term2tfidf:
                self.term2tfidf[termID] = 1
            else:
                self.term2tfidf[termID] += 1
        for termID in self.term2tfidf:
            self.term2tfidf[termID] = (1 + log(self.term2tfidf[termID],10))*(self.docCount/self.termId2docFre[str(termID)])

    #Efficient Cosine Ranking
    def calculate_doc_score(self): 
        for termID in self.term2tfidf:
            queryTermScore = self.term2tfidf[termID]
            for docID in self.postingLists[str(termID)]:
                if docID not in self.docID2score:
                    self.docID2score[docID] = 0
                self.docID2score[docID] += queryTermScore*(self.postingLists[str(termID)][docID])
        for docID in self.docID2score:
            self.docID2score[docID] /= sqrt(self.magnitude[docID])
        self.docID2score = sorted(self.docID2score.items(), key=operator.itemgetter(1),reverse=True)

    #Below is our original way of calculating scores for related documents (without using cosine similarity)
    #But we did normalized scores for documents
    def calculate_tfidf_original(self):
        for termID in self.termIDs:
            for docID in self.postingLists[str(termID)]:
                if docID not in self.docID2score:
                    self.docID2score[docID] = 0
                self.docID2score[docID] += self.postingLists[str(termID)][docID]
        for docID in self.docID2score:
            self.docID2score[docID] /= sqrt(self.magnitude[docID])
        self.docID2score = sorted(self.docID2score.items(), key=operator.itemgetter(1),reverse=True)

    def return_urls(self):
        result = []
        for pair in self.docID2score[:10]:
            result.append(self.docID2doc[pair[0]])
        return result

    def return_top10(self, inputs):
        self.load_data()
        self.get_termIDs(inputs)
        self.calculate_term_tfidf()
        self.calculate_doc_score()
        #self.calculate_tfidf_original()
        return self.return_urls()

if __name__ == "__main__":
    query = raw_input("Please input the query: ")
    # start_time = time.time()
    MyEngine = SearchEng()
    result = MyEngine.return_top10(query)
    for url in result:
        print(url[0])
    # print("Time elapsed: {}".format(time.time() - start_time))

