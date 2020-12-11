import json
import csv

def get_price(dict):
	"""
	This function is used to get the price of a manuscript.
	"""
	price = dict["price"]
	return price


def get_all_prices(file):
	"""
	This function is used to produce a list of all prices.
	:param file: a json file containing the mss
	:return: a list 
	"""
	prices_list = []

	for mss in file["single_sale"]:
		price = get_price(mss)
		if price is not None:
			prices_list.append(price)

	for mss in file["multiple_sales"]:
		for ms in mss["mss"]:
			price = get_price(ms)
			if price is not None:
				prices_list.append(price)

	return prices_list


def get_average(lst):
	"""
	This function is used to calculate the average of a list of float.
	:param lst: a list
	:return: a float
	"""
	sum = 0
	if len(lst) != 0:
		for i in lst:
			if i is float or int:
				sum = sum + i
		average = sum / len(lst)
		average = round(average, 2)
		return average
	else:
		return None


def price_evolution(mss_dict):
	"""
	This function is used to get the evolution of the price for a multiple time sold manuscript.
	:para mss_dict: the data of a manuscript, as a dict
	:return: a dict containing data
	"""
	# This if the final dict.
	data = {}
	# This list contains all prices, used for the average.
	prices_list = []
	# This list contains price and sell date of each sell, it's a list of dict.
	sales_list = []
	for mss in mss_dict["mss"]:
		id = mss["id"]
		# This dict will contains two keys : the date and the price of the sell.
		sales = {}
		# The two entries are overwrite : it's ok because we only want to keep one id and one desc.
		data["id"] = id
		data["author"] = mss["author"]
		data["desc"] = mss["desc"]
		price = get_price(mss)
		sales["date"] = mss["sell_date"]
		sales["price"] = price
		sales_list.append(sales)

		if price is not None:
			prices_list.append(price)

	data["sales"] = sales_list

	# Prices are sorted : the lowest to the highest.
	prices_list.sort()

	if prices_list != []:
		data["average"] = get_average(prices_list)
		data["highest_price"] = prices_list[-1]
		data["lowest_price"] = prices_list[0]

	return data



if __name__ == "__main__":

	# First, we retrieve data from the JSON file.
    with open('../output/reconciliated.json') as json_file:
    	data = json.load(json_file)

    average = get_average(get_all_prices(data))
    print("The average price is " + str(average))

    with open('../output/price/price_evolution.csv', 'w+') as csv_file:
    	fieldnames = ['id', 'author', 'desc', 'sales', 'average', 'highest_price', 'lowest_price']
    	csv = csv.DictWriter(csv_file, fieldnames=fieldnames)
    	csv.writeheader()

    	for mss in data["multiple_sales"]:
    		data = price_evolution(mss)
    		csv.writerow(data)

