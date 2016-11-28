#put this file the same level as url.txt
import os
import CommonWords

def main():
    result = {}
    with open("url.txt", "r") as infile:
        url = infile.readlines()
        print("Question 2:",len(url))
        findSubdomain(url)
        print("Question 4:",findLongestPage(url))
        MostCommonWord(url)

def findSubdomain(url: list):
    result = {}
    listforSort = []
    for i in url:
        x = i.split(",")
        newurl = x[1][:-1]
        findIndex = newurl.find("ics.uci.edu")
        findstart = newurl.find("://")
        if findIndex > 11:
            mainpage = newurl[findstart+3:findIndex] + "ics.uci.edu"
            if mainpage in result:
                result[mainpage]+=1
            else:
                listforSort.append(mainpage)
                result[mainpage] = 1
    listforSort.sort()
    with open('Subdomains.txt', 'w') as file:
        for i in listforSort:
            file.write(i + ", " + str(result[i]) + "\n")


def findLongestPage(url: list):
    dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    MaxWord = [0,0]
    for i in range(len(url)):
        filename = "{}.txt".format(i)
        data = os.path.join(dirpath, filename)
        length = len(CommonWords.tokenizeFile(data))
        if length > MaxWord[1]:
            MaxWord[1] = length
            MaxWord[0] = i
    for i in url:
        x = i.split(",")
        if x[0] == str(MaxWord[0]):
            return [ x[1][:-1] , MaxWord[1] ]


def MostCommonWord(url: list):
    dirpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "data")
    result = []
    counter = 0
    top500 = []
    stopwords = ['a',
    'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an',
    'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because',
    'been', 'before', 'being', 'below', 'between', 'both', 'but',
    'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't",
    'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
    'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has',
    "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll",
    "he's", 'her', 'here', "here's", 'hers', 'herself', 'him',
    'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm",
    "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its',
    'itself', "let's", 'me', 'more', 'most', "mustn't", 'my',
    'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only',
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',
    'own', 'same', "shan't", 'she', "she'd", "she'll", "she's",
    'should', "shouldn't", 'so', 'some', 'such', 'than', 'that',
    "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then',
    'there', "there's", 'these', 'they', "they'd", "they'll",
    "they're", "they've", 'this', 'those', 'through', 'to', 'too',
    'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd",
    "we'll", "we're", "we've", 'were', "weren't", 'what', "what's",
    'when', "when's", 'where', "where's", 'which', 'while', 'who',
    "who's", 'whom', 'why', "why's", 'with', "won't", 'would',
    "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your',
    'yours', 'yourself', 'yourselves']
    for i in range(len(url)):
        filename = "{}.txt".format(i)
        data = os.path.join(dirpath, filename)
        tokens = CommonWords.tokenizeFile(data)
        result.extend(tokens)
    DictResult = CommonWords.computeWordFrequencies(result)
    for i in sorted(DictResult, key = DictResult.get, reverse = True):
        if counter == 500:
            break
        if i not in stopwords:
            top500.append((i, DictResult[i]))
            counter += 1
    top500.sort(key = lambda x: x[0])
    top500.sort(key = lambda x: x[1], reverse = True)
    print(top500)
    with open('CommonWords.txt', 'w') as file:
        for i in top500:
            file.write(i[0]  + "\n")
    




if __name__ == "__main__":
    main()
