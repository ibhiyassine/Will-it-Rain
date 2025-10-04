from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import os

import pandas as pd
from datetime import datetime, date, timedelta
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import quote
from torch.nn import parameter
from chatbot import ChatBot
from predictionModel import PredictionModel
from env import ENV

app = FastAPI()
prediction = PredictionModel.getInstance()
environment = ENV.getInstance()

static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "static"))

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(static_dir, "favicon.ico"))

PARAMETERS = {
    "t2m": "t_2m:C",                        
    "precip_h": "precip_1h:mm",       
    "wind_speed": "wind_speed_10m:kmh",
    "UVA":"uv:idx",
    "snodb":"snow_depth:mm"      
}

async def statistics(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    """
    Fetch daily weather data from Meteomatics API for the specified coordinates and date range.

    Uses basic HTTP auth with the provided trial credentials. Returns a list of daily records.
    """

    # Meteomatics trial credentials (replace with your own)
    METEO_USERNAME = "igadern_aya"
    METEO_PASSWORD = "7U47m3882wgXSd8xm2EO"

    # Generate list of hourly timestamps between start and end date
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    hours = []
    cur = start_dt
    while cur <= end_dt:
        hours.append(cur.strftime("%Y-%m-%dT%H:%M:%SZ"))
        cur += timedelta(hours=1)

    time_path = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_path += "--"
    time_path += end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_path += ":PT24H"

    # Properly URL-encode parameters 
    meteoparams = ",".join([quote(v, safe=":") for v in PARAMETERS.values()])

    # Build API URL
    url = f"https://api.meteomatics.com/{time_path}/{meteoparams}/{lat},{lon}/json"

    try:
        # Authenticate and send request
        auth = HTTPBasicAuth(METEO_USERNAME, METEO_PASSWORD)
        resp = requests.get(url, auth=auth, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # Convert Meteomatics JSON to hourly DataFrame
        df_daily = pd.DataFrame()
        for series in data.get("data", []):
            param = series.get("parameter")
            points = series.get("coordinates", [])[0].get("dates", [])
            times = [pd.to_datetime(p["date"]) for p in points]
            values = [p.get("value") for p in points]
            s = pd.Series(data=values, index=times, name=param)
            df_daily = pd.concat([df_daily, s], axis=1)

        print(df_daily)

        if df_daily.empty:
            return {"error": "No data returned from Meteomatics for the requested range/parameters."}

        # Format output
        df_daily = df_daily.reset_index().rename(columns={"index": "date"})
        df_daily["date"] = df_daily["date"].dt.date

        return df_daily.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}

async def formattedStatistics(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    """
    Takes the output of the Nasa API and prepare it for studying
    TODO: Continue implementing the function
    """
    data = await statistics(lat, lon, start_date, end_date)
    ret = [[] for i in range(len(PARAMETERS))]
    # for key in data:
    #     ret.append(data[key])
    # print(ret)

    idx = 0
    for obj in data:
        for key, val in obj.items():
            if(key == "date"):
                continue
            ret[idx].append(val)
            idx = (idx + 1) % len(PARAMETERS)

    return ret

async def formattedPredictions(
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD"),
):
    """
    Takes the output of the prediction model and make it usable for the model
    """
    data = await formattedStatistics(lat, lon, start_date, end_date)

    keys = list( PARAMETERS.keys() )
    point_forecast = {
        keys[i] : data[i] for i in range(len(keys))
    }

    return point_forecast




@app.get("/predict")
async def predict(
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
    point_forecast = await formattedPredictions(lat, lon, start_date, end_date)
    print(point_forecast)
    
    response = chat.askBot(point_forecast, activity)
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

