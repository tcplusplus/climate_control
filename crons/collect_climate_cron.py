from datetime import datetime, timezone, timedelta

from climate_control import ClimateControl
from cronbase import CronBase

try:
    import smbus
except:
    print('might not compile outside the raspberry pi')
import time
# Constants for the DHT10 sensor
DHT10_ADDR = 0x38
DHT10_INIT_CMD = [0x33, 0x00]
DHT10_START_CMD = [0xac, 0x33, 0x00]
DHT10_STATUS_REG = 0x71


def read_dht10():
    try:
        bus = smbus.SMBus(4)  # Initialize the SMBus for I2C communication

        # Initialize the DHT10 sensor
        bus.write_i2c_block_data(DHT10_ADDR, DHT10_INIT_CMD[0], DHT10_INIT_CMD[1:])
        time.sleep(0.5)  # Wait for the sensor to initialize

        # Start a measurement
        bus.write_i2c_block_data(DHT10_ADDR, DHT10_START_CMD[0], DHT10_START_CMD[1:])
        time.sleep(0.75)  # Wait for the measurement to complete

        # Read the status register to check if the measurement is complete
        status = bus.read_byte_data(DHT10_ADDR, DHT10_STATUS_REG)
        while status & 0x80:  # Wait until the measurement is done
            time.sleep(0.1)
            status = bus.read_byte_data(DHT10_ADDR, DHT10_STATUS_REG)

        # Read the 6 bytes of measurement data from the sensor
        data = bus.read_i2c_block_data(DHT10_ADDR, 0x00, 6)

        # Convert the data to temperature and humidity
        humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) / (1 << 20) * 100.0
        temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) / (1 << 20) * 200.0 - 50
    except:
        temperature = 0
        humidity = 0
    return temperature, humidity

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
        temperature, humidity = read_dht10()
        print(f"Temperature: {temperature:.2f} C, Humidity: {humidity:.2f} %")
        self.climate_control.set_climate_state(temperature=temperature, humidity=humidity)
