import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions

###############Load config.json and get path variables
with open('config.json','r') as f:
    config = json.load(f) 

dataset_csv_path = os.path.join(os.path.abspath(os.getcwd()),config['output_folder_path'])
test_data_path = os.path.join(os.path.abspath(os.getcwd()),config['test_data_path'])
model_path = os.path.join(os.path.abspath(os.getcwd()),config['output_model_path'])

##############Function for reporting
def score_model():
    #calculate a confusion matrix using the test data and the deployed model
    #write the confusion matrix to the workspace
    test_data_file = os.path.join(test_data_path, 'testdata.csv')
    df = pd.read_csv(test_data_file)
    drop_columns= ['corporation', 'exited']
    X = df.drop(drop_columns, axis=1)
    y = df['exited']

    y_pre = model_predictions(X)
    cf_matrix = metrics.confusion_matrix(y, y_pre)

    cf_matrix_png = os.path.join(model_path, 'confusionmatrix.png')

    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues')
    ax.set_title('Seaborn Confusion Matrix\n');
    ax.set_xlabel('Predicted Values')
    ax.set_ylabel('Actual Values ');
    ## Ticket labels - List must be in alphabetical order
    ax.xaxis.set_ticklabels(['False','True'])
    ax.yaxis.set_ticklabels(['False','True'])
    # bbox_inches	Set it as “tight” for proper fit of the saved figure.
    ax.figure.savefig(cf_matrix_png, dpi=300, bbox_inches='tight')
    plt.show()

    # #The other method
    # disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cf_matrix)
    # disp.plot()
    # plt.title('Confusion Matrix\n')
    # plt.savefig('confusionmatrix.png', dpi=300, bbox_inches='tight')
    # plt.show()

if __name__ == '__main__':
    score_model()
