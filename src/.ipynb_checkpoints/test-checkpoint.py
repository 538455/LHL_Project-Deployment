## Python test file for flask to test locally
import requests as r
import pandas as pd
import json


base_url = 'http://127.0.0.1:5000/' #base url local host

json_data = [
    {
    "Loan_ID" : 
    "Gender" : 
    "Married" : 
    "Dependents" : 
    "Education" : 
    "Self_Employed" : 
    "ApplicantIncome" : 
    "CoapplicantIncome" : 
    "LoanAmount" : 
    "Loan_Amount_Term" : 
    "Credit_History" : 
    "Property_Area" : 
    "TotalIncome" : 
    }
]



# Get Response
# response = r.get(base_url)
response = r.post(base_url + "predict", json = json_data)


if response.status_code == 200:
    print('...')
    print('request successful')
    print('...')
    print(response.json())
else:
    print(response.json())
    print('request failed')
