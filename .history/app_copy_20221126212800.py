from flask import Flask,request, url_for, redirect, render_template, jsonify
from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np
from pycaret.time_series import TSForecastingExperiment
app = Flask(__name__)


# init environment

#exp = TSForecastingExperiment()
model =load_model('my_best_model')
cols = ['Magna_6 Wind Direction', 'Magna_6 Wind Speed (m/s)',
       'Magna_6 Meteo Ambient Temperature (C)',
       'Magna_6 Meteo Air Pressure (hpa)', 'Magna_6 Meteo Relative Humidity',
       'Magna_6 Meteo Dew Point Temperature (C)', 'Power Supply (V)',
       'Magna_6 Water EC muS/cm', 'Magna_6 Water Level Above Sensor mm',
       'segment1(EC)', 'Magna_6 PH', 'Magna_6 ORP_mV',
       'Magna_6 pH_Sensor_Temperature_C', 'Magna_6 Precipitation_24hr_mm',
       'Magna_6 Cumulative Precipitation_mm', 'Magna_6 CTD_Temperature_C',
       'CTD_Pressure_BAR', 'CTD_Conductivity__mS', 'Metres above MSL',
       'TOW _MH2O']

@app.route('/')
def home():
    return render_template("home.html")

#@app.route('/predict',methods=['POST'])
#def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns = cols)
    prediction = predict_model(model, data=data_unseen)
    prediction = int(prediction.y_pred[0])
    return render_template('home.html',pred=prediction)
                          
 # Define predict function
@app.post("/predict", methods=['POST'])
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"moisture_prediction": predictions["prediction_label"].iloc[0]}                         
                          
                          
if __name__ == '__main__':
    app.run(debug=True)