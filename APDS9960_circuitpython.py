from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const

_COMMAND_BIT = const(0x80)
_DEFAULT_ADDRESS = const(0x39)
_VALID_ID1 = 0xAB
_VALID_ID2 = 0x9C

_DEVICE_MODES = {
  "POWER": 0,
  "AMBIENT_LIGHT": 1,
  "PROXIMITY": 2,
  "WAIT": 3,
  "AMBIENT_LIGHT_INT": 4,
  "PROXIMITY_INT": 5,
  "GESTURE": 6,
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

_DEVICE_DEFAULT_WTIME = 246
_DEVICE_DEFAULT_PPULSE = 0x87
_DEVICE_DEFAULT_POFFSET_UR = 0
_DEVICE_DEFAULT_POFFSET_DL = 0
_DEVICE_DEFAULT_CONFIG1 = 0x60

_REGISTER_ID = const(0x92)
_REGISTER_ENABLE = const(0x80)
_REGISTER_ATIME = const(0x81)
_REGISTER_WTIME = const(0x83)
_REGISTER_PPULSE = const(0x8E)
_REGISTER_POFFSET_UR = const(0x9D)
_REGISTER_POFFSET_DL = const(0x9E)
_REGISTER_CONFIG1 = const(0x8D)
_REGISTER_CONTROL = const(0x8F)

class APDS9960():
  def __init__(self, i2c, address=_DEFAULT_ADDRESS):
    self.buffer = bytearray(3)
    self.i2c_device = I2CDevice(i2c, address)
    self.get_ID()
    self._set_mode(_DEVICE_MODES["ALL"], False)
    self._write_register(_REGISTER_ATIME, _DEVICE_ATIMES["DEFAULT"])
    self._write_register(_REGISTER_PPULSE, _DEVICE_DEFAULT_PPULSE)
    self._write_register(_REGISTER_POFFSET_UR, _DEVICE_DEFAULT_POFFSET_UR)
    self._write_register(_REGISTER_POFFSET_DL, _DEVICE_DEFAULT_POFFSET_DL)
    self._write_register(_REGISTER_CONFIG1, _DEVICE_DEFAULT_CONFIG1)
    self.set_LED_current(_DEVICE_LED_CURRENTS["12.5mA"])

  def get_ID(self):
    chip_ID = self._read_register(_REGISTER_ID)
    if chip_ID == _VALID_ID1 or chip_ID == _VALID_ID2:
      print("APDS9960 Found!")
    else:
      print("ERROR: ADPS9960 ID is not valid!")

  def set_LED_current(self, current):
    currentControlValue = self._read_register(_REGISTER_CONTROL)
    
    current &= 0b00000011
    current = current << 6
    currentControlValue &= 0b00111111
    currentControlValue |= current

    self._write_register(_REGISTER_CONTROL, currentControlValue)

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