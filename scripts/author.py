import json
import csv
from collections import Counter

def count_authors(file):
	"""
	This function is used to count the number of occurences of each author.
	:param file: an open JSON file 
	:return: a dict
	"""
	author_list = []

	for mss in file["single_sale"]:
		author = mss["author"]
		if author is not None:
			author = author.lower().capitalize()
			author_list.append(author)

	for mss in file["multiple_sales"]:
		author = mss["mss"][0]["author"]
		if author is not None:
			author = author.lower().capitalize()
			author_list.append(author)

	count = Counter(author_list)

	return count



if __name__ == "__main__":

	# First, we retrieve data from the JSON file.
    with open('../output/reconciliated.json') as json_file:
    	data = json.load(json_file)

    author_count = count_authors(data)

    # This file will contain the occurrence of each author.
    occurrence = open("../output/author/occurrence.txt", "w+")

    n = 1
    # This way the dict is ordered as we want : the most popular author to the less.
    author_count = dict(sorted(author_count.items(), key=lambda item: item[1], reverse=True))
    for author, count in author_count.items():
    	occurrence.write(str(n) + ". " + author + " : " + str(count) + "\n")
    	n = n + 1
    occurrence.close()