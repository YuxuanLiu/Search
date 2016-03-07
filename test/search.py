import re
import json
import yaml

test = "machine learning a motherfucker"


class Search(object):
	def __init__(self):
		self.token = []
		self.term2tf_idf = {}


	def get_token(self, input):
		self.token = re.split("[^a-zA-Z0-9]+",input)
		with open('term2termID.json', 'r') as f:
			temp =  json.load(f)
		for i in range(len(search.token)):
			if search.token[i] in temp.keys():
				search.token[i] = temp[search.token[i]]
			else:
				search.token[i] = None

	def calculate_tf_idf(self):
		with open('postingLists.json', 'r') as f:
			temp =  json.load(f)

		for token in self.token:
			if token != None:
				self.term2tf_idf[token] = temp[ unicode(token)]
			else:
				self.term2tf_idf[token] = 0



		return None

	def load_data(self):
		
		with open('docID2doc.json', 'r') as f:
			self.docID2doc =  json.load(f)

		with open('term2termID.json', 'r') as f:
			temp =  json.load(f)



if __name__ == "__main__":

	search = Search()
	search.get_token(test)
	print(search.token)
	search.calculate_tf_idf()
	print(search.term2tf_idf)



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









