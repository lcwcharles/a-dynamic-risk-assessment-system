import requests
import json
import os

#Specify a URL that resolves to your workspace
URL = "http://127.0.0.1:8000"
with open('config.json','r') as f:
    config = json.load(f) 

model_path = os.path.join(os.path.abspath(os.getcwd()),config['output_model_path'])
apireturns_txt = os.path.join(model_path, 'apireturns.txt')
#Call each API endpoint and store the responses
response1 = requests.post(URL + '/prediction?filename=testdata/testdata.csv')
response2 = requests.get(URL + '/scoring')
response3 = requests.get(URL + '/summarystats')
response4 = requests.get(URL + '/diagnostics')

#combine all API responses
responses = [
    response1,
    response2,
    response3,
    response4]

#write the responses to your workspace
with open(apireturns_txt, 'w') as f:
    for response in responses:
        f.write(str(response.json()) + '\n')
    f.close()
