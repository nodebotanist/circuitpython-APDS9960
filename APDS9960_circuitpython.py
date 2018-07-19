from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const

_COMMAND_BIT = const(0x80)
_DEFAULT_ADDRESS = const(0x39)
_VALID_ID1 = 0xAB
_VALID_ID2 = 0x9C

_REGISTER_ID = const(0x92)

class APDS9960():
  def __init__(self, i2c, address=_DEFAULT_ADDRESS):
    self.buffer = bytearray(3)
    self.i2c_device = I2CDevice(i2c, address)

  def get_ID(self):
    chip_ID = self._read_register(_REGISTER_ID)
    if chip_ID == _VALID_ID1 or chip_ID == _VALID_ID2:
      print("APDS9960 Found!")
    else:
      print("ERROR: ADPS9960 ID is not valid!")

  def _read_register(self, reg):
    self.buffer[0] = _COMMAND_BIT | reg
    with self.i2c_device as i2c:
      i2c.write(self.buffer, end=1, stop=False)
      i2c.readinto(self.buffer, start=1)
    return self.buffer[1]

  def _write_control_register(self, reg, data):
    self.buffer[0] = _COMMAND_BIT | reg
    self.buffer[1] = data
    with self.i2c_device as i2c:
      i2c.write(self.buffer, end=2)