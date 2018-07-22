from adafruit_bus_device.i2c_device import I2CDevice

_COMMAND_BIT = 0x80
_DEFAULT_ADDRESS = 0x39
_VALID_ID1 = 0xAB
_VALID_ID2 = 0x9C

_DEVICE_MODES = {
  "POWER": 0,
  "AMBIENT_LIGHT": 1,
  "AMBIENT_LIGHT_INT": 4,
  "ALL": 7
}

_DEVICE_ATIMES = {
  "DEFAULT": 219
}

_DEVICE_LED_CURRENTS = {
  "100mA": 0,
  "50mA": 1,
  "25mA": 2,
  "12.5mA": 3
}

_DEVICE_PGAIN = {
  "1X": 0,
  "2X": 1,
  "4X": 2,
  "8X": 3
}

_DEVICE_AGAIN = {
  "1X": 0,
  "4X": 1,
  "16X": 2,
  "64X": 3
}

_DEVICE_LED_BOOST = {
  "100": 0,
  "150": 1,
  "200": 2,
  "300": 3
}

_DEVICE_DEFAULT_WTIME = 246
_DEVICE_DEFAULT_PPULSE = 0x87
_DEVICE_DEFAULT_POFFSET_UR = 0
_DEVICE_DEFAULT_POFFSET_DL = 0
_DEVICE_DEFAULT_CONFIG1 = 0x60

_REGISTER_ID = 0x92
_REGISTER_ENABLE = 0x80
_REGISTER_ATIME = 0x81
_REGISTER_WTIME = 0x83
_REGISTER_PPULSE = 0x8E
_REGISTER_CONFIG1 = 0x8D
_REGISTER_CONTROL = 0x8F
_REGISTER_CDATAL = 0x94
_REGISTER_CDATAH = 0x95
_REGISTER_RDATAL = 0x96
_REGISTER_RDATAH = 0x97
_REGISTER_GDATAL = 0x98
_REGISTER_GDATAH = 0x99
_REGISTER_BDATAL = 0x9A
_REGISTER_BDATAH = 0x9B

class APDS9960():
  def __init__(self, i2c, address=_DEFAULT_ADDRESS):
    self.buffer = bytearray(3)
    self.i2c_device = I2CDevice(i2c, address)

    self.get_ID()
    self._set_mode(_DEVICE_MODES["ALL"], False)
    self._write_register(_REGISTER_ATIME, _DEVICE_ATIMES["DEFAULT"])
    self._write_register(_REGISTER_PPULSE, _DEVICE_DEFAULT_PPULSE)
    self._write_register(_REGISTER_CONFIG1, _DEVICE_DEFAULT_CONFIG1)
    self._set_mask(_REGISTER_CONTROL, _DEVICE_LED_CURRENTS["25mA"], 6, 2) # set LED current
    self._set_mask(_REGISTER_CONTROL, _DEVICE_PGAIN["4X"], 2, 2) # set proximity gain
    self._set_mask(_REGISTER_CONTROL, _DEVICE_AGAIN["4X"], 0, 2) # set ambient light gain

  def startColorSensor(self):
    self._set_mode(_DEVICE_MODES["POWER"], True)
    self._set_mode(_DEVICE_MODES["AMBIENT_LIGHT"], True)
    print("color sensor ON")

  def getColorReading(self):
    clear = self._read_register(_REGISTER_CDATAH) << 8
    clear |= self._read_register(_REGISTER_CDATAL)
    red = self._read_register(_REGISTER_RDATAH) << 8
    red |= self._read_register(_REGISTER_RDATAL)
    green = self._read_register(_REGISTER_GDATAH) << 8
    green |= self._read_register(_REGISTER_GDATAL)
    blue = self._read_register(_REGISTER_BDATAH) << 8
    blue |= self._read_register(_REGISTER_BDATAL)

    return clear, red, green, blue

  def get_ID(self):
    chip_ID = self._read_register(_REGISTER_ID)
    if chip_ID == _VALID_ID1 or chip_ID == _VALID_ID2:
      print("APDS9960 Found!")
    else:
      print("ERROR: ADPS9960 ID is not valid!")

  def _set_mode(self, mode, on):
    currentValue = self._get_mode()

    if mode >= 0 and mode <= 6:
      if on is True:
        currentValue |= (1 << mode)
      else:
        currentValue &= ~(1 << mode)
    if mode == _DEVICE_MODES["ALL"]:
      if on is True:
        currentValue = 0x7F
      else:
        currentValue = 0x00

    self._write_register(_REGISTER_ENABLE, currentValue)

  def _get_mode(self):
    return self._read_register(_REGISTER_ENABLE)

  def _set_mask(self, reg, value, shift, length, clear=False):
    currentValue = self._read_register(reg)
    print("Current Register: ")
    print(currentValue)

    mask = 0b00000000
    for i in range(shift, shift + length):
      mask |= (1 << i)
  
    currentValue &= ~(mask)
    currentValue |= (value << shift)

    print("New Register: ")
    print(currentValue)
    self._write_register(reg, currentValue)

  def _read_register(self, reg):
    self.buffer[0] = _COMMAND_BIT | reg
    with self.i2c_device as i2c:
      i2c.write(self.buffer, end=1, stop=False)
      i2c.readinto(self.buffer, start=1)
    return self.buffer[1]

  def _write_register(self, reg, data):
    self.buffer[0] = _COMMAND_BIT | reg
    self.buffer[1] = data
    with self.i2c_device as i2c:
      i2c.write(self.buffer, end=2)