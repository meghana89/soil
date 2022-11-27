# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.time_series import load_model, predict_model
from fastapi import FastAPI
import uvicorn
from pydantic import create_model

# Create the app
app = FastAPI()

# Load trained Pipeline
model = load_model("soil_api")

# Create input/output pydantic models
input_model = create_model("soil_api_input",
                           **{'Magna_6 Wind Direction': 328.2,
                              'Magna_6 Wind Speed (m/s)': 0.5, 'Magna_6 Meteo Ambient Temperature (C)': 7.1, 'Magna_6 Meteo Air Pressure (hpa)': 988.9, 'Magna_6 Meteo Relative Humidity': 98.3, 'Magna_6 Meteo Dew Point Temperature (C)': 6.9, 'Power Supply (V)': 13.115, 'Magna_6 Water EC muS/cm': 264.5, 'Magna_6 Water Level Above Sensor mm': 1685.9, 'segment1(EC)': 2.12, 'Magna_6 PH': 0.0, 'Magna_6 ORP_mV': 0.0, 'Magna_6 pH_Sensor_Temperature_C': 0.0, 'Magna_6 Precipitation_24hr_mm': 55.0, 'Magna_6 Cumulative Precipitation_mm': 308.0, 'Magna_6 CTD_Temperature_C': 8.848389, 'CTD_Pressure_BAR': 0.165328, 'CTD_Conductivity__mS': 0.264529, 'Metres above MSL': 206.26, 'TOW _MH2O': 0.77})
output_model = create_model("soil_api_output", moisture_prediction=72.3)


# Define predict function
@app.post("/predict",response_model=output_model)
def predict(data= input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"moisture_prediction": predictions["y_pred"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
