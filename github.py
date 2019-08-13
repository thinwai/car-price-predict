# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 21:31:17 2019

@author: hello_world
"""

# user_input = [2010, 124999.5, 6, 'Diesel', 'BMW']
user_input = {'year_model':2006, 'mileage':82499.5, 'fiscal_power':6, 'fuel_type':'Diesel', 'mark':'Dacia'}
def input_to_one_hot(data):
    # initialize the target vector with zero values
    enc_input = np.zeros(61)
    # set the numerical input as they are
    enc_input[0] = data['year_model']
    enc_input[1] = data['mileage']
    enc_input[2] = data['fiscal_power']
    ##################### Mark #########################
    # get the array of marks categories
    marks = df.mark.unique()
    # redefine the the user inout to match the column name
    redefinded_user_input = 'mark_'+data['mark']
    # search for the index in columns name list 
    mark_column_index = X.columns.tolist().index(redefinded_user_input)
    #print(mark_column_index)
    # fullfill the found index with 1
    enc_input[mark_column_index] = 1
    ##################### Fuel Type ####################
    # get the array of fuel type
    fuel_types = df.fuel_type.unique()
    # redefine the the user inout to match the column name
    redefinded_user_input = 'fuel_type_'+data['fuel_type']
    # search for the index in columns name list 
    fuelType_column_index = X.columns.tolist().index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[fuelType_column_index] = 1
    return enc_input

print(input_to_one_hot(user_input))

a = input_to_one_hot(user_input)

price_pred = gbr.predict([a])

price_pred[0]

#########
from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import numpy as np
import json

# load the built-in model 
gbr = joblib.load('model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def get_delay():
    result=request.form
    year_model = result['year_model']
    mileage = result['mileage']
    mark = result['mark']
    fiscal_power = result['fiscal_power']
    fuel_type = result['fuel_type']
    # we create a json object that will hold data from user inputs
    user_input = {'year_model':year_model, 'mileage':mileage, 'fiscal_power':fiscal_power, 'fuel_type':fuel_type, 'mark':mark}
    # encode the json object to one hot encoding so that it could fit our model
    a = input_to_one_hot(user_input)
    # get the price prediction
    price_pred = gbr.predict([a])[0]
    price_pred = round(price_pred, 2)
    # return a json value
    return json.dumps({'price':price_pred});

if __name__ == '__main__':
    app.run(port=8080, debug=True)