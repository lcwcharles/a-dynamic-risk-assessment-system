import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import glob
import logging
import time

logging.basicConfig(
    filename=f"logs/logs_{time.strftime('%b_%d_%Y_%H')}.log",
    level=logging.INFO,
    filemode='a+',
    format='%(name)s - %(levelname)s - %(message)s')

#############Load config.json and get input and output paths
with open('config.json','r') as f:
    config = json.load(f) 

input_folder_path = os.path.join(os.path.abspath(os.getcwd()),config['input_folder_path'])
output_folder_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])

#############Function for data ingestion
def merge_multiple_dataframe():
    #check for datasets, compile them together, and write to an output file

    # https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/
    input_file = glob.glob(input_folder_path + '/*.csv')
    df = pd.concat(map(pd.read_csv, input_file))
    df.drop_duplicates()

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    output_file = os.path.join(output_folder_path,'finaldata.csv')
    try:
        if config['output_model_path'] == 'models':
            df.to_csv(output_file, mode='a', index = False, header=False)
        else:
            df.to_csv(output_file, index = False)
        logging.info(
            "Saved data in %s - %s", output_file, time.strftime('%b_%d_%Y_%H_%M_%S'))
    except AssertionError as err:
        logging.error("Failed to save in  %s - %s", output_file, time.strftime('%b_%d_%Y_%H_%M_%S'))
        raise err

    output_txt = os.path.join(output_folder_path,'ingestedfiles.txt')
    with open(output_txt,'w') as f:
        for file_name in input_file:
            try:
                f.write(file_name + '\n')
                logging.info(
                    "Saved file name %s in %s - %s", file_name, output_txt, 
                    time.strftime('%b_%d_%Y_%H_%M_%S'))
            except AssertionError as err:
                logging.error("Failed to save in  %s - %s", output_txt, 
                time.strftime('%b_%d_%Y_%H_%M_%S'))
                raise err
            
if __name__ == '__main__':
    merge_multiple_dataframe()