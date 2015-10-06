#!/bin/python3

""" Provides analysis about the R-Mappings """

__author__  = 'Loraine'
__version__ = '1.0'

import pandas as pd
from config import path

class Mapping(object):

	def __init__(self, csv):
		self.csv = csv
		self.path = path

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
							'response' : raw_df['response.rt'].apply(lambda x: float(x[x.find('[')+1:x.find(']')]))
			})
		df = df.sort(['location']) 
		df = df.groupby(['location']).mean()
		return df

	def group_uni_bi(self):
		"""Groups Unilateral with bilateral counter part"""

		pass

	def run_t_test(self):
		""" Must compare results with a t-test """
		pass

	def generate_matrix(self):
		pass

	# sorting the data and running a t-test

filename = 'FULL_RTEbehtask_2015_Aug_02_1837.csv'
test = Mapping(filename)
print(test.sort())


