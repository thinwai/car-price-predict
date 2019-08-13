from flask import Flask, render_template, request
import joblib
app = Flask(__name__)
model = joblib.load('model_joblib')

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    result=request.form
    present_price = result['present_price']
    fuel_type = result['fuel_type']
    transmission = result['transmission']
    year = result['year']
    kms_driven = result['kms_driven']

    # we create a json object that will hold data from user inputs
    user_input = {{'present_price':present_price, 'fuel_type':fuel_type, 'transmission':transmission, 'year':year, 'kms_driven':kms_driven}}
    price_pred = model.predict(user_input)
    return render_template('index.html', prediction_text=price_pred)
    
    #return render_template('index.html', prediction_text='Predicted Price of This car: Rs{}'.format(price_pred))

if __name__ =="__main__":
	app.run(debug="True")