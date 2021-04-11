import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')


# Funtions
def main_data_transform():
	main = {}
	for i in range(1,11):
		print('Reading Labelmaster Daily Sales by Product Group Part ' + str(i) + '.xlsx')
		main[i] = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Labelmaster Daily Sales by Product Group Part ' + str(i) + '.xlsx', 'rb'))
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
	return books


def trucking_database():
	print('Freight sheet')
	freight_m = pd.read_excel(open('Trucking Database.xlsx', 'rb'), sheet_name='freight-m')
	freight_m = freight_m.T
	freight_m.columns = freight_m.iloc[1, :]
	freight_m = freight_m.drop(index=['Unnamed: 1'], axis=0)
	freight_m = freight_m.reset_index()
	freight_m = freight_m.drop('index', axis=1)
	freight_m = freight_m.dropna(how='all', axis=1)  # for removing columns having null values
	freight_m = freight_m.drop(index=[0, 1], axis=0)  # because row 0 has Nan and row 1 has just column names
	freight_m = freight_m.rename(columns={np.nan: 'Year', 'Seasonally Adjusted': 'Month'})
	freight_m.reset_index(drop=True, inplace=True)

	# Converting month names to numbers for uniformity
	months = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP': '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}
	freight_m['Month'] = freight_m['Month'].map(months)
	freight_m['Year_Month'] = freight_m['Year'].astype(str) + '-' + freight_m['Month']
	freight_m = freight_m.drop(['Year', 'Month'], axis=1)

	new_names = []
	for i in freight_m.columns:
		new_names.append(i + '_freight_m_trucking')
	freight_m.columns = new_names
	freight_m = freight_m.rename(columns={'Year_Month_freight_m_trucking': 'Year_Month'})

# Main data
main_data = main_data_transform()

# Books data
books = books_data(main_data)

# getting external data
# First we will extract columns from Trucking Database












