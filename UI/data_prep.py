import pandas as pd
import re
import numpy as np
from functools import partial, reduce
import warnings
warnings.filterwarnings('ignore')

#filepath = "/Users/rahulnair/Desktop/Labelmaster_"
filepath = "UI_Data"
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


def external_database():
	print('Reading from Trucking Database Freight sheet')
	freight_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Trucking Database.xlsx', 'rb'), sheet_name='freight-m')
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

	print('Reading from Trucking Database Rates sheet')
	rates_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Trucking Database.xlsx', 'rb'), sheet_name='rates-m')
	rates_m = rates_m.T
	rates_m.columns = rates_m.iloc[1, :]
	rates_m = rates_m.reset_index()
	rates_m = rates_m.drop('index', axis=1)
	rates_m = rates_m.dropna(how='all', axis=1)  # for removing columns having null values
	rates_m = rates_m.drop(index=[0, 1, 2], axis=0)  # because row 0 has Nan and row 1 has just column names
	rates_m = rates_m.rename(columns={np.nan: 'Year', '2008Q1=100, Seasonally Adjusted': 'Month'})
	rates_m.reset_index(drop=True, inplace=True)


	rates_m['Month'] = rates_m['Month'].map(months)
	rates_m['Year_Month'] = rates_m['Year'].astype(str) + '-' + rates_m['Month']
	rates_m = rates_m.drop(['Year', 'Month'], axis=1)
	new_names = []
	for i in rates_m.columns:
		new_names.append(i + '_rates_m_trucking')

	rates_m.columns = new_names
	rates_m = rates_m.rename(columns={'Year_Month_rates_m_trucking': 'Year_Month'})

	print('Reading from Trucking Database Indicator sheet')
	indicators_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Trucking Database.xlsx', 'rb'), sheet_name='indicators-m')
	indicators_m = indicators_m.T
	indicators_m.columns = indicators_m.iloc[1, :]
	indicators_m = indicators_m.reset_index()
	indicators_m = indicators_m.drop('index', axis=1)
	indicators_m = indicators_m.dropna(how='all', axis=1)  # for removing columns having null values
	indicators_m = indicators_m.drop(index=[0, 1, 2], axis=0)  # because row 0 has Nan and row 1 has just column names
	indicators_m = indicators_m.rename(columns={np.nan: 'Year', 'ID': 'Month'})
	indicators_m.reset_index(drop=True, inplace=True)


	indicators_m['Month'] = indicators_m['Month'].map(months)
	indicators_m['Year_Month'] = indicators_m['Year'].astype(str) + '-' + indicators_m['Month']
	indicators_m = indicators_m.drop(['Year', 'Month'], axis=1)
	new_names = []
	for i in indicators_m.columns:
		new_names.append(i + '_indicators_m_trucking')

	indicators_m.columns = new_names
	indicators_m = indicators_m.rename(columns={'Year_Month_indicators_m_trucking': 'Year_Month'})

	print('Reading from Trucking Database Driver Indicators sheet')
	driver_indicators_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Trucking Database.xlsx', 'rb'), sheet_name='driver_indicators-m')
	driver_indicators_m = driver_indicators_m.T
	driver_indicators_m.iloc[1, 6] = driver_indicators_m.iloc[2, 6]
	driver_indicators_m.iloc[1, 9] = driver_indicators_m.iloc[2, 9]
	driver_indicators_m.iloc[1, 12] = driver_indicators_m.iloc[2, 12]
	driver_indicators_m.iloc[1, 15] = driver_indicators_m.iloc[2, 15]
	driver_indicators_m.iloc[1, 18] = driver_indicators_m.iloc[2, 18]
	driver_indicators_m.iloc[1, 21] = driver_indicators_m.iloc[2, 21]
	driver_indicators_m.iloc[1, 24] = driver_indicators_m.iloc[2, 24]
	driver_indicators_m.columns = driver_indicators_m.iloc[1, :]
	driver_indicators_m = driver_indicators_m.reset_index()
	driver_indicators_m = driver_indicators_m.drop('index', axis=1)
	driver_indicators_m = driver_indicators_m.dropna(how='all', axis=1)  # for removing columns having null values
	driver_indicators_m = driver_indicators_m.drop(index=[0, 1, 2], axis=0) # because row 0 has Nan and row 1 has just column names
	driver_indicators_m = driver_indicators_m.rename(columns={np.nan: 'Year', 'ID': 'Month'})
	driver_indicators_m.reset_index(drop=True, inplace=True)
	driver_indicators_m['Month'] = driver_indicators_m['Month'].map(months)
	driver_indicators_m['Year_Month'] = driver_indicators_m['Year'].astype(str) + '-' + driver_indicators_m['Month']
	driver_indicators_m = driver_indicators_m.drop(['Year', 'Month'], axis=1)
	new_names = []
	for i in driver_indicators_m.columns:
		new_names.append(i + '_driver_indicators_m_trucking')

	driver_indicators_m.columns = new_names
	driver_indicators_m = driver_indicators_m.rename(columns={'Year_Month_driver_indicators_m_trucking': 'Year_Month'})
	dfs = [freight_m, rates_m, indicators_m, driver_indicators_m]
	monthly_df = pd.concat(dfs, join='inner', axis=1)
	monthly_df = monthly_df.loc[:, ~monthly_df.columns.duplicated()]

	print('Reading from Truck & Trailer Database Economics sheet')
	economics_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Truck & Trailer Database.xlsx', 'rb'), sheet_name='economics-m')
	economics_m = economics_m.T
	economics_m.columns = economics_m.iloc[2, :]
	economics_m = economics_m.reset_index()
	economics_m = economics_m.drop('index', axis=1)
	economics_m = economics_m.drop(index=[0, 1, 2], axis=0)  # because row 0 has Nan and row 1 has just column names
	economics_m = economics_m.dropna(how='all', axis=1)  # for removing columns having null values
	economics_m = economics_m.rename(columns={np.nan: 'Year', 'Name': 'Month'})
	economics_m.reset_index(drop=True, inplace=True)
	economics_m['Month'] = economics_m['Month'].map(months)
	economics_m['Year_Month'] = economics_m['Year'].astype(str) + '-' + economics_m['Month']
	economics_m = economics_m.drop(['Year', 'Month'], axis=1)
	new_names = []
	for i in economics_m.columns:
		new_names.append(i + '_economics_m_trucking_trailer')

	economics_m.columns = new_names
	economics_m = economics_m.rename(columns={'Year_Month_economics_m_trucking_trailer': 'Year_Month'})

	print('Reading from Truck & Trailer Database Indicator sheet')
	indicators_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Truck & Trailer Database.xlsx', 'rb'), sheet_name='indicators-m_modified')
	indicators_m = indicators_m.T
	indicators_m = indicators_m.iloc[:, 0:31]
	indicators_m.columns = indicators_m.iloc[2, :]
	indicators_m = indicators_m.reset_index()
	indicators_m = indicators_m.drop('index', axis=1)
	indicators_m = indicators_m.drop(index=[0, 1, 2], axis=0)
	indicators_m.columns = ["Year",
							"Month",
							"Total Class 8, North America_OEM Net Orders",
							"Total Class 8, North America_OEM Net Orders_M/M % Change",
							"Total Class 8, North America_OEM Net Orders_Y/Y % Change",
							"Total Class 8, North America_Factory Shipments (Ward's)",
							"Total Class 8, North America_Factory Shipments (Ward's)_M/M % Change",
							"Total Class 8, North America_Factory Shipments (Ward's)_Y/Y % Change",
							"Total Class 8, North America_Retail Sales (Ward's)",
							"Total Class 8, North America_Retail Sales (Ward's)_M/M % Change",
							"Total Class 8, North America_Retail Sales (Ward's)_Y/Y % Change",
							"Total Class 8, North America_Inventories (Ward's)",
							"Total Class 8, North America_Inventories (Ward's)_M/M % Change",
							"Total Class 8, North America_Inventories (Ward's)_Y/Y % Change",
							"Total Trailers, U.S._Production",
							"Total Trailers, U.S._Production_M/M % Change",
							'Total Trailers, U.S._Production_Y/Y % Change',
							"Total Classes 4-7, North America_Factory Shipments (Ward's)",
							"Total Classes 4-7, North America_Factory Shipments (Ward's)_M/M % Change",
							"Total Classes 4-7, North America_Factory Shipments (Ward's)_Y/Y % Change",
							"Total Classes 4-7, North America_Retail Sales (Ward's)",
							"Total Classes 4-7, North America_Retail Sales (Ward's)_M/M % Change",
							"Total Classes 4-7, North America_Retail Sales (Ward's)_Y/Y % Change",
							"Total Classes 4-7, North America_Inventories (Ward's)",
							"Total Classes 4-7, North America_Inventories (Ward's)_M/M % Change",
							"Total Classes 4-7, North America_Inventories (Ward's)_Y/Y % Change",
							"Class 4, North America_Factory Shipments (Ward's)",
							"Class 4, North America_Retail Sales (Ward's)",
							"Class 4, North America_Inventories (Ward's)",
							"Class 6-7 Bus, North America_Factory Shipments (Ward's)",
							"Class 4-7, US_Retail Sales (Ward's)'"]
	indicators_m['Month'] = indicators_m['Month'].map(months)
	indicators_m['Year_Month'] = indicators_m['Year'].astype(str) + '-' + indicators_m['Month']
	indicators_m = indicators_m.drop(['Year', 'Month'], axis=1)
	new_names = []
	for i in indicators_m.columns:
		new_names.append(i + '_indicators_m_trucking_trailer')

	indicators_m.columns = new_names
	indicators_m = indicators_m.rename(columns={'Year_Month_indicators_m_trucking_trailer': 'Year_Month'})

	print('Reading from Truck & Trailer Database Freight sheet')
	freight_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Truck & Trailer Database.xlsx', 'rb'), sheet_name='freight-m')
	freight_m = freight_m.T
	freight_m = freight_m.reset_index()
	freight_m = freight_m.drop('index', axis=1)
	freight_m.columns = freight_m.iloc[2, :]
	freight_m = freight_m.drop(index=[0, 1, 2], axis=0)
	freight_m = freight_m.dropna(how='all', axis=1)
	freight_m.columns = ["Year", "Month", "FTR Truck Loadings (000s, SA)",
						 "FTR Truck Loadings Index (1992=100)", "FTR Truck Loadings_M/M % Change",
						 "FTR Truck Loadings_Y/Y % Change", "FTR Rail Intermodal Loadings (000, SA)",
						 "FTR Rail Intermodal Loadings Index (1992=100)", "FTR Rail Intermodal Loadings_M/M % Change",
						 "FTR Rail Intermodal Loadings_Y/Y % Change",
						 "FTR Rail Carloadings (carload + intermodal) (000s, SA)",
						 "FTR Rail Carloadings Index (1992=100)", "FTR Rail Carloadings_M/M % Change",
						 "FTR Rail Carloadings_Y/Y % Change",
						 "FTR Cl. 8 Truck Tonnage (000s, SA)", "FTR Cl. 8 Truck Tonnage Index (1992=100)",
						 "FTR Cl. 8 Truck Tonnage_M/M % Change",
						 "FTR Cl. 8 Truck Tonnage_Y/Y % Change", "FTR Cl. 8 Truck Tonmiles (000000s, SA)",
						 "FTR Cl. 8 Truck Tonmiles Index (1992=100)", "FTR Cl. 8 Truck Tonmiles_M/M % Change",
						 "FTR Cl. 8 Truck Tonmiles__Y/Y % Change", "FTR Class 8 Truck Utilization (%, SA)",
						 "Dry Van Trailer Loadings (000s, SA)", "Reefer Trailer Loadings (000s, SA)",
						 "Platform Trailer Loadings (000s, SA)", "Straight Truck Loadings (000s, SA)",
						 "Bulk Trailer Loadings (000s, SA)", "Food & Kindred Products (000s, SA)",
						 "Stone, Clay, Glass & Concrete (000s, SA)", "Nonmetallic Minerals, Except Fuels (000s, SA)",
						 "Chemicals & Allied Products (000s, SA)", "Transportation Equipment (000s, SA)",
						 "All Other Freight (000s, SA)", "FTR MD Truck Tonnage (000s, SA)",
						 "FTR MD Truck Tonnage Index (1992=100)", "FTR MD Truck Tonnage_M/M % Change",
						 "FTR MD Truck Tonnage_Y/Y % Change", "FTR MD Truck Tonmiles (000000s, SA)",
						 "FTR MD Truck Tonmiles Index (1992=100)", "FTR MD Truck Tonmiles_M/M % Change",
						 "FTR MD Truck Tonmiles_Y/Y % Change"]
	freight_m['Month'] = freight_m['Month'].map(months)
	freight_m['Year_Month'] = freight_m['Year'].astype(str) + '-' + freight_m['Month']
	freight_m = freight_m.drop(['Year', 'Month'], axis=1)
	new_names = []
	for i in freight_m.columns:
		new_names.append(i + '_freight_m_trucking_trailer')

	freight_m.columns = new_names
	freight_m = freight_m.rename(columns={'Year_Month_freight_m_trucking_trailer': 'Year_Month'})
	truck_trailer_monthly_list = [economics_m, indicators_m, freight_m]
	truck_trailer_monthly_df = pd.concat(truck_trailer_monthly_list, join='inner', axis=1)
	truck_trailer_monthly_df = truck_trailer_monthly_df.loc[:, ~truck_trailer_monthly_df.columns.duplicated()]
	l = [monthly_df, truck_trailer_monthly_df]
	merge = partial(pd.merge, on='Year_Month', how='inner')
	new_df = reduce(merge, l)

	print('Reading from Indicators_trailers Database')
	xl = pd.ExcelFile('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/indicators_trailers_2008.xlsx')
	sheet_list = xl.sheet_names[1:]
	df_dict = {}
	for i in sheet_list:
		df_dict[i] = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/indicators_trailers_2008.xlsx', 'rb'), sheet_name=i)
		df_dict[i].columns = df_dict[i].iloc[0, :]
		df_dict[i] = df_dict[i].drop(index=0, axis=0)
		df_dict[i] = df_dict[i].replace('\s*', np.nan, regex=True)
		df_dict[i] = df_dict[i].dropna(how='all', axis=1)
		df_dict[i] = df_dict[i].rename(columns={pd.NaT: 'Date'})
		new_names = []
		for j in df_dict[i].columns:
			new_names.append(j + '_' + i)
		df_dict[i].columns = new_names
		df_dict[i] = df_dict[i].rename(columns={'Date' + '_' + i: 'Date'})
	df_list = [df_dict[i] for i in df_dict.keys()]
	merge = partial(pd.merge, on='Date', how='inner')
	dfs = reduce(merge, df_list)
	y_m = []
	for i in dfs['Date'].astype(str):
		y_m.append(''.join(re.findall('\d{4}-\d{2}', i)))

	dfs['Year_Month'] = pd.Series(y_m)
	dfs = dfs.drop('Date', axis=1)
	merge = partial(pd.merge, on='Year_Month', how='outer')
	complete_external_monthly = reduce(merge, [new_df, dfs])

	print('Reading from Intermodal Database Freight sheet')
	freight_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Intermodal Database.xlsx', 'rb'), sheet_name='indicators-m')
	freight_m = freight_m.T
	freight_m.columns = freight_m.iloc[2, :]
	freight_m = freight_m.drop(index=['U.S. Monthly Indicators', 'Unnamed: 1', 'Unnamed: 2'], axis=0)
	freight_m = freight_m.dropna(how='all', axis=1)
	freight_m = freight_m.reset_index(drop=True)
	freight_m = freight_m.rename(columns={np.nan: 'Year', 'Name': 'Month'})
	freight_m['Month'] = freight_m['Month'].map(months)
	freight_m['Year_Month'] = freight_m['Year'].astype(str) + '-' + freight_m['Month']
	freight_m = freight_m.drop(['Year', 'Month'], axis=1)

	print('Reading from Intermodal Database Summary sheet')
	summary_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Intermodal Database.xlsx', 'rb'), sheet_name='summary-m_modified')
	summary_m = summary_m.T
	summary_m = summary_m.reset_index(drop=True)
	summary_m.columns = summary_m.iloc[2, :]
	summary_m = summary_m.drop(index=[0, 1, 2], axis=0)
	summary_m = summary_m.reset_index(drop=True)
	summary_m = summary_m.dropna(how='all', axis=1)
	summary_m.columns = ['Year',
						 'Month',
						 'Intermodal Revenue Movements (IANA-ETSO)_Total',
						 'Intermodal Revenue Movements (IANA-ETSO)_International',
						 'Intermodal Revenue Movements (IANA-ETSO)_Domestic',
						 'Intermodal Revenue Movements (IANA-ETSO)_Domestic Containers',
						 "Intermodal Revenue Movements (IANA-ETSO)_Memo: Domestic Containers & 53'+ Trailers",
						 'S.A. Total Revenue Movements Index (Jan 2001 = 100)_International Movements Index (Jan 2001 = 100)',
						 'S.A. Total Revenue Movements Index (Jan 2001 = 100)_Domestic Movements Index (Jan 2001 = 100)',
						 'Container Share %, Total Intermodal_Total Domestic % (Dom. Container+Trailers)',
						 "Container Share %, Total Intermodal_Truckload Only % (Dom. Container+53' Trailers)",
						 'FTR Intermodal Competitive Index_Intermodal Competitive Index (0=Neutral)',
						 'U.S. Origin Intermodal Volumes_International',
						 'U.S. Origin Intermodal Volumes_Domestic',
						 'U.S. Origin Intermodal Volumes_Total',
						 'Canada Origin Intermodal Volumes_International',
						 'Canada Origin Intermodal Volumes_Domestic',
						 'Canada Origin Intermodal Volumes_Total',
						 'Mexico Origin Intermodal Volumes_International',
						 'Mexico Origin Intermodal Volumes_Domestic',
						 'Mexico Origin Intermodal Volumes_Total',
						 'N.A. Port Activity, Total TEUs_Imports',
						 'N.A. Port Activity, Total TEUs_Exports',
						 'N.A. Port Activity, Total TEUs_SA Imports',
						 'West Coast Port Activity, Total TEUs_Imports',
						 'West Coast Port Activity, Total TEUs_Exports',
						 'West Coast Port Activity, Total TEUs_SA Imports',
						 'East Coast Port Activity, Total TEUs_Imports',
						 'East Coast Port Activity, Total TEUs_Exports',
						 'East Coast Port Activity, Total TEUs_SA Imports',
						 'Gulf Coast Port Activity, Total TEUs_Imports',
						 'Gulf Coast Port Activity, Total TEUs_Exports',
						 'Gulf Coast Port Activity, Total TEUs_SA Imports',
						 'Western Canadian Port Activity, Total TEUs_Imports',
						 'Western Canadian Port Activity, Total TEUs_Exports',
						 'Western Canadian Port Activity, Total TEUs_SA Imports']
	summary_m['Month'] = summary_m['Month'].map(months)
	summary_m['Year_Month'] = summary_m['Year'].astype(str) + '-' + summary_m['Month']
	summary_m = summary_m.drop(['Year', 'Month'], axis=1)

	print('Reading from Intermodal Database Rates sheet')
	rates_m = pd.read_excel(open('/Users/rahulnair/Desktop/Labelmaster_/Labelmaster data/Intermodal Database.xlsx', 'rb'), sheet_name='rates-m')
	rates_m = rates_m.T
	rates_m = rates_m.reset_index(drop=True)
	rates_m = rates_m.dropna(how='all', axis=1)
	rates_m.columns = ['Year', 'Month', 'Intermodal (Rail+Drayage) Rates (Rev/Load)', 'Total Intermodal (w/o FSC)', 'Total Intermodal (w/ FSC)']
	rates_m = rates_m.drop(index=[0, 1, 2], axis=0)
	rates_m = rates_m.drop('Intermodal (Rail+Drayage) Rates (Rev/Load)', axis=1)
	rates_m['Month'] = rates_m['Month'].map(months)
	rates_m['Year_Month'] = rates_m['Year'].astype(str) + '-' + rates_m['Month']
	rates_m = rates_m.drop(['Year', 'Month'], axis=1)
	intermodal_dfs_l = [freight_m, summary_m, rates_m]
	merge = partial(pd.merge, on='Year_Month', how='inner')
	intermodal_dfs = reduce(merge, intermodal_dfs_l)
	merge = partial(pd.merge, on='Year_Month', how='outer')
	complete_external_monthly = reduce(merge, [complete_external_monthly, intermodal_dfs])
	return complete_external_monthly


def feature_selection(data):
	features = ['Year_Month', 'Sum of Sales',
       'FTR Truck Loadings (000s, SA)_freight_m_trucking',
       'FTR Active Truck Utilization (%, SA)_freight_m_trucking',
       'Reefer Trailer Loadings (000s, SA)_freight_m_trucking',
       'Tank Trailer Loadings (000s, SA)_freight_m_trucking',
       'Chemicals & Allied Products (000s, SA)_freight_m_trucking',
       'Spot TL Rates (w/o FSC)_rates_m_trucking',
       'Total LTL (w/o FSC)_rates_m_trucking',
       'Total LTL (w/ FSC)_rates_m_trucking',
       'Contract TL Tank Rates (w/o FSC)_rates_m_trucking',
       'OEM Net Orders (U.S. / CAN, units)_indicators_m_trucking',
       'New Truck Lead Time (N.A. Backlog/Build Ratio, months)_indicators_m_trucking',
       'B50001_indicators_m_trucking', 'GMFN_indicators_m_trucking',
       'G325_indicators_m_trucking', 'G332_indicators_m_trucking',
       'ISM_indicators_m_trucking', 'PORTEU_indicators_m_trucking',
       'CASS_indicators_m_trucking', 'MANEMP_indicators_m_trucking',
       'USTRADE_indicators_m_trucking', 'LEI_indicators_m_trucking',
       'SPREAD_indicators_m_trucking', 'ISRATIO_indicators_m_trucking',
       'NDCGO_indicators_m_trucking', 'CF3M_indicators_m_trucking',
       'PUBCON_indicators_m_trucking', 'D/GAL_indicators_m_trucking',
       'D/STOCK_indicators_m_trucking',
       "Change in Payroll Employment (000's)_driver_indicators_m_trucking",
       "Change in Truck Emp. (000's)_driver_indicators_m_trucking",
       'LABORINDEX_driver_indicators_m_trucking',
       'Total Class 8, North America_OEM Net Orders_indicators_m_trucking_trailer',
       'Total Class 8, North America_OEM Net Orders_M/M % Change_indicators_m_trucking_trailer',
       'Total Class 8, North America_OEM Net Orders_Y/Y % Change_indicators_m_trucking_trailer',
       "Total Class 8, North America_Factory Shipments (Ward's)_indicators_m_trucking_trailer",
       "Total Class 8, North America_Factory Shipments (Ward's)_M/M % Change_indicators_m_trucking_trailer",
       "Total Class 8, North America_Factory Shipments (Ward's)_Y/Y % Change_indicators_m_trucking_trailer",
       "Total Class 8, North America_Retail Sales (Ward's)_indicators_m_trucking_trailer",
       "Total Class 8, North America_Retail Sales (Ward's)_M/M % Change_indicators_m_trucking_trailer",
       "Total Class 8, North America_Inventories (Ward's)_M/M % Change_indicators_m_trucking_trailer",
       "Total Class 8, North America_Inventories (Ward's)_Y/Y % Change_indicators_m_trucking_trailer",
       'Total Trailers, U.S._Production_M/M % Change_indicators_m_trucking_trailer',
       'Total Trailers, U.S._Production_Y/Y % Change_indicators_m_trucking_trailer',
       "Total Classes 4-7, North America_Factory Shipments (Ward's)_indicators_m_trucking_trailer",
       "Total Classes 4-7, North America_Factory Shipments (Ward's)_M/M % Change_indicators_m_trucking_trailer",
       "Total Classes 4-7, North America_Factory Shipments (Ward's)_Y/Y % Change_indicators_m_trucking_trailer",
       "Total Classes 4-7, North America_Retail Sales (Ward's)_M/M % Change_indicators_m_trucking_trailer",
       "Total Classes 4-7, North America_Retail Sales (Ward's)_Y/Y % Change_indicators_m_trucking_trailer",
       "Total Classes 4-7, North America_Inventories (Ward's)_M/M % Change_indicators_m_trucking_trailer",
       "Total Classes 4-7, North America_Inventories (Ward's)_Y/Y % Change_indicators_m_trucking_trailer",
       "Class 4, North America_Factory Shipments (Ward's)_indicators_m_trucking_trailer",
       "Class 4, North America_Retail Sales (Ward's)_indicators_m_trucking_trailer",
       "Class 4, North America_Inventories (Ward's)_indicators_m_trucking_trailer",
       "Class 6-7 Bus, North America_Factory Shipments (Ward's)_indicators_m_trucking_trailer",
       'FTR Truck Loadings_M/M % Change_freight_m_trucking_trailer',
       'FTR Truck Loadings_Y/Y % Change_freight_m_trucking_trailer',
       'FTR Rail Intermodal Loadings_M/M % Change_freight_m_trucking_trailer',
       'FTR Rail Intermodal Loadings_Y/Y % Change_freight_m_trucking_trailer',
       'FTR Rail Carloadings (carload + intermodal) (000s, SA)_freight_m_trucking_trailer',
       'FTR Rail Carloadings_M/M % Change_freight_m_trucking_trailer',
       'FTR Rail Carloadings_Y/Y % Change_freight_m_trucking_trailer',
       'FTR Class 8 Truck Utilization (%, SA)_freight_m_trucking_trailer',
       'BUILD FOR_Total_Trailer', 'BUILD FOR_Flatbed', 'BUILD FOR_Liquid_Tank',
       'BUILD FOR_Dry_Tank', 'BUILD FOR_Dump', 'BUILD FOR_Lowbed',
       'BUILD FOR_All_Other']

	data = data[features]
	return data


def final_data(books, external):
	data = pd.merge(books, external, on='Year_Month', how='inner')
	data = feature_selection(data)
	data = data.set_index(keys='Year_Month')
	return data


# Main data
# main_data = main_data_transform()

# Books data
# books = books_data(main_data)

# getting external data and merging with the books data
# external = external_database()
# data = final_data(books, external)
# print(data.shape)












