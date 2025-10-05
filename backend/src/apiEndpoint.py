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
DISPLAY_NAMES = {
    "t2m": "Temperature 2m (°C)",
    "precip_h": "Precipitation 1h (mm)",
    "wind_speed": "Wind Speed 10m (km/h)",
    "UVA": "Ultraviolet Index",
    "snodb": "Snow Depth (mm)"
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
    print(point_forecast)
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

import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd

from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
@app.get("/statistics/{parameter}")
async def study(
    parameter: str,
    lat: float = Query(..., ge=-90, le=90, description="Latitude (-90 to 90)"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude (-180 to 180)"),
    start_date: date = Query(..., description="Start date YYYY-MM-DD"),
    end_date: date = Query(..., description="End date YYYY-MM-DD")
):
    # Get raw data using statistics()
    raw_data = await statistics(lat, lon, start_date, end_date)
    if isinstance(raw_data, dict) and "error" in raw_data:
        return raw_data

    df = pd.DataFrame(raw_data)
    if df.empty:
        return {"error": "No data available for the given range."}

    # Convert 'date' column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Determine actual column name and friendly name
    if parameter in PARAMETERS:
        actual_col_name = PARAMETERS[parameter]
        friendly_name = DISPLAY_NAMES.get(parameter, parameter)
    else:
        actual_col_name = parameter
        matched_key = next((k for k, v in PARAMETERS.items() if v == parameter), None)
        friendly_name = DISPLAY_NAMES.get(matched_key, parameter)

    # Check if column exists
    if actual_col_name not in df.columns:
        return {"error": f"Parameter '{parameter}' not available. Available columns: {list(df.columns)}"}

    # Rename column for plotting and stats
    df.rename(columns={actual_col_name: friendly_name}, inplace=True)

    # Aggregate daily data (sum for precipitation/snow, mean for others)
    if friendly_name.lower() in ["precipitation 1h (mm)", "snow depth (mm)"]:
        df_daily = df.groupby(df["date"].dt.date)[friendly_name].sum().reset_index()
    else:
        df_daily = df.groupby(df["date"].dt.date)[friendly_name].mean().reset_index()
    df_daily.rename(columns={'date': 'date'}, inplace=True)

    dates = df_daily["date"].astype(str).tolist()
    values = df_daily[friendly_name].astype(float).tolist()

    # Calculate stats
    stats = {
        "mean": float(df_daily[friendly_name].mean()),
        "std": float(df_daily[friendly_name].std()),
        "variance": float(df_daily[friendly_name].var()),
        "min": float(df_daily[friendly_name].min()),
        "max": float(df_daily[friendly_name].max()),
        "median": float(df_daily[friendly_name].median()),
        "percentile_25": float(np.percentile(df_daily[friendly_name], 25)),
        "percentile_75": float(np.percentile(df_daily[friendly_name], 75))
    }

    # Plotting
    plots = {}
    os.makedirs(static_dir, exist_ok=True)

    # Line plot with mean, median, and point annotations
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=dates, y=values, marker="o", color="b", label=f"{friendly_name}")
    plt.title(f"{friendly_name} over time (Daily)", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel(friendly_name, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)

    mean_val = df_daily[friendly_name].mean()
    median_val = df_daily[friendly_name].median()
    plt.axhline(mean_val, color='r', linestyle='--', label=f"Mean: {mean_val:.2f}")
    plt.axhline(median_val, color='g', linestyle='-.', label=f"Median: {median_val:.2f}")

    # Annotate each data point
    for x, y in zip(dates, values):
        plt.text(x, y, f"{y:.1f}", fontsize=8, ha='center', va='bottom', rotation=45)

    num_days = (pd.to_datetime(dates[-1]) - pd.to_datetime(dates[0])).days + 1
    if num_days <= 30:
        plt.xticks(rotation=45)
    else:
        plt.xticks([])

    plt.legend()
    plt.tight_layout()
    line_path = os.path.join(static_dir, f"{parameter}_line.png")
    plt.savefig(line_path)
    plt.close()
    plots["line"] = f"/static/{parameter}_line.png"

    # Boxplot with mean marker
    plt.figure(figsize=(6, 5))
    sns.boxplot(y=values, color="lightblue")
    plt.title(f"{friendly_name} Distribution (Daily Boxplot)", fontsize=14)
    plt.ylabel(friendly_name, fontsize=12)
    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.scatter(0, mean_val, color='red', zorder=10, label=f"Mean: {mean_val:.2f}")
    plt.legend()
    plt.tight_layout()
    box_path = os.path.join(static_dir, f"{parameter}_box.png")
    plt.savefig(box_path)
    plt.close()
    plots["boxplot"] = f"/static/{parameter}_box.png"
    # Histogram with KDE, mean, median, and ±1 std shading
    plt.figure(figsize=(8, 5))

    # Compute mean and std
    mean_val = df_daily[friendly_name].mean()
    std_val = df_daily[friendly_name].std()

    # Plot histogram
    sns.histplot(values, bins=20, kde=False, color="lightgreen", stat="density")

    # Overlay KDE with custom color
    sns.kdeplot(values, color="darkblue", lw=2, label="Density (KDE)")

    # Shade ±1 std area around the mean
    plt.axvspan(mean_val - std_val, mean_val + std_val, color="yellow", alpha=0.3, label="±1 Std Dev")

    # Mean and median vertical lines
    plt.axvline(mean_val, color='r', linestyle='--', label=f"Mean: {mean_val:.2f}")
    median_val = df_daily[friendly_name].median()
    plt.axvline(median_val, color='g', linestyle='-.', label=f"Median: {median_val:.2f}")

    plt.title(f"{friendly_name} Distribution (Daily Histogram)", fontsize=14)
    plt.xlabel(friendly_name, fontsize=12)
    plt.ylabel("Density", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()

    hist_path = os.path.join(static_dir, f"{parameter}_hist.png")
    plt.savefig(hist_path)
    plt.close()
    plots["histogram"] = f"/static/{parameter}_hist.png"


    return {
        "parameter": friendly_name,
        "stats": stats,
        "plots": plots,
        "data": {
            "dates": dates,
            "values": values
        }
    }
