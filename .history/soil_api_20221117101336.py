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
input_model = create_model("soil_api_input", **{'Magna_6 Wind Direction': 226.5, 'Magna_6 Wind Speed (m/s)': 3.7, 'Magna_6 Meteo Ambient Temperature (C)': 8.4, 'Magna_6 Meteo Air Pressure (hpa)': 996.1, 'Magna_6 Meteo Relative Humidity': 94.3, 'Magna_6 Meteo Dew Point Temperature (C)': 7.5, 'Power Supply (V)': 13.089, 'Magna_6 Water EC muS/cm': 422.8, 'Magna_6 Water Level Above Sensor mm': 1754.6, 'segment1(EC)': 2.16, 'Magna_6 PH': 8.50717, 'Magna_6 ORP_mV': -539.455, 'Magna_6 pH_Sensor_Temperature_C': 8.85812, 'Wind Speed (x10)': 37.0, 'Wind Direction (x10)': 2265.0, 'Temperature (x10)': 84.0, 'Air Pressure (x10)': 9961.0, 'Relative Humidity (x10)': 943.0, 'Dew Point Temperature (x10)': 75.0, 'Magna_6 Precipitation_24hr_mm': 6.0, 'Magna_6 Cumulative Precipitation_mm': 44.0, 'Magna_6 CTD_Temperature_C': 8.5896, 'CTD_Pressure_BAR': 0.172068, 'CTD_Conductivity__mS': 0.422807, 'Metres above MSL': 0.0, 'TOW _MH2O': 0.0})
output_model = create_model("soil_api_output", y_pred=92.72)


# Define predict function
@app.post("/predict", response_model=output_model)
def predict(data: input_model):
    data = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=data)
    return {"moisture_prediction": predictions["prediction_label"].iloc[0]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
