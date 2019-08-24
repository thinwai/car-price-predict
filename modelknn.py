from flask import Flask, render_template, request
import numpy as np
import joblib
app = Flask(__name__)
model = joblib.load('newknn_joblib')

@app.route('/')
def index():
	return render_template("index.html")


def input_to_one_hot(data):
    # initialize the target vector with zero values
    enc_input = np.zeros(7)
    # set the numerical input as they are
    enc_input[0] = data['present_price']
    #enc_input[1] = data['year']
    enc_input[1] = data['kms_driven']
        ##################### Fuel Type ####################
    # get the array of fuel type
    fuel_type = ['Diesel', 'Petrol', 'CNG']
    cols =[ 'Present_Price', 'Kms_Driven','Fuel_Type_CNG', 'Fuel_Type_Diesel',
       'Fuel_Type_Petrol','Transmission_Automatic', 'Transmission_Manual']
    # redefine the the user inout to match the column name
    redefinded_user_input = 'Fuel_Type_'+data['fuel_type']
    # search for the index in columns name list 
    fuelType_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[fuelType_column_index] = 1

    ##################### Fuel Type ####################
    # get the array of fuel type
    transmission = ['Automatic', 'Manual']
    # redefine the the user inout to match the column name
    redefinded_user_input = 'Transmission_'+data['transmission']
    # search for the index in columns name list 
    transmission_column_index = cols.index(redefinded_user_input)
    # fullfill the found index with 1
    enc_input[transmission_column_index] = 1
        
    return enc_input

@app.route('/predict', methods=['POST'])
def predict():
    result=request.form
    present_price = result['present_price']
    fuel_type = result['fuel_type']
    transmission = result['transmission']
    #year = result['year']
    kms_driven = result['kms_driven']

    # we create a json object that will hold data from user inputs
    user_input ={'present_price':present_price, 'kms_driven':kms_driven, 'fuel_type':fuel_type, 'transmission':transmission}
    a = input_to_one_hot(user_input)
    price_pred = model.predict([a])[0]
    price_pred = round(price_pred, 2)
    #return json.dumps({'price':price_pred});
    #price_pred = model.predict(user_input)
    return render_template('result.html', prediction_text="Estimate price for the car is Lakhs {} ".format(price_pred))
    
    #return render_template('index.html', prediction_text='Predicted Price of This car: Rs{}'.format(price_pred))

if __name__ =="__main__":
    app.run(debug="True")