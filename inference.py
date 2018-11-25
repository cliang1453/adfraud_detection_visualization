from sklearn.metrics import roc_auc_score, roc_curve, auc
import argparse
import numpy as np
import pickle
import matplotlib.pyplot as plt
import csv
import os 

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

def write_csv(args, data, pred):
 
	pred = np.expand_dims(np.array(pred), 1)
	row = np.concatenate((np.array(data), pred), 1)
	with open(os.path.splitext(args.test_data)[0] + '.csv', 'w') as f:
		wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		wr.writerow(['ip', 'app', 'device', 'os', 'channel','click_scalar','is_attributed'])
		for r in row:
			wr.writerow(r)


def main(args):
	
	model = pickle.load(open(args.model, 'rb'))
	test_data = pickle.load(open(args.test_data, 'rb'))
	test_label = pickle.load(open(args.test_label, 'rb'))

	pred = model.predict(test_data)
	binary_pred = [round(value) for value in pred]
	eval(binary_pred, test_label)
	write_csv(args, test_data, binary_pred)




if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='inference_file')
	parser.add_argument('--test_data', type=str, default='data/mat1.pickle',
	                    help='file_path')
	parser.add_argument('--test_label', type=str, default='data/y1.pickle',
	                    help='file_path')
	parser.add_argument('--model', type=str, default='models/model.pickle',
	                    help='model_path')
	args = parser.parse_args()
	main(args)