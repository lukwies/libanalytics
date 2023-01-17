import pandas as pd
import numpy as np

def log_transform(x):
	'''
	Returns the logarithm of x or np.NAN if given value is zero.
	The idea is to replace all NaN values later using the mean..

	Args:
		x: Value to calculate logarithm from
	Return:
		Logarithm of x or np.NAN if x==0
	'''
	x = np.log10(x)
	return x if np.isfinite(x) else np.NAN
