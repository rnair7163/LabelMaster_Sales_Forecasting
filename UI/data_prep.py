import pandas as pd
import re
import numpy as np
from functools import partial, reduce
import warnings
warnings.filterwarnings('ignore')

filepath = "/Users/rahulnair/Desktop/Labelmaster_"
# filepath = "UI_Data"
# Funtions
def main_data_transform():
	main = {}
	for i in range(1,11):
		print('Reading Labelmaster Daily Sales by Product Group Part ' + str(i))
		main[i] = pd.read_excel(open(filepath+'/Labelmaster data/Labelmaster Daily Sales by Product Group Part ' + str(i) + '.xlsx', 'rb'))
		main[i].columns = main[i].iloc[1, :]
		main[i] = main[i].drop(index=[0, 1], axis=0)

	l = [main[i] for i in range(1,11)]
	main_data = pd.concat(l)
	return main_data


def books_data(data):
	books = data[data['Department Dim'] == '504']
	books.sort_values(by='Posting Date', inplace=True) # sorting the data based on date
	books.reset_index(drop=True, inplace=True)
	books['Posting Date'] = [str(i) for i in books['Posting Date']]

	# We will be needing month and year for merging with the external data
	books[['Date', 'Time']] = books['Posting Date'].str.split(' ', expand=True)
	
	y_m = []
	for i in books['Date']:
		y_m.append(''.join(re.findall('\d+-\d+', i)))
	books['Year_Month'] = pd.Series(y_m)
	books = books.groupby('Year_Month').agg({'Sum of Sales':'sum'})
	books = books.reset_index(drop= False)
	books = books[books.Year_Month >= '2008-01']
	return books


def packaging_data(data):
	packaging = data[data['Department Dim'] == '506']
	packaging.sort_values(by='Posting Date', inplace=True)  # sorting the data based on date
	packaging.reset_index(drop=True, inplace=True)
	packaging['Posting Date'] = [str(i) for i in packaging['Posting Date']]

	# We will be needing month and year for merging with the external data
	packaging[['Date', 'Time']] = packaging['Posting Date'].str.split(' ', expand=True)

	y_m = []
	for i in packaging['Date']:
		y_m.append(''.join(re.findall('\d+-\d+', i)))
	packaging['Year_Month'] = pd.Series(y_m)
	packaging = packaging.groupby('Year_Month').agg({'Sum of Sales': 'sum'})
	packaging = packaging.reset_index(drop=False)
	packaging = packaging[packaging.Year_Month >= '2008-01']
	return packaging


# def final_data(books, external):
# 	data = pd.merge(books, external, on='Year_Month', how='inner')
# 	data = feature_selection(data)
# 	data = data.set_index(keys='Year_Month')
# 	return data


# Main data
# main_data = main_data_transform()

# Books data
# books = books_data(main_data)

# getting external data and merging with the books data
# external = external_database()
# data = final_data(books, external)
# print(data.shape)












