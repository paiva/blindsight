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

	def get_sign(self,val):
		"""Gets the x sign of the location"""
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			return '-'
		return '+'

	def get_x_coordinate(self,val):
		"""Gets x coordinate of Location"""
		return float(val[val.find('[') + 1 : val.find(',')])

	def get_y_coordinate(self,val):
		"""Gets y coordinate of Location""" 
		return float(val[val.find(',') + 1 : val.find(']')])

	def get_type(self,val):
		"""Identifies Location type"""
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			return 'unilateral'
		return 'bilateral'		

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

	def get_responses(self):
		
		responses = []
		for location in self.locations:
			sign = self.get_sign(location)
			x_coordinate = self.get_x_coordinate(location)
			y_coordinate = self.get_y_coordinate(location)

			# 1- Get Unilateral Responses
			if sign is not '-':
				location = '[' + '-' + str(x_coordinate) + ', ' + str(y_coordinate) + ']'
			unilateral_responses = self.df['response'].where(self.df['location'] == location).dropna().tolist()

			# 2- Get Bilateral Responses
			if sign is '-':
				location = '[' + str(x_coordinate) + ', ' + str(y_coordinate) + ']' 
			bilateral_responses = self.df['response'].where(self.df['location'] == location).dropna().tolist()#.astype(float)

			dic = {	'location': location,
					'unilateral_responses' : unilateral_responses,
					'bilateral_responses' : bilateral_responses,
					'pval' : ttest_ind(unilateral_responses, bilateral_responses)[1]}
			
			responses.append(dic)
		
		self.df = pd.DataFrame(responses) 
		return self.df


################## Run Test #########################

filename = 'FULL_RTEbehtask_2015_Aug_02_1837.csv'
trial = RMapping(filename)

trial.read_csv()
trial.sort()
trial.get_responses()
trial.print_df()

