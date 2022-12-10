# import Flask and jsonify
import flask
from flask import render_template, Flask, jsonify, request
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import traceback #allows you to send error to user
import pandas as pd
import numpy as np
import pickle

# App definition
app = Flask(__name__)
api = Api(app)

# importing models
model = pickle.load( open( "savedModel.pkl", "rb" ) )
model_columns = pickle.load( open( "modelColumns.pkl", "rb" ) )

# Now, we need to create an endpoint where we can communicate with our ML model. This time, we are going to use POST request.

class Prediction(Resource):
    def post(self):
        json_data = request.get_json()
        
        df = pd.DataFrame(json_data.values(), index=json_data.keys()).transpose()
        
        # getting predictions from our model.
        # it is much simpler because we used pipelines during development

        # still, we need to create our totalIncome feature
        df['totalIncome'] = df['ApplicantIncome'] + df['CoapplicantIncome']

        # we need to make sure that we have all the columns that our model was trained on
        df = df.reindex(columns=model_columns, fill_value=0)

        Return = model.predict(df).tolist()
        
        if str(Return) == '[1]':
            Return = "Your loan is likely to approved!"
        elif str(Return) == '[0]':
            Return = "Your loan is likely to be rejected..."
        else:
            Return = "There was an error with your request, make sure you have entered all the required fields and try again."
        
        return Return

# assign endpoint
api.add_resource(Prediction, '/prediction')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    app.run()
