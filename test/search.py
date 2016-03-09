import re
import json
import operator
import os

test = "machine learning"

class SearchEng(object):
	def __init__(self):
		self.token = []
		self.term2tf_idf = {}
		self.docID2score = {}
		self.docID2doc = {}


	def get_token(self, inputs):
		inputs = inputs.lower()
		self.token = re.split("[^a-zA-Z0-9]+",inputs)
		file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'term2termID.json')
		with open(file_name, 'r') as f:
			temp =  json.load(f)
		for i in range(len(self.token)):
			if self.token[i] in temp.keys():
				self.token[i] = temp[self.token[i]]
			else:
				self.token[i] = None

	def calculate_tf_idf(self):
		file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'postingLists.json')
		with open(file_name, 'r') as f:
			temp =  json.load(f)

		for token in self.token:
			if token != None:
				self.term2tf_idf[token] = temp[ unicode(token)]
			else:
				self.term2tf_idf[token] = 0

		for doclist in self.term2tf_idf.values():
			if type(doclist) == dict:
				for key in doclist:
					if key.encode("utf-8") in self.docID2score:
						self.docID2score[key.encode("utf-8")] += doclist[key]
					else:
						self.docID2score[key.encode("utf-8")] = doclist[key]

		self.docID2score = sorted(self.docID2score.items(), key=operator.itemgetter(1),reverse=True)


	def load_data(self):
		file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docID2doc.json')
		with open(file_name, 'r') as f:		
			self.docID2doc =  json.load(f)


	def return_top10(self, inputs):
		self.get_token(inputs)
		self.calculate_tf_idf()
		self.load_data()
		result = []
		for item in  self.docID2score[:11]:
			result.append(self.docID2doc[item[0]].encode("utf-8"))
		return result




if __name__ == "__main__":

	search = SearchEng()
	result = search.return_top10(test)
	print( result )






	# with open('docID2doc.json', 'r') as f:
	# 	data = yaml.safe_load(f)

	# with open('docID2doc.json', 'r') as f:
	# 	data = json.load(f)
	# print(data)

	# with open('term2termID.json', 'r') as f:
	# 		temp =  json.load(f)



	# for i in range(len(search.token)):
	# 	if search.token[i] in temp.keys():
	# 		search.token[i] = temp[search.token[i]]
	# 	else:
	# 		search.token[i] = None

	# print(search.token)









