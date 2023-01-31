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



#################Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 


dataset_csv_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])
test_data_path = os.path.join(os.path.abspath(os.getcwd()),config['test_data_path'])
model_path = os.path.join(os.path.abspath(os.getcwd()),config['output_model_path'])

#################Function for model scoring
def score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
    test_data_file = glob.glob(test_data_path + '/*.csv')
    model_file = glob.glob(model_path + '/*.pkl')
    df = pd.read_csv(test_data_file[0])
    model_lr = pickle.load(open(model_file[0], 'rb'))
    drop_columns= ['corporation', 'exited']
    X = df.drop(drop_columns, axis=1)
    y = df['exited']
    y_pre = model_lr.predict(X)
    f1_score= metrics.fbeta_score(y, y_pre, beta=1, zero_division=1)
    logging.info('f1_score: %s - %s', f1_score, time.strftime('%b_%d_%Y_%H_%M_%S'))

    f1score_txt = os.path.join(model_path,'latestscore.txt')
    with open(f1score_txt,'w') as f:
        f.write(str(f1_score))

    return str(f1_score)
     

if __name__ == '__main__':
    score_model()
