import json

def get_mss(file):
	"""
	This function is used to produce a list of all the sold mss.
	:param file: a json file containing the mss
	:return: three lists 
	"""
	mss_list = []
	single_mss = []
	recon_mss = []

	for mss in file["single_sale"]:
		author = mss["author"]
		desc = mss["desc"]
		if author is not None:
			item = author.lower().capitalize() + " - " + desc
			single_mss.append(item)

	single_mss.sort()

	for mss in file["multiple_sales"]:
		author = mss["mss"][0]["author"]
		desc = mss["mss"][0]["desc"]
		if author is not None:
			item = author.lower().capitalize() + " - " + desc
			recon_mss.append(item)

	recon_mss.sort()

	mss_list = single_mss + recon_mss
	mss_list.sort()
	return single_mss, recon_mss, mss_list




if __name__ == "__main__":

	# First, we retrieve data from the JSON file.
    with open('../output/reconciliated.json') as json_file:
    	data = json.load(json_file)
    	MSS = get_mss(data)


    # This first file contains all the sold manuscripts.
    all_mss = open("../output/MSS_list/all_mss_list.txt", "w+")
    # This second file contains all the sold manuscripts that have been sold only once.
    single_mss = open("../output/MSS_list/single_sale_mss_list.txt", "w+")
    # This third file contains all the sold manuscripts that have been sold twice or more.
    recon_mss = open("../output/MSS_list/multiple_sales_mss_list.txt", "w+")

    single_sale_mss = MSS[0]
    for mss in single_sale_mss:
    	single_mss.write(mss + "\n")
    single_mss.close()

    multiple_sales_mss = MSS[1]
    for mss in multiple_sales_mss:
    	recon_mss.write(mss + "\n")
    recon_mss.close()

    all_mss_list = MSS[2]
    for mss in all_mss_list:
    	all_mss.write(mss + "\n")
    all_mss.close()



