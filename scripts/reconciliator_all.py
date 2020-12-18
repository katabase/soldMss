import json
import tqdm
from difflib import SequenceMatcher
import networkx
from networkx.algorithms.components.connected import connected_components
import os
import re

import argparse
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("json_file", help="a JSON file containing data to cluster")

# https://stackoverflow.com/a/17388505
def similar(a, b):
    """
    This function is used to compare pairs of sequences of any type.
    :param a: a string
    :param b: a string
    :return: a measure of the sequences' similarity as a float in the range [0, 1]
    """
    return SequenceMatcher(None, a, b).ratio()


# https://stackoverflow.com/a/4843408
def to_graph(l):
    """
    This function is used to create graphs (collections of nodes).
    :param l: a list
    :return: a list with graphs
    """
    graphed_list = networkx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        graphed_list.add_nodes_from(part)
        # it also imlies a number of edges:
        graphed_list.add_edges_from(to_edges(part))
    return graphed_list


# https://stackoverflow.com/a/4843408
def to_edges(l):
    """
    This function creates edges from graphs :
    It reats the param `l` as a Graph and returns it's edges :
    Ex : to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    :param l: a list of graphs
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current


def similarity_score(desc_a, desc_b):
    """
    This function calculates the similarity score between two descs.
    :param desc_a: first desc to compare
    :param desc_b: second desc to compare
    :return: the score
    """

    score = 0
    if  desc_a["term"] == desc_b["term"]:
        score = score + 0.3
    else:
        score = score - 0.1

    if  desc_a["date"] == desc_b["date"]and desc_b["date"] is not None:
        score = score + 0.5
    else:
        score = score - 0.1

    if  desc_a["number_of_pages"] == desc_b["number_of_pages"]:
        score = score + 0.1
    else:
        score = score - 0.1

    if  desc_a["format"] == desc_b["format"]:
        score = score + 0.2
    else:
        score = score - 0.1

    if  desc_a["price"] == desc_b["price"]:
        score = score + 0.1
    else:
        score = score - 0.1

    if score >= 0.5 and similar(desc_b["desc"], desc_a["desc"]) <= 0.75:
        score = score - 0.2

    return score



def double_loop(input_dict):
    """
    This function creates pairs of matching entries.
    :param input_dict: a dictionary
    :return: two lists
    """
    output_dict1 = {}
    # First we compare each entry with each other one and give a score to each pair.
    items = list(input_dict.items())
    for i in tqdm.tqdm(range(len(items))):
        id_a, desc_a = items[i]
        # We only keep the id of the catalogue : "CAT_000001_e1_d1" becomes "000001"
        CAT_id_a = id_a.split("_", 2)[1]
        # We can pass items from 0 to i since we already have processed it.
        for j in range(i + 1, len(items)):
            id_b, desc_b = items[j]
            CAT_id_b = id_b.split("_", 2)[1]
            # To compare two entries of a same catalogue makes no sense.
            if CAT_id_a == CAT_id_b:
                continue

            # This dict will contain the score and the author distance.
            score_entry = {}
            score_entry["score"] = similarity_score(desc_a, desc_b)
            
            if score_entry["score"] <= 0.5:
                continue

            # If there is a strong possibility that autors are not the same, we simply pass.
            if desc_b["author"] and desc_a["author"] and similar(desc_b["author"], desc_a["author"]) < 0.75:
                continue

            try:
                score_entry["author_distance"] = similar(desc_b["author"], desc_a["author"])
            except:
                score_entry["author_distance"] = 0
            output_dict1["%s-%s" % (id_a, id_b)] = score_entry

    # The final list contains the result of the whole comparison process, without filtering, sorted by score.
    final_list = []
    print("Start filling the final_list")
    for key in output_dict1:
        first_entry = key.split("-")[0]
        second_entry = key.split("-")[1]
        final_list.append((
                          output_dict1[key]["score"], [first_entry, second_entry], output_dict1[key]["author_distance"],
                          {first_entry: input_dict[first_entry]}, {second_entry: input_dict[second_entry]}))
    # We sort by author distance first, and then by the score.
    final_list.sort(reverse=True, key=lambda x: (x[2], x[0]))

    # The filtered list removes all entries with a score lower or equal to 0.6
    sensibility = 0.6
    print("Star filling the filtered_list_with_score")
    filtered_list_with_score = [[item[1], item[0]] for item in final_list if item[0] >= sensibility and item[2] >= 0.4]

    print("Start adding scores")
    desc_score = {}
    for (desc_a, desc_b), score in filtered_list_with_score:
    	if desc_a not in desc_score:
    		desc_score[desc_a] = []
    	desc_score[desc_a].append([desc_a, desc_b, score])

    # Now let's create the clusters. We transform the list of pairs into a graph. The connected nodes are our clusters !
    # See https://stackoverflow.com/a/4843408
    print("Creation of the clusters")
    filtered_list = [item[0] for item in filtered_list_with_score]
    graphed_list = to_graph(filtered_list)
    cleaned_list = [list(sorted(item)) for item in list(sorted(connected_components(graphed_list)))]

    print("Start filling the multiple_sales list")
    reconciliated_desc_list = []
    multiple_sales = []
    for item in cleaned_list:
    	mss_group = {
    		"mss" : [], 
    		"scores" : []
    	}
    	for desc_id in item:
    		reconciliated_desc_list.append(desc_id)
    		desc = input_dict[desc_id].copy()
    		desc["id"] = desc_id
    		mss_group["mss"].append(desc)
    		if desc_id in desc_score:
    			mss_group["scores"].extend(desc_score[desc_id])
    	multiple_sales.append(mss_group)


    print("Start filling the single_sale_list")
    # We can now know which manuscripts are sold only once.
    single_sale_list = []
    for desc_id, desc in input_dict.items():
    	if desc_id not in reconciliated_desc_list:
    		desc["id"] = desc_id
    		single_sale_list.append(desc)

    return single_sale_list, filtered_list_with_score, multiple_sales, reconciliated_desc_list




def reconciliator(data):
    """
    This function is the main function used for queries.
    :param data: a dict
    :return: a dict containing all results
    """
    final_results = {}

    # Usefull if you don't want to try the script on all the data.
    #all_data = dict(list(all_data.items())[:2500])

    results_lists = double_loop(data)

    final_results["descs_processed"] = len(data)
    final_results["mss_reconciliated"] = len(results_lists[2])
    final_results["single_sale_count"] = len(results_lists[0])
    final_results["multiple_sales_count"] = len(results_lists[3])
    final_results["multiple_sales"] = results_lists[2]
    final_results["single_sale"] = results_lists[0]

    # We want to be sure that each desc correspond either to a single sale or to multiple sales.
    assert final_results["descs_processed"] == final_results["single_sale_count"] + final_results["multiple_sales_count"], "Warning : there is an issue with your data."
    
    return final_results



if __name__ == "__main__":

    args = arg_parser.parse_args()

    # Loading of all the data in JSON.
    json_file = args.json_file
    actual_path = os.path.dirname(os.path.abspath(__file__))
    file_to_open = os.path.join(actual_path, json_file)
    with open(file_to_open, 'r') as data:
        all_data = json.load(data)
        results = reconciliator(all_data)

    with open('../output/reconciliated.json', 'w+') as outfile:
        outfile.truncate(0)
        json.dump(results, outfile)
