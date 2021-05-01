import pandas as pd
import re
import os
import statsmodels.api as sm
import pickle
import warnings
warnings.filterwarnings('ignore')
filepath = "UI_Data"


# Funtions
def main_data_transform():
	main = {}
	for i, j in enumerate(os.listdir(filepath)):
		print('Reading ' + str(j))
		main[i] = pd.read_excel(
			open(filepath + '/' + str(j), 'rb'))
		main[i].columns = main[i].iloc[1, :]
		main[i] = main[i].drop(index=[0, 1], axis=0)

	l = [main[i] for i in range(1,len(os.listdir(filepath)))]
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


def sarima_books(books):
	sales = books['Sum of Sales']
	# running the model
	mod = sm.tsa.statespace.SARIMAX(sales, order=(1, 0, 0), seasonal_order=(0, 1, 1, 12))
	results = mod.fit()

	# saving the final model
	pickle.dump(results, open('models/sarima_model.pkl', 'wb'))


def sarima_package(package):
	sales = package['Sum of Sales']

	# running the model
	mod = sm.tsa.statespace.SARIMAX(sales, order=(0, 1, 1), seasonal_order=(0, 1, 1, 12))

	results = mod.fit()

	# saving the final model
	pickle.dump(results, open('models/sarima_packaging_model.pkl', 'wb'))













