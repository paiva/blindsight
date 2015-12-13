#!/bin/python3

""" Provides analysis about the R-Mappings """

__author__  = 'Loraine'
__version__ = '1.0'

import pandas as pd
from config import path
from scipy.stats import ttest_ind

class FirstExperiment(object):

	def __init__(self,filename):
		self.df = pd.read_csv(path + filename)
		self.locations = self.df['location'].unique().tolist()
		
	def print_df(self):
		print(self.df)

	def count_pval(self):
		print(self.df.groupby('pval').count())

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

	def get_pvalues(self):
		return self.df[['location','pval']]

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

		self.df = self.df.sort_values(by=['x_coordinate', 'y_coordinate'], ascending=[1,1])
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
				unilateral_location = '[' + '-' + str(x_coordinate) + ', ' + str(y_coordinate) + ']'
			elif sign is '-':
				unilateral_location = location
			unilateral_responses = self.df['response'].where(self.df['location'] == unilateral_location).dropna().tolist()

			# 2- Get Bilateral Responses
			if sign is '-':
				bilateral_location = '[' + str(abs(x_coordinate)) + ', ' + str(y_coordinate) + ']' 
			elif sign is not '-':
				bilateral_location = location
			bilateral_responses = self.df['response'].where(self.df['location'] == bilateral_location).dropna().tolist()


			dic = {	'location': location,
					'unilateral_responses' : unilateral_responses,
					'bilateral_responses' : bilateral_responses,
					'pval' : ttest_ind(unilateral_responses, bilateral_responses)[1]
				  }

			responses.append(dic)			

		self.df = pd.DataFrame(responses).sort_values(by='pval').drop_duplicates(['pval'])
		return self.df

	def run(self):
		self.read_csv()
		self.sort()
		self.get_responses().to_csv('blindsight.csv')


class SecondExperiment(object):

	def __init__(self, filename):
		self.df = pd.read_csv(path + filename)
		self.locations = self.df['location'].unique().tolist()

	def get_x_coordinate(self,val):
		"""Gets x coordinate of Location"""
		return float(val[val.find('[') + 1 : val.find(',')])

	def get_y_coordinate(self,val):
		"""Gets y coordinate of Location""" 
		return float(val[val.find(',') + 1 : val.find(']')])

	def read_csv(self):

		self.df = pd.DataFrame({
							'x_coordinate': self.df['location'].apply(self.get_x_coordinate),
							'y_coordinate': self.df['location'].apply(self.get_y_coordinate),
							'location' : self.df['location'],
							'correct_response': self.df['corrResp'],
							'given_response' : self.df['response.keys'].map(lambda x: str(x[x.find('[')+2:x.find(']')-1]))
						  })
		return self.df


	def sort(self):

		self.df = self.df.sort_values(by=['x_coordinate', 'y_coordinate'], ascending=[1,1])
		self.df = self.df[['location','correct_response','given_response']]

		return self.df


	def calculate_percentages(self, list_1, list_2):

		count = 0
		for i,j in zip(list_1,list_2):
			if i == j:
				count = count + 1

		return (count/5)*100

	def get_responses(self):
		
		responses = []
		for location in self.locations:

			correct_responses = self.df['correct_response'].where(self.df['location'] == location).dropna().tolist()
			given_responses = self.df['given_response'].where(self.df['location'] == location).dropna().tolist()

			dic = {	'location': location,
					'correct_responses' : correct_responses,
					'given_responses' : given_responses,
					'percentage' : self.calculate_percentages(correct_responses,given_responses)
				  }

			responses.append(dic)			

		self.df = pd.DataFrame(responses).sort_values(by='location')
		return self.df

	def run(self):
		self.read_csv()
		self.sort()
		self.get_responses().to_csv('responses.csv')

### Running Files

#FirstExperiment('FULL_RTEbehtask_2015_Aug_02_1837.csv').run()
SecondExperiment('FULL_SameDifftest_2015_Aug_02_1929.csv').run()