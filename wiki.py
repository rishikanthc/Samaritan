import wikipedia


# query = "theory of relativity"
def searchWiki(query):
	try:
		page = wikipedia.summary(query)
		print page
		return page
	except:
		topics = wikipedia.search(query)
		wiki_result = "Sorry, coudln't find that. Did you mean these ?"
		print query + " may refer to: "
		for i, topic in enumerate(topics):
			if i != 0:
				print i, topic
				wiki_result += topic
		return wiki_result
