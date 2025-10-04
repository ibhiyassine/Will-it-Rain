# Multivariate Weather Forecasting with TimesFM
# Using Temperature, Precipitation, and Humidity

import timesfm
import torch
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta
from env import ENV 

environment = ENV.getInstance()

class PredictionModel:

    predictionInstance = None

    def __init__(self):
    # Configure TimesFM model for comprehensive multivariate forecasting
        torch.set_float32_matmul_precision("high")

        self.model = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch")
        self.model.compile(
            timesfm.ForecastConfig(
                max_context=environment.TIMESFM_CONTEXT,  # treating 7 variables simultaneously
                max_horizon=environment.TIMESFM_HORIZON,   # can predict the next 365 days
                normalize_inputs=True,
                use_continuous_quantile_head=True,
                force_flip_invariance=True,
                infer_is_positive=False,
                fix_quantile_crossing=True,
            )
        )

    def predict(self, multivariate_input, horizon):
        point_forecast, quantile_forecast = self.model.forecast(
            horizon = horizon,
            inputs = multivariate_input
        )
        return point_forecast, quantile_forecast

    @classmethod
    def getInstance(cls):
        if(cls.predictionInstance is None):
            cls.predictionInstance = PredictionModel()
        return cls


    
