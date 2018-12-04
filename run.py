from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.datasets import load_svmlight_file
from sklearn.ensemble import RandomForestClassifier
import argparse
import numpy as np
from sklearn.model_selection import GridSearchCV
import pickle
from inference import eval
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

def main(args):


	# load data
	X = np.load(args.mat)
	Y = np.load(args.y)
	
	# split data into train and test sets
	test_size = 0.2
	seed = 4
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

	if args.method == 'xgboost':
		rnd_model = XGBClassifier()
		parameters = {
			  'objective': ['binary:logistic'],
			  'booster': ['gbtree'],
			  'n_estimators': [100],
              'learning_rate': [0.1],
              'min_child_weight':[4],
              'max_depth': [20],
              'reg_alpha':[0.01],
              'gamma': [0.9], 
              'subsample':[1.0],
              'colsample_bytree':[0.9]
              }

		model = GridSearchCV(estimator=rnd_model, param_grid=parameters, \
		                          scoring='roc_auc', cv = 10, n_jobs = -1, verbose = 2)
	elif args.method == 'rf':
		model = RandomForestClassifier()
		parameters = {
		    'max_depth': [70, 80, 90],
		    'n_estimators': [50, 80, 90]}
		model = GridSearchCV(estimator=rnd_model, param_grid=parameters, \
		                          scoring='roc_auc', cv = 10, n_jobs = -1, verbose = 2)
	elif args.method == 'svm':
		scaler = StandardScaler().fit(X_train.astype(np.float64))
		X_train = scaler.transform(X_train)
		X_train = normalize(X_train)
		rnd_model = SVC(gamma='auto')
		parameters = {
		    'C': [1e-3, 1e-2, 1e-1, 1],
		    'kernel': ['rbf', 'linear']}
		model = GridSearchCV(estimator=rnd_model, param_grid=parameters, \
		                          scoring='roc_auc', cv = 10, n_jobs = -1, verbose = 2)
	elif args.method == 'nn':
		scaler = StandardScaler().fit(X_train.astype(np.float64))
		X_train = scaler.transform(X_train)
		X_train = normalize(X_train)
		model = MLPClassifier(learning_rate_init = 0.01)
	else:
		print("Invalid method name.")


	model.fit(X_train, y_train)
	y_pred = model.predict(X_train)
	eval(y_pred, y_train)
	print(classification_report(y_train,y_pred, digits=4))
	
	
	y_pred = model.predict(X_test)
	print(classification_report(y_test, y_pred, digits=4))
	pickle.dump('models', args.model_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run_file')
	parser.add_argument('--mat', type=str, default='data_unbalanced/mat.pickle',
	                    help='file_path')
	parser.add_argument('--y', type=str, default='data_unbalanced/y.pickle',
	                    help='file_path')
	parser.add_argument('--method', type=str, default='xgboost',
	                    help='[xgboost][rf][svm][nn]')
	parser.add_argument('--model_path', type=str, default='models/model.pickle',
	                    help='path to save model')
	args = parser.parse_args()
	main(args)