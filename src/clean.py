import pandas as pd
import numpy as np
import re



def normalize_column_names(columns):
	'''
	Normalize column names.
	The following transformations will be applied:

	- Remove parenthesis and their content
	- Convert all letters to lower case
	- Replace whitespaces with underlines (' ' -> '_')
	- Remove leading/trailing whitespaces, tabs and newlines

	Args:
		columns: List of column names
	Return:
		List of normalized columns
	'''
	norm_columns = []

	for col in columns:
		colstr = re.sub('\(.*\)', '', col)
		colstr = colstr.strip().lower().replace(' ', '_')
		norm_columns.append(colstr)

	return norm_columns


