from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import json
import shutil
import logging
import time

logging.basicConfig(
    filename=f"logs/logs_{time.strftime('%b_%d_%Y_%H')}.log",
    level=logging.INFO,
    filemode='a+',
    format='%(name)s - %(levelname)s - %(message)s')

##################Load config.json and correct path variable
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])
prod_deployment_path = os.path.join(os.path.abspath(os.getcwd()),config['prod_deployment_path'])
model_path = os.path.join(os.path.abspath(os.getcwd()),config['output_model_path'])


####################function for deployment
def store_model_into_pickle():
    #copy the latest pickle file, the latestscore.txt value, and the ingestfiles.txt file into the deployment directory
    model_file = os.path.join(model_path, 'trainedmodel.pkl')
    txt_file = os.path.join(model_path, 'latestscore.txt')
    csv_file = os.path.join(dataset_csv_path, 'finaldata.csv')

    if not os.path.exists(prod_deployment_path):
        os.makedirs(prod_deployment_path)
        
    shutil.copy(model_file, prod_deployment_path)
    logging.info('Copied file %s to folder %s - %s', model_file, prod_deployment_path, 
        time.strftime('%b_%d_%Y_%H_%M_%S'))
    shutil.copy(txt_file, prod_deployment_path)
    logging.info('Copied file %s to folder %s - %s', txt_file, prod_deployment_path, 
        time.strftime('%b_%d_%Y_%H_%M_%S'))
    shutil.copy(csv_file, prod_deployment_path)
    logging.info('Copied file %s to folder %s - %s', csv_file, prod_deployment_path, 
        time.strftime('%b_%d_%Y_%H_%M_%S'))

if __name__ == '__main__':
    store_model_into_pickle()
        

