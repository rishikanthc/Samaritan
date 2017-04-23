from aylienapiclient import textapi
from googleapiclient.discovery import build





# query = "theory of relativity"

client = textapi.Client("98b7ecc2", "4e9829432bb78e1cc8a1ff11101e2a41")

my_api_key = "AIzaSyAhXcKuWQJRWUAkXJHLs2T6PggVi7MMpaU"
my_cse_id = "009066246134499923801:pjldjdtd_bm"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

def parse_results(query):
	results = google_search(query, my_api_key, my_cse_id, num=1)
	consolidate = ""
	for result in results:
		link = result['link']
	summary = client.Summarize({'url': link, 'sentences_number': 3})
	for sentence in summary['sentences']:
		consolidate = consolidate + sentence
  		# print sentence
  	return consolidate

if __name__ == "__main__":
	t = parse_results("Barack Obama")
	print t
