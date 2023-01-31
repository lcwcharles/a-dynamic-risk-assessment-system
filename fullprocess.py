import pandas as pd
import numpy as np
import pickle
import os
import sys
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import shutil
import logging
import time
import training
import scoring
import deployment
import diagnostics
import reporting
import glob
import timeit
from itertools import chain

logging.basicConfig(
    filename=f"logs/logs_{time.strftime('%b_%d_%Y_%H')}.log",
    level=logging.INFO,
    filemode='a+',
    format='%(name)s - %(levelname)s - %(message)s')

with open('config.json','r') as f:
    config = json.load(f) 
dataset_csv_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])
prod_deployment_path = os.path.join(os.path.abspath(os.getcwd()),config['prod_deployment_path'])
model_path = os.path.join(os.path.abspath(os.getcwd()),config['output_model_path'])
input_folder_path = os.path.join(os.path.abspath(os.getcwd()),config['input_folder_path'])

if not os.path.exists(model_path):
    os.makedirs(model_path)

##################Check and read new data
#first, read ingestedfiles.txt
with open(os.path.join(dataset_csv_path, 'ingestedfiles.txt')) as f:
    old_file = pd.read_csv(f,header=None )

old_files = list(chain.from_iterable(old_file.values.tolist()))

#second, determine whether the source data folder has files that aren't listed in ingestedfiles.txt
new_input_file = glob.glob(input_folder_path + '/*.csv')
len_new_files = len(set(new_input_file) - set(old_files))
##################Deciding whether to proceed, part 1
#if you found new data, you should proceed. otherwise, do end the process here
if len_new_files>0:
    os.system('python3 ingestion.py')
else :
    sys.exit()

##################Checking for model drift
#check whether the score from the deployed model is different from the score from the model that uses the newest ingested data
f1score_txt = os.path.join(prod_deployment_path,'latestscore.txt')
with open(f1score_txt,'r') as f:
    deployed_model_score = f.read()

def new_score_model():
    #this function should take a trained model, load test data, and calculate an F1 score for the model relative to the test data
    #it should write the result to the latestscore.txt file
    final_data_file = glob.glob(dataset_csv_path + '/*.csv')
    df = pd.read_csv(final_data_file[0])
    with open(os.path.join(prod_deployment_path, 'trainedmodel.pkl'), 'rb') as f:
        model_lr = pickle.load(f)
    drop_columns= ['corporation', 'exited']
    X = df.drop(drop_columns, axis=1)
    y = df['exited']
    y_pre = model_lr.predict(X)
    f1_score= metrics.fbeta_score(y, y_pre, beta=1, zero_division=1)
    logging.info('f1_score: %s - %s', f1_score, time.strftime('%b_%d_%Y_%H_%M_%S'))
#     f1score_txt = os.path.join(model_path,'latestscore.txt')
#     with open(f1score_txt,'w') as f:
#         f.write(str(f1_score))
    return str(f1_score)

new_f1_score = new_score_model()
os.system('python3 scoring.py')

##################Deciding whether to proceed, part 2
#if you found model drift, you should proceed. otherwise, do end the process here
model_drift = new_f1_score < deployed_model_score
if model_drift:
    os.system('python3 training.py')
else:
    os.exit()

##################Re-deployment
#if you found evidence for model drift, re-run the deployment.py script
os.system('python3 deployment.py')

##################Diagnostics and reporting
#run diagnostics.py and reporting.py for the re-deployed model
os.system('python3 apicalls.py')
os.system('python3 reporting.py')


