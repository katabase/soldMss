import json
from functools import lru_cache

import tqdm
from difflib import SequenceMatcher
import networkx
from networkx.algorithms.components.connected import connected_components
from main_functions import *


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
    def equals(field):
        return desc_a[field] == desc_b[field]

    score = 0
    # Desc of a same document are often strongly similar.
    if similar(desc_b["desc"], desc_a["desc"]) > 0.75:
        score = score + 0.3
    else:
        score = score - 0.2

    if equals("term"):
        score = score + 0.2
    else:
        score = score - 0.1

    if equals("date") and desc_b["date"] is not None:
        score = score + 0.5
    else:
        score = score - 0.5

    if equals("number_of_pages"):
        score = score + 0.1
    else:
        score = score - 0.1

    if equals("format"):
        score = score + 0.1
    else:
        score = score - 0.3

    if equals("price"):
        score = score + 0.1
    else:
        score = score - 0.1
    
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
        entry_id_a = validate_entry_id(id_a)
        # We can pass items from 0 to i since we already have processed it.
        for j in range(i + 1, len(items)):
            id_b, desc_b = items[j]
            entry_id_b = validate_entry_id(id_b)
            # To compare two sub-entries (two tei:desc from the same item) makes no sense.
            if entry_id_a == entry_id_b:
                continue
            # If there is a strong possibility that autors are not the same, we simply pass.
            if desc_b["author"] and desc_a["author"] and similar(desc_b["author"], desc_a["author"]) < 0.75:
                continue
            # This dict will contain the score and the author distance.
            score_entry = {}
            score_entry["score"] = similarity_score(desc_a, desc_b)
            try:
                score_entry["author_distance"] = similar(desc_b["author"], desc_a["author"])
            except:
                score_entry["author_distance"] = 0
            output_dict1["%s-%s" % (id_a, id_b)] = score_entry

    # The final list contains the result of the whole comparison process, without filtering, sorted by score.
    final_list = []
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
    filtered_list_with_score = [[item[1], item[0]] for item in final_list if item[0] > sensibility and item[2] >= 0.4]

    # Now let's create the clusters. We transform the list of pairs into a graph. The connected nodes are our clusters !
    # See https://stackoverflow.com/a/4843408
    filtered_list = [item[0] for item in filtered_list_with_score]
    graphed_list = to_graph(filtered_list)
    cleaned_list = [list(item) for item in list(connected_components(graphed_list))]
    cleaned_output_list = []
    reconciliated_desc_list = []
    n = 0
    for item in cleaned_list:
        temp_list = []
        for entry in item:
            # .copy() is used to prevent the modification of the original dictionary.
            temp_list.append({entry: input_dict[entry].copy()})
            reconciliated_desc_list.append(entry)
        cleaned_output_list.append(temp_list)
        cleaned_output_list[n].append(item)
        temp_list.reverse()
        n += 1

    return filtered_list_with_score, cleaned_output_list, reconciliated_desc_list




def reconciliator():
    """
    This function is the main function used for queries.
    :param author: a string
    :param date: a string, optional parameter
    """
    final_results = {}
    # Loading of all the data in JSON.
    json_file = '../export.json'
    actual_path = os.path.dirname(os.path.abspath(__file__))
    file_to_open = os.path.join(actual_path, json_file)
    with open(file_to_open, 'r') as data:
        all_data = json.load(data)
    
    #all_data = dict(list(all_data.items())[:1000])

    results_lists = double_loop(all_data)

    final_results["score"] = results_lists[0]
    final_results["groups"] = results_lists[1]
    final_results["items"] = len(all_data)

    return final_results


if __name__ == "__main__":
    results = reconciliator()

    with open('results.json', 'w+') as outfile:
        outfile.truncate(0)
        json.dump(results, outfile)
