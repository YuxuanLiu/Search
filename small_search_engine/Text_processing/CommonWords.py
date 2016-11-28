import re

def tokenizeFile(pathName):
	with open(pathName, 'r') as file1:
		tokens = []
		for line in file1.readlines():
			s = line.strip()

			wordList = re.split("[^a-zA-Z]*", s)
			for w in wordList:
				if len(w) > 1:
					tokens.append(w.lower())
		return tokens

def computeWordFrequencies(words):
	wordCount = {}
	for word in words:
		if word not in wordCount:
			wordCount[word] = 1
		else:
			wordCount[word] += 1
	return wordCount



#l = tokenizeFile("/Users/lewis/Desktop/CS121/0.txt")
#print()
#print(l)
#print()
#print(computeWordFrequencies(l))
