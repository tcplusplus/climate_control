from climate_control import ClimateControl, ClimateState
from webhandlerbase import WebHandlerBase


class ClimateHandler(WebHandlerBase):
    def __init__(self, climate_control: ClimateControl) -> None:
        self.climate_control = climate_control

    async def get(self) -> ClimateState:
        """
        Get the params you pass to it
        """
        return self.climate_control.climate_state
