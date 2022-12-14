import pandas as pd
import numpy as np


def get_unique(data):
	'''
	Show unique values for each column.
	'''
	for col in data.columns:
		uniq = data[col].unique()
		print(f"COLUMN \x1b[1;31m{col}\x1b[0m ({data[col].dtype})")

		# Show first 20 values only
		if len(uniq) > 20:
			print(f'{uniq[:20]}...')
		else:
			print(uniq)
		print()



def print_outlier_count(data, lower_percentile=25, upper_percentile=75):
	'''
	Print number of outliers for each column in given dataframe.
	Outliers are defined as values outside of the interquantile range.

	Args:
		lower_percentile: The lower percentile
		upper_percentile: The upper percentile
		data: Dataframe where to look for outliers
	Return:
		Dictionary with columnname as key and number of outliers as value
	'''
	n = len(max(data.columns, key=len))

	for col in data.select_dtypes(np.number).columns:
		iqr = np.percentile(data[col], upper_percentile) - np.percentile(data[col], lower_percentile)
		upper_limit = np.percentile(data[col], upper_percentile) + 1.5*iqr
		lower_limit = np.percentile(data[col], lower_percentile) - 1.5*iqr
		n_outliers  = data[(data[col] < lower_limit) | (data[col] > upper_limit)].shape[0]

		if n_outliers > 0:
		        perc = round(n_outliers * (100.0/len(data)), 2)
		        print(f'\x1b[1;31m{col:<{n}}\x1b[0m : {n_outliers} ({perc}%)')
		else:
		        print(f'\x1b[37m{col:<{n}}\x1b[0m : none')

def print_nan_percentage(data):
	'''
	Print percentage of Nan values in each column
	in given pandas dataframe.
	'''

	n = len(max(data.columns, key=len))
	for col in data.columns:
		pnan = round(data[col].isna().sum() * (100.0/len(data)), 2)
		if pnan > 0.00:
			print(f'\x1b[1;31m{col:<{n}}\x1b[0m : {pnan}%')
		else:
			print(f'\x1b[37m{col:<{n}}\x1b[0m : 0%')
