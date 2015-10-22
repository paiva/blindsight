#!/bin/python3

""" Provides analysis about the R-Mappings """

__author__  = 'Loraine'
__version__ = '1.0'

import pandas as pd
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

	def get_unilateral(self,val):
		print(self.df['response.rt'].where(self.df['location'] == val))
		
	def get_bilateral(self,val):
		return self.df['response.rt']

	def read_csv(self):
		
		#df = pd.DataFrame({
		#					'x' : raw_df['location'].apply(self.get_x_coordinate),
		#					'y' : raw_df['location'].apply(self.get_y_coordinate),
		#					'location' : raw_df['location'],
		#					'response' : raw_df['response.rt'].map(lambda x: float(x[x.find('[')+1:x.find(']')])),
		#					'type' : raw_df['location'].apply(self.get_type)
		#				  })
		
		df = pd.DataFrame({
							'location' : self.df['location'],
							'unilateral_response' : self.df['location'].apply(self.get_unilateral)
							#'bilateral_response' : self.df['location'].apply(self.get_bilateral)
						  })
		

		return df

	def sort(self,df):

		data = df.sort(['location']) 
		data = df.groupby(['location','type'], as_index=False).mean()
		
		return data 

	def get_pval(self, df):

		unilateral = df[df['type'] == 'Unilateral']
		bilateral = df[df['type'] == 'Bilateral']
     
		ttest = ttest_ind(unilateral['response'], bilateral['response'], equal_var=False)
		pval = ttest[1]

		return pval

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

df = trial.sort(trial.read_csv())
print(df)
#df2 = print(trial.run_t_test(df))


