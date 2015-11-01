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
		self.locations = self.df['location'].unique().tolist()
		
	def print_df(self):
		print(self.df)

	def get_x_coordinate(self,val):
		"""Gets x coordinate of Location"""
		return float(val[val.find('[') + 1 : val.find(',')])

	def get_y_coordinate(self,val):
		"""Gets y coordinate of Location""" 
		return float(val[val.find(',') +1 : val.find(']')])

	def get_type(self,val):
		"""Identifies Location type"""
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			return 'unilateral'
		return 'bilateral'		

	def get_unilateral_response(self,val):
		response = self.df['response'].where(self.df['location'] == val).dropna()
		return response

	def get_bilateral_response(self,val):
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			val = '[' + val[val.find('[') + 2 : val.find(']')] + ']' 
		response = self.df['response'].where(self.df['location'] == val).dropna().mean()
		return response

	def get_pval_values(self,val1,val2):
		return ttest_ind(val1, val2, equal_var=False)[1]

	def read_csv(self):
		
		self.df = pd.DataFrame({
							'x_coordinate': self.df['location'].apply(self.get_x_coordinate),
							'y_coordinate': self.df['location'].apply(self.get_y_coordinate),
							'location' : self.df['location'],
							'response' : self.df['response.rt'].map(lambda x: float(x[x.find('[')+1:x.find(']')])),
							'type' : self.df['location'].apply(self.get_type)
						  })
		return self.df

	def sort(self):

		self.df = self.df.sort(['x_coordinate', 'y_coordinate'], ascending=[1,1])
		self.df = self.df[['location','type','response']]

		return self.df

	def run_t_test(self):   

		self.df = pd.DataFrame({
							'location': self.df['location'],
							'response_unilateral' : self.df['location'].apply(self.get_unilateral_response),
							'response_bilateral'  : self.df['location'].apply(self.get_bilateral_response)
						 })

		return self.df

################## Run Test #########################

filename = 'FULL_RTEbehtask_2015_Aug_02_1837.csv'
trial = RMapping(filename)

trial.read_csv()
trial.sort()
trial.print_df()
#trial.run_t_test()

