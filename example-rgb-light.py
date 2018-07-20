import board
import busio
import time
from APDS9960_circuitpython import APDS9960

print("Starting APDS9960 Example")

i2c = busio.I2C(board.SCL, board.SDA)
sensor = APDS9960(i2c)
sensor.startColorSensor()

while True:
  clear, red, green, blue = sensor.getColorReading()
  print("Clear: " + str(clear))
  print("Red: " + str(red))
  print("Green: " + str(green))
  print("Blue: " + str(blue))
  time.sleep(.500)