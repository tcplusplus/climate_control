from datetime import datetime, timezone, timedelta

from climate_control import ClimateControl
from cronbase import CronBase


class CollectClimateCron(CronBase):
    def __init__(self, climate_control: ClimateControl) -> None:
        super().__init__()
        self.climate_control = climate_control
        self.__last_checked = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def should_run(self) -> bool:
        if datetime.now(timezone.utc) - self.__last_checked > timedelta(seconds=2):
            self.__last_checked = datetime.now(timezone.utc)
            return True
        return False

    async def run_once(self) -> None:
       self.climate_control.set_climate_state(temperature=25, humidity=50)
