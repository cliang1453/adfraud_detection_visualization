from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import RandomForestClassifier
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV

def eval(predictions, y_test):
	
	# evaluate predictions
	score = roc_auc_score(y_test, predictions)
	fpr, tpr, thresholds = roc_curve(y_test, predictions, pos_label=1)
	roc_auc = auc(fpr, tpr)

	plt.title('ROC')
	plt.plot(fpr, tpr, 'r', label = 'AUC = %0.2f' % roc_auc)
	plt.legend(loc = 'lower right')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.ylabel('True Positive Rate')
	plt.xlabel('False Positive Rate')
	plt.show()


def main(args):


	# load data
	X = np.load(args.mat)
	Y = np.load(args.y)
	
	# split data into train and test sets
	test_size = 0.2
	seed = 7
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

	if args.method == 'xgboost':
		rnd_model = XGBClassifier()
		parameters = {
              'learning_rate': [0.05, 0.1, 0.5, 1], 
              'max_depth': [6, 7, 8]}
		model = GridSearchCV(estimator=rnd_model, param_grid=parameters, \
		                          scoring='roc_auc', cv = 5, n_jobs = -1, verbose = 2)
	elif args.method == 'rf':
		rnd_model = RandomForestClassifier()
		parameters = {
		    'max_depth': [70, 80, 90],
		    'n_estimators': [50, 80, 90]}
		model = GridSearchCV(estimator=rnd_model, param_grid=parameters, \
		                          scoring='roc_auc', cv = 5, n_jobs = -1, verbose = 2)


	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)
	predictions = [round(value) for value in y_pred]
	eval(predictions, y_test)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run_file')
	parser.add_argument('--mat', type=str, default='data/mat.pickle',
	                    help='file_path')
	parser.add_argument('--y', type=str, default='data/y.pickle',
	                    help='file_path')
	parser.add_argument('--method', type=str, default='xgboost',
	                    help='[xgboost][rf]')
	args = parser.parse_args()
	main(args)