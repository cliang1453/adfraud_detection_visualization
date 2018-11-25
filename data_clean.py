import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import dump_svmlight_file
import argparse
import random
import os

class DataLoader():

	def __init__(self, args):
		self.chunksize = 5000
		self.num_batch = 3000
		self.test_batch = 200
		self.args = args

	def negative_sampling(self, mat, y):
		
		num_ones = np.count_nonzero(y)
		ones_to_save = np.nonzero(y)[0]
		zeros_to_save = np.random.choice(np.arange(self.chunksize), num_ones, replace=False)
		save = np.concatenate((ones_to_save, zeros_to_save), axis=0)
		np.random.shuffle(save)

		return mat[save], y[save] 
	
	def clean(self, file):

		result_mat = []
		result_y = []
		cnt = 0
		
		for df in pd.read_csv(file, chunksize=self.chunksize):
			
			#since most of rows in attribute_time column is null, we directly drop it 
			df.drop(df.columns[6], axis=1, inplace=True)
			
			#convert click_time column type from object to datetime
			df['click_time'] =  pd.to_datetime(df['click_time'])
			
			#convert click_time to the difference between current click_time with minimal click_time in seconds unit
			min_click_time = min(df['click_time'])
			df['click_time'] = df['click_time'].apply(lambda x : x-min_click_time)
			df['click_scalar'] = df['click_time'].apply(lambda x : x.total_seconds())
			
			#drop original click_time column,
			df.drop(df.columns[5], axis=1, inplace=True)
			
			#adjust column order move is_attribute to last column
			df = df[['ip', 'app', 'device', 'os', 'channel','click_scalar','is_attributed']]

			#write from dataframe to numpy array
			y = np.array(df.is_attributed)
			dummy = pd.get_dummies(df)
			mat = np.array(dummy)[:, :-1]

			# negative sampling
			mat, y = self.negative_sampling(mat, y)
			result_mat.append(mat)
			result_y.append(y)
			
			if cnt==0 and len(result_mat) > self.num_batch:
				self.dump(result_mat, result_y, args.mat, args.y, cnt)
				result_mat = []
				result_y = []
				cnt += 1
				print('dump training set')

			if cnt>0 and len(result_mat) > self.test_batch:
				self.dump(result_mat, result_y, args.mat, args.y, cnt)
				result_mat = []
				result_y = []
				cnt += 1
				print('dump test set')

			if cnt > 5: 
				break


	def dump(self, mat, y, mat_file, y_file, cnt):
		mat = np.vstack(mat)	
		y = np.concatenate(y)
		if cnt == 0:
			mat.dump(mat_file)
			y.dump(y_file)
		else:
			mat.dump(os.path.splitext(mat_file)[0] + str(cnt) + os.path.splitext(mat_file)[1])
			y.dump(os.path.splitext(y_file)[0] + str(cnt) + os.path.splitext(y_file)[1])


def main(args):
	loader = DataLoader(args)
	loader.clean(args.file)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='file_reader.')
	parser.add_argument('--file', type=str, default='data/train.csv',
	                    help='file_path')
	parser.add_argument('--mat', type=str, default='data/mat.pickle',
	                    help='file_path')
	parser.add_argument('--y', type=str, default='data/y.pickle',
	                    help='file_path')
	args = parser.parse_args()
	main(args)