# Adclick Fraud Detection Visualisation #

Under Construction

1. Data cleaning

Run following command to save data and labels. One training set xxx.pickle and 5 testing sets xxx1.pickle, xxx2.pickle, xxx3.pickle, xxx4.pickle, xxx5.pickle will be saved to the [output_unbalanced_set_path] and [output_balanced_set_path] specified. The training set size will be the same for both balanced and unbalanced trainset.  

python3 data_clean.py --file=[csv_file_path] --mat_ub=[output_unbalanced_set_path/xxx.pickle] --mat_b=[output_balanced_set_path/xxx.pickle] --y_ub=[output_labels_path_for_unbalanced_set/xxx.pickle] --y_b=[output_labels_path_for_balanced_set/xxx.pickle]

2. Model training

Run following command to fit data and labels using specified method, visualize the training AUC and precision recall matrix and save the model

python3 run.py --mat=[data_file_path/xxx.pickle] --y=[label_file_path/xxx.pickle] --method=[[xgboost][rf][svm][nn]] --model_path=[path to save model/xxx.pickle]

3. Model inference

Run following command to inference the pretrained model on test sets, visualize the testing AUC and precision recall matrix, and dump the prediction result in data_file_path/xxx.csv]

python3 inference.py --test_data=[data_file_path/xxx.pickle] --test_label=[label_file_path/xxx.pickle] --model=[pretrained_model_path/xxx.pickle]

4. To run flask
Run following command:
$ export FLASK_APP=backend.py
$ flask run
