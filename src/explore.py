import pandas as pd
import numpy as np


def describe_numericals(df):
	'''
	Returns a dataframe describing all numerical columns of
	given dataframe (Similar to df.describe()).

	The dataframe has the following columns:
	 - Datatype        Datatype of column
	 - Unique          Number of unique values
	 - Nans            Number/Percentage of Nan values
	 - Mean            Mean
	 - Std             Standard deviation
	 - Min             Lowest value
	 - Max             Biggest value
	 - < 25% Quantile  Number/Percentage of values lower than 25% quantile
	 - > 75% Quantile  Number/Percentage of values bigger than 75% quantile

	Args:
	    df: Dataframe
	Return:
	    Dataframe describing numerical columns
	'''

	colnames = ['Datatype', 'Unique', 'NaNs',
			'Mean', 'Std', 'Min', 'Max',
			'< 25% Quantile', '> 75% Quantile']

	df_num = df.select_dtypes(np.number)
	num_df = pd.DataFrame(columns=colnames)

	for col in df_num.columns:

		num_nans  = df_num[col].isna().sum()
		lower_q25 = len(df_num[df_num[col] < np.percentile(df_num[col], .25)])
		upper_q75 = len(df_num[df_num[col] > np.percentile(df_num[col], .75)])

		a = [
			df_num[col].dtype,
			df_num[col].nunique(),
			"{}/{:.1f}%".format(num_nans, num_nans*100/len(df)),
			df_num[col].mean(), df_num[col].std(),
			df_num[col].min(), df_num[col].max(),
			"{}/{:.1f}%".format(lower_q25, lower_q25*100/len(df)),
			"{}/{:.1f}%".format(upper_q75, upper_q75*100/len(df))
		]

		num_df = pd.concat([num_df, pd.DataFrame([a],
				columns=colnames, index=[col])])
	return num_df


def describe_categoricals(df):
	'''
	Returns a dataframe describing all categorical columns
	of the given dataframe (Similar to df.describe(object)).

	The dataframe has the following columns:
	 - Datatype  Datatype of column
	 - Unique    Number of unique values
	 - Nans      Number/Percentage of Nan values
	 - Unique    First three unique values

	Args:
	    df: Dataframe
	Return:
	    Dataframe
	'''

	colnames = ['Datatype', 'Unique', 'Nans', 'Values']
	df_cat = df.select_dtypes(object)
	cat_df = pd.DataFrame(columns=colnames)

	def get_uniques(col):
		uniq = []
		for i,val in enumerate(col.unique()):
			if i < 3:
				uniq.append(val)
			else:
				uniq.append('...')
				break
		return ", ".join(uniq)

	for col in df_cat.columns:
		nans = df_cat[col].isna().sum()

		a = [
			df_cat[col].dtype,
			df_cat[col].nunique(),
			"{}/{:.1f}%".format(nans, nans*100/len(df)),
			get_uniques(df_cat[col])
		]

		cat_df = pd.concat([cat_df, pd.DataFrame([a],
			columns=colnames, index=[col])])
	return cat_df


def get_outliers(data, column=None, lower_percentile=25, upper_percentile=75):
	'''
	Returns a list with row indeces of outliers, found within
	the given dataframe.

	Usage:
	        i = get_outliers(data)
	        data.loc[i,:]

	        i = get_outliers(data, 'age')
	        data.loc[i,:]

	Args:
	    data: Dataframe where to look for outliers
	    column: Name of column (None for all columns)
	    lower_percentile: The lower percentile
	    upper_percentile: The upper percentile
	Return:
	    List with row indeces of outliers
	'''
	cols = [column] if column else list(data.columns)
	indeces = []

	for col in data[cols].select_dtypes(np.number).columns:
		q3,q1 = np.percentile(data[col], [upper_percentile,
				lower_percentile])
		iqr = q3 - q1
		upper_limit = q3 + 1.5 * iqr
		lower_limit = q1 - 1.5 * iqr
		i = data[(data[col] < lower_limit) | (data[col] > upper_limit)].index
		indeces += list(i)

	return indeces
