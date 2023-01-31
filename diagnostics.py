
import pandas as pd
import numpy as np
import timeit
import os
import json
import pickle
import logging
import time
import glob
import subprocess
import sys

logging.basicConfig(
    filename=f"logs/logs_{time.strftime('%b_%d_%Y_%H')}.log",
    level=logging.INFO,
    filemode='a+',
    format='%(name)s - %(levelname)s - %(message)s')

##################Load config.json and get environment variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])
test_data_path = os.path.join(os.path.abspath(os.getcwd()),config['test_data_path'])
prod_deployment_path = os.path.join(os.path.abspath(os.getcwd()),config['prod_deployment_path'])

##################Function to get model predictions
def model_predictions(X):
    #read the deployed model and a test dataset, calculate predictions
    with open(os.path.join(prod_deployment_path, 'trainedmodel.pkl'), 'rb') as f:
        model_lr = pickle.load(f)
    
    predictions = model_lr.predict(X)
    try:
        assert len(predictions) == len(X)
        logging.info('The list of predictions has the same length as the number of \
                    rows in the input dataset. - %s', time.strftime('%b_%d_%Y_%H_%M_%S'))
    except AssertionError as err:
        logging.error("The list of predictions has the different length as the number of \
                    rows in the input dataset. - %s",  time.strftime('%b_%d_%Y_%H_%M_%S'))
        raise err
    return list(predictions)#return value should be a list containing all predictions

##################Function to get summary statistics
def dataframe_summary():
    #calculate summary statistics here
    df = pd.read_csv(os.path.join(dataset_csv_path, 'finaldata.csv'))
    numeric_columns = ['lastmonth_activity', 'lastyear_activity', 'number_of_employees']
    summary_statistics = df[numeric_columns].agg(['mean', 'median', 'std'])
    logging.info('The summary statistics are %s. - %s', summary_statistics, 
        time.strftime('%b_%d_%Y_%H_%M_%S'))
    try:
        assert summary_statistics.shape == (3, len(numeric_columns))
        logging.info('Had calculated summary statistics for each numeric column. - %s', 
            time.strftime('%b_%d_%Y_%H_%M_%S'))
    except AssertionError as err:
        logging.error("Something wrong with summary statistics for each numeric column. - %s", 
            time.strftime('%b_%d_%Y_%H_%M_%S'))
        raise err
    #return value should be a list containing all summary statistics
    return summary_statistics.values.tolist()

def missing_data():
    df = pd.read_csv(os.path.join(dataset_csv_path, 'finaldata.csv'))
    percent_na_values = df.isna().sum() / len(df)
    try:
        assert len(percent_na_values) == len(df.columns)
        logging.info('Has same number of elements with the number of columns in the dataset. - %s', 
            time.strftime('%b_%d_%Y_%H_%M_%S'))
    except AssertionError as err:
        logging.error("Something wrong with calculate percent of each column \
            consists of NA values. - %s", time.strftime('%b_%d_%Y_%H_%M_%S'))
        raise err
    return percent_na_values.tolist()

def ingestion_timing():
    starttime = timeit.default_timer()
    os.system('python3 ingestion.py')
    timming = timeit.default_timer() - starttime
    return timming

def training_timing():
    starttime = timeit.default_timer()
    os.system('python3 training.py')
    timming = timeit.default_timer() - starttime
    return timming

##################Function to get timings
def execution_time():
    #calculate timing of training.py and ingestion.py
    ingestion_time = ingestion_timing()
    training_time = training_timing()
    #return a list of 2 timing values in seconds
    return [ingestion_time, training_time]

##################Function to check dependencies
def outdated_packages_list():
    #get a list of 
    with open('requirements.txt', 'r') as f:
        rdf = pd.read_csv(f,sep='==',header=None, names=['Package','Version'])
    outdated_packages = subprocess.check_output(['pip', 'list', '--outdated']).decode(sys.stdout.encoding).split('\n')
    outdated_packages_list = [package.split() for package in outdated_packages]
    outdated_packages_df = pd.DataFrame(outdated_packages_list,index=None )
    outdated_packages_df.columns = outdated_packages_df.iloc[0]
    outdated_packages_df = outdated_packages_df.iloc[2:-1]
    packages_df = pd.merge(rdf, outdated_packages_df, on='Package', how='left')
    packages_df = packages_df[['Package', 'Version_y', 'Latest']]
    packages_df.rename(columns = {'Version_y':'currently_version'}, inplace = True)
    return packages_df.values.tolist()

if __name__ == '__main__':
    test_data_file = glob.glob(test_data_path + '/*.csv')
    df = pd.read_csv(test_data_file[0])
    drop_columns= ['corporation', 'exited']
    X = df.drop(drop_columns, axis=1)

    model_predictions(X)
    dataframe_summary()
    missing_data()
    execution_time()
    outdated_packages_list()





    
