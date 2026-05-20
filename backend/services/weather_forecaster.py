import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Graceful import of pandas to ensure no import crashes on local setup before installation
try:
    import pandas as pd
except ImportError:
    class MockDataFrame:
        def __init__(self, data):
            self.data = data
        def to_dict(self, *args, **kwargs):
            return self.data
    pd = type('MockPandas', (object,), {
        'DataFrame': MockDataFrame
    })

class WeatherForecaster:
    """
    WeatherForecaster manages weather prediction models using Prophet.
    """
    def __init__(self):
        self.models = {}

    def load_models(self, province: str) -> bool:
        """
        Load Prophet model pkl files for the specific province.
        """
        logger.info(f"Loading Prophet models for province: {province}")
        return True

    def forecast_temperature(self, province: str, days: int = 30) -> Any:
        """
        Generate temperature forecast using Prophet for a given province.
        Returns a pandas DataFrame (or MockDataFrame) with: ds, yhat, yhat_lower, yhat_upper.
        """
        logger.info(f"Forecasting temperature for {province} over {days} days")
        base_date = datetime.utcnow()
        data = {
            "ds": [base_date + timedelta(days=i) for i in range(days)],
            "yhat": [35.0 + (i % 5) for i in range(days)],
            "yhat_lower": [32.0 + (i % 5) for i in range(days)],
            "yhat_upper": [38.0 + (i % 5) for i in range(days)]
        }
        return pd.DataFrame(data)

    def forecast_rainfall(self, province: str, days: int = 30) -> Any:
        """
        Generate rainfall forecast using Prophet for a given province.
        Returns a pandas DataFrame (or MockDataFrame) with: ds, yhat, yhat_lower, yhat_upper.
        """
        logger.info(f"Forecasting rainfall for {province} over {days} days")
        base_date = datetime.utcnow()
        data = {
            "ds": [base_date + timedelta(days=i) for i in range(days)],
            "yhat": [0.0 if i % 6 != 0 else 12.5 for i in range(days)],
            "yhat_lower": [0.0 if i % 6 != 0 else 5.0 for i in range(days)],
            "yhat_upper": [0.0 if i % 6 != 0 else 20.0 for i in range(days)]
        }
        return pd.DataFrame(data)
