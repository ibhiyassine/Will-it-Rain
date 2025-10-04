from fastapi import FastAPI, Query
import pandas as pd
from datetime import date
import requests
from chatbot import ChatBot
from predictionModel import PredictionModel

app = FastAPI()
prediction = PredictionModel.getInstance()


PARAMETERS = {
    "TS" : "temperature",
    "ALLSKY_SFC_UVA" : "UVA index",
    "WS2M" : "Wind speed",
    "PRECTOTCORR" : "Precipitation",
    "QV2M" : "Relative humidity",
    "SNODP" : "Snow Depth"
}

def statistics(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    """
    Fetch daily weather data from NASA POWER API for the specified coordinates and date range.
    Includes temperature, wind, precipitation, radiation, UV, snow depth, and relative humidity.
    """
    # Format dates
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # Add all parameters
    params = {
        "parameters": ",".join(PARAMETERS.keys()),
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_str,
        "end": end_str,
        "format": "JSON"
    }


    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Build dataframe
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        df = pd.DataFrame({'date': dates})

        for p in PARAMETERS.keys():
            param_data = data["properties"]["parameter"].get(p)
            if param_data:  # Some parameters might be missing for certain locations
                df[p] = [param_data.get(date.strftime("%Y%m%d"), None) for date in df['date']]
            else:
                df[p] = None

        df.set_index('date', inplace=True)
        return df.reset_index().to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

def formattedStatistics(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    """
    Takes the output of the Nasa API and prepare it for studying
    TODO: Continue implementing the function
    """
    data = statistics(lat, lon, start_date, end_date)

def formattedPredictions(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    """
    Takes the output of the prediction model and make it usable for the model
    """
    data = formattedStatistics(lat, lon, start_date, end_date)
    point_forecast, quantile_forecast = prediction.predict(data, (end_date - start_date).days)

    return point_forecast, quantile_forecast




@app.get("/predict")
def predict(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD"),
    activity: str = Query(..., description="The activity the person wants to do.")
):
    """
    1. takes input from formattedPredictions.
    2. give it to the chatbot.
    3. return the answer.
    """
    chat = ChatBot.getInstance()
    data = formattedPredictions(lat, lon, start_date, end_date)
    
    response = chat.askBot(data, activity)
    return {"response" : response};

@app.get("/statistics/{parameter}")
def study(
    parameter: str, 
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    """
    TODO:
    1. Takes the past values of the parameters (and maybe future ones predicted)
    2. Apply any know statistical formula that will let us infere something (anything we studied from Mrs. Hammouti)
    """
    return {"Hi There" : "It's Me Yassine"}

