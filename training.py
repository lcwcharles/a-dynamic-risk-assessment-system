from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import glob
import logging
import time

logging.basicConfig(
    filename=f"logs/logs_{time.strftime('%b_%d_%Y_%H')}.log",
    level=logging.INFO,
    filemode='a+',
    format='%(name)s - %(levelname)s - %(message)s')

###################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])
model_path = os.path.join(os.path.abspath(os.getcwd()),config['output_model_path'])

#################Function for training the model
def train_model():
    
    dataset_file = glob.glob(dataset_csv_path + '/*.csv')
    df = pd.read_csv(dataset_file[0])
    drop_columns= ['corporation', 'exited']
    X = df.drop(drop_columns, axis=1)
    y = df['exited']

    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=40, 
                                                    test_size=0.25, 
                                                    shuffle=True)
    #use this logistic regression for training
    model_lr = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                    intercept_scaling=1, l1_ratio=None, max_iter=100,
                    multi_class='auto', n_jobs=None, penalty='l2',
                    random_state=0, solver='liblinear', tol=0.0001, verbose=0,
                    warm_start=False)
    
    #fit the logistic regression to your data
    logging.info(
        "Training model - %s", time.strftime('%b_%d_%Y_%H_%M_%S'))
    trained_model = model_lr.fit(X_train, y_train)
    logging.info(
        "Train model finished - %s", time.strftime('%b_%d_%Y_%H_%M_%S'))

    #write the trained model to your workspace in a file called trainedmodel.pkl
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    model_file = os.path.join(model_path,'trainedmodel.pkl')
    try:
        pickle.dump(trained_model, open(model_file, 'wb'))
        logging.info(
            "Saved the model in %s - %s", model_file, time.strftime('%b_%d_%Y_%H_%M_%S'))
    except AssertionError as err:
        logging.error("Failed to save the model in  %s - %s", model_file, time.strftime('%b_%d_%Y_%H_%M_%S'))
        raise err
    
if __name__ == '__main__':
    train_model()