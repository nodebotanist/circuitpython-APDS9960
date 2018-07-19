import board
import busio
from APDS9960_circuitpython import APDS9960

print("Starting APDS9960 Example")

i2c = busio.I2C(board.SCL, board.SDA)
sensor = APDS9960(i2c)