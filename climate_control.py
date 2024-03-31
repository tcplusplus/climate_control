import os

import pandas as pd
from pydantic import BaseModel


class ClimateState(BaseModel):
    temperature: float
    humidity: float

class ClimateControl:
    def __init__(self) -> None:
        self.climate_state = ClimateState(temperature=0, humidity=0)
        self.filename = 'climate_states.csv'
        if os.path.exists(self.filename):
            self.dataframe = pd.read_csv(self.filename)
        else:
            self.dataframe = pd.DataFrame(columns=['time', 'temperature', 'humidity'])

    def set_climate_state(self, temperature: float, humidity: float) -> None:
        self.climate_state = ClimateState(temperature=temperature, humidity=humidity)
        entry = pd.DataFrame([[pd.Timestamp.now(), temperature, humidity]], columns=['time', 'temperature', 'humidity'])
        self.dataframe = pd.concat([self.dataframe, entry])
        self.dataframe.to_csv(self.filename)
