#!/bin/python3

""" Provides analysis about the R-Mappings """

__author__  = 'Loraine'
__version__ = '1.0'

import pandas as pd
import numpy as np
from config import path
from scipy.stats import ttest_ind

class RMapping(object):

	def __init__(self,filename):
		self.df = pd.read_csv(path + filename)
		
	def get_x_coordinate(self,val):
		"""Gets x coordinate of Location"""
		return val[val.find('[') + 1 : val.find(',')]  

	def get_y_coordinate(self,val):
		"""Gets y coordinate of Location""" 
		return val[val.find(',') +1 : val.find(']')]

	def get_type(self,val):
		"""Identifies Location type"""
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			return 'Unilateral'
		return 'Bilateral'		

	def get_val(self,val):
		return val

	def get_unilateral_response(self,val):
		response = self.df['response'].where(self.df['location'] == val).dropna().mean()
		return response

	def get_bilateral_response(self,val):
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			val = '[' + val[val.find('[') + 2 : val.find(']')] + ']' 
		response = self.df['response'].where(self.df['location'] == val).dropna().mean()
		return response

	def get_pval_values(self,val1,val2):
		return ttest_ind(val1, val2, equal_var=False)[1]


	def read_csv(self):
		
		df = pd.DataFrame({
							'location' : self.df['location'],
							'response' : self.df['response.rt'].map(lambda x: float(x[x.find('[')+1:x.find(']')])),
							'type' : self.df['location'].apply(self.get_type)
						  })
		self.df = df
		return self.df

	def sort(self,df):

		data = df.sort(['location']) 
		data = df.groupby(['location','type'], as_index=False).mean()
		
		return data 

	def get_pval(self,df):   

		mydf = pd.DataFrame({
							'location': df['location'],
							'response_unilateral' : df['location'].apply(self.get_unilateral_response),
							'response_bilateral'  : df['location'].apply(self.get_bilateral_response)
						 })

		mydf2 = pd.DataFrame({
							'location': mydf['location'],
							'response_unilateral' : mydf['response_unilateral'],
							'response_bilateral'  : mydf['response_bilateral'],
							't_test' : self.get_pval_values(mydf['response_unilateral'].apply(self.get_val),mydf['response_bilateral'].apply(self.get_val))
						 })

		return mydf2

		#if pval >= 0.95:
		#	return(True, ttest)
		#else:
		#	return(False, ttest)
		#return dict(ttest = ttest)

	def generate_matrix(self):
		pass

################## Run Test #########################

filename = 'FULL_RTEbehtask_2015_Aug_02_1837.csv'
trial = RMapping(filename)

df = trial.read_csv()
df2 = trial.sort(df)
df3 = trial.get_pval(df2)
print(df3)

