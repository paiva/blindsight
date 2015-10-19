#!/bin/python3

""" Provides analysis about the R-Mappings """

__author__  = 'Loraine'
__version__ = '1.0'

import pandas as pd
from math import sqrt
from config import path
from scipy.stats import ttest_ind

class Mapping(object):

	def __init__(self,csv):
		self.csv = csv
		self.path = path

	def get_type(self,val):
		if val[val.find('[') + 1 : val.find('[') + 2] is '-':
			return 'Unilateral'
		return 'Bilateral'


	def get_t_test(self,df):

		def get_mu(self,val):
			pass
		
		n = len(df.index)
		x = df['response'].mean()
		
		#t = (x - mu)/(s - sqrt(n))

		print(n)
		print(x)

	def read_csv(self):
		
		# Rename column names
		col_names = { 
    					'trials.thisRepN' : 'trials_repn', 
    					'trials.thisTrialN' : 'trials_trialn',
    					'trials.thisN' : 'trials_n',
    					'trials.thisIndex' : 'trials_index',
    					'response.keys' : 'response_keys',
    					'response.rt' : 'response_rt',
    					'frameRate' : 'frame_rate',
    					'expName' : 'exp_name'
		}

		# Read csv file into dataframe
		df = pd.read_csv(self.path + self.csv)
		df = df.rename(columns=col_names)
		return df

	def sort(self):
		raw_df = pd.read_csv(self.path + self.csv)
		df = pd.DataFrame({
							'image' : raw_df['image'],
							'location' : raw_df['location'],
							'mirror' : raw_df['mirror'],
							'response' : raw_df['response.rt'].map(lambda x: float(x[x.find('[')+1:x.find(']')])),
							'type' : raw_df['location'].apply(self.get_type)
						  })
		df = df.sort(['location']) 
		df = df.groupby(['location', 'type'], as_index=False).mean()
		
		return df 

	def run_t_test(self, df):

		data = pd.DataFrame({'location' : df['location'],
								'type' : df['type'],
								'response' : df['response']
		})

		unilateral = data[data['type'] == 'unilateral']
		bilateral = data[data['type'] == 'bilateral']
     
		ttest = ttest_ind(unilateral['response'], bilateral['response'], equal_var=False)
		if ttest[1] >= 0.95:
			return(True, ttest)
		else:
			return(False, ttest)
		return dict(ttest = ttest)

	def generate_matrix(self):
		pass

filename = 'FULL_RTEbehtask_2015_Aug_02_1837.csv'
test = Mapping(filename)

df = test.sort()
df2 = print(test.run_t_test(df))


