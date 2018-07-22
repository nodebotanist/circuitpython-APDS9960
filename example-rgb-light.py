import board
import busio
import time
import neopixel

from APDS9960_circuitpython import APDS9960

print("Starting APDS9960 Example")

i2c = busio.I2C(board.SCL, board.SDA)
sensor = APDS9960(i2c)
sensor.startColorSensor()

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill((0, 0, 0))
pixels.show()

while True:
  clear, red, green, blue = sensor.getColorReading()
  print("Clear: " + str(clear))
  print("Red: " + str(red))
  print("Green: " + str(green))
  print("Blue: " + str(blue))
  if clear != 0:
    red = round((red / clear) * 255)
    green = round((green / clear) * 255)
    blue = round((blue / clear) * 255)
    print("Red (formatted): " + str(red))
    print("Green: (formatted) " + str(green))
    print("Blue: (formatted) " + str(blue))
    pixels.fill((red, green, blue))
    pixels.show()
  time.sleep(2)