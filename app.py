from flask import Flask, session, jsonify, request
import pandas as pd
# import numpy as np
# import pickle
import diagnostics
import scoring
import json
import os



######################Set up variables for use in our script
app = Flask(__name__)
app.config['DEBUG'] = False
# app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

# with open('config.json','r') as f:
#     config = json.load(f) 

# dataset_csv_path = os.path.join(config['output_folder_path']) 

# prediction_model = None

def readpandas(filename):
    thedata = pd.read_csv(filename)
    return thedata

# @app.route('/')
# def index():
#     user = request.args.get('user')
#     return "Hello " + user
######################Prediction Endpoint
@app.route("/prediction", methods=['POST','OPTIONS'])
def predict():        
    #call the prediction function you created in Step 3
    filename = request.args.get('filename')
    df = readpandas(filename)
    drop_columns= ['corporation', 'exited']
    X = df.drop(drop_columns, axis=1)
    y_pre = diagnostics.model_predictions(X)
    return {'predictions': str(y_pre)}#add return value for prediction outputs

#######################Scoring Endpoint
@app.route("/scoring", methods=['GET','OPTIONS'])
def stats_score():        
    #check the score of the deployed model
    score = scoring.score_model()
    return {'score': score}#add return value (a single F1 score number)

#######################Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET','OPTIONS'])
def stats_summary():        
    #check means, medians, and modes for each column
    summary = diagnostics.dataframe_summary()
    return {'summary': summary}#return a list of all calculated summary statistics

#######################Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET','OPTIONS'])
def stats_diagnostics():        
    #check timing and percent NA values
    [ingestion_time, training_time] = diagnostics.execution_time()
    missing_data = diagnostics.missing_data()
    outdated_packages_list = diagnostics.outdated_packages_list()
    result = {
        'ingestion_time' : ingestion_time,
        'training_time' : training_time,
        'missing_data' : missing_data,
        'outdated_packages_list' : outdated_packages_list
    }
    return result #add return value for all diagnostics

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)